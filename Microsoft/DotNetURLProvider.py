#!/usr/bin/python
#
# Copyright 2021 Gerard kok
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Adopted to Windows, extended to distinguish standard/Core and SDK/ASP/Desktop

from __future__ import absolute_import

import re

from autopkglib import Processor, ProcessorError, URLGetter


BASE_URL = "https://dotnet.microsoft.com"

__all__ = ["DotNetURLProvider"]

#https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
def checkbool(v):
    # makes checking a bool argument a lot easier...
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
    # end of checkbool()

class DotNetURLProvider(URLGetter):
    """Returns url where latest download url of .NET can be found."""
    description = __doc__
    input_variables = {
        "release": {
            "required": False,
            "description": "Major version. Valid values are:"
                            "- a version X.Y (e.g. '5.0'), or"
                            "- a status: 'Preview', 'Current' or 'LTS'",
            "default": "Current",
        },
        "dotnet_core": {
            "default": False,
            "required": False,
            "description": "DotNet type (Core/Standard), default: Standard.",
        },
        "language_code": {
            "required": False,
            "description": "Language code to use in urls",
            "default": "en-us"
        },
    }
    output_variables = {
        "release_url": {
            "description": "Url where download url of this release can be found.",
        },
    }


    def status_release(self, status, url_path, dotnet_core):
        base_url = '{BASE_URL}/{url_path}'.format(BASE_URL=BASE_URL, url_path=url_path)
        self.output("base_url: %s" % base_url)
        raw_html = self.download(base_url, text=True)

        # if dotnet_core == "":
        if len(dotnet_core) == 0:
            release_re = '<a href="/{url_path}/(\d\.\d){dotnet_core}.*?<span class="badge badge-([a-z]+)">'.format(url_path=url_path, dotnet_core=dotnet_core)
        else:
            release_re = '<a href="/{url_path}/(\d\.\d){dotnet_core}.*?<td class="eol-channel-cell">'.format(url_path=url_path, dotnet_core=dotnet_core)

        self.output("release_re: %s" % release_re)
        test_find = re.findall(release_re, raw_html, re.DOTALL)
        self.output("test_find: %s" % test_find)
        for (release, badge) in re.findall(release_re, raw_html, re.DOTALL):
            self.output("release: %s" % release)
            self.output("badge: %s" % badge)
            if badge == status:
                return release
        
        raise ProcessorError('Unable to find .DotNet status.')


    def release(self, release, url_path, dotnet_core):
        release_re = r'^(\d\.\d|preview|current|lts)$'
        m = re.match(release_re, release, re.IGNORECASE)
        if not m:
            raise ProcessorError('Unable to parse .DotNet release.')

        n = re.match(r'^\d.\d$', m.group())
        if n:
            return m.group()
       
        status = release.lower()
        return self.status_release(status, url_path, dotnet_core)


    def release_url(self, release, url_path, dotnet_core):
        releasetemp = self.release(release, url_path, dotnet_core)
        return "{BASE_URL}/{url_path}/{releasetemp}".format(BASE_URL=BASE_URL, url_path=url_path, releasetemp=releasetemp)
   
    
    def main(self):
        language_code = self.env["language_code"]
        url_path = "{language_code}/download/dotnet".format(language_code=language_code)
        dotnet_core = self.env.get('dotnet_core')
        # if not "".__eq__(self.env["dotnet_core"] ):
        if checkbool(dotnet_core):
            dotnet_core = '">\.NET Core'
        else:
            dotnet_core = ''

        release = self.env["release"]
        self.env["release_url"] = self.release_url(release, url_path, dotnet_core)


if __name__ == '__main__':
    processor = DotNetURLProvider()
    processor.execute_shell()
