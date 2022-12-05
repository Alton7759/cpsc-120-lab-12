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
""" Given a file, verify if the file has a header.
 Example C++ header
// Michael Shafae
// CPSC 120-01
// 2021-01-30
// mshafae@csu.fullerton.edu
// @mshafae
//
// Lab 00-00
// Partners: @peteranteater, @ivclasers
//
// This is my first program and it prints out Hello World!
//
"""

import sys
import logging
from logger import setup_logger
from parse_header import dict_header

def header_check(file):
    """ Check file's header if it conforms to the standard given \
    in the example in the body of the function. Returns True if \
    the header is good. """
    # https://docs.google.com/document/d/17WkDlxO92zpb26pYM1NIACPcMWtCOlKO7WCrWC6YxRo/edit#
    # Example C++ header
    #// Michael Shafae
    #// CPSC 120-01
    #// 2021-01-30
    #// mshafae@csu.fullerton.edu
    #// @mshafae
    #//
    #// Lab 00-00
    #// Partners: @peteranteater, @ivclasers
    #//
    #// This is my first program and it prints out Hello World!
    #//

    # return true if header is good
    keys = ['name', 'class', 'email', 'github', 'asgt', 'partners', 'comment']
    with open(file) as file_handle:
        contents = file_handle.read()
    header = dict_header(contents, silent=True)
    status = True
    if header:
        for k in keys:
            if not k in header.keys():
                logging.warning('%s: missing %s', file, k)
                status = False
    else:
        status = False
    return status


def get_header_and_check(file):
    """ Check file's header if it conforms to the standard given \
    in the example in the body of the function. Returns True if \
    the header is good. """
    # https://docs.google.com/document/d/17WkDlxO92zpb26pYM1NIACPcMWtCOlKO7WCrWC6YxRo/edit#
    # Example C++ header
    #// Michael Shafae
    #// CPSC 120-01
    #// 2021-01-30
    #// mshafae@csu.fullerton.edu
    #// @mshafae
    #//
    #// Lab 00-00
    #// Partners: @peteranteater, @ivclasers
    #//
    #// This is my first program and it prints out Hello World!
    #//

    # return true if header is good
    keys = ['name', 'class', 'email', 'github', 'asgt', 'partners', 'comment']
    with open(file) as file_handle:
        contents = file_handle.read()
    header = dict_header(contents)
    status = True
    if header:
        for k in keys:
            if not k in header.keys():
                logging.warning('%s: missing %s', file, k)
                status = False
    else:
        status = False
    return (status, header)

def main():
    """ Main function; process each file given through get_header_and_check. """
    logger = setup_logger()
    status = 0
    if len(sys.argv) < 2:
        logger.warning('Only %s arguments provided.', len(sys.argv))
    for in_file in sys.argv[1:]:
        logger.info('Check header for file: %s', in_file)
        has_header, header_d = get_header_and_check(in_file)
        if not has_header:
            logger.warning('Header is malformed or missing.')
            logger.warning('Could not find a header in the file.')
            logger.warning('Information about header formatting is'
                'at https://docs.google.com/document/d/'
                '17WkDlxO92zpb26pYM1NIACPcMWtCOlKO7WCrWC6YxRo/'
                'edit?usp=sharing')
            status = 1
        else:
            logger.info('Header found.')
            logger.info("Name: %s", header_d['name'])
            logger.info("Class: %s", header_d['class'])
            logger.info("Email: %s", header_d['email'])
            logger.info("GitHub Handle: %s", header_d['github'])
            logger.info("Lab: %s", header_d['asgt'])
            logger.info("Partners: %s", header_d['partners'])
            logger.info("Comment: %s", header_d['comment'])
    sys.exit(status)

if __name__ == '__main__':
    main()
