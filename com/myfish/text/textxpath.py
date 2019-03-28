from lxml import etree

text = '''
<li class="lili" style="margin-bottom: 20px; margin-top: 10px;">
        <span class="span1">学习强国</span>
        <span class="span2">span2</span>
 '''

html = etree.HTML(text)
ss = etree.tostring(html)
result = html.xpath('//li/span[@class="span1"]/text()')
print(result)