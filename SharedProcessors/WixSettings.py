#!/usr/bin/python
#
# Copyright 2023 Swiss federal institute of technology (ETHZ).
#
# Created by Nick Heim (heim)@ethz.ch) on 2023-03-21.
#
# Create Wix (Windows installer XML Toolset) preprocessor (WXI/WXL) files.
# For now, only include file is implemented.
# https://stackoverflow.com/questions/61252951/how-to-insert-a-processing-instruction-in-xml-file
# https://stackoverflow.com/questions/28813876/how-do-i-get-pythons-elementtree-to-pretty-print-to-an-xml-file
# Output needs work.
# 20230320 Nick Heim: Initial release.

"""
WixSettings

This is a processor for AutoPkg.

Important! You *must* install the lxml library to AutoPkg's Python framework.
You can do this by running:

pip install lxml
"""
import os
import sys
import uuid
from lxml import etree as ET

from autopkglib import Processor, ProcessorError


__all__ = ["WixSettings"]

class WixSettings(Processor):
    description = "Create an preprocessor file for a WIX-build."
    input_variables = {
        "preproc_file": {
            "required": True,
            "description": "Path to the preprocessor (include) file to write, required",
        },
        "new_settings": {
            "required": True,
            "description": "Array of dicts with setting(s) to add, required",
        },
        "template_file": {
            "required": False,
            "default": "default_content",
            "description": "Template, containing predefined variables. 'None' for a blank start.",
        },
        "ignore_errors": {
            "required": False,
            "description": "Ignore any errors during the run.",
        },
    }
    output_variables = {
    }

    __doc__ = description

    def main(self):


        preproc_file = self.env.get('preproc_file')
        new_settings = self.env.get('new_settings')
        ignore_errors = self.env.get('ignore_errors', True)
        verbosity = self.env.get('verbose', 1)

        sharedproc_dir = os.path.dirname(os.path.realpath(__file__))
        # self.output( "new_settings: %s" % new_settings)
        if "template_file" in self.env:
            template_file = self.env.get('template_file')

            if template_file == "None":
                WixData = ET.Element('Include')
                WixData.text = '\n  '
            elif template_file == "default_content":
                default_content = '''\
<Include>
  <?if $(var.Platform)="x86"?>
    <?define ProgramFilesFolder="ProgramFilesFolder" ?>
    <?define Win64="no" ?>
    <?define Arch="(x86)" ?>
  <?else?>
    <?define ProgramFilesFolder="ProgramFiles64Folder" ?>
    <?define Win64="yes" ?>
    <?define Arch="(x64)" ?>
  <?endif?>
</Include>
'''
                WixData = ET.fromstring(default_content)
            else:
                WixData = ET.parse(template_file).getroot()

        new_set_length = len(new_settings)
        print(new_set_length)
        new_set_iter = 1
        for pi,pi_dict in enumerate(new_settings):
            # self.output( "defines: %s %s" % (pi,pi_dict))
            for key, value in pi_dict.items():
                # print(type(key))
                # print(value)
                if value.find('NNEEWWGGUUIIDD') > 0:
                    newGUID = (str(uuid.uuid4())).upper()
                    value = value.replace("NNEEWWGGUUIIDD",newGUID)
                pi_item = ET.ProcessingInstruction(key, value)
                if template_file == "default_content":
                    WixData[-1].tail = "\n  "
                if new_set_length > new_set_iter:
                    pi_item.tail = "\n  "
                else:
                    pi_item.tail = "\n"
                WixData.append(pi_item)
            new_set_iter += 1

        tree = ET.ElementTree(WixData)
        tree.write(preproc_file,
            xml_declaration=True,
            encoding='utf-8',
            # pretty_print=True,
            method="xml")

if __name__ == '__main__':
    processor = WixSettings()
    processor.execute_shell()
