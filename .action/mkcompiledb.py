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
""" Create a Clang compile commands DB named compile_commands.json
    which is used by the clang-tidy utility. """
import glob
import json
import os
from os.path import exists
import platform
import logging
from logger import setup_logger


def create_clang_compile_commands_db(
    files=None, remove_existing_db=False, compile_cmd=None
):
    """Create a Clang compile commands DB named
    compile_commands.json in the current working directory."""
    out = 'compile_commands.json'
    linux_includes = ' -I/usr/include/c++/9/'
    darwin_includes = ' -D OSX -nostdinc++ -I/opt/local/include/libcxx/v1'
    my_platform = platform.system()
    logger = setup_logger()
    if not compile_cmd:
        compile_cmd = 'clang++ -g -O3 -Wall -pipe -std=c++14'
    if my_platform == 'Linux':
        compile_cmd = compile_cmd + linux_includes
    elif my_platform == 'Darwin':
        compile_cmd = compile_cmd + darwin_includes
    if not files:
        files = glob.glob('*.cc')
    compile_commands_db = [
        {
            'directory': '/tmp',
            'command': '{} {}'.format(compile_cmd, f),
            'file': f,
        }
        for f in files
    ]
    if exists(out) and remove_existing_db:
        logger.debug('Removing %s', out)
        os.unlink(out)
    elif exists(out) and not remove_existing_db:
        logger.warning(
            'The file %s already exists and will not be removed.', out
        )
        logger.warning('Compile commands DB not created. Using existing.')
    if not exists(out):
        with open(out, 'w') as file_handle:
            logger.debug('Writing %s', out)
            json.dump(compile_commands_db, file_handle)


if __name__ == '__main__':
    create_clang_compile_commands_db()
