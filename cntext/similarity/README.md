



# simtext

simtext可以计算两文档间四大文本相似性指标，分别为：

- Sim_Cosine    cosine相似性
- Sim_Jaccard   Jaccard相似性
- Sim_MinEdit  最小编辑距离
- Sim_Simple  微软Word中的track changes

具体算法介绍可翻看Cohen, Lauren, Christopher Malloy&Quoc Nguyen(2018) 第60页

![](img/论文中的公式.png)

### 安装

```
pip install simtext
```

### 使用

中文文本相似性

```python
from simtext import similarity

text1 = '在宏观经济背景下，为继续优化贷款结构，重点发展可以抵抗经济周期不良的贷款'
text2 = '在宏观经济背景下，为继续优化贷款结构，重点发展可三年专业化、集约化、综合金融+物联网金融四大金融特色的基础上'

sim = similarity()
res = sim.compute(text1, text2)
print(res)
```

Run

```
{'Sim_Cosine': 0.46475800154489, 
'Sim_Jaccard': 0.3333333333333333, 
'Sim_MinEdit': 29, 
'Sim_Simple': 0.9889595182335229}
```



英文文本相似性

```python
from simtext import similarity

A = 'We expect demand to increase.'
B = 'We expect worldwide demand to increase.'
C = 'We expect weakness in sales'

sim = similarity()
AB = sim.compute(A, B)
AC = sim.compute(A, C)

print(AB)
print(AC)
```

Run

```
{'Sim_Cosine': 0.9128709291752769, 
'Sim_Jaccard': 0.8333333333333334, 
'Sim_MinEdit': 2, 
'Sim_Simple': 0.9545454545454546}

{'Sim_Cosine': 0.39999999999999997, 
'Sim_Jaccard': 0.25, 
'Sim_MinEdit': 4, 
'Sim_Simple': 0.9315789473684211}

```



### 参考文献

Cohen, Lauren, Christopher Malloy, and Quoc Nguyen. *Lazy prices*. No. w25084. National Bureau of Economic Research, 2018.

## 如果

如果您是经管人文社科专业背景，编程小白，面临海量文本数据采集和处理分析艰巨任务，个人建议学习[《python网络爬虫与文本数据分析》](https://ke.qq.com/course/482241?tuin=163164df)视频课。作为文科生，一样也是从两眼一抹黑开始，这门课程是用五年时间凝缩出来的。自认为讲的很通俗易懂o(*￣︶￣*)o，

- python入门
- 网络爬虫
- 数据读取
- 文本分析入门
- 机器学习与文本分析
- 文本分析在经管研究中的应用

感兴趣的童鞋不妨 戳一下[《python网络爬虫与文本数据分析》](https://ke.qq.com/course/482241?tuin=163164df)进来看看~

[![](img/课程.png)](https://ke.qq.com/course/482241?tuin=163164df)



## 更多

- [B站:大邓和他的python](https://space.bilibili.com/122592901/channel/detail?cid=66008)

- 公众号：大邓和他的python

- [知乎专栏：数据科学家](https://zhuanlan.zhihu.com/dadeng)


![](img/大邓和他的Python.png)
