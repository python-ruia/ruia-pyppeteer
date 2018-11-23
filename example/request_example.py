#!/usr/bin/env python
"""
 Created by howie.hu at 2018/11/23.
"""

import asyncio

from ruia_pyppeteer import PyppeteerRequest as Request

pyppeteer_page_options = {'waitUntil': 'networkidle0'}

request = Request("https://www.jianshu.com/", load_js=True, pyppeteer_page_options=pyppeteer_page_options)
response = asyncio.get_event_loop().run_until_complete(request.fetch())
print(response.html)