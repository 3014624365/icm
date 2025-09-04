import numpy
import pandas
from spsspro.algorithm import statistical_model_analysis
#生成案例数据
data = pandas.DataFrame({
    "A": numpy.random.random(size=20),
    "B": numpy.random.random(size=20),
    "C": numpy.random.random(size=20),
    "D": numpy.random.random(size=20)
})
#主成分分析，输入参数详细可以光标放置函数括号内按shift+tab查看，输出结果参考spsspro模板分析报告
result = statistical_model_analysis.principal_component_analysis(data, n_factors=3)
print(result)