# Copyright (C) 2004,2005 PreludeIDS Technologies. All Rights Reserved.
# Author: Nicolas Delon 
#
# This file is part of the Confutatis program.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING.  If not, write to
# the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.


import re
from confutatis import utils

class Error(Exception):
    pass



class ParseError(Error):
    def __init__(self, filename, lineno, line):
        self.filename = filename
        self.lineno = lineno
        self.line = line

    def __str__(self):
        return "parse error in \"%s\" at %s line %d" % (self.line.rstrip(), self.filename, self.lineno)


class ConfigParserSection(utils.OrderedDict):
    def __init__(self, name):
        utils.OrderedDict.__init__(self)
        self.name = name

    def __nonzero__(self):
        return True

    def getOption(self, name):
        return self[name]

    def getOptionValue(self, key, value=None):
        try:
            return self[key].value
        except KeyError:
            return value

    def getOptions(self):
        return self.values()



class ConfigParserOption:
    def __init__(self, name, value, lineno, line):
        self.name = utils.toUnicode(name)
        self.value = utils.toUnicode(value)
        self.lineno = lineno
        self.line = line



class MyConfigParser:
    """
    A config parser class ala ConfigParser.ConfigParser (only read operations
    are (will be) supported).
    ConfigParser.ConfigParser did not feed all our needs:
    - we need the '= value' part of option to be optionnal
    - we need to support special characters (like ':') in option name (for urls)
    - we need to keep the right order of options in sections (this is done via
      the OrderedDict class that subclass dict)
    """

    EMPTY_LINE_REGEXP = re.compile("^\s*(\#.*)?$")
    SECTION_REGEXP = re.compile("^\s*\[(?P<name>.+)]")
    OPTION_REGEXP = re.compile("^\s*(?P<name>[\s]*[^:]+)(\:\s*(?P<value>.+))?$")

    def __init__(self, filename):
        self.filename = filename
        self._sections = utils.OrderedDict()
        self._root_section = utils.OrderedDict()
        self._current_section = self._root_section

    def load(self):
        lineno = 0

        for line in open(self.filename).readlines():
            lineno += 1
            result = self.EMPTY_LINE_REGEXP.match(line)
            if result:
                continue
            else:
                result = self.SECTION_REGEXP.match(line)
                if result:
                    name = result.group("name")
                    name = name.strip()
                    self._current_section = self._sections[name] = ConfigParserSection(name)
                else:
                    result = self.OPTION_REGEXP.match(line)
                    if result:
                        name, value = result.group("name", "value")
                        name = name.strip()
                        if value:
                            value = value.strip()
                        self._current_section[name] = ConfigParserOption(name, value, lineno, line)
                    else:
                        raise ParseError(file.name, lineno, line)

    def getSection(self, name):
        return self._sections[name]

    def getSections(self):
        return self._sections.values()

    def __str__(self):
        content = ""
        for section in self.getSections():
            content += "[%s]\n" % section.name
            for option in section.getOptions():
                content += "%s: %s\n" % (option.name, option.value)
            content += "\n"

        return content
