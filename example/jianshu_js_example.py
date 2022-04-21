#!/usr/bin/env python
"""
 Created by howie.hu at 2018/9/8.
"""

from ruia import AttrField, Item, TextField

from ruia_pyppeteer import PyppeteerSpider as Spider


class JianshuItem(Item):
    target_item = TextField(css_select="ul.list>li")
    author_name = TextField(css_select="a.name")
    author_url = AttrField(attr="href", css_select="a.name")

    async def clean_author_name(self, author_name):
        return author_name.strip()

    async def clean_author_url(self, author_url):
        return f"https://www.jianshu.com{author_url}"


class JianshuSpider(Spider):
    start_urls = ["https://www.jianshu.com/"]
    concurrency = 10

    async def parse(self, response):
        html = await response.page.content()
        async for item in JianshuItem.get_items(html=html):
            # Loading js by using PyppeteerRequest
            print(item)
        await response.browser.close()


if __name__ == "__main__":
    JianshuSpider.start()
