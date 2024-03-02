# !/usr/local/autopkg/python
#
# Based on code from Greg Neagle, Timoty Sutton,
# Per Olofsson, and Michael Moravec
#
# Copyleft 2021 The Pennsylvania State University
#
# Slightley altered for Windows. 220602, Nick Heim
# Added a 1 second sleep after each command for stability.
# Implemented Edge compatibility, see: https://docs.microsoft.com/en-us/microsoft-edge/webdriver-chromium/?tabs=python
# Changes to selenium 4. "executable_path" was deprecated and has been removed!
# See: https://stackoverflow.com/questions/64717302/deprecationwarning-executable-path-has-been-deprecated-selenium-python
# More work to follow...

from autopkglib import Processor, ProcessorError
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import shutil
import os
import re
import time
import fnmatch

__all__ = ["Selenium"]
__version__ = "1.0.5"


class Selenium(Processor):
    """
    This processor aims to expose Selenium functionality
    to AutoPkg. The end result of this processor could be
    a regexp match. Although this processor could be used
    where a download URL can only be retrieved after a user
    navigates a website.
    This processor can do a full array of webdriver-calls
    in one sweep.    
    """

    input_variables = {
        "primary_url": {
            "description": "The first url that will be retrieved.",
            "required": True
        },
        "re_pattern": {
            "description": (
                "Regular expression (Python) to match against page."
            ),
            "required": False,
            "default": "[\s\S]*"
        },
        "browser_used": {
            "description": (
                "Browser to use with webdriver. "
                "Chrome or Edge(Chromium). Defaults to Chrome."
            ),
            "required": False,
            "default": "Chrome"
        },
        "selenium_options": {
            "description": (
                "An array of strings to execute prior to the web driver "
                "being initialized.  While some options may be set after "
                "initialization, within the 'selenium_commands' section, "
                "most should be set here."
            ),
            "required": False,
            "default": []
        },
        "selenium_commands": {
            "description": (
                "An array of strings to execute once the web driver is "
                "initialized.  Note that when these commands finish "
                "executing, the page_source property will be matched "
                "against the re_pattern variable to return your final "
                "result. "
                "If no commands are given in this variable, a simple "
                "regex match will be performed against the primary_url "
                "similar to the standard URLTexSearcher processor."
            ),
            "required": False,
            "default": None
        },
        "result_output_var_name": {
            "description": (
                "The name of the output variable that is returned "
                "by the match. If not specified then a default of "
                '"match" will be used.'
            ),
            "required": False,
            "default": "match"
        },
        "browser_binary_path": {
            "description": (
                "The full path to the binary of the web browser to use. "
                "Must be compatible with the selenium web driver binary."
            ),
            "required": False,
            "default": (
                "/Library/AutoPkg/SeleniumEngine/bin/Google Chrome.app/"
                "Contents/MacOS/Google Chrome"
            )
        },
        "webdriver_binary_path": {
            "description": (
                "The full path to the selenium web driver binary. "
                "This must be compatible with the web browser used."
            ),
            "required": False,
            "default": "/Library/AutoPkg/SeleniumEngine/bin/chromedriver"
        },
        "user_data_dir": {
            "description": (
                "The path to the directory to use for user data for "
                "the Selenium session. Cookies will be saved here. "
                "Setting this variable to an empty string "
                "will cause Selenium use its randomly generated path. "
                "This effectively purges the session once this processor "
                "run completes. Optionally you may wish to use PathDeleter "
                "between subsequent Selenium calls to purge and re-use the "
                "default directory."
                "Defaults to %RECIPE_CACHE_DIR%/selenium_user_data"
            ),
            "required": False
        }
    }
    output_variables = {
        "result_output_var_name": {
            "description": (
                "First matched sub-pattern from input found on the fetched "
                "URL. Note the actual name of variable depends on the input "
                'variable "result_output_var_name" or is assigned a default '
                'of "match." Named capture groups are also returned with the '
                'capture group name as the AutoPkg variable name.'
            )
        }
    }

    description = __doc__

    # RegEx matching functions copied nearly verbatim from
    # URLTextSearcher.

    def prepare_re_flags(self):
        self.output("Preparing RegEx flags", verbose_level=3)
        """Create flag varible for re.compile"""
        flag_accumulator = 0
        for flag in self.env.get("re_flags", {}):
            if flag in re.__dict__:
                flag_accumulator += re.__dict__[flag]

        self.output("Done Preparing RegEx flags", verbose_level=3)
        return flag_accumulator

    def re_search(self, content, url):
        """Search for re_pattern in content"""
        self.output("Entering regex search function.", verbose_level=3)
        re_pattern = re.compile(
            self.env["re_pattern"], flags=self.prepare_re_flags())

        self.output("Performing match.", verbose_level=3)
        match = re_pattern.search(content)

        if not match:
            raise ProcessorError(
                "No match found on url ({})".format(
                    url
                )
            )

        self.output("Finished regex search.", verbose_level=3)
        # return the last matched group with the dict of named groups
        return (match.group(match.lastindex or 0), match.groupdict())

    def main(self):

        # Declare/import variables
        self.re_pattern = self.env.get('re_pattern')
        self.output("Pattern: {}".format(self.re_pattern), verbose_level=3)
        self.result_output_var_name = self.env.get(
            "result_output_var_name", self.input_variables
            ["result_output_var_name"]["default"]
        )
        self.primary_url = self.env.get(
            "primary_url", None
        )
        self.selenium_options = self.env.get(
            "selenium_options", self.input_variables
            ["selenium_options"]["default"]
        )
        self.selenium_commands = self.env.get(
            "selenium_commands", self.input_variables
            ["selenium_commands"]["default"]
        )
        self.browser_binary_path = self.env.get(
            "browser_binary_path", self.input_variables
            ["browser_binary_path"]["default"]
        )
        self.webdriver_binary_path = self.env.get(
            "webdriver_binary_path", self.input_variables
            ["webdriver_binary_path"]["default"]
        )
        self.browser_used = self.env.get(
            "browser_used", self.input_variables
            ["browser_used"]["default"]
        )
        self.user_data_dir = self.env.get(
            "user_data_dir", (
                self.env["RECIPE_CACHE_DIR"]
                + "/selenium_user_data"
            )
        )

        # Declare the base 'content' string to be matched against
        self.content = ''

        # Create a Selenium WebDriver Options object.
        self.output(
            "Constructing WebDriver Options object.",
            verbose_level=2
        )
        # load variant specific modules for webdriver
        if self.browser_used == 'Chrome':
            from selenium.webdriver.chrome.service import Service
            s_binary=Service(self.webdriver_binary_path)
            from selenium.webdriver.chrome.options import Options
            options = Options()
            webdriver_engine = webdriver.Chrome
        elif self.browser_used == 'Edge':
            from selenium.webdriver.edge.service import Service
            s_binary=Service(self.webdriver_binary_path)
            from selenium.webdriver.edge.options import Options
            options = Options()
            webdriver_engine = webdriver.Edge
        else:
            self.output(
                "Not a valid value for a browser! Only 'Chrome' or 'Edge' supported.",
                verbose_level=1
            )

        # self.options = webdriver.ChromeOptions()
        self.options = Options()

        # Set the user data directory if needed.
        self.output(
            "Setting user data directory.",
            verbose_level=3
        )
        if self.user_data_dir == '':
            self.output(
                "Empty string specified for user data directory. "
                "The browser session will not persist following this "
                "processor run.",
                verbose_level=2
            )
        else:
            self.output(
                "User data directory: {}".format(
                    self.user_data_dir
                ),
                verbose_level=2
            )
            self.options.add_argument(
                "user-data-dir={}".format(self.user_data_dir)
            )

        # Make a KeyPress object so 'ENTER/END/etc.' keys can be inserted.
        self.output(
            "Creating utility keypress object.",
            verbose_level=3
        )
        keypress = webdriver.common.keys.Keys

        output_var_name = self.env["result_output_var_name"]

        # Run Pre-initialization commands.
        if len(self.selenium_options) > 1:
            self.output(
                (
                    "Processing {} Selenium option commands before "
                    "initilizing browser."
                ).format(str(len(self.selenium_options))),
                verbose_level=2
            )
            for o in self.selenium_options:
                self.output(
                    "Processing Command ({})".format(o),
                    verbose_level=3
                )
                exec(o)
        else:
            self.output(
                (
                    "No commands to process prior to browser "
                    "initialization."
                ),
                verbose_level=2
            )

        self.output(
            "Finished processing pre-init commands.",
            verbose_level=2
        )

        # Initializing browser
        self.output(
            "Initializing browser object.",
            verbose_level=2
        )
        self.output(
            "Chrome web driver: {}".format(self.webdriver_binary_path),
            verbose_level=3
        )
        self.output(
            "Chrome executable driver: {}".format(self.browser_binary_path),
            verbose_level=3
        )
        # intialize the webdriver variant (Chrome or Edge)
        browser = webdriver_engine(
            service=s_binary,
            options=self.options
        )
        self.output("Browser initialized", verbose_level=2)

        try:
            # Load the first URL
            self.output(
                "Loading initial url ({})".format(
                    self.primary_url
                ),
                verbose_level=2
            )
            browser.get(self.primary_url)

            # Run commands from input_variables
            if len(self.selenium_commands) > 1:
                self.output(
                    "Processing {} Selenium commands."
                    .format(str(len(self.selenium_commands))),
                    verbose_level=2
                )
                for c in self.selenium_commands:
                    self.output(
                        "Processing command ({})".format(c),
                        verbose_level=3
                    )
                    exec(c)
                    self.output("Command Complete.", verbose_level=3)
                    time.sleep(1.0)

                self.output(
                    "Finished processing commands.",
                    verbose_level=2
                )
            else:
                self.output(
                    (
                        "No commands to process."
                    ),
                    verbose_level=2
                )

            # Ensure we have a content variable to perform regex match against.
            self.output(
                '"content" variable is set to ({})'.
                format(self.content),
                verbose_level=3
            )
            if self.content == '':
                self.output(
                    "Variable 'content' remains unset following Selenium "
                    "commands. Setting it to the page source of the current "
                    "browser state. Browser is currently at ({})".format(
                        browser.title
                    ), verbose_level=2
                )
                content = browser.page_source
            else:
                self.output(
                    "Variable 'content' was set during Selenium command "
                    "execution. Continuing.",
                    verbose_level=3
                )
                content = self.content

            url = browser.current_url

            self.output("Finished Selenium tasks.", verbose_level=1)
            self.output("Beginning RegEx Matching", verbose_level=2)

            # RegEx matching
            groupmatch, groupdict = self.re_search(content, url)

            # Favor a named group over a normal group match
            if output_var_name not in groupdict.keys():
                groupdict[output_var_name] = groupmatch

            self.output("Performing RegEx matching.", verbose_level=1)
            self.output_variables = {}
            for key in groupdict.keys():
                self.output("Looping a key", verbose_level=3)
                self.env[key] = groupdict[key]
                self.output_variables[key] = {
                    "description": "Matched regular expression group"
                }

        except Exception:
            self.output(
                "An error occurred while running Selenium tasks.",
                verbose_level=2
            )

        finally:
            # Ensure the Selenium browser exits.
            self.output(
                "Selenium actions complete. Closing browser and exiting.",
                verbose_level=2
            )
            time.sleep(3.0)
            browser.close()
            time.sleep(1.0)
            browser.quit()
            if not self.user_data_dir == '':
                shutil.rmtree(self.user_data_dir)

    if __name__ == "__main__":
        PROCESSOR = Processor()
        PROCESSOR.execute_shell()
