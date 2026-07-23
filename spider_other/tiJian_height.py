import pandas as pd
import math

# 显示设置
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# ==================== 1. 读取数据 ====================
followup_df = pd.read_excel("C:\\Users\\Donkey\\Desktop\\Test2.xlsx")          # 随访记录
physical_df = pd.read_excel("C:\\Users\\Donkey\\Desktop\\tiJian.xlsx")        # 体检记录

# ==================== 2. 数据清洗 ====================
# 随访表
followup_df['证件号码'] = followup_df['证件号码'].astype(str)
followup_df['随访日期'] = pd.to_datetime(followup_df['随访日期'])
followup_df['姓名'] = followup_df['姓名'].str.strip()
# 删除体重或体质指数缺失的记录（无法计算身高）
followup_df.dropna(subset=['体重', '体质指数'], inplace=True)

# 体检表
physical_df['身份证号'] = physical_df['身份证号'].astype(str)
physical_df['体检日期'] = pd.to_datetime(physical_df['体检日期'])
physical_df['姓名'] = physical_df['姓名'].str.strip()
# 删除身高或体重缺失的记录（无法比对）
physical_df.dropna(subset=['身高(cm)', '体重(kg)'], inplace=True)

# ==================== 3. 从随访记录计算身高 ====================
def compute_height(row):
    """根据体重(kg)和体质指数(kg/m²)计算身高(cm)，保留1位小数"""
    weight = row['体重']
    bmi = row['体质指数']
    if weight > 0 and bmi > 0:
        height_m = math.sqrt(weight / bmi)
        return round(height_m * 100, 1)   # 转换为厘米并保留1位小数
    else:
        return None

followup_df['计算身高(cm)'] = followup_df.apply(compute_height, axis=1)
followup_df.dropna(subset=['计算身高(cm)'], inplace=True)

# ==================== 4. 每人取最近一次随访记录（含随访医生） ====================
followup_latest = (
    followup_df.sort_values('随访日期')
    .groupby(['姓名', '证件号码'], as_index=False)
    .last()
)

# 保留关键字段：姓名、证件号码、计算身高、体重、随访医生
followup_summary = followup_latest[['姓名', '证件号码', '计算身高(cm)', '体重', '随访医生']].copy()
followup_summary.rename(columns={
    '计算身高(cm)': '随访身高(cm)',
    '体重': '随访体重(kg)',
    '随访医生': '责任医生'          # 直接作为责任医生
}, inplace=True)

# ==================== 5. 体检表每人取最近一次记录 ====================
physical_latest = (
    physical_df.sort_values('体检日期')
    .groupby(['姓名', '身份证号'], as_index=False)
    .last()
)

physical_summary = physical_latest[['姓名', '身份证号', '身高(cm)', '体重(kg)']].copy()
physical_summary.rename(columns={
    '身高(cm)': '体检身高(cm)',
    '体重(kg)': '体检体重(kg)'
}, inplace=True)

# ==================== 6. 合并随访与体检数据 ====================
merged = pd.merge(
    followup_summary,
    physical_summary,
    left_on=['姓名', '证件号码'],
    right_on=['姓名', '身份证号'],
    how='inner'   # 只保留两边都有的记录
)

# ==================== 7. 计算差异并筛选 ====================
merged['身高差(cm)'] = (merged['随访身高(cm)'] - merged['体检身高(cm)']).abs().round(1)
merged['体重差(kg)'] = (merged['随访体重(kg)'] - merged['体检体重(kg)']).abs().round(1)

# 筛选条件：身高差>=2 或 体重差>=2
result = merged[(merged['身高差(cm)'] >= 3) | (merged['体重差(kg)'] >= 5)]

# ==================== 8. 格式化输出（身高体重保留1位小数） ====================
if not result.empty:
    # 重新整理输出列，并确保数值格式
    output_cols = [
        '姓名', '证件号码', '责任医生',
        '体检身高(cm)', '随访身高(cm)', '身高差(cm)',
        '体检体重(kg)', '随访体重(kg)', '体重差(kg)'
    ]
    # 对数值列四舍五入到1位小数（已做，但再确保）
    for col in ['体检身高(cm)', '随访身高(cm)', '身高差(cm)', '体检体重(kg)', '随访体重(kg)', '体重差(kg)']:
        result[col] = result[col].round(1)

    print("\n===== 身高或体重差异较大的人员名单 =====")
    print(result[output_cols].to_string(index=False))

    # 可选保存到Excel
    result[output_cols].to_excel('C:\\Users\\Donkey\\Desktop\\Results.xlsx', index=False)
else:
    print("未发现身高差≥2cm或体重差≥2kg的人员。")