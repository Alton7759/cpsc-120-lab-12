#!/usr/bin/env python3
#
# Copyright 2021 Michael Shafae
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
""" Run the files given as arguments with the provided arguments. """

import os.path
import os
import sys
import logging
import subprocess
from logger import setup_logger


def run(binary='asgt', args='', expect=None):
    """Run binary in a spawned. This run does not test."""
    status = True
    cmd = './' + binary
    if os.path.exists(cmd):
        if len(args) > 0:
            cmd = cmd + ' ' + args
        proc = subprocess.run(
            [cmd],
            capture_output=True,
            shell=True,
            timeout=10,
            check=False,
            text=True,
        )
        if proc.stdout:
            logging.info('Output (stdout): %s', str(proc.stdout).rstrip("\n\r"))
            if expect:
                logging.info('Expected: %s', expect)
        if proc.stderr:
            logging.warning(
                'Errors (stderr): %s', str(proc.stderr).rstrip("\n\r")
            )
        if proc.returncode != 0:
            status = False
    else:
        logging.warning('The binary %s does not exist.', cmd)
        status = False
    return status


def main():
    """Main function; process the given binary and included
    command line options."""
    setup_logger()
    if len(sys.argv) < 2:
        logging.warning('Only %s arguments provided.', len(sys.argv))
    cmd = sys.argv[1]
    cmd_args = ""
    if len(sys.argv) > 2:
        cmd_args = " ".join(sys.argv[2:])
    logging.warning(
        'This is not an exhaustive test or a grader. The'
        ' program shall be executed to verify that it does not crash.'
        ' Students are required to develop their own testing regimen.'
    )
    if len(cmd_args) > 0:
        logging.info('Executing: "%s %s"', cmd, cmd_args)
    else:
        logging.info('Executing: "%s"', cmd)
    if run(cmd, cmd_args, 'Hello your-name!'):
        logging.info(
            'Your program executed and exited cleanly.'
            ' Perform further testing to ensure that your program'
            ' meets or exceeds all requirements.'
        )
    else:
        logging.warning('Your program did not execute cleanly.')


if __name__ == '__main__':
    main()
