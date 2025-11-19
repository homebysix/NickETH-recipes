#!/usr/bin/python
#
# Copyright 2025 Swiss federal institute of technology (ETHZ).
#
# Created by Nick Heim (heim)@ethz.ch) on 2025-11-19.
#
# Extracts a resource from a Wix based setup.exe file using the Wix.exe command.
# Wix Toolset >= 6 needs to be present.
# Wix >=6 does not need to be installed. Access to the extracted files is ok.
# Define the WIX_PATH_6 variable in config.json


import os
import sys
import subprocess

from autopkglib import Processor, ProcessorError


__all__ = ["WixExtractor"]


class WixExtractor(Processor):
    description = "Extracts the files from a Wix 6+ based exe using Wix.exe."
    input_variables = {
        "exe_path": {
            "required": False,
            "description": "Path to the (setup.)exe, defaults to %pathname%",
        },
        "extract_dir": {
            "required": True,
            "description": "Output path (absolute) for the extracted archive.",
        },
        # "xtract_file": {
            # "required": False,
            # "description": "Output filename of the resource to be extracted.",
        # },
        "ignore_errors": {
            "required": False,
            "description": "Ignore any errors during the extraction.",
        },
    }
    output_variables = {
    }

    __doc__ = description

    def main(self):

        exe_path = self.env.get('exe_path', self.env.get('pathname'))
        working_directory = self.env.get('RECIPE_CACHE_DIR')
        extract_directory = self.env.get('extract_dir', '.')
        ignore_errors = self.env.get('ignore_errors', 'False')
        verbosity = self.env.get('verbose', 0)

        wix_exe = os.path.join(self.env['WIX_PATH_6'], "Wix.exe")
        cmd = [wix_exe, 'burn', 'extract', '-oba', extract_directory, exe_path,'-o', extract_directory]

        # if {"xtract_file"}.issubset(self.env):
            # xtract_file = self.env.get('xtract_file')
            # cmd.extend([xtract_file])

        self.output("Working on: %s" % exe_path)

        print("Dark CL %s" % cmd, file=sys.stdout)

        try:
            if verbosity > 1:
                subprocess.check_call(cmd)
            else:
                subprocess.check_call(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except:
            if ignore_errors != 'True':
                raise

        self.output("Extracted Archive Path: %s" % extract_directory)

if __name__ == '__main__':
    processor = WixExtractor()
    processor.execute_shell()
