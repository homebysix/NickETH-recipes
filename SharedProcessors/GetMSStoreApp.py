#!/usr/bin/python
#
# Copyright 2025 Swiss federal institute of technology (ETHZ).
#
# Created by Nick Heim (heim)@ethz.ch) on 2025-02-07.
#
# Download App with dependencies from MS store to install offline. 
# Output needs work. Goal would be to return the exitcode/errorlevel.

import os
import sys
import subprocess

from autopkglib import Processor, ProcessorError


__all__ = ["GetMSStoreApp"]


class GetMSStoreApp(Processor):
    description = "Download App and dependencies from MS store."
    input_variables = {
        "app_url": {
            "required": True,
            "description": "Url to the store app, required",
        },
        "dl_dir": {
            "required": True,
            "description": "Folder, where the packages are downloaded to, required",
        },
        "org_ver": {
            "required": False,
            "description": "Original version string",
        },
        "prop_file": {
            "required": False,
            "description": "XMLfile, containing additional build properties.",
        },
        "ignore_errors": {
            "required": False,
            "description": "Ignore any errors during the run.",
        },
    }
    output_variables = {
        "file_list": {
            "description": "List of downloaded apps."
        }
    }
    __doc__ = description

    def main(self):

        app_url = self.env.get('app_url')
        dl_dir = self.env.get('dl_dir')
        ignore_errors = self.env.get('ignore_errors', True)
        verbosity = self.env.get('verbose', 5)

        self.output("Working on: %s" % app_url)
        sharedproc_dir = os.path.dirname(os.path.realpath(__file__))
        ps_script = os.path.join(sharedproc_dir, 'GetMSStoreApp.ps1')
        powershell = "C:\\windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"
        # Call the powershell script with its arguments.
        cmd = [powershell, '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
            ps_script,
            app_url,
            dl_dir,]

        if "org_ver" in self.env:
            org_ver = self.env.get('org_ver')
            cmd.extend(['-org_ver', org_ver])

        if "prop_file" in self.env:
            prop_file = self.env.get('prop_file')
            cmd.extend(['-prop_file', prop_file])

        try:
            if verbosity > 1:
                Output = subprocess.getoutput(cmd)
            else:
                Output = subprocess.getoutput(cmd)
        except:
            if ignore_errors != 'True':
                raise

        #self.env['pkg_dir'] = Output
		
        archiveVersion = ""
        for line in Output.split("\n"):
            if verbosity > 2:
                print(line)
            if "|" in line:
                AppList = line
                continue
        
        self.env['file_list'] = AppList
        #self.output("New build_ver: %s" % (self.env['build_ver']))
        self.output("%s" % AppList)
if __name__ == '__main__':
    processor = GetMSStoreApp()
    processor.execute_shell()
