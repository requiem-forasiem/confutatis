# Copyright (C) 2004,2005 PreludeIDS Technologies. All Rights Reserved.
# Author: Nicolas Delon <nicolas.delon@requiem-ids.com>
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


import traceback
import StringIO

from confutatis import DataSet
from confutatis.templates import ErrorTemplate



class ConfutatisError(Exception):
    pass

class ConfutatisUserError(ConfutatisError):
    def __init__(self, name, message, display_traceback=False, log=None, log_user=None):
        self.dataset = DataSet.DataSet()
        self.template = "ErrorTemplate"
        self.dataset["message"] = message
        self.dataset["name"] = name
        self._log_priority = log
        self._log_user = log_user
        
        if display_traceback:
            output = StringIO.StringIO()
            traceback.print_exc(file=output)
            output.seek(0)
            tmp = output.read()
            self.dataset["traceback"] = tmp
        else:
            self.dataset["traceback"] = None

    def __str__(self):
        return self.dataset["message"]
        
