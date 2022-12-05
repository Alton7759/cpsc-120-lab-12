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
""" Check the given files to see if they conform to the Google C++
    Programming style using clang-format. """

import sys
import logging
import os.path
from logger import setup_logger
from ccsrcutilities import format_check

def main():
    """ Main function; check the format of each file on the
    command line. """
    logger = setup_logger()
    if len(sys.argv) < 2:
        logger.warning('Only %s arguments provided.', len(sys.argv))
        logger.warning('Provide a list of files to check.')
    status = 0
    for in_file in sys.argv[1:]:
        logger.info('Checking format for file: %s', in_file)
        if not os.path.exists(in_file):
            logger.debug('File %s does not exist. Continuing.', in_file)
            continue
        diff = format_check(in_file)
        if len(diff) != 0:
            logger.warning("Error: Formatting needs improvement.")
            diff_string = 'Contextual Diff\n' + '\n'.join(diff)
            logger.warning(diff_string)
            status = 1
            logger.error("🤯😳😤😫🤬")
            logger.error(
                "Your formatting doesn't conform to the Google C++ style."
            )
            logger.error("Use the output from this program to help guide you.")
            logger.error("If you get stuck, ask your instructor for help.")
            logger.error(
                "Remember, you can find the Google C++ style online "
                "at https://google.github.io/styleguide/cppguide.html."
            )
        else:
            logger.info('😀 Formatting looks pretty good! 🥳')
    sys.exit(status)

if __name__ == '__main__':
    main()
