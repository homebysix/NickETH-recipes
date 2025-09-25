#!/usr/bin/python
#
# Copyright 2019 Swiss federal institute of technology (ETHZ).
#
# Created by Nick Heim (heim)@ethz.ch) on 2019-03-17.
# Was MSIApplySumInfo.
#
# msiinfo "msi" /t "String"
# Alternative could be the msilib SummaryInformation.GetProperty(field) functions.
# 20210517 Nick Heim: Python v3 changes
# 211029 Nick Heim: Clean up, set debug output to verbose > 1.
# 240201 Nick Heim: Implement the dump function to read out the actual values.

import os
import sys
import subprocess

from autopkglib import Processor, ProcessorError


__all__ = ["MSISumInfo"]


class MSISumInfo(Processor):
    description = "Dump or apply summary info changes to MSI-file using msiinfo.exe."
    input_variables = {
        "msi_path": {
            "required": True,
            "description": "Path to the msi, required",
        },
        "cmnds_sinfo": {
            "required": False,
            "description": "Dict of Suminfo commands to execute. Pairs of key(flag)/string are expected.",
        },
        "ignore_errors": {
            "required": False,
            "description": "Ignore any errors during the extraction.",
        },
    }
    output_variables = {
        "SumInfo_Dump": {
            "description": "Dump the actual values of MSI's SumInfo."
        }
    }

    __doc__ = description

    def main(self):

        msi_path = self.env.get('msi_path', self.env.get('pathname'))
        cmnds_sinfo = self.env.get('cmnds_sinfo', '')
        verbosity = self.env.get('verbose', 1)
        if verbosity > 1:
            self.output( "cmnds_sinfo: %s" % cmnds_sinfo)
        ignore_errors = self.env.get('ignore_errors', True)
        extract_flag = 'l'
        msiinfo_exe = os.path.join(self.env['TOOLS_DIR'], "msiinfo.exe")		

        if "cmnds_sinfo" in self.env and cmnds_sinfo != '':
            for key, value in list(cmnds_sinfo.items()):
                cmd = [msiinfo_exe, msi_path, key, value]
                try:
                    if verbosity > 1:
                        self.output("Applying: %s" % msi_path)
                        self.output( "cmd %s %s" % (key, value))
                        Output = subprocess.check_output(cmd)
                    else:
                        Output = subprocess.check_output(cmd)
                except OSError as err:
                    if ignore_errors != 'True':
                        raise ProcessorError(
                            "Could not apply %s: %s" % (cmd, err))
        else:
            cmd = [msiinfo_exe, msi_path]
            try:
                if verbosity > 1:
                    self.output("Applying: %s" % msi_path)
                    # self.output( "cmd %s %s" % (key, value))
                    Output = subprocess.check_output(cmd)
                else:
                    Output = subprocess.check_output(cmd)
                #self.env['SumInfo_Dump'] = Output.decode("utf-8")
                self.env['SumInfo_Dump'] = Output.decode("windows-1252")
            except OSError as err:
                if ignore_errors != 'True':
                    raise ProcessorError(
                        "Could not apply %s: %s" % (cmd, err))
                            
if __name__ == '__main__':
    processor = MSISumInfo()
    processor.execute_shell()
