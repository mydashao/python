from lxml import etree

text='''
<li class="li" name="item"><a href="cvdv"><span>first item</span></a></li>

'''

html =etree.HTML(text)
result=html.xpath('//li[contains(@class,"pi")and @name="comtent"]/b/text()')
print(result)

result=html.xpath('//li[1]//*')
print(result)