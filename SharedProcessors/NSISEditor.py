#!/usr/local/autopkg/python
#
# Copyright 2025 Swiss federal institute of technology (ETHZ).
#
# Created by Nick Heim (heim)@ethz.ch) on 2025-10-08.
#
# Can decompile an NSIS-Setup EXE-file, 
# Altering the script and recompiling to be implemented.
# See: https://github.com/myfreeer/7z-build-nsis
#      https://nsis.sourceforge.io
# More to come to really edit the script...
# Output needs work. Goal would be to return the exitcode/errorlevel.


import os
import sys
import subprocess

from autopkglib import Processor, ProcessorError


__all__ = ["NSISEditor"]

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

class NSISEditor(Processor):
    description = "Decompiles an NSIS-Setup EXE-file, Alters the script and Recompiles it."
    input_variables = {
        "nsis_path": {
            "required": False,
            "description": "Path to the NSIS-Setup file, required",
        },
        "nsis_compiler": {
            "required": False,
            "description": "Absolute path to the NSIS compiler (makensis.exe).",
        },
        "workfolder": {
            "required": False,
            "description": "Path to the folder, where the work on the package should be done, defaults to %pathname%",
        },
        "script_only": {
            "required": False,
            "description": "eXtract only the [NSIS].nsi file, defaults to 'True'",
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
        nsis_path = self.env.get('nsis_path', self.env.get('pathname'))
        workfolder = self.env.get('workfolder')
        #mst_paths = self.env.get('mst_paths')
        ignore_errors = self.env.get('ignore_errors', True)
        script_only = self.env.get('script_only', True)
        verbosity = self.env.get('verbose', 1)
        extract_flag = 'l'
        self.output("Working on: %s" % nsis_path)
        # nsisunp_exe = os.path.join(self.env['TOOLS_DIR'], "nsisunp.exe")
        # cmd_decomp = [innounp_exe, '-x', '-m', '-b', '-q', '-d{}'.format(workfolder), inno_path]

        if {"nsis_path"}.issubset(self.env) and checkbool(script_only):
            nsisunp_exe = os.path.join(self.env['7ZNSIS_PATH'])
            # cmd_comp = [inno_compiler, '-d{}'.format(workfolder), (os.path.join(self.env[workfolder], "install_script.iss"))]
            # cmd_comp = [inno_compiler, (os.path.join(workfolder, "install_script.iss"))]
            # cmd = [sevenzipcmd, extract_flag, '-y', '-o%s' % extract_directory , exe_path]
            cmd_decomp = [nsisunp_exe, 'x', '-y', '-o%s' % workfolder, nsis_path, '[NSIS].nsi']
            
            try:
                if verbosity > 1:
                    #print >> sys.stdout, "verbosity %s" % verbosity
                    Output = subprocess.check_output(cmd_decomp)
                else:
                    Output = subprocess.check_output(cmd_decomp)
            except:
                if ignore_errors != 'True':
                    raise

        if {"nsis_compiler"}.issubset(self.env):
            nsis_compiler = self.env.get('nsis_compiler')
            #cmd_comp = [nsis_compiler, '-d{}'.format(workfolder), (os.path.join(self.env[workfolder], "install_script.iss"))]
            cmd_comp = [nsis_compiler, '/V0', (os.path.join(workfolder, "[NSIS].nsi"))]

            try:
                if verbosity > 1:
                    #print >> sys.stdout, "verbosity %s" % verbosity
                    Output = subprocess.check_output(cmd_comp)
                else:
                    Output = subprocess.check_output(cmd_comp)
            except:
                if ignore_errors != 'True':
                    raise
		
if __name__ == '__main__':
    processor = NSISEditor()
    processor.execute_shell()
