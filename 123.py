import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# 数据
data = {
    'Year': [1896, 1900, 1904, 1906, 1908, 1912, 1920, 1924, 1928, 1932, 1936, 1948, 1952, 1956, 1960, 1964, 1968, 1972, 1976, 1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020, 2024],
    'F': [0.0, 33.0, 16.0, 11.0, 47.0, 87.0, 134.0, 244.0, 404.0, 347.0, 468.0, 628.0, 1497.0, 893.0, 1435.0, 1348.0, 1777.0, 2193.0, 2172.0, 1756.0, 2447.0, 3543.0, 4124.0, 5008.0, 5431.0, 5546.0, 5816.0, 5815.0, 6223.0, 7266.0, 7312.0],
    'M': [380.0, 1903.0, 1285.0, 1722.0, 3054.0, 3953.0, 4158.0, 4989.0, 4588.0, 2622.0, 6038.0, 5777.0, 6773.0, 4234.0, 6684.0, 6354.0, 6811.0, 8111.0, 6469.0, 5435.0, 7007.0, 8494.0, 8853.0, 8772.0, 8390.0, 7897.0, 7786.0, 7105.0, 7465.0, 7855.0, 7580.0],
    'Male/Female Ratio': [np.inf, 57.666667, 80.312500, 156.545455, 64.978723, 45.436782, 31.029851, 20.446721, 11.356436, 7.556196, 12.901709, 9.199045, 4.524382, 4.741321, 4.657840, 4.713650, 3.832864, 3.698586, 2.978361, 3.095103, 2.863506, 2.397403, 2.146702, 1.751597, 1.544835, 1.423909, 1.338721, 1.221840, 1.199582, 1.081062, 1.036652]
}

df = pd.DataFrame(data)

# 设置风格
sns.set_style("whitegrid")

# 第一张图：男女数量的柱状图和男女比例的折线图
fig, ax1 = plt.subplots(figsize=(14, 6))

# 绘制男女数量的柱状图（增加宽度）
bar_width = 0.6
ax1.bar(df['Year'] - bar_width/2, df['F'], width=bar_width, label='Female Athletes', color='pink', alpha=0.8)
ax1.bar(df['Year'] + bar_width/2, df['M'], width=bar_width, label='Male Athletes', color='blue', alpha=0.8)
ax1.set_xlabel('Year', fontsize=14)
ax1.set_ylabel('Number of Athletes', fontsize=14)
ax1.set_title('Number of Male and Female Athletes Over Time', fontsize=16)

# 添加第二个 y 轴（男女比例的折线图）
ax2 = ax1.twinx()
ax2.plot(df['Year'], df['Male/Female Ratio'], color='red', label='Male/Female Ratio', marker='o', linestyle='-', markersize=8, linewidth=2)
ax2.set_ylabel('Male/Female Ratio', fontsize=14)
ax2.set_ylim(0, 50)  # 限制比例范围，避免无穷大值影响

# 合并图例
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc='upper left', fontsize=12)

plt.tight_layout()
plt.show()

# 第二张图：男女数量的热力图
plt.figure(figsize=(14, 6))
# 为了让男女数量变化更明显，采用蓝色渐变的热力图
heatmap_data = df[['Year', 'F', 'M']].set_index('Year')
sns.heatmap(heatmap_data.T, cmap='Blues', annot=True, fmt=".0f", cbar_kws={'label': 'Number of Athletes'})
plt.title('Number of Male and Female Athletes Over Time (Heatmap)', fontsize=16)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Athletes', fontsize=14)
plt.tight_layout()
plt.show()
