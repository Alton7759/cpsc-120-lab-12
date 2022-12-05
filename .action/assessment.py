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
""" Utilities to build, run, and evaluate student projects. """
import csv
import json
import os
import pickle
import re
import sys
import subprocess
from ccsrcutilities import glob_all_src_files, strip_and_compare_files, format_check, lint_check, glob_cc_src_files
from parse_header import dict_header, null_dict_header
from header_check import header_check
from logger import setup_logger

def make_spotless(target_dir):
    """Given a directory that contains a GNU Makefile, clean with the `make
    spotless` target."""
    status = True
    status = make(target_dir, 'spotless')
    return status


def make_build(target_dir, always_clean=True):
    """Given a directory that contains a GNU Makefile, build with `make all`.
    This function call will call `make spotless` via make_spotless()"""
    status = True
    if always_clean:
        status = make_spotless(target_dir)
    if status:
        status = make(target_dir, 'all')
    return status

def make_unittest(target_dir, always_clean=True, output_format="json", output_file="test_detail.json"):
    """Given a directory that contains a GNU Makefile, build with `make unittest`.
    This function call will call `make spotless` via make_spotless()"""
    status = True
    os.environ['GTEST_OUTPUT_FORMAT'] = output_format
    os.environ['GTEST_OUTPUT_FILE'] = output_file
    if always_clean:
        status = make_spotless(target_dir)
    if status:
        status = make(target_dir, 'unittest')
    del os.environ['GTEST_OUTPUT_FORMAT']
    del os.environ['GTEST_OUTPUT_FILE']
    return status

def make(target_dir, make_target):
    """Given a directory, execute make_target given the GNU Makefile in the
    directory."""
    status = True
    logger = setup_logger()
    if not os.path.exists(os.path.join(target_dir, 'Makefile')):
        logger.error('Makefile does not exist in %s', target_dir)
        status = False
    else:
        cmd = 'make -C {} {}'.format(target_dir, make_target)
        logger.debug(cmd)
        proc = subprocess.run(
            [cmd],
            capture_output=True,
            shell=True,
            timeout=15,
            check=False,
            text=True,
        )
        # if proc.stdout:
        #    logger.info('stdout: %s', str(proc.stdout).rstrip("\n\r"))
        if proc.stderr:
            logger.info('stderr: %s', str(proc.stderr).rstrip("\n\r"))
        if proc.returncode != 0:
            status = False
    return status


def build(file, target='asgt', compiletimeout=10):
    """Given a C++ source file, build with clang C++14 with -Wall
    and -pedantic. Output is 'asgt'. Binary is left on the file system."""
    logger = setup_logger()
    # rm the file if exists
    if os.path.exists(target):
        os.unlink(target)
    status = True
    cmd = 'clang++ -Wall -pedantic -std=c++14 -o {} {}'.format(target, file)
    logger.debug(cmd)
    proc = subprocess.run(
        [cmd],
        capture_output=True,
        shell=True,
        timeout=compiletimeout,
        check=False,
        text=True,
    )
    if proc.stdout:
        logger.info('stdout: %s', str(proc.stdout).rstrip("\n\r"))
    if proc.stderr:
        logger.info('stderr: %s', str(proc.stderr).rstrip("\n\r"))
    if proc.returncode != 0:
        status = False
    return status


def identify(header):
    """String to identify submission's owner."""
    ident = '(Malformed Header)'
    if header:
        ident = f"Testing {header['name']} {header['email']} {header['github']}"
    return ident

def has_main_function(file):
    """Check if a given file has a C++ main function."""
    status = False
    main_regex = re.compile(
        r'int\s*main\s*\(int\s*argc,\s*(const)?\s*char\s*(const)?\s*\*\s*argv\[\]\)'
    )
    with open(file, 'r') as file_handle:
        src_code = file_handle.read()
        matches = main_regex.search(src_code)
        if matches:
            status = True
    return status


def solution_check_simple(run=None, files=None, do_format_check=True, do_lint_check=True, tidy_options=None, skip_compile_cmd=False):
    """Main function for checking student's solution. Provide a pointer to a
    run function."""
    logger = setup_logger()
    if len(sys.argv) < 3:
        logger.error(
            'provide target directory, program name, and optionally a base directory to run a diff'
        )
        sys.exit(1)
    target_directory = sys.argv[1]
    if len(sys.argv) == 4:
        base_directory = sys.argv[3]
    else:
        base_directory = None
    if not files:
        files = glob_all_src_files(target_directory)
    else:
        files = [os.path.join(sys.argv[1], file) for file in files]
    if len(files) == 0:
        logger.error("❌ No files in %s.", target_directory)
        sys.exit(1)

    # Header checks
    files_missing_header = [file for file in files if not header_check(file)]
    files_with_header = [file for file in files if header_check(file)]
    header = None
    if len(files_with_header) == 0:
        logger.error('❌ No header provided in any file in %s. Exiting.', target_directory)
        logger.error('All files: %s', ' '.join(files))
        sys.exit(1)
    else:
        with open(files_with_header[0]) as file_handle:
            contents = file_handle.read()
        header = dict_header(contents)
    
    logger.info('Start %s', identify(header))
    logger.info('All files: %s', ' '.join(files))
    if len(files_missing_header) != 0:
        logger.warning(
            'Files missing headers: %s', ' '.join(files_missing_header)
        )

    # Check if files have changed
    if base_directory:
        count = 0
        for file in files:
            diff = strip_and_compare_files(file, os.path.join(base_directory, file))
            if len(diff) == 0:
                count += 1
                logger.error('No changes made to the file %s.', file)
        if count == len(files):
            logger.error('No changes made to any files.')
            sys.exit(1)
    else:
        logger.debug('Skipping base file comparison.')

    # Format
    if do_format_check:
        for file in files:
            diff = format_check(file)
            if len(diff) != 0:
                logger.warning('❌ Formatting needs improvement in %s.', file)
                logger.info(
                    'Please make sure your code conforms to the Google C++ style.'
                )
                logger.debug('\n'.join(diff))
            else:
                logger.info('✅ Formatting passed on %s', file)

    # Lint
    if do_lint_check:
        for file in files:
            lint_warnings = lint_check(file, tidy_options, skip_compile_cmd)
            if len(lint_warnings) != 0:
                logger.warning('❌ Linter found improvements in %s.', file)
                logger.debug('\n'.join(lint_warnings))
            else:
                logger.info('✅ Linting passed in %s', file)


    status = 0
    # check to see if all the files end with .cc, if not, then we have to
    # find the file with the main function.
    if sum([True for file in files if file.endswith('.cc')]):
        cc_files = files
    else:
        cc_files = glob_cc_src_files(target_directory)
    # Clean, Build, & Run
    if len(cc_files) > 1:
        logger.info(
            'Found more than one C++ source file: %s', ' '.join(cc_files)
        )
    main_src_file = None
    for file in files:
        if has_main_function(file):
            if not main_src_file:
                main_src_file = file
                logger.info('Main function found in %s', file)
            else:
                logger.warning('Extra main function found in %s', file)
    if main_src_file:
        logger.info('Checking build for %s', main_src_file)
        if build(main_src_file):
            logger.info('✅ Build passed')
            # Run
            if not run:
                logger.info('No run function specified...skipping.')
            elif run and run('./' + sys.argv[2]):
                logger.info('✅ Run passed')
            else:
                logger.error('❌ Run failed')
                status = 1
        else:
            logger.error('❌ Build failed')
            status = 1
    else:
        logger.error('❌ No main function found in files: %s', ' '.join(cc_files))
        status = 1
    logger.info('End %s', identify(header))
    sys.exit(status)


def solution_check_make(target_directory, program_name='asgt', base_directory=None, run=None, files=None, do_format_check=True, do_lint_check=True, tidy_options=None, skip_compile_cmd=False):
    """Main function for checking student's solution. Provide a pointer to a
    run function."""
    logger = setup_logger()
    # if len(sys.argv) < 3:
    #     logger.error(
    #         'provide target directory, program name, and optionally a base directory'
    #     )
    #     sys.exit(1)
    # target_directory = sys.argv[1]
    # if len(sys.argv) == 4:
    #     base_directory = sys.argv[3]
    # else:
    #     base_directory = None
    if not files:
        # This could be a target in the Makefile
        files = glob_all_src_files(target_directory)
    else:
        files = [os.path.join(target_directory, file) for file in files]
    if len(files) == 0:
        logger.error("❌ No files in %s.", target_directory)
        sys.exit(1)

    # Header checks
    files_missing_header = [file for file in files if not header_check(file)]
    files_with_header = [file for file in files if header_check(file)]
    header = None
    if len(files_with_header) == 0:
        logger.error('❌ No header provided in any file in %s. Exiting.', target_directory)
        logger.error('All files: %s', ' '.join(files))
        sys.exit(1)
    else:
        with open(files_with_header[0]) as file_handle:
            contents = file_handle.read()
        header = dict_header(contents)

    logger.info('Start %s', identify(header))
    logger.info('All files: %s', ' '.join(files))
    files_missing_header = [file for file in files if not header_check(file)]
    if len(files_missing_header) != 0:
        logger.warning(
            'Files missing headers: %s', ' '.join(files_missing_header)
        )

    # Check if files have changed
    if base_directory:
        count = 0
        for file in files:
            diff = strip_and_compare_files(file, os.path.join(base_directory, file))
            if len(diff) == 0:
                count += 1
                logger.error('No changes made in file %s.', file)
        if count == len(files):
            logger.error('No changes made ANY file. Stopping.')
            sys.exit(1)
    else:
        logger.debug('Skipping base file comparison.')

    # Format
    if do_format_check:
        for file in files:
            diff = format_check(file)
            if len(diff) != 0:
                logger.warning('❌ Formatting needs improvement in %s.', file)
                logger.info(
                    'Please make sure your code conforms to the Google C++ style.'
                )
                logger.debug('\n'.join(diff))
            else:
                logger.info('✅ Formatting passed on %s', file)

    # Lint
    if do_lint_check:
        for file in files:
            lint_warnings = lint_check(file, tidy_options, skip_compile_cmd)
            if len(lint_warnings) != 0:
                logger.warning('❌ Linter found improvements in %s.', file)
                logger.debug('\n'.join(lint_warnings))
            else:
                logger.info('✅ Linting passed in %s', file)

    status = 0
    # Clean, Build, & Run
    if make_build(target_directory):
        logger.info('✅ Build passed')
        # Run
        run_stats = run(os.path.join(target_directory, program_name))
        total_stats = sum(run_stats)
        if total_stats:
            logger.info('✅ Test run passed')
        else:
            logger.error('❌ Test run failed')
            status = 1
    else:
        logger.error('❌ Build failed')
        status = 1
    logger.info('End %s', identify(header))
    sys.exit(status)

def csv_solution_check_make(csv_key, target_directory, program_name='asgt', base_directory=None, run=None, files=None, do_format_check=True, do_lint_check=True, tidy_options=None, skip_compile_cmd=False):
    """Main function for checking student's solution. Provide a pointer to a
    run function."""
    logger = setup_logger()
    students_file = os.environ.get("MS_GITUSER_PICKLE")
    students_dict = None
    if not students_file:
        logger.debug('Missing environment variable MS_GITUSER_PICKLE. Cannot convert GitHub logins to sortable names.')
    else:
        logger.info("Loading student information")
        with open(students_file, "rb") as fh:
            # The students file contains only one dict
            students_dict = pickle.load(fh)
    abs_path_target_dir = os.path.abspath(target_directory)
    repo_root = os.path.dirname(abs_path_target_dir)
    cwd_name = os.path.basename(abs_path_target_dir)
    csv_filename = f'.{csv_key}_{cwd_name}_gradelog.csv'
    csv_path = os.path.join(repo_root, csv_filename)
    csv_fields = ['Repo Name', 'Part', 'Author', 'Partner1', 'Partner2', 'Partner3', 'PartnerN', 'Formatting', 'Linting', 'Build', 'Tests', 'UnitTests', 'Notes', 'UnitTestNotes']
    status = 0
    with open(csv_path, 'w') as csv_output_handle:
        outcsv = csv.DictWriter(csv_output_handle, csv_fields)
        outcsv.writeheader()
        row = {}
        row['Repo Name'] = csv_key
        row['Part'] = cwd_name
        # Init to empty string so you're always adding notes.
        row['Notes'] =''
        if not files:
            # This could be a target in the Makefile
            files = glob_all_src_files(target_directory)
        else:
            files = [os.path.join(target_directory, file) for file in files]

        if len(files) == 0:
            logger.error("❌ No files in %s.", target_directory)
            row['Formatting'] = 0
            row['Linting'] = 0
            row['Build'] = 0
            row['Tests'] = 0
            row['Notes'] = f"❌ No files in {target_directory}."
            status = 1
        else:
            # Header checks
            files_missing_header = [file for file in files if not header_check(file)]
            files_with_header = [file for file in files if header_check(file)]
            header = null_dict_header()
            if len(files_with_header) == 0:
                logger.error('❌ No header provided in any file in %s. Exiting.', target_directory)
                logger.error('All files: %s', ' '.join(files))
                row['Formatting'] = 0
                row['Linting'] = 0
                row['Build'] = 0
                row['Tests'] = 0
                all_files = ' '.join(files)
                row['Notes'] = f'❌ No header provided in any file in {target_directory}. All files: {all_files}.'
                status = 1
            else:
                with open(files_with_header[0]) as file_handle:
                    contents = file_handle.read()
                header = dict_header(contents)


            logger.info('Start %s', identify(header))
            logger.info('All files: %s', ' '.join(files))
            files_missing_header = [file for file in files if not header_check(file)]
            names = header['name'].split()
            sortable_name = '{}, {}'.format(names[-1], ' '.join(names[:len(names)-1]))
            row['Author'] = sortable_name
            partners = header['partners'].replace(',', ' ').replace('@', '').lower().split()
            sortable_names = []
            
            # Map GitHub login to student name
            if students_dict:
                # sortable partner names
                for github_login in partners:
                    print(github_login)
                    student_name = students_dict[github_login] if github_login in students_dict else None
                    if not student_name:
                        logger.warning(f"No such user in db '{github_login}'. Skipping.")
                        row['Notes'] = row['Notes'] + f'❌ Partner: no such user in db {github_login}.'
                        name = github_login
                    else:
                        name = '"{}, {}"'.format(student_name[0], student_name[1])
                    sortable_names.append(name)
            else:
                # Can't map the logins to names, just use them as is.
                sortable_names = partners
            for num, name in enumerate(sortable_names, start=1):
                key = f'Partner{num}'
                if num > 3:
                    break
                row[key] = name
            if len(sortable_names) > 3:
                row['PartnerN'] = ';'.join(sortable_names[3:])

            if len(files_missing_header) != 0:
                files_missing_header_str = ' '.join(files_missing_header)
                logger.warning(
                    'Files missing headers: %s', files_missing_header_str
                )
                row['Notes'] = row['Notes'] + f'❌Files missing headers: {files_missing_header_str}\n'
                status = 1
            # Check if files have changed
            if base_directory:
                count = 0
                for file in files:
                    diff = strip_and_compare_files(file, os.path.join(base_directory, file))
                    if len(diff) == 0:
                        count += 1
                        logger.error('No changes made in file %s.', file)
                if count == len(files):
                    logger.error('No changes made ANY file. Stopping.')
                    sys.exit(1)
            else:
                logger.debug('Skipping base file comparison.')

            # Format
            if do_format_check:
                count = 0
                for file in files:
                    diff = format_check(file)
                    if len(diff) != 0:
                        logger.warning('❌ Formatting needs improvement in %s.', file)
                        logger.info(
                            'Please make sure your code conforms to the Google C++ style.'
                        )
                        logger.debug('\n'.join(diff))
                        row['Notes'] = row['Notes'] + f'❌ Formatting needs improvement in {file}.\n'
                        status = 1
                    else:
                        logger.info('✅ Formatting passed on %s', file)
                        count += 1
                row['Formatting'] = f'{count}/{len(files)}'

            # Lint
            if do_lint_check:
                count = 0
                for file in files:
                    lint_warnings = lint_check(file, tidy_options, skip_compile_cmd)
                    if len(lint_warnings) != 0:
                        logger.warning('❌ Linter found improvements in %s.', file)
                        logger.debug('\n'.join(lint_warnings))
                        row['Notes'] = row['Notes'] + f'❌ Linter found improvements in {file}.\n'
                        status = 1
                    else:
                        logger.info('✅ Linting passed in %s', file)
                        count += 1
                row['Linting'] = f'{count}/{len(files)}'
            # Unit tests
            # We don't know if there are unit tests in this project
            # or not. We'll assume there are and then check to see
            # if an output file was created.
            logger.info('✅ Attempting unit tests')
            unit_test_output_file="test_detail.json"
            make_unittest(target_directory, output_file=unit_test_output_file)
            unit_test_output_path = os.path.join(target_directory, unit_test_output_file)
            if os.path.exists(unit_test_output_path):
                logger.info('✅ Unit test output found')
                with open(unit_test_output_path, 'r') as json_fh:
                    unit_test_results = json.load(json_fh)
                    total_tests = unit_test_results['tests']
                    failures = unit_test_results.get('failures', 0)
                    passed_tests = total_tests - failures
                    if failures > 0:
                        logger.error(f'❌ One or more unit tests failed ({passed_tests}/{total_tests})')
                    else:
                        logger.info('✅ Passed all unit tests')                    
                    row['UnitTests'] = f'{passed_tests}/{total_tests}'
                    row['UnitTestNotes'] = ""
                    for test_suite in unit_test_results['testsuites']:
                        name = test_suite['name']
                        for inner_suite in test_suite['testsuite']:
                            inner_name = inner_suite['name']
                            if 'failures' in inner_suite:
                                for fail in inner_suite['failures']:
                                    this_fail = fail['failure']
                                    unit_test_note = f'{name}:{inner_name}:{this_fail}\n'
                                    row['UnitTestNotes'] = row['UnitTestNotes'] + unit_test_note
                                    logger.error(f'❌ {unit_test_note}')
                                    
            # Clean, Build, & Run
            if make_build(target_directory):
                logger.info('✅ Build passed')
                row['Build'] = 1
                # Run
                run_stats = run(os.path.join(target_directory, program_name))
                # passed tests / total tests
                test_notes = f'{sum(run_stats)}/{len(run_stats)}'
                if all(run_stats):
                    logger.info('✅ All test runs passed')
                else:
                    logger.error(f'❌ One or more runs failed ({test_notes})')
                    row['Notes'] = row['Notes'] + f'❌ One or more test runs failed\n'
                    status = 1
                row['Tests'] = test_notes
            else:
                logger.error('❌ Build failed')
                row['Build'] = 0
                row['Notes'] = row['Notes'] + f'❌ Build failed\n'
                row['Tests'] = '0/0'
                status = 1
            logger.info('End %s', identify(header))
        outcsv.writerow(row)
    sys.exit(status)
