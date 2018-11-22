#!/usr/bin/env python
"""
 Created by howie.hu at 2018/11/22.
"""
import asyncio

from signal import SIGINT

from ruia import Spider
from ruia_pyppeteer.request import PyppeteerRequest


class PyppeteerSpider(Spider):

    async def start_master(self):
        for url in self.start_urls:
            request_ins = PyppeteerRequest(url=url,
                                           callback=self.parse,
                                           headers=getattr(self, 'headers', {}),
                                           load_js=getattr(self, 'load_js', False),
                                           metadata=getattr(self, 'metadata', {}),
                                           request_config=getattr(self, 'request_config'),
                                           request_session=getattr(self, 'request_session', None),
                                           res_type=getattr(self, 'res_type', 'text'),
                                           **getattr(self, 'kwargs', {}))
            # self.request_queue.put_nowait(request_ins.fetch_callback(self.sem))
            self.request_queue.put_nowait(self.handle_request(request_ins))
        workers = [asyncio.ensure_future(self.start_worker()) for i in range(2)]
        await self.request_queue.join()
        await self.stop(SIGINT)
