from lxml import etree

text='''
    <div class="div1_1">
        <div class="div2_1">
            <h2 id="h2">h2的标签</h2>
			<h3 id="h3">h3的标签</h3>
		    div2_1的内容
		</div>
        <div class="div2_2" id="last_div">
        	<h4 class="h4 pic">h4的标签</h4>
        	<h4 class="h4 pic" id="otherH4">另一个h4的标签</h4>
            <a href="a1"><img src="https://www.text.jpg" alt="pic" /></a>div2_2的内容</div>
        <div class="div2_3">div2_3的内容</div>
    </div>
'''
print('XPath测试')
html =etree.HTML(text)
# 标签对象获取
result0=html.xpath('//div[@class="div2_1"]')
# 父节点获取
result1=html.xpath('//h4/../@class')
# 子孙节点获取
result2=html.xpath('//div[@class="div1_1"]//@class')
# 标签文本获取
result3=html.xpath('//div[@class="div2_1"]/h2/text()')
# 标签属性获取
result4=html.xpath('//div[@class="div2_2"]/a/img/@src')
# 属性多值匹配
result5=html.xpath('//h4[@class="h4 pic"]/text()')
result6=html.xpath('//h4[contains(@class,"h4")]/text()')
# 多属性匹配
result7=html.xpath('//h4[@id="otherH4" and contains(@class,"h4")]/text()')

# print('     标签对象获取：',result0)
# print('     父节点获取  ：',result1)
# print('     子孙节点获取：',result2)
# print('     标签文本获取：',result3)
# print('     标签属性匹配：',result4)
# print('     属性多值匹配：',result5)
# print('     属性多值匹配：',result6)
# print('     多属性匹配  ：',result7)

print('requests测试')

from bs4 import BeautifulSoup
soup = BeautifulSoup(text,'lxml')
# 顺序定位与精确匹配，结果一样
result0 = soup.div.div.h2
result0 = soup.find('h2',id='h2')
# 父子节点定位
result1 = soup.find_parent('div', class_="div2_1")
# 标签文本获取
result3 = soup.div.div.h2.text
result3 = soup.div.div.h2.string
result3 = soup.div.div.h2.get_text()
# 标签信息获取
result4 = soup.find('a', href="a1").img.attrs['src']
result4 = soup.find(attrs={'alt':'pic'}).attrs['src']
# 属性多值匹配
result5 = soup.find('h4', class_="h4 pic").text
# 多属性匹配
result6 = soup.find(attrs={'class':'h4','id':'otherH4'}).text

print('     标签对象获取：',result0)
print('     父节点获取  ：',result1)
print('     子孙节点获取：',result1)
print('     标签文本获取：',result3)
print('     标签属性匹配：',result4)
print('     属性多值匹配：',result5)
print('     多属性匹配  ：',result6)










