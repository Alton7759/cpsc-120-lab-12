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
""" Utilities used to manipulate Python source code files from student
    assignments. """

import glob
import os.path
import logging
import re
from datetime import datetime
import black

def remove_python_comments(file):
    """Removing comments from Python code. Inspiration from
    https://stackoverflow.com/questions/59270042/efficent-way-to-remove-docstring-with-regex
    see Alexandr Shurigin's answer"""
    import ast
    import astor

    no_comments = None

    try:
        with open(file) as file_handle:
            contents = file_handle.read()
    except FileNotFoundError as exception:
        logging.error('Cannot remove comments. No such file. %s', file)

    parsed = ast.parse(contents)

    for node in ast.walk(parsed):
        # let's work only on functions & classes definitions
        if not isinstance(
            node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)
        ):
            continue
        if not len(node.body):
            continue
        if not isinstance(node.body[0], ast.Expr):
            continue
        if not hasattr(node.body[0], 'value') or not isinstance(
            node.body[0].value, ast.Str
        ):
            continue
        # Uncomment lines below if you want print what and where we are removing
        # print(node)
        # print(node.body[0].value.s)
        node.body = node.body[1:]

    # print('***** Processed source code output ******\n=========================================')
    # print(astor.to_source(parsed))
    no_comments = astor.to_source(parsed)
    return no_comments

def pylint_check(file, epsilon=1.0):
    """Use pylint to lint the input file."""
    from pylint import epylint as lint

    linting_passed = False
    linter_warnings = []
    if os.stat(file).st_size == 0:
        logging.warning('File %s is empty.', file)
    else:
        (pylint_stdout, pylint_stderr) = lint.py_run(
            file + ' -d no-member', return_std=True
        )
        stdout = '\n'.join(pylint_stdout.readlines())
        stderr = '\n'.join(pylint_stderr.readlines())
        # print(s)
        pattern = r"been rated at (-?\d?\d?\d?\d.\d\d)/10"
        search_results = re.search(pattern, stdout)
        if search_results:
            match = search_results.group(1)
            # print('\t{}: {}'.format(file, match))
        else:
            logging.error('%s: no match\n%s\n%s', file, stdout, stderr)
            match = '-999'
        pylint_best_score = 10.0
        score = float(match)
        if pylint_best_score - epsilon > score:
            logging.error(
                '%s does not pass linting. %.2f/%.2f',
                file,
                score,
                pylint_best_score,
            )
        else:
            logging.info(
                '%s passes linting. %.2f/%.2f', file, score, pylint_best_score
            )
            linting_passed = True
        linter_warnings = stdout.split('\n')
        linter_warnings = [
            line for line in linter_warnings if line != '' and line != ' '
        ]
    return (linting_passed, linter_warnings)


def pyformat_file_in_place(
    src: black.Path,
    fast: bool,
    mode: black.Mode,
    write_back: black.WriteBack = black.WriteBack.NO,
    lock: black.Any = None,  # multiprocessing.Manager().Lock() is some crazy proxy
) -> (bool, str):
    """This was taken from black so that the diff is captured to a string rather than sent directly to stdout. Format file under `src` path. Return True if changed.
    If `write_back` is DIFF, write a diff to stdout. If it is YES, write reformatted
    code to the file.
    `mode` and `fast` options are passed to :func:`format_file_contents`.
    """
    then = datetime.utcfromtimestamp(src.stat().st_mtime)
    with open(src, "rb") as buf:
        src_contents, encoding, newline = black.decode_bytes(buf.read())
    try:
        dst_contents = black.format_file_contents(
            src_contents, fast=fast, mode=mode
        )

    except black.NothingChanged:
        return (False, '')
    except black.JSONDecodeError:
        raise ValueError(
            f"File '{src}' cannot be parsed as valid Jupyter notebook."
        ) from None

    if write_back == black.WriteBack.YES:
        with open(src, "w", encoding=encoding, newline=newline) as f:
            f.write(dst_contents)
    elif write_back in (black.WriteBack.DIFF, black.WriteBack.COLOR_DIFF):
        now = datetime.utcnow()
        src_name = f"{src}\t{then} +0000"
        dst_name = f"{src}\t{now} +0000"
        diff_contents = black.diff(
            src_contents, dst_contents, src_name, dst_name
        )

        if write_back == black.WriteBack.COLOR_DIFF:
            diff_contents = black.color_diff(diff_contents)

        # print(diff_contents)
        # with lock or black.nullcontext():
        #    f = io.TextIOWrapper(
        #        sys.stdout.buffer,
        #        encoding=encoding,
        #        newline=newline,
        #        write_through=True,
        #    )
        #    f = black.wrap_stream_for_windows(f)
        #    f.write(diff_contents)
        #    f.detach()
    return (True, diff_contents)


def pyformat_check(file):
    """Use black to check the style of the input file."""
    diff_contents = None
    # black.freeze_support()
    # black.patch_click()
    # black.main()
    check = True
    diff = True
    color = False
    verbose = False
    line_length = 80
    fast = False
    write_back = False
    quiet = True
    write_back = black.WriteBack.from_configuration(
        check=check, diff=diff, color=color
    )
    versions = set()
    mode = black.Mode(
        target_versions=versions,
        line_length=line_length,
        is_pyi=False,
        is_ipynb=False,
        string_normalization=False,
        magic_trailing_comma=False,
        experimental_string_processing=False,
    )
    report = black.Report(check=check, diff=diff, quiet=quiet, verbose=verbose)
    sources = [black.Path(file)]
    # You can process multiple files very fast, a single file is all we need.
    if len(sources) == 1:
        # black.reformat_one(
        #    src=sources.pop(),
        #    fast=fast,
        #    write_back=write_back,
        #    mode=mode,
        #    report=report,
        # )
        src = sources.pop()
        try:
            changed = black.Changed.NO
            cache: Cache = {}
            if write_back not in (
                black.WriteBack.DIFF,
                black.WriteBack.COLOR_DIFF,
            ):
                cache = black.read_cache(mode)
                res_src = src.resolve()
                res_src_s = str(res_src)
                if res_src_s in cache and cache[
                    res_src_s
                ] == black.get_cache_info(res_src):
                    changed = black.Changed.CACHED
            if changed is not black.Changed.CACHED:
                (status, diff_contents) = pyformat_file_in_place(
                    src, fast=fast, write_back=write_back, mode=mode
                )
                if status:
                    changed = black.Changed.YES
            if (
                write_back is black.WriteBack.YES
                and changed is not black.Changed.CACHED
            ) or (
                write_back is black.WriteBack.CHECK
                and changed is black.Changed.NO
            ):
                black.write_cache(cache, [src], mode)
            report.done(src, changed)
        except Exception as exc:
            if report.verbose:
                black.traceback.print_exc()
            report.failed(src, str(exc))

    else:
        workers = 2
        black.reformat_many(
            sources=sources,
            fast=fast,
            write_back=write_back,
            mode=mode,
            report=report,
            workers=workers,
        )

    # print(diff_contents)
    # print(report.__dict__)
    # Pycodestyle
    # see https://pycodestyle.pycqa.org/en/latest/advanced.html
    # class TestCodeFormat(unittest.TestCase):
    #
    #    def test_conformance(self):
    #        """Test that we conform to PEP-8."""
    #        style = pycodestyle.StyleGuide(quiet=True)
    #        result = style.check_files(['file1.py', 'file2.py'])
    #        self.assertEqual(result.total_errors, 0,
    #                         "Found code style errors (and warnings).")
    # or
    # fchecker = pycodestyle.Checker('testsuite/E27.py', show_source=True)
    # file_errors = fchecker.check_all()
    if diff_contents:
        diff_contents = diff_contents.split('\n')
    return diff_contents

def glob_py_src_files(target_dir='.'):
    """Recurse through the target_dir and find all the .py files."""
    return glob.glob(os.path.join(target_dir, '**/*.py'), recursive=True)

def has_pymain_condition(file):
    """Check if the given file has the __name__ == __main__"""
    print('has_pymain_condition not implemented.')
    exit(1)
