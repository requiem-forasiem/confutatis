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


import sys


class DataSet(dict):
    def __setitem__(self, key, value):
        keys = key.split(".", 1)
        if len(keys) == 1:
            dict.__setitem__(self, key, value)
        else:
            key1, key2 = keys
            if not self.has_key(key1):
                dict.__setitem__(self, key1, DataSet())
            dict.__getitem__(self, key1)[key2] = value
    
    def __getitem__(self, key):
        try:
            keys = key.split(".", 1)
            if len(keys) == 1:
                return dict.__getitem__(self, key)
            return dict.__getitem__(self, keys[0])[keys[1]]
        except KeyError:
            return ""
