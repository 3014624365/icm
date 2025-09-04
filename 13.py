import pandas as pd

# 输入文件路径
input_file = "athletes.xlsx"  # 原始数据文件
output_file = "processed_olympics.xlsx"  # 输出文件路径

# 读取 Excel 文件的所有工作表
xls = pd.ExcelFile(input_file)

# 创建一个 ExcelWriter 对象，用于写入新的 Excel 文件
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    for sheet_name in xls.sheet_names:
        # 读取当前工作表
        df = pd.read_excel(xls, sheet_name=sheet_name)

        # 筛选荷兰（NED）的获奖数据
        medals_ned = df[df['NOC'] == 'NED'][['Year', 'Sport', 'Medal']].dropna()

        # 如果有获奖数据，进行统计
        if not medals_ned.empty:
            # 按年份和项目分组，统计奖牌
            medal_summary = medals_ned.groupby(['Year', 'Sport', 'Medal']).size().unstack(fill_value=0)

            # 保存到新的工作表中
            medal_summary.to_excel(writer, sheet_name=sheet_name)

print(f"处理完成，结果已保存到 {output_file}")