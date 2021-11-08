import pyecharts.options as opts
from pyecharts.charts import WordCloud
from cntext.stats.stats import term_freq
from shifterator import EntropyShift


def wordcloud(text, title, html_path):
    """
    使用pyecharts库绘制词云图
    :param text:  中文文本字符串数据
    :param title:  词云图标题
    :param html_path:  词云图html文件存储路径
    :return:
    """
    wordfreq_dict = dict(term_freq(text))
    wordfreqs = [(word, str(freq)) for word, freq in wordfreq_dict.items()]
    wc = WordCloud()
    wc.add(series_name="", data_pair=wordfreqs, word_size_range=[20, 100])
    wc.set_global_opts(
        title_opts=opts.TitleOpts(title=title,
                                  title_textstyle_opts=opts.TextStyleOpts(font_size=23)
                                  ),
        tooltip_opts=opts.TooltipOpts(is_show=True))
    wc.render(html_path)  #存储位置
    print('可视化完成，请前往 {} 查看'.format(html_path))




def wordshiftor(text1, text2, title, top_n=50, matplotlib_family='Arial Unicode MS'):
    """
    使用shifterator库绘制词移图，可用于查看两文本在词语信息熵上的区别
    :param text1:  文本数据1；字符串
    :param text2:  文本数据2；字符串
    :param title:  词移图标题
    :param top_n:  显示最常用的前n词； 默认值15
    :param matplotlib_family matplotlib中文字体，默认"Arial Unicode MS"；如绘图字体乱码请，请参考下面提示

        设置参数matplotlib_family，需要先运行下面代码获取本机字体列表
        from matplotlib.font_manager import FontManager
        mpl_fonts = set(f.name for f in FontManager().ttflist)
        print(mpl_fonts)
    """
    import matplotlib
    matplotlib.rc("font", family=matplotlib_family)
    type2freq_1 = term_freq(text1)

    type2freq_2 = term_freq(text2)

    entropy_shift = EntropyShift(type2freq_1=type2freq_1,
                                 type2freq_2=type2freq_2,
                                 base=2)
    entropy_shift.get_shift_graph(title=title, top_n=top_n)

