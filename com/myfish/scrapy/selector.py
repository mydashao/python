from scrapy.selector import Selector

text = '''
<html>
    <body>
        <h1>Hello World</h1>
        <h1>Hello Scrapy</h1>
        <b>Hello python</b>
        <ul>
            <li>C++</li>
            <li>Java</li>
            <li>Python</li>
        </ul>
    </body>
</html>
'''

selector = Selector(text=text)
selector_list = selector.xpath('//li/text()')
for text in selector_list:
    print(text)
    print(text.extract())
print(selector_list.extract())
