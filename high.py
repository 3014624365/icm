import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# ============================
# 数据预处理与特征工程
# ============================

def load_and_preprocess_data(file_path):
    """
    加载数据并进行预处理
    """
    # 加载数据
    data = pd.read_csv(file_path)

    # 按国家(NOC)、项目(Sport)和年份(Year)分组聚合
    grouped = data.groupby(['NOC', 'Sport', 'Year']).agg(
        Gold=('Medal', lambda x: (x == 'Gold').sum()),
        Silver=('Medal', lambda x: (x == 'Silver').sum()),
        Bronze=('Medal', lambda x: (x == 'Bronze').sum())
    ).reset_index()

    # 计算项目总分（Gold:3, Silver:2, Bronze:1）
    grouped['Score'] = grouped['Gold'] * 3 + grouped['Silver'] * 2 + grouped['Bronze']

    return grouped

def build_feature_matrix(grouped):
    """
    构建特征矩阵
    """
    # 定义核心特征维度
    features = {
        '奖牌稳定性': lambda df: df.groupby(['NOC', 'Sport'])['Score'].std(),  # 标准差衡量稳定性
        '时间趋势': lambda df: df.groupby(['NOC', 'Sport'])['Year'].apply(
            lambda x: np.polyfit(x, df.loc[x.index, 'Score'], 1)[0]  # 线性趋势斜率
        ),
        '竞争力指数': lambda df: df.groupby(['NOC', 'Sport'])['Score'].sum() /
                             df.groupby('NOC')['Score'].sum().max(),  # 项目贡献占比
        '持续参赛性': lambda df: df.groupby(['NOC', 'Sport'])['Year'].nunique()  # 参赛届数
    }

    # 生成特征矩阵
    feature_matrix = pd.DataFrame()
    for name, func in features.items():
        feature_matrix[name] = func(grouped)
    feature_matrix = feature_matrix.fillna(0)

    return feature_matrix

# ============================
# 主成分分析-灰色关联度融合算法
# ============================

def pca_transform(feature_matrix):
    """
    主成分分析（PCA）降维
    """
    # 标准化数据
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(feature_matrix)

    # PCA降维（保留85%方差）
    pca = PCA(n_components=0.85)
    principal_components = pca.fit_transform(scaled_data)

    return principal_components, pca

def grey_relation_coeff(reference, compared, rho=0.5):
    """
    计算灰色关联系数
    """
    delta = np.abs(reference - compared)
    min_delta = np.min(delta)
    max_delta = np.max(delta)
    return (min_delta + rho * max_delta) / (delta + rho * max_delta)

def calculate_grey_relations(feature_matrix):
    """
    计算各项目与总奖牌的灰色关联度
    """
    # 以国家总奖牌为参考序列
    national_total = feature_matrix.groupby('NOC').sum().sum(axis=1)

    # 计算各项目与总奖牌的关联度
    grey_relations = []
    for sport in feature_matrix.index.levels[1]:
        sport_scores = feature_matrix.xs(sport, level='Sport').sum(axis=1)
        coeff = grey_relation_coeff(national_total, sport_scores)
        grey_relations.append(coeff.mean())  # 取国家平均关联度

    return grey_relations

def calculate_final_weights(pca, grey_relations):
    """
    计算融合权重
    """
    # PCA权重（方差贡献率）
    pca_weights = pca.explained_variance_ratio_

    # GRA权重归一化
    grey_weights = grey_relations / np.sum(grey_relations)

    # 融合权重（各50%）
    final_weights = 0.5 * pca_weights + 0.5 * grey_weights

    return final_weights

def calculate_sport_scores(principal_components, final_weights, feature_matrix):
    """
    计算项目综合评分
    """
    sport_scores = pd.Series(
        np.dot(principal_components, final_weights),
        index=feature_matrix.index
    )
    return sport_scores

# ============================
# 战略核心项目识别与可视化
# ============================

def identify_strategic_sports(sport_scores, country_code='CHN', top_n=5):
    """
    识别指定国家的战略核心项目
    """
    # 获取指定国家的项目评分
    country_sports = sport_scores.xs(country_code, level='NOC').sort_values(ascending=False)[:top_n]

    # 可视化
    plt.figure(figsize=(10, 6))
    country_sports.plot(kind='barh', color='goldenrod')
    plt.title(f'{country_code} Strategic Core Sports Identification')
    plt.xlabel('Comprehensive Score (PCA-GRA Fusion)')
    plt.grid(axis='x')
    plt.show()

    return country_sports

# ============================
# 主程序
# ============================

if __name__ == "__main__":
    # 数据文件路径
    file_path = 'summerOly_athletes.csv'

    # 数据预处理与特征工程
    grouped_data = load_and_preprocess_data(file_path)
    feature_matrix = build_feature_matrix(grouped_data)

    # 主成分分析（PCA）降维
    principal_components, pca = pca_transform(feature_matrix)

    # 计算灰色关联度
    grey_relations = calculate_grey_relations(feature_matrix)

    # 计算融合权重
    final_weights = calculate_final_weights(pca, grey_relations)

    # 计算项目综合评分
    sport_scores = calculate_sport_scores(principal_components, final_weights, feature_matrix)

    # 识别并可视化战略核心项目
    identify_strategic_sports(sport_scores, country_code='CHN', top_n=5)