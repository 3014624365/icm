import pandas as pd

# 输入文件名（CSV 文件）
input_file = 'summerOly_athletes.csv'
# 输出文件名（Excel 文件）
output_file = 'athletes.xlsx'

# 读取 CSV 文件
try:
    df = pd.read_csv(input_file)
except FileNotFoundError:
    print(f"错误: 找不到文件 {input_file}。")
    exit()
except Exception as e:
    print(f"读取文件时发生错误: {e}")
    exit()

# 获取第二列（B列，也就是索引1）
column_b = df.iloc[:, 1]

# 找到重复值
duplicates = column_b[column_b.duplicated(keep=False)]

# 创建一个 Excel 写入器
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # 将整个数据框写入第一个工作表
    df.to_excel(writer, sheet_name='Sheet1', index=False)

    # 遍历重复值
    for value in duplicates.unique():
        # 找到对应的行
        duplicate_rows = df[df.iloc[:, 1] == value]

        # 创建新的工作表，确保名称合法
        new_sheet_name = str(value)[:31]  # 限制工作表名称长度为31
        new_sheet_name = ''.join(char for char in new_sheet_name if char.isalnum() or char in ('_', ' '))

        # 如果工作表名称重复，添加后缀
        counter = 1
        original_name = new_sheet_name
        while new_sheet_name in writer.sheets:
            new_sheet_name = f"{original_name}_{counter}"
            counter += 1

        # 将重复的行写入新的工作表
        duplicate_rows.to_excel(writer, sheet_name=new_sheet_name, index=False)

print(f"处理完成，结果已保存到 {output_file}")