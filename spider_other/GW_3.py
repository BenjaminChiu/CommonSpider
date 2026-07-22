import pandas as pd

pd.set_option('display.max_rows', 1000)

# ==================== 1. 读取数据 ====================
df = pd.read_excel("C:\\Users\\Donkey\\Desktop\\Test2.xlsx")

# ==================== 2. 数据清洗 ====================
df['证件号码'] = df['证件号码'].astype(str)
df['随访日期'] = pd.to_datetime(df['随访日期'])
df['姓名'] = df['姓名'].str.strip()
df.dropna(subset=['此次随访分类'], inplace=True)

# ==================== 3. 定义不满意条件 ====================
UNSATISFIED = '控制不满意'

# ==================== 4. 按人分组，并按季度筛选 ====================
all_filtered = []
grouped = df.groupby(['姓名', '证件号码'])

for (name, id14), group in grouped:
    group = group.sort_values('随访日期').reset_index(drop=True)
    group['季度'] = group['随访日期'].dt.to_period('Q')

    for quarter, sub in group.groupby('季度', group_keys=False):
        sub = sub.reset_index(drop=True)
        sub['下次随访日期'] = sub['随访日期'].shift(-1)
        sub['间隔天数'] = (sub['下次随访日期'] - sub['随访日期']).dt.days

        cond_super = (sub['此次随访分类'] == UNSATISFIED) & (sub['间隔天数'] >= 15)
        cond_empty = sub['随访结局'].isna() | (sub['随访结局'].astype(str).str.strip() == '')
        combined_mask = cond_super | cond_empty
        filtered = sub.loc[combined_mask].copy()

        if not filtered.empty:
            reasons = []
            for idx in filtered.index:
                is_super = cond_super.loc[idx]
                is_empty = cond_empty.loc[idx]
                if is_super and is_empty:
                    reasons.append("超期且随访结局为空")
                elif is_super:
                    reasons.append("超期")
                elif is_empty:
                    reasons.append("随访结局为空")
                else:
                    reasons.append("")
            filtered['筛选原因'] = reasons
            all_filtered.append(filtered)

if all_filtered:
    result = pd.concat(all_filtered, ignore_index=True)
else:
    result = pd.DataFrame()
    print("未找到符合条件的记录。")

# ==================== 6. 保存到文件（已注释） ====================
# output_file = 'C:\\Users\\Donkey\\Desktop\\out.xlsx'
# result.to_excel(output_file, index=False)
# print(f"筛选完成！共找到 {len(result)} 条记录，已保存至：{output_file}")

# ===== 修改后的打印部分（对齐输出） =====
if len(result) > 0:
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    print("\nResult preview:")
    print(result[['姓名','证件号码','季度','随访日期','随访方式','随访医生','录入人','间隔天数','筛选原因']].to_string())
else:
    print("未找到符合条件的记录。")