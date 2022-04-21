#!/usr/bin/env python
"""
 Created by howie.hu at 2018/11/23.
"""

import asyncio

from ruia_pyppeteer import PyppeteerRequest as Request

# pyppeteer_args = ['--proxy-server=127.0.0.1:1087']
pyppeteer_args = []
pyppeteer_page_options = {
    "waitUntil": "networkidle0",
}


async def load_js_script():
    request = Request("https://www.jianshu.com/")
    response = await request.fetch()
    # await response.page.screenshot(path="example.png")
    dimensions = await response.page.evaluate(
        """() => {
            return {
                width: document.documentElement.clientWidth,
                height: document.documentElement.clientHeight,
                deviceScaleFactor: window.devicePixelRatio,
            }
        }"""
    )

    print(dimensions)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(load_js_script())
