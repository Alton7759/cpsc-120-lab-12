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
""" Parses the header define by the example given below. """
# https://docs.google.com/document/d/17WkDlxO92zpb26pYM1NIACPcMWtCOlKO7WCrWC6YxRo/edit#
# Example C++ header
# // Michael Shafae
# // CPSC 120-01
# // 2021-01-30
# // mshafae@csu.fullerton.edu
# // @mshafae
# //
# // Lab 00-00
# // Partners: @peteranteater, @ivclasers
# //
# // This is my first program and it prints out Hello World!
# //

import datetime
import itertools
import re

from logger import setup_logger

def null_dict_header():
    result_dict = {
        'name' : 'No Header',
        'class' : 'CPSC XXX',
        'email' : 'no-reply@csu.fullerton.edu',
        'github' : 'UnknownGitHub',
        'asgt' : 'Lab Unknown',
        'partners' : 'UnknownPartners',
        'comment' : 'UnknownComment',
    }
    return result_dict

def dict_header(contents, silent=False):
    """Given a single string, parse the header and return the result
    as a dictionary with the keys class, email, github, asgt, comment.
    On parse error, log a descriptive message and return an empty dictionary."""

    logger = setup_logger()
    
    FAILURE = dict()

    lines = contents.splitlines()

    # reject: empty source file
    if len(lines) == 0:
        if not silent:
            logger.warning('header missing because source file is empty')
        return FAILURE

    # reject: whitespace on first line
    assert(len(lines) > 0)
    if len(lines[0]) == 0 or lines[0].isspace():
        if not silent:
            logger.warning('line 1: expected a // comment holding a header, but found whitespace instead')
        return FAILURE

    # find prefix of all comment lines
    #
    # At this point we are permissive about leading and trailing whitespace, so
    # we can give constructive feedback about more important issues.
    # The strict whitespace check is last, below.
    comment_lines = list(itertools.takewhile(lambda line: line.lstrip().startswith('//'), lines))

    # reject: no comments (meaning the first line is neither whitespace nor a comment)
    if len(comment_lines) == 0:
        if not silent:
            logger.warning('line 1: expected a // comment holding a header, but instead found: %s', lines[0])
        return FAILURE

    # strip whitespace for parsing purposes
    header_lines = [line.strip() for line in comment_lines]
    
    # reject: header is impossibly short
    MIN_HEADER_LENGTH = 10 
    if len(header_lines) < MIN_HEADER_LENGTH:
        if not silent:
            logger.warning('line %i: header is only %i lines long', len(header_lines) + 1, len(header_lines))
            logger.warning('a header must be at least %i lines long to contain all required information', MIN_HEADER_LENGTH)
        return FAILURE

    # reject: missing blank lines 6 or 9
    def check_blank_line(line_number, previous_field_name):
        if header_lines[line_number - 1] != '//':
            if not silent:
                logger.warning('line %i: should be a blank // comment after the %s',
                                line_number, previous_field_name)
            return False
        return True
    if not check_blank_line(6, 'GitHub username'):
        return FAILURE
    if not check_blank_line(9, 'Partners'):
        return FAILURE

    # extract the fields: name, class, date, email, github, asgt, partners, comment
    # check that each is nonempty and has a space after //
    def check_field(line_number, name):
        line = header_lines[line_number - 1]
        assert(line.startswith('//'))
        assert(line.strip() == line)
        if line == '//':
            if not silent:
                logger.warning('line %i: should contain %s, but it is missing',
                                line_number, name)
            return False
        assert(len(line) > 2)
        if line[2] != ' ':
            if not silent:
                logger.warning('line %i: there must be a space between // and %s',
                                line_number, name)
            return False
        assert(len(line) > 3) # must be a non-whitespace char after '// '
        value = line[3:].strip()
        if len(value) == 0:
            if not silent:
                logger.warning('line %i: %s field is empty', line_number, name)
            return False
        return value

    NAME_LINE = 1
    KLASS_LINE = 2
    DATE_LINE = 3
    EMAIL_LINE = 4
    GITHUB_LINE = 5
    ASSIGNMENT_LINE = 7
    PARTNERS_LINE = 8
    COMMENT_LINE = 10

    name = check_field(NAME_LINE, 'name')
    klass = check_field(KLASS_LINE, 'class') # class is a reserved word
    date = check_field(DATE_LINE, 'date')
    email = check_field(EMAIL_LINE, 'email')
    github = check_field(GITHUB_LINE, 'GitHub')
    assignment = check_field(ASSIGNMENT_LINE, 'assignment')
    partners = check_field(PARTNERS_LINE, 'Partners:')
    comment = check_field(COMMENT_LINE, 'comment')
    if not all([name, klass, date, email, github, assignment, partners, comment]):
        return FAILURE

    # check name
    if not any([char.isalpha() for char in name]):
        if not silent:
            logger.warning('line %i: does not resemble a name', NAME_LINE)
            logger.warning('a name is expected to have at least one letter')
        return FAILURE

    # check class
    if not re.fullmatch('(?i)CPSC\s\d{3}[A-Z]?-\d{1,2}', klass):
        if not silent:
            logger.warning('line %i: does not resemble a class section number', KLASS_LINE)
            logger.warning('an example valid class section number is: 120L-01')
        return FAILURE
    
    # check date
    try:
        datetime.date.fromisoformat(date)
    except ValueError:
        if not silent:
            logger.warning('line %i: does not resemble a date in YYYY-MM-DD format', DATE_LINE)
            logger.warning('an example valid date is: 2022-12-31')
        return FAILURE

    # check email
    # any domain whatsoever
    if not re.fullmatch('\w+[.\-_0-9\w]*@.+', email):
        if not silent:
            logger.warning('line %i: does not resemble an email address', EMAIL_LINE)
            logger.warning('an example email address is: adalovelace@csu.fullerton.edu')
        return FAILURE
    # CSUF domain
    if not re.fullmatch('(?i)\w+[.\-_0-9\w]*@(csu\.)?fullerton\.edu', email):
        if not silent:
            logger.warning('line %i: email address is not CSUF-issued', EMAIL_LINE)
            logger.warning('use your CSUF-issued email ending in @csu.fullerton.edu or @fullerton.edu')
            logger.warning('an example email address is: adalovelace@csu.fullerton.edu')
        return FAILURE

    # github
    def is_github_username(str): # will reuse this for partners below
        return bool(re.fullmatch('@([a-zA-Z\d](?:[a-zA-Z\d]|-(?=[a-zA-Z\d])){0,38})', str))
    if not is_github_username(github):
        if not silent:
            logger.warning('line %i: does not resemble a GitHub username starting with @', GITHUB_LINE)
            logger.warning('an example GitHub username is: @AdaLovelace')
        return FAILURE

    # assignment
    if not re.fullmatch('(?i)Lab \d\d-\d\d', assignment):
        if not silent:
            logger.warning('line %i: does not resemble a Lab assignment number', ASSIGNMENT_LINE)
            logger.warning('an example lab assignment number is: Lab 01-02')
        return FAILURE

    # partners
    if not partners.startswith('Partners:'):
        if not silent:
            logger.warning('line %i: does not contain a Partners: list', PARTNERS_LINE)
        return FAILURE
    partner_string = partners.split('Partners:')[1].strip()
    partner_usernames = [str.strip()
                         for str in partner_string.split(',')
                         if len(str.strip()) > 0]
    partner_count = len(partner_usernames)
    if partner_count == 0:
        if not silent:
            logger.warning('line %i: partners list is empty; expected you to have a pair-programming partner', PARTNERS_LINE)
        # do not return FAILURE; proceed with grading this; life happens
    if partner_count > 2:
        if not silent:
            logger.warning('line %i: expected only one or two partners, but you have %i', PARTNERS_LINE, partner_count)
        # do not return FAILURE; proceed with grading this; life happens
    for username in partner_usernames:
        if not is_github_username(username):
            if not silent:
                logger.warning('line %i: partner "%s" does not resemble a GitHub username starting with @', PARTNERS_LINE, username)
                logger.warning('an example GitHub username is: @AdaLovelace')
            return FAILURE

    # comment
    if not any([char.isalpha() for char in comment]):
        if not silent:
            logger.warning('line %i: does not resemble a descriptive comment', COMMENT_LINE)
            logger.warning('a descriptive comment is expected to have at least one letter', COMMENT_LINE)
        return FAILURE

    # finally check for stray whitespace
    # use the un-stripped source lines in comment_lines, not the stripped ones in header_lines
    for index, line in enumerate(comment_lines):
        if line != line.lstrip():
            if not silent:
                logger.warning('line %i: unexpected leading whitespace; delete whitespace before //', index + 1)
            return FAILURE
        if line != line.rstrip():
            if not silent:
                logger.warning('line %i: unexpected trailing whitespace; delete whitespace at the end of the line', index + 1)
            return FAILURE

    # Success!
    # create a dictionary object
    result_dict = {
        'name' : name,
        'class' : klass,
        'email' : email,
        'github' : github,
        'asgt' : assignment,
        'partners' : partner_string,
        'comment' : comment,
    }

    return result_dict

def parse_header(contents, keyword=None):
    """Given Given a single string, parse the header and return the keyword's value."""
    result = dict_header(contents)
    if len(result) == 0:
        return None # failure
    if keyword is None:
        return result # everything
    if keyword in result:
        return result[keyword] # found single keyword
    return None # invalid keyword
