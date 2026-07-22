import pandas as pd

pd.set_option('display.max_rows', 1000)

# ==================== 1. 读取数据 ====================
df = pd.read_excel("C:\\Users\\Donkey\\Desktop\\Test.xlsx")  # 请替换为实际文件路径

# ==================== 2. 数据清洗 ====================
df['证件号码'] = df['证件号码'].astype(str)  # 确保为字符串
df['随访日期'] = pd.to_datetime(df['随访日期'])  # 转为日期格式
df['姓名'] = df['姓名'].str.strip()  # 去除姓名首尾空格

# 如果此次随访分类列中存在空值，可先删除或填充（此处直接丢弃空值所在行）
df.dropna(subset=['此次随访分类'], inplace=True)

# ==================== 3. 定义不满意条件（请根据实际值修改）====================
# 假设此次随访分类列中'不满意'的文字为"不满意"，若是数字评分则相应修改
UNSATISFIED = '控制不满意'

# ==================== 4. 按人分组，并按季度筛选 ====================
all_filtered = []

# 按姓名 + 身份证前14位分组
grouped = df.groupby(['姓名', '证件号码'])

for (name, id14), group in grouped:
    # 按随访日期排序
    group = group.sort_values('随访日期').reset_index(drop=True)

    # 添加季度列（年份+季度，如 2023Q1）
    group['季度'] = group['随访日期'].dt.to_period('Q')

    # 对每个季度内的记录分别处理（保证下次随访在同一季度）
    for quarter, sub in group.groupby('季度', group_keys=False):
        sub = sub.reset_index(drop=True)

        # 计算下一次随访日期（下一条记录的随访日期）
        sub['下次随访日期'] = sub['随访日期'].shift(-1)
        # 计算间隔天数（整数）
        sub['间隔天数'] = (sub['下次随访日期'] - sub['随访日期']).dt.days

        # 筛选条件：当前此次随访分类不满意 且 与下次随访间隔 ≥ 15天
        # 注意：最后一条记录的下次随访日期为NaT，间隔为NaN，条件自动不成立
        mask = (sub['此次随访分类'] == UNSATISFIED) & (sub['间隔天数'] >= 15)
        filtered = sub.loc[mask].copy()

        if not filtered.empty:
            all_filtered.append(filtered)

# ==================== 5. 合并所有符合条件的记录 ====================
if all_filtered:
    result = pd.concat(all_filtered, ignore_index=True)
else:
    result = pd.DataFrame()
    print("未找到符合条件的记录。")

# ==================== 6. 保存到文件 ====================
# output_file = 'C:\\Users\\Donkey\\Desktop\\out.xlsx'
# result.to_excel(output_file, index=False)
# print(f"筛选完成！共找到 {len(result)} 条记录，已保存至：{output_file}")

# 可选：同时输出一个简短的摘要
if len(result) > 0:
    print("\nResult preview:")
    print(result[['姓名','证件号码','季度','随访日期','随访方式','随访医生','录入人','间隔天数']])