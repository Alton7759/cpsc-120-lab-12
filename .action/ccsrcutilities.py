#
# Copyright 2021-2022 Michael Shafae
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
""" Utilities used to manipulate C++ source code files from student
    assignments. """

import glob
import subprocess
import difflib
import os.path
import logging
from mkcompiledb import create_clang_compile_commands_db
from logger import setup_logger

def remove_cpp_comments(file):
    """Remove CPP comments from a file using the CPP preprocessor"""
    # Inspired by
    # https://stackoverflow.com/questions/13061785/remove-multi-line-comments
    # and
    # https://stackoverflow.com/questions/35700193/how-to-find-a-search-term-in-source-code/35708616#35708616
    no_comments = None
    cmd = 'clang++ -E -P -'
    try:
        with open(file) as file_handle:
            # replace 'a', '__' and '#' to avoid preprocessor handling
            filtered_contents = (
                file_handle.read()
                .replace('a', 'aA')
                .replace('__', 'aB')
                .replace('#', 'aC')
            )
        proc = subprocess.run(
            [cmd],
            capture_output=True,
            shell=True,
            timeout=10,
            check=False,
            text=True,
            input=filtered_contents,
        )
        if proc.returncode == 0:
            no_comments = (
                proc.stdout.replace('aC', '#')
                .replace('aB', '__')
                .replace('aA', 'a')
            )
        else:
            logging.error('Errors encountered removing comments.')
            logging.error('stderr {}'.format(str(proc.stderr).rstrip("\n\r")))
    except FileNotFoundError as exception:
        logging.error('Cannot remove comments. No such file. %s', file)
    return no_comments


def makefile_has_compilecmd(target_makefile):
    """Given a Makefile, see if it has the compilecmd target which prints
    the compilation command to stdout."""
    has_compilecmd = False

    try:
        with open(target_makefile) as file_handle:
            has_compilecmd = file_handle.read().find('compilecmd:') != -1
    except FileNotFoundError as exception:
        logging.error('Cannot open Makefile "%s" for reading.', target_makefile)
    return has_compilecmd


def makefile_get_compilecmd(target_dir, compiler='clang++'):
    """Given a Makefile with the compilecmd target, return the string
    which represents the compile command. For use with making the
    compile database for linting."""
    logger = setup_logger()
    compilecmd = None
    makefiles = glob.glob(
        os.path.join(target_dir, '*Makefile'), recursive=False
    )
    # Break on the first matched Makefile with compilecmd
    matches = None
    for makefile in makefiles:
        if makefile_has_compilecmd(makefile):
            cmd = 'make -C {} compilecmd'.format(target_dir)
            proc = subprocess.run(
                [cmd],
                capture_output=True,
                shell=True,
                timeout=10,
                check=False,
                text=True,
            )
            matches = [
                line
                for line in str(proc.stdout).split('\n')
                if line.startswith(compiler)
            ]
            break
    if matches:
        compilecmd = matches[0]
    else:
        logger.debug('Could not identify compile command; using default.')
    return compilecmd

def strip_and_compare_files(base_file, submission_file):
    """ Compare two source files with a contextual diff, return \
    result as a list of lines. """
    base_file_contents_no_comments = remove_cpp_comments(base_file)
    contents_no_comments = remove_cpp_comments(submission_file)
    diff = ""
    if contents_no_comments and base_file_contents_no_comments:
        base_file_contents_no_comments = base_file_contents_no_comments.split(
            '\n'
        )
        contents_no_comments = contents_no_comments.split('\n')
        diff = difflib.context_diff(
            base_file_contents_no_comments,
            contents_no_comments,
            'Base',
            'Submission',
            n=3,
        )
    else:
        logging.error('Cannot perform contextual diff.')
    return list(diff)


def format_check(file):
    """ Use clang-format to check file's format against the \
    Google C++ style. """
    # logger = setup_logger()
    # clang-format
    cmd = 'clang-format'
    cmd_options = '-style=Google --Werror'
    cmd = cmd + ' ' + cmd_options + ' ' + file
    # logger.debug('clang format: %s', cmd)
    proc = subprocess.run(
        [cmd],
        capture_output=True,
        shell=True,
        timeout=10,
        check=False,
        text=True,
    )
    correct_format = str(proc.stdout).split('\n')
    with open(file) as file_handle:
        original_format = file_handle.read().split('\n')
    diff = difflib.context_diff(
        original_format,
        correct_format,
        'Student Submission (Yours)',
        'Correct Format',
        n=3,
    )
    # print('\n'.join(list(diff)))
    return list(diff)


def lint_check(file, tidy_options=None, skip_compile_cmd=False):
    """ Use clang-tidy to lint the file. Options for clang-tidy \
    defined in the function. """
    logger = setup_logger()
    # clang-tidy
    if not skip_compile_cmd:
        logger.debug('Checking for makefile in %s', os.path.dirname(os.path.realpath(file)))
        compilecmd = makefile_get_compilecmd(
            os.path.dirname(os.path.realpath(file))
        )
        logger.debug('Makefile reported compile commmand as %s', compilecmd)
    if not skip_compile_cmd and compilecmd:
        logger.debug('Using compile command %s', compilecmd)
        create_clang_compile_commands_db(
            remove_existing_db=True, compile_cmd=compilecmd
        )
        logger.debug('Created clang compile command db.')
    elif not skip_compile_cmd and not compilecmd:
        logger.debug('Creating compile commands.')
        create_clang_compile_commands_db(files=[file], remove_existing_db=True)
    cmd = 'clang-tidy'
    if not tidy_options:
        logger.debug('Using default tidy options.')
        cmd_options = r'-checks="-*,google-*, modernize-*, \
        readability-*,cppcoreguidelines-*,\
        -google-build-using-namespace,\
        -google-readability-todo,\
        -modernize-use-trailing-return-type,\
        -cppcoreguidelines-avoid-magic-numbers,\
        -readability-magic-numbers,\
        -cppcoreguidelines-pro-type-union-access,\
        -cppcoreguidelines-pro-bounds-constant-array-index"'
        # cmd_options = '-checks="*"'
    else:
        cmd_options = tidy_options
    cmd = cmd + ' ' + cmd_options + ' ' + file
    if skip_compile_cmd:
        cmd = cmd + ' -- -std=c++17'
    logger.debug('Tidy command %s', cmd)
    proc = subprocess.run(
        [cmd],
        capture_output=True,
        shell=True,
        timeout=60,
        check=False,
        text=True,
    )
    linter_warnings = str(proc.stdout).split('\n')
    linter_warnings = [line for line in linter_warnings if line != '']
    return linter_warnings

def glob_cc_src_files(target_dir='.'):
    """Recurse through the target_dir and find all the .cc files."""
    return glob.glob(os.path.join(target_dir, '**/*.cc'), recursive=True)


def glob_h_src_files(target_dir='.'):
    """Recurse through the target_dir and find all the .h files."""
    return glob.glob(os.path.join(target_dir, '**/*.h'), recursive=True)


def glob_all_src_files(target_dir='.'):
    """Recurse through the target_dir and find all the .cc and .h files."""
    files = glob_cc_src_files(target_dir) + glob_h_src_files(target_dir)
    return files
