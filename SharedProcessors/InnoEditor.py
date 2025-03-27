#!/usr/local/autopkg/python
#
# Copyright 2022 Swiss federal institute of technology (ETHZ).
#
# Created by Nick Heim (heim)@ethz.ch) on 2022-01-30.
#
# Decompiles an Inno-Setup EXE-file, Alters the script and Recompiles it.
# See: https://github.com/Surgo/python-innosetup/blob/master/innosetup/innosetup.py
# More to come to really edit the script...
# Output needs work. Goal would be to return the exitcode/errorlevel.


import os
import sys
import subprocess

from autopkglib import Processor, ProcessorError


__all__ = ["InnoEditor"]


class InnoEditor(Processor):
    description = "Decompiles an Inno-Setup EXE-file, Alters the script and Recompiles it."
    input_variables = {
        "inno_path": {
            "required": False,
            "description": "Path to the Inno-Setup file, required",
        },
        "inno_compiler": {
            "required": False,
            "description": "Absolute path to the inno compiler (iscc.exe).",
        },
        "workfolder": {
            "required": False,
            "description": "Path to the folder, where the work on the package should be done, defaults to %pathname%",
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

        mode = self.env.get('mode',)
        inno_path = self.env.get('inno_path', self.env.get('pathname'))
        workfolder = self.env.get('workfolder')
        #mst_paths = self.env.get('mst_paths')
        ignore_errors = self.env.get('ignore_errors', True)
        verbosity = self.env.get('verbose', 1)
        extract_flag = 'l'
        self.output("Working on: %s" % inno_path)
        # innounp_exe = os.path.join(self.env['TOOLS_DIR'], "innounp.exe")
        # cmd_decomp = [innounp_exe, '-x', '-m', '-b', '-q', '-d{}'.format(workfolder), inno_path]

        if {"inno_path"}.issubset(self.env):
            innounp_exe = os.path.join(self.env['TOOLS_DIR'], "innounp.exe")
            # cmd_comp = [inno_compiler, '-d{}'.format(workfolder), (os.path.join(self.env[workfolder], "install_script.iss"))]
            # cmd_comp = [inno_compiler, (os.path.join(workfolder, "install_script.iss"))]
            cmd_decomp = [innounp_exe, '-x', '-m', '-b', '-q', '-d{}'.format(workfolder), inno_path]
            
            try:
                if verbosity > 1:
                    #print >> sys.stdout, "verbosity %s" % verbosity
                    Output = subprocess.check_output(cmd_decomp)
                else:
                    Output = subprocess.check_output(cmd_decomp)
            except:
                if ignore_errors != 'True':
                    raise

        if {"inno_compiler"}.issubset(self.env):
            inno_compiler = self.env.get('inno_compiler')
            #cmd_comp = [inno_compiler, '-d{}'.format(workfolder), (os.path.join(self.env[workfolder], "install_script.iss"))]
            cmd_comp = [inno_compiler, (os.path.join(workfolder, "install_script.iss"))]

            try:
                if verbosity > 1:
                    #print >> sys.stdout, "verbosity %s" % verbosity
                    Output = subprocess.check_output(cmd_comp)
                else:
                    Output = subprocess.check_output(cmd_comp)
            except:
                if ignore_errors != 'True':
                    raise

        # if mode.lower() in ["-e","-i"]:
            # if {"workfolder"}.issubset(self.env):
                # workfolder = self.env.get('workfolder')
            # if {"workfile"}.issubset(self.env):
                # workfile = self.env.get('workfile')
            # else:
                # workfile = '*'
            # cmd_patch = [innounp_exe, '-d', inno_path, mode, workfile, '-f', workfolder]
            # try:
                # Output = subprocess.check_output(cmd_patch)
            # except:
                # if ignore_errors != 'True':
                    # raise
		
if __name__ == '__main__':
    processor = InnoEditor()
    processor.execute_shell()
