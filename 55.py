import pandas as pd
import re

# 读取数据
df_awards = pd.read_excel('award.xlsx', header=0)  # 确保第一行是列名
df_events = pd.read_csv('event.csv', header=0)  # 项目历史数据

# 打印列名以确保正确读取
print("Awards DataFrame columns:", df_awards.columns)
print("Events DataFrame columns:", df_events.columns)

# 确保年份列是整数类型
df_awards['年份'] = df_awards['年份'].astype(int)
df_events['Year'] = df_events['Year'].astype(int)

# 清理工作表名称中的无效字符
def clean_sheet_name(name):
    # 替换无效字符为下划线
    return re.sub(r'[\\/*?\[\]:]', '_', name)

# 创建一个新的Excel文件来存储结果
with pd.ExcelWriter('country_awards_ratio.xlsx') as writer:
    # 遍历每个国家
    for country in df_awards.columns[1:]:  # 假设第一列是“年份”，其余列是国家
        # 创建一个新的DataFrame来存储结果
        result_df = pd.DataFrame(columns=['Year', 'Project', 'Total Golds', 'Sub Events', 'Proportion'])

        # 遍历每个年份
        for year in df_awards['年份']:
            # 获取该年该国家的奖牌数据
            awards_data = df_awards.loc[df_awards['年份'] == year, country].values[0] if not df_awards.loc[
                df_awards['年份'] == year, country].empty else 0

            # 遍历每个项目（假设 df_awards 的列名是项目名）
            for project in df_events.columns[1:-3]:  # 排除 'Year', 'Total events', 'Total disciplines', 'Total sports'
                # 获取该年该项目的子项目数量
                sub_events = df_events.loc[df_events['Year'] == year, project].values[0] if not df_events.loc[
                    df_events['Year'] == year, project].empty else 0

                # 计算比例
                ratio = awards_data / sub_events if sub_events > 0 else 0

                # 使用 pd.concat 替代 append
                new_row = pd.DataFrame({
                    'Year': [year],
                    'Project': [project],
                    'Total Golds': [awards_data],
                    'Sub Events': [sub_events],
                    'Proportion': [ratio]
                })
                result_df = pd.concat([result_df, new_row], ignore_index=True)
        print(country)
        # 如果结果不为空，则写入Excel文件中的新工作表
        if not result_df.empty:
            # 清理工作表名称
            sheet_name = clean_sheet_name(country)
            result_df.to_excel(writer, sheet_name=sheet_name, index=False)
        else:
            print(f"警告：国家 {country} 没有数据，未生成工作表。")

print("处理完成，结果已保存到 'country_awards_ratio.xlsx'")