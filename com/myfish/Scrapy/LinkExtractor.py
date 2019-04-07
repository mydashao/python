from scrapy.linkextractors import LinkExtractor
import scrapy
# 创建一个LinkExtractor对象，使用一个或多个构造器参数描述提取规则，这
# 里传递给restrict_css参数一个CSS选择器表达式。它描述出下一页链接所在
# 的区域（在li.next下）。
class BooksSpider(scrapy.Spider):
    def parse(self, response):
        # 提取链接
        # 下一页的url 在ul.pager > li.next > a 里面
        # 例如: <li class="next"><a href="catalogue/page-2.html">next</a></li>
        le = LinkExtractor(restrict_css='ul.pager li.next')
        # 调用LinkExtractor对象的extract_links方法传入一个Response对象，该方法
        # 依据创建对象时所描述的提取规则，在Response对象所包含的页面中提取链
        # 接，最终返回一个列表，其中的每一个元素都是一个Link对象，即提取到的一
        # 个链接。
        links = le.extract_links(response)
        # 由于页面中的下一页链接只有一个，因此用links[0]
        # 获取Link对象，Link对象
        # 的url属性便是链接页面的绝对url地址（无须再调用response.urljoin方
        # 法），用其构造Request对象并提交。
        if links:
            next_url = links[0].url
        yield scrapy.Request(next_url, callback=self.parse)