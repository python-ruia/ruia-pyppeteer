#!/usr/bin/env python
"""
 Created by howie.hu at 2018/11/22.
"""
import asyncio
import async_timeout
import pyppeteer

from inspect import iscoroutinefunction

from ruia import Request
from ruia.response import Response


class PyppeteerRequest(Request):

    def __init__(self, url: str, method: str = 'GET', *,
                 callback=None,
                 headers: dict = {},
                 load_js: bool = False,
                 metadata: dict = {},
                 pyppeteer_args: list = [],
                 pyppeteer_launch_options: dict = {},
                 pyppeteer_page_options: dict = {},
                 request_config: dict = {},
                 request_session=None,
                 res_type: str = 'text',
                 **kwargs):
        super(PyppeteerRequest, self).__init__(url, method,
                                               callback=callback,
                                               headers=headers,
                                               metadata=metadata,
                                               request_config=request_config,
                                               request_session=request_session,
                                               res_type=res_type,
                                               **kwargs)
        self.load_js = load_js
        self.pyppeteer_args = pyppeteer_args
        self.pyppeteer_launch_options = pyppeteer_launch_options
        self.pyppeteer_page_options = pyppeteer_page_options

    async def fetch(self) -> Response:
        if self.request_config.get('DELAY', 0) > 0:
            await asyncio.sleep(self.request_config['DELAY'])
        try:
            timeout = self.request_config.get('TIMEOUT', 10)

            if self.load_js:
                if not hasattr(self, "browser"):
                    self.pyppeteer_args.extend(['--no-sandbox'])
                    self.browser = await pyppeteer.launch(
                        headless=True,
                        args=self.pyppeteer_args,
                        options=self.pyppeteer_launch_options
                    )
                page = await  self.browser.newPage()
                self.pyppeteer_page_options.update({'timeout': int(timeout * 1000)})
                res = await page.goto(self.url, options=self.pyppeteer_page_options)
                data = await page.content()
                res_cookies = await page.cookies()
                res_headers = res.headers
                res_history = None
                res_status = res.status
            else:
                async with async_timeout.timeout(timeout):
                    async with self.current_request_func as resp:
                        res_status = resp.status
                        assert res_status in [200, 201]
                        if self.res_type == 'bytes':
                            data = await resp.read()
                        elif self.res_type == 'json':
                            data = await resp.json()
                        else:
                            data = await resp.text()
                        res_cookies, res_headers, res_history = resp.cookies, resp.headers, resp.history
        except Exception as e:
            res_headers = {}
            res_history = ()
            res_status = 0
            data, res_cookies = None, None
            self.logger.error(f"<Error: {self.url} {res_status} {str(e)}>")

        if self.retry_times > 0 and data is None:
            retry_times = self.request_config.get('RETRIES', 3) - self.retry_times + 1
            self.logger.info(f'<Retry url: {self.url}>, Retry times: {retry_times}')
            self.retry_times -= 1
            retry_func = self.request_config.get('RETRY_FUNC')
            if retry_func and iscoroutinefunction(retry_func):
                request_ins = await retry_func(self)
                if isinstance(request_ins, Request):
                    return await request_ins.fetch()
            return await self.fetch()

        await self.close()

        response = Response(url=self.url,
                            html=data,
                            metadata=self.metadata,
                            res_type=self.res_type,
                            cookies=res_cookies,
                            headers=res_headers,
                            history=res_history,
                            status=res_status)
        return response
