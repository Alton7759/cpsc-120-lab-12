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
""" Check the given files to see if they conform to good programming
    practices using clang-tidy. """

import sys
import logging
import os.path
from logger import setup_logger
from ccsrcutilities import lint_check


def main():
    """ Main function; process each file given through the linter. """
    logger = setup_logger()
    if len(sys.argv) < 2:
        logger.warning('Only %s arguments provided.', len(sys.argv))
        logger.warning('Provide a list of files to check.')
    status = 0
    for in_file in sys.argv[1:]:
        logger.info('Linting file: %s', in_file)
        if not os.path.exists(in_file):
            logger.debug('File %s does not exist. Continuing.', in_file)
            continue
        tidy_opts = (
            '-checks="*,-misc-unused-parameters,'
            '-modernize-use-trailing-return-type,-google-build-using-namespace,'
            '-cppcoreguidelines-avoid-magic-numbers,-readability-magic-numbers,'
            '-fuchsia-default-arguments-calls,-clang-analyzer-deadcode.DeadStores,'
            '-bugprone-exception-escape,-llvm-header-guard,-cert-err58-cpp,'
            '-fuchsia-statically-constructed-objects,-cert-msc32-c,-cert-msc51-cpp,'
            '-google-runtime-references"'
            ' -config="{CheckOptions: [{key: readability-identifier-naming.ClassCase, value: CamelCase}, '
            '{key: readability-identifier-naming.ClassMemberCase, value: lower_case}, '
            '{key: readability-identifier-naming.ConstexprVariableCase, value: CamelCase}, '
            '{key: readability-identifier-naming.ConstexprVariablePrefix, value: k}, '
            '{key: readability-identifier-naming.EnumCase, value: CamelCase}, '
            '{key: readability-identifier-naming.EnumConstantCase, value: CamelCase}, '
            '{key: readability-identifier-naming.EnumConstantPrefix, value: k}, '
            '{key: readability-identifier-naming.GlobalFunctionCase, value: CamelCase}, '
            '{key: readability-identifier-naming.FunctionCase, value: lower_case}, '
            '{key: readability-identifier-naming.GlobalConstantCase, value: CamelCase}, '
            '{key: readability-identifier-naming.GlobalConstantPrefix, value: k}, '
            '{key: readability-identifier-naming.StaticConstantCase, value: CamelCase}, '
            '{key: readability-identifier-naming.StaticConstantPrefix, value: k}, '
            '{key: readability-identifier-naming.StaticVariableCase, value: lower_case}, '
            '{key: readability-identifier-naming.MacroDefinitionCase, value: UPPER_CASE}, '
            '{key: readability-identifier-naming.MacroDefinitionIgnoredRegexp, value: \'^[A-Z]+(_[A-Z]+)*_$\'}, '
            '{key: readability-identifier-naming.MemberCase, value: lower_case}, '
            '{key: readability-identifier-naming.PrivateMemberSuffix, value: _}, '
            '{key: readability-identifier-naming.PublicMemberSuffix, value: \'\'}, '
            '{key: readability-identifier-naming.NamespaceCase, value: lower_case}, '
            '{key: readability-identifier-naming.ParameterCase, value: lower_case}, '
            '{key: readability-identifier-naming.TypeAliasCase, value: CamelCase}, '
            '{key: readability-identifier-naming.TypedefCase, value: CamelCase}, '
            '{key: readability-identifier-naming.VariableCase, value: lower_case}, '
            '{key: readability-identifier-naming.IgnoreMainLikeFunctions, value: 1}]}"'
        )
        lint_warnings = lint_check(in_file, tidy_opts)
        if len(lint_warnings) != 0:
                logger.error('Linter found improvements.')
                logger.warning('\n'.join(lint_warnings))
                status = 1
                logger.error("🤯😳😤😫🤬")
                logger.error("Use the output from this program to help guide you.")
                logger.error("If you get stuck, ask your instructor for help.")
                logger.error(
                    "Remember, you can find the Google C++ style online "
                    "at https://google.github.io/styleguide/cppguide.html."
                )
        else:
                logger.info('😀 Linting passed 🥳')
                logger.info('This is not an auto-grader.')
                logger.info(
                    'Make sure you followed all the instructions and requirements.'
                )
    sys.exit(status)


if __name__ == '__main__':
    main()
