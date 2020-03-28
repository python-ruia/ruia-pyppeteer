#!/usr/bin/env python
from typing import Callable

from ruia.response import Response


class PyppeteerResponse(Response):
    def __init__(
        self,
        url: str,
        method: str,
        *,
        encoding: str = "",
        html: str = "",
        page,
        browser,
        metadata: dict,
        cookies,
        history,
        headers: dict = None,
        status: int = -1,
        aws_json: Callable = None,
        aws_read: Callable = None,
        aws_text: Callable = None,
    ):
        super(PyppeteerResponse, self).__init__(
            url=url,
            method=method,
            encoding=encoding,
            html=html,
            metadata=metadata,
            cookies=cookies,
            history=history,
            headers=headers,
            status=status,
            aws_json=aws_json,
            aws_read=aws_read,
            aws_text=aws_text,
        )
        self._page = page
        self._browser = browser

    @property
    def page(self):
        return self._page

    @property
    def browser(self):
        return self._browser

    async def json(self, **kwargs):
        """Read and decodes JSON response."""
        return await self._aws_json(**kwargs)

    async def read(self, **kwargs):
        """Read response payload."""
        return await self._aws_read(**kwargs)

    async def text(self, **kwargs):
        """Read response payload and decode."""
        return await self._aws_text(**kwargs)

    def __str__(self):
        return f"<PyppeteerResponse url[{self._method}]: {self._url} status:{self._status}>"
