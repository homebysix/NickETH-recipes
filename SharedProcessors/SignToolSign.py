#!/usr/local/autopkg/python
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
# Quick and dirty first steps... 220702, Nick Heim
# Based on SignToolVerifier

"""See docstring for SignToolSign class"""

import os
import os.path
import subprocess
import keyring
from typing import Any, Dict, List, Optional

from autopkglib import Processor, ProcessorError

__all__ = ["SignToolSign"]


def signtool_default_path() -> Optional[str]:
    """Looks for signtool in a few well known paths. Deliberately naive."""
    for program_files_candidate, arch in (
        (os.environ.get("ProgramFiles(x86)"), "x64"),
        (os.environ.get("ProgramFiles(x86)"), "x86"),
        (os.environ.get("ProgramFiles"), "x64"),
        (os.environ.get("ProgramFiles"), "x86"),
    ):
        if program_files_candidate is None:
            continue
        candpath = os.path.abspath(
            os.path.join(
                program_files_candidate, r"Windows Kits\10\bin\10.0.22000.0", arch, "signtool.exe"
            )
        )
        if os.path.exists(candpath):
            return candpath
    return None


class SignToolSign(Processor):
    """Signs a file by using the Microsoft SDK signtool executable."""

    EXTENSIONS: List[str] = [".exe", ".msi"]

    # TODO: How much of this is needed to act as a drop-in replacement in an
    # override recipe??
    input_variables: Dict[str, Any] = {
        "DISABLE_CODE_SIGNATURE_SIGN": {
            "required": False,
            "description": ("Prevents this processor from running."),
        },
        "input_path": {
            "required": True,
            "description": (
                "File path to an `.msi` or `.exe` file for Authenticode verification",
            ),
        },
        "signtool_path": {
            "required": False,
            "description": (
                "The path to signtool.exe. This varies between versions of the "
                "Windows SDK, so you can explicitly set that here in an override."
            ),
            "default": signtool_default_path(),
        },
        "signtool_CM_entry": {
            "required": True,
            "description": "Name of the object in the credential manager, required",
        },
        "signtool_CM_username": {
            "required": True,
            "description": "Username to get the password from credential manager, required",
        },
        "timestamp_server": {
            "required": True,
            "description": (
                "Specifies the RFC 3161 timestamp server's URL",
            ),
        },
        "time_digest_algo": {
            "required": True,
            "description": (
                "Specifies the digest algorithm used by the RFC 3161 timestamp server",
            ),
        },
        "file_digest_algo": {
            "required": True,
            "description": (
                "Specifies the file digest algorithm to use for creating file signatures. (Default is SHA1)",
            ),
        },
        "cert_thumbprint": {
            "required": True,
            "description": (
                "Specify the SHA1 thumbprint of the signing cert",
            ),
        },
        "additional_arguments": {
            "required": False,
            "description": (
                "Array of additional argument strings to pass to signtool. "
                "Note that currently '/v' and '/pa' are always passed."
            ),
            "default": None,
        },
        "ignore_errors": {
            "required": False,
            "description": "Ignore any errors during the run.",
        },
    }
    output_variables: Dict[str, Any] = {}

    description: str = __doc__

    def codesign_sign(
        self,
        signtool_path: str,
        path: str,
        TS_server: str,
        TS_digest_algo: str,
        file_digest_algo: str,
        cert_thumbprint: str,
        cert_passwd: str,
        ignore_errors: bool,
        verbosity: str,
        additional_arguments: Optional[List[str]] = None,
    ) -> bool:
        """
        Runs 'signtool.exe sign'. Returns True if signtool exited with 0
        and False otherwise.
        """
        if not additional_arguments:
            additional_arguments = []

        # Create the signtool commandline.
        process = [signtool_path, "sign", "/tr", TS_server, "/td", TS_digest_algo, "/fd", file_digest_algo, "/sha1", cert_thumbprint] + additional_arguments

        # Makes the path absolute and normalizes it into standard Windows form.
        # E.g., /Program Files (x86)/Windows Kits/10/bin/x64/signtool.exe will be
        # converted to the appropriate C:\\... path after this.
        process.append(os.path.abspath(path))

        try:
            if verbosity > 1:
                #Output = subprocess.run(cmd, capture_output=True)
                Output = subprocess.run(process)
                self.output("cmdline Output: %s" % Output)
            else:
                #Output = subprocess.run(cmd, capture_output=True)
                Output = subprocess.run(process)

        except:
            if ignore_errors != 'True':
                raise
        
    def main(self):
        if self.env.get("DISABLE_CODE_SIGNATURE_SIGN"):
            self.output("Codesigning disabled for this recipe run.")
            return

        input_path = self.env["input_path"]
        #signtool_path = self.env["signtool_path"]
        signtool_path = self.env.get('signtool_path', signtool_default_path())
        signtool_CM_entry = self.env["signtool_CM_entry"]
        signtool_CM_username = self.env["signtool_CM_username"]
        timestamp_server = self.env["timestamp_server"]
        time_digest_algo = self.env["time_digest_algo"]
        file_digest_algo = self.env["file_digest_algo"]
        cert_thumbprint = self.env["cert_thumbprint"]
        #ignore_errors = self.env["ignore_errors"]
        ignore_errors = self.env.get('ignore_errors', True)
        verbosity = self.env.get('verbose', 1)
        
        self.output(signtool_path)
        
        additional_arguments = self.env["additional_arguments"]
        cert_passwd = keyring.get_password(signtool_CM_entry, signtool_CM_username)

        self.codesign_sign(
            signtool_path,
            input_path,
            timestamp_server,
            time_digest_algo,
            file_digest_algo,
            cert_thumbprint,
            cert_passwd,
            ignore_errors,
            verbosity,
            additional_arguments=additional_arguments,
        )


if __name__ == "__main__":
    PROCESSOR = SignToolSign()
    PROCESSOR.execute_shell()
