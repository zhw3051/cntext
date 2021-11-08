from setuptools import setup
import setuptools

setup(
    name='cntext',     # 包名字
    version='0.9',   # 包版本
    description='中文文本分析库，可对文本进行词频统计、词典扩充、情绪分析、相似度、可读性等',   # 简单描述
    author='大邓',  # 作者
    author_email='thunderhit@qq.com',  # 邮箱
    url='https://github.com/thunderhit/cntext',      # 包的主页
    packages=setuptools.find_packages(),
    install_requires=['jieba', 'numpy', 'scikit-learn==1.0', 'numpy', 'matplotlib', 'pyecharts', 'shifterator'],
    python_requires='>=3.5',
    license="MIT",
    keywords=['chinese', 'text mining', 'sentiment', 'sentiment analysis', 'natural language processing', 'sentiment dictionary development', 'text similarity'],
    long_description=open('README.md').read(), # 读取的Readme文档内容
    long_description_content_type="text/markdown")  # 指定包文档格式为markdown
    #py_modules = ['eventextraction.py']
