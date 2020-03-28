#!/usr/bin/env python
"""
 Created by howie.hu at 2018/11/22.
"""

from typing import Optional

from ruia import Spider
from ruia_pyppeteer.request import PyppeteerRequest as Request


class PyppeteerSpider(Spider):
    pyppeteer_args = []
    pyppeteer_launch_options = {}
    pyppeteer_page_options = {}
    pyppeteer_viewport = {}
    close_pyppeteer_browser = True

    def request(
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
        close_pyppeteer_browser: bool = None,
        **kwargs
    ):
        """Init a Request class for crawling html"""
        headers = headers or {}
        metadata = metadata or {}
        request_config = request_config or {}
        request_session = request_session or self.request_session
        pyppeteer_args = pyppeteer_args or []
        pyppeteer_launch_options = pyppeteer_launch_options or {}
        pyppeteer_page_options = pyppeteer_page_options or {}
        pyppeteer_viewport = pyppeteer_viewport or {}
        close_pyppeteer_browser = (
            close_pyppeteer_browser or self.close_pyppeteer_browser
        )

        headers.update(self.headers.copy())
        request_config.update(self.request_config.copy())

        pyppeteer_args.extend(self.pyppeteer_args.copy())
        pyppeteer_launch_options.update(self.pyppeteer_launch_options.copy())
        pyppeteer_page_options.update(self.pyppeteer_page_options.copy())
        pyppeteer_viewport.update(self.pyppeteer_viewport.copy())

        return Request(
            url,
            method,
            callback=callback,
            encoding=encoding,
            headers=headers,
            metadata=metadata,
            request_config=request_config,
            request_session=request_session,
            load_js=load_js,
            pyppeteer_args=pyppeteer_args,
            pyppeteer_launch_options=pyppeteer_launch_options,
            pyppeteer_page_options=pyppeteer_page_options,
            pyppeteer_viewport=pyppeteer_viewport,
            close_pyppeteer_browser=close_pyppeteer_browser,
        )
