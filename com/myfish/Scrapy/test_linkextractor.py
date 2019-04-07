example1='''
<html>
<body>
<div id="top">
<p>下面是一些站内链接</p>
<a class="internal" href="/intro/install.html">Installation guide</<a class="internal" href="/intro/tutorial.html">Tutorial</a>
<a class="internal" href="../examples.html">Examples</a>
</div>
<div id="bottom">
<p>下面是一些站外链接</p>
<a href="http://stackoverflow.com/tags/scrapy/info">StackOverflow</<a href="https://github.com/scrapy/scrapy">Fork on Github</a>
</div>
</body>
</html>
'''

example2='''

<!-- example2.html -->
<html>
<head>
<script type='text/javascript' src='/js/app1.js'/>
<script type='text/javascript' src='/js/app2.js'/>
</head>
<body>
<a href="/home.html">主页</a>
<a href="javascript:goToPage('/doc.html'); return false">文档</a>
<a href="javascript:goToPage('/example.html'); return false">案例</a>
</body>
</html>
'''

from scrapy.http import HtmlResponse
# html1 = open('exmaple1.html').read()
# html2 = open('exmaple2.html').read()
response1 = HtmlResponse(url='',body=example1, encoding='GBK')
response2 = HtmlResponse(url='',body=example2, encoding='GBK')

from scrapy.linkextractors import LinkExtractor
le = LinkExtractor()
links = le.extract_links(response1)
[link.url for link in links]
