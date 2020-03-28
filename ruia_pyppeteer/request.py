#!/usr/bin/env python
"""
 Created by howie.hu at 2018/11/22.
"""
import asyncio
import async_timeout
import pyppeteer

from typing import Optional

from ruia import Request
from ruia.response import Response
from ruia_pyppeteer.response import PyppeteerResponse


class PyppeteerRequest(Request):
    def __init__(
        self,
        url: str,
        method: str = "GET",
        *,
        callback=None,
        encoding: Optional[str] = None,
        headers: dict = None,
        metadata: dict = None,
        request_config: dict = None,
        request_session=None,
        load_js: bool = True,
        pyppeteer_args: list = None,
        pyppeteer_launch_options: dict = None,
        pyppeteer_page_options: dict = None,
        pyppeteer_viewport: dict = None,
        close_pyppeteer_browser=False,
        **kwargs,
    ):
        super(PyppeteerRequest, self).__init__(
            url,
            method,
            callback=callback,
            encoding=encoding,
            headers=headers,
            metadata=metadata,
            request_config=request_config,
            request_session=request_session,
            **kwargs,
        )
        self.load_js = load_js
        self.pyppeteer_args = pyppeteer_args or []
        self.pyppeteer_launch_options = pyppeteer_launch_options or {}
        self.pyppeteer_page_options = pyppeteer_page_options or {}
        self.pyppeteer_viewport = pyppeteer_viewport or {"width": 1080, "height": 900}
        self.close_pyppeteer_browser = close_pyppeteer_browser

    async def fetch(self) -> PyppeteerResponse:
        """Fetch all the information by using aiohttp"""
        if self.request_config.get("DELAY", 0) > 0:
            await asyncio.sleep(self.request_config["DELAY"])

        timeout = self.request_config.get("TIMEOUT", 10)
        try:
            if self.load_js:
                if not hasattr(self, "browser"):
                    self.pyppeteer_args.extend(["--no-sandbox"])
                    self.browser = await pyppeteer.launch(
                        headless=True,
                        args=self.pyppeteer_args,
                        options=self.pyppeteer_launch_options,
                    )
                page = await self.browser.newPage()
                self.pyppeteer_page_options.update({"timeout": int(timeout * 1000)})

                resp = await page.goto(self.url, options=self.pyppeteer_page_options)
                await page.setViewport(self.pyppeteer_viewport)

                resp_data = await page.content()
                response = PyppeteerResponse(
                    url=self.url,
                    method=self.method,
                    encoding=self.encoding,
                    html=resp_data,
                    page=page,
                    browser=self.browser,
                    metadata=self.metadata,
                    cookies=await page.cookies(),
                    headers=resp.headers,
                    history=(),
                    status=resp.status,
                    aws_json=resp.json,
                    aws_text=resp.text,
                    aws_read=resp.buffer,
                )
            else:
                async with async_timeout.timeout(timeout):
                    resp = await self._make_request()
                resp_data = await resp.text(encoding=self.encoding)
                response = Response(
                    url=self.url,
                    method=self.method,
                    encoding=resp.get_encoding(),
                    html=resp_data,
                    metadata=self.metadata,
                    cookies=resp.cookies,
                    headers=resp.headers,
                    history=resp.history,
                    status=resp.status,
                    aws_json=resp.json,
                    aws_text=resp.text,
                    aws_read=resp.read,
                )
            if not response.ok:
                return await self._retry(
                    error_msg=f"Request url failed with status {response.status}!"
                )
            return response
        except asyncio.TimeoutError:
            # Retry for timeout
            return await self._retry("timeout")
        finally:
            # Close client session
            await self._close_request()
            if self.close_pyppeteer_browser:
                await self.browser.close()
