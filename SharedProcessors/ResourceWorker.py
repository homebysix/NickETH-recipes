#!/usr/local/autopkg/python
#
# Copyright 2019 Swiss federal institute of technology (ETHZ).
#
# Created by Nick Heim (heim)@ethz.ch) on 2019-11-01 as ResourceExtractor.
#
# Working with resources from a Windows PE file using the ResourceHacker utility.
# Expanded to ResourceWorker. Hm, 221122
# Work to do: Embed an IconStub.exe as base64-string and write it on the fly, when needed.


import os
import sys
import subprocess

from autopkglib import Processor, ProcessorError


__all__ = ["ResourceWorker"]


class ResourceWorker(Processor):
    description = "Extracts a resource from a Windows exe using ResourceHacker."
    input_variables = {
        "exe_path": {
            "required": False,
            "description": "Path to the (setup.)exe, defaults to %pathname%",
        },
        # "inout_dir": {
            # "required": True,
            # "description": "In-/Output path (absolute) for files to work with.",
        # },
        "output_file": {
            "required": True,
            "description": "Output filename (absolute path) of the resource to be written.",
        },
        "input_file": {
            "required": False,
            "description": "Input filename (absolute path) of the resource to be added.",
        },
        "reswork_action": {
            "required": False,
            "default": "extract",
            "description": "Action to execute (extract/add). Default: extract.",
        },
        "reswork_cmd": {
            "required": True,
            "description": "Mask command (e.g. 'BIN,123,').",
        },
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
        # working_directory = self.env.get('RECIPE_CACHE_DIR')
        # inout_directory = self.env.get('inout_dir')
        output_file = self.env.get('output_file')
        if self.env.get("input_file"):
            input_file = self.env.get("input_file")
        reshack_action = self.env.get('reswork_action')
        reshack_cmd = self.env.get('reswork_cmd').strip('\"')
        self.output("Extract string: %s" % reshack_cmd)
        ignore_errors = self.env.get('ignore_errors', 'False')
        verbosity = self.env.get('verbose', 0)

        reshacker_exe = os.path.join(self.env['TOOLS_DIR'], "ResourceHacker.exe")		
        self.output("Working on: %s" % exe_path)
        if reshack_action == "extract":
            cmd = [reshacker_exe, '-open', exe_path, '-action', reshack_action, '-mask', reshack_cmd, '-save', output_file]
        elif reshack_action == "add":
            cmd = [reshacker_exe, '-open', exe_path, '-action', reshack_action, '-res', input_file, '-mask', reshack_cmd, '-save', output_file]
        else:
            self.output("Could not determine action to execute. Exiting")
            return None
                
        try:
            if verbosity > 1:
                subprocess.check_call(cmd)
            else:
                subprocess.check_call(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except:
            if ignore_errors != 'True':
                raise

        self.output("New file with resoureces: %s" % output_file)

if __name__ == '__main__':
    processor = ResourceWorker()
    processor.execute_shell()
