#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Derived from Nick McSpadden's PackageInfoVersioner.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.#
"""See docstring for MSIXInfoVersioner class."""

# Disabling warnings for env members and imports that only affect recipe-
# specific processors.
# pylint: disable=e1101,f0401

from __future__ import absolute_import

from xml.dom import minidom

from autopkglib import Processor, ProcessorError

__all__ = ["MSIXInfoVersioner"]


class MSIXInfoVersioner(Processor):
    """Get version from a PackageInfo file in a distribution/bundle package."""

    description = __doc__
    input_variables = {
        "appx_manifest_path": {
            "required": True,
            "description": (
                "Path to AppxManifest file from an APPX or MSIX."
            ),
        }
    }
    output_variables = {
        "pkg_id": {
            "description": "Package Name returned from Identity field in AppxManifest."
        },
        "version": {
            "description": "Version returned from Version field in AppxManifest."
        }
    }

    __doc__ = description

    def main(self):
        try:
            dom = minidom.parse(self.env["appx_manifest_path"])
        except IOError as err:
            raise ProcessorError(err)
        pkgrefs = dom.getElementsByTagName("Identity")
        self.env["pkg_id"] = pkgrefs[0].attributes["Name"].value
        self.output("Found pkg_id %s" % self.env["pkg_id"]) 
        self.env["version"] = pkgrefs[0].attributes["Version"].value
        self.output("Found version %s" % self.env["version"])


if __name__ == "__main__":
    PROCESSOR = MSIXInfoVersioner()
    PROCESSOR.execute_shell()
