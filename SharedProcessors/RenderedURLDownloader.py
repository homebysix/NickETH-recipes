#!/usr/local/autopkg/python

import re
import asyncio
import html

from autopkglib import Processor, ProcessorError

from playwright.async_api import async_playwright

__all__ = ["RenderedURLDownloader"]

class RenderedURLDownloader(Processor):
    """Uses Playwright to fetch and render a JavaScript-heavy URL, then performs a regex search."""

    input_variables = {
        # "re_pattern": {
            # "description": "Regular expression (Python) to match against the rendered page.",
            # "required": True,
        # },
        "url": {"description": "URL to fetch and render", "required": True},
        "result_output_var_name": {
            "description": (
                "The name of the output variable that will hold the match. "
                "Defaults to 'match'."
            ),
            "required": False,
            "default": "match",
        },
        # "re_flags": {
            # "description": (
                # "Optional array of Python regex flags (e.g. IGNORECASE, MULTILINE)."
            # ),
            # "required": False,
        # },
        "file_path": {"required": True, "description": "Path to a file to create."},
        "wait_until": {
            "description": (
                "Optional waitUntil option for Playwright (load, domcontentloaded, networkidle). Default: load"
            ),
            "required": False,
            "default": "load",
        },
        "time2load": {
            "description": "Optional wait time to load the page in milliseconds. Default: 2000",
            "required": False,
            "default": 2000,
        },
        "timeout": {
            "description": "Optional timeout in milliseconds. Default: 30000",
            "required": False,
            "default": 30000,
        }
    }

    output_variables = {
        "result_output_var_name": {
            "description": "Matched value from the rendered page.",
        }
    }

    description = __doc__

    # def prepare_re_flags(self) -> int:
        # """Compile regex flags."""
        # flag_accumulator = 0
        # for flag in self.env.get("re_flags", []):
            # if hasattr(re, flag):
                # flag_accumulator |= getattr(re, flag)
        # return flag_accumulator

    async def fetch_page_content(self, url: str, wait_until: str, timeout: int, time2load: int) -> str:
        """Use Playwright to render and extract HTML from the given URL."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
    
            # Ange user-agent manuellt
            user_agent = self.env.get(
                "user_agent",
                #"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15"
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
            )
    
            context = await browser.new_context(user_agent=user_agent)
            page = await context.new_page()
    
            await page.goto(url, wait_until=wait_until, timeout=timeout)
            self.output(f"Time to load page {time2load}")
            await page.wait_for_timeout(time2load)
            content = await page.content()
            await browser.close()
            return content

    # def re_search(self, content: str) -> tuple[str, dict[str, str]] | None:
        # """Search for re_pattern in content"""
        # re_pattern = re.compile(self.env["re_pattern"], flags=self.prepare_re_flags())
        # match = re_pattern.search(content)

        # if not match:
            # raise ProcessorError(f"No match found on rendered URL: {self.env['url']}")

        # return (match.group(match.lastindex or 0), match.groupdict())

    def main(self) -> None:
        url = self.env["url"]
        wait_until = self.env.get("wait_until", "load")
        timeout = int(self.env.get("timeout", 30000))
        time2load = int(self.env.get("time2load", 2000))
        output_var_name = self.env.get("result_output_var_name", "match")

        try:
            content = asyncio.run(
                self.fetch_page_content(url, wait_until=wait_until, timeout=timeout, time2load=time2load)
            )
        except Exception as e:
            raise ProcessorError(f"Playwright error while loading {url}: {e}")
        
        #groupmatch, groupdict = self.re_search(content)

        # for key, value in groupdict.items():
            # if isinstance(value, str):
                # groupdict[key] = html.unescape(value)

        try:
            with open(self.env["file_path"], "w",encoding='utf-8') as fileref:
                #fileref.write(self.env["file_content"])
                fileref.write(content)
            self.output(f"Created file at {self.env['file_path']}")
        except BaseException as err:
            raise ProcessorError(f"Can't create file at {self.env['file_path']}: {err}")


# with open('text.txt', 'w', encoding='utf-8') as f:
    # f.write(text)

        # Favor a named group over unnamed match
        # if output_var_name not in groupdict:
            # groupdict[output_var_name] = groupmatch

        # for key, value in groupdict.items():
            # self.env[key] = value
            # self.output(f"Found match ({key}): {value}")

if __name__ == "__main__":
    processor = RenderedURLDownloader()
    processor.execute_shell()
