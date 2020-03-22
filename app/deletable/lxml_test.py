# lxml_test.py

# 使用 lxml 的 etree 库
import requests
from lxml import etree

# response = requests.get('http://gdutnews.gdut.edu.cn/')
# content = response.content
# content = content.decode('utf-8')
# html = etree.HTML(content)
# print(html)


text = requests.get('http://gdutnews.gdut.edu.cn/')
# print(text)
text = text.content

# print(text)
text = text.decode('utf-8')
# print(text)

# 利用etree.HTML，将字符串解析为HTML文档
html = etree.HTML(text)
tmp = html.xpath('//li')
print(tmp)
for i in tmp:
    print(i)
# print(html)
# print(type(html))
# 按字符串序列化HTML文档
result = etree.tostring(html)
# print(result)
# print(type(result))
