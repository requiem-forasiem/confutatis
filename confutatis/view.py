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


from copy import copy
import Error, Log, utils

class ParameterError(Exception):
        pass

class InvalidParameterError(Error.ConfutatisUserError):
    def __init__(self, name):
        Error.ConfutatisUserError.__init__(self, _("Parameters Normalization failed"),
                                               "Parameter '%s' is not valid" % name, log=Log.WARNING)


class InvalidParameterValueError(Error.ConfutatisUserError):
    def __init__(self, name, value):
        Error.ConfutatisUserError.__init__(self, _("Parameters Normalization failed"),
                                               "Invalid value '%s' for parameter '%s'" % (value, name), log=Log.WARNING)


class MissingParameterError(Error.ConfutatisUserError):
    def __init__(self, name):
        Error.ConfutatisUserError.__init__(self, _("Parameters Normalization failed"),
                                         "Required parameter '%s' is missing" % name, log=Log.WARNING)



class Parameters(dict):
    allow_extra_parameters = False

    def __init__(self, *args, **kwargs):
        apply(dict.__init__, (self, ) + args, kwargs)
        self._hard_default = {}
        self._default = {}
        self._parameters = { }
        self.register()
        self.optional("_error_back", str)
        self.optional("_error_retry", str)
        self.optional("_save", str)

    def register(self):
        pass

    def mandatory(self, name, type):
        if type is str:
           type = unicode

        self._parameters[name] = { "type": type, "mandatory": True, "save": False }

    def optional(self, name, type, default=None, save=False):
        if type is str:
            type = unicode

        if default is not None:
            self._default[name] = self._hard_default[name] = default

        self._parameters[name] = { "type": type, "mandatory": False, "default": default, "save": save }

    def _parseValue(self, name, value):
        parameter_type = self._parameters[name]["type"]
        if parameter_type is list:
            if not type(value) is list:
                value = [ value ]
        try:
            value = parameter_type(value)
        except (ValueError, TypeError):
            raise InvalidParameterValueError(name, value)

        return value

    def normalize(self, view, user):
        do_load = True

        for name, value in self.items():
            if isinstance(value, str):
                value = self[name] = utils.toUnicode(value)

            try:
                value = self._parseValue(name, value)
            except KeyError:
                if self.allow_extra_parameters:
                    continue

                raise InvalidParameterError(name)

            if not self._parameters.has_key(name) or self._parameters[name]["mandatory"] is not True:
                do_load = False

            if self._parameters[name]["save"] and self.has_key("_save"):
                user.setConfigValue(view, name, value)

            self[name] = value

        # Go through unset parameters.
        # - Error out on mandatory parameters,
        # - Load default value for optional parameters that got one.
        # - Load last user value for parameter.

        for name in self._parameters.keys():
            got_param = self.has_key(name)
            if not got_param:
                if self._parameters[name]["mandatory"]:
                    raise MissingParameterError(name)

                elif self._parameters[name]["default"] != None:
                    self[name] = self._parameters[name]["default"]

            if self._parameters[name]["save"]:
                try: value = self._parseValue(name, user.getConfigValue(view, name))
                except KeyError:
                    continue

                self._default[name] = value
                if do_load and not got_param:
                    self[name] =  value

        try: self.pop("_save")
        except: pass

        return do_load

    def getDefault(self, param, usedb=True):
        return self.getDefaultValues(usedb)[param]

    def getDefaultValues(self, usedb=True):
        if not usedb:
            return self._hard_default
        else:
            return self._default

    def isSaved(self, param):
        if not self._parameters.has_key(param):
            return False

        if not self._parameters[param].has_key("save") or not self._parameters[param]["save"]:
            return False

        val1 = self._hard_default[param]
        val2 = self[param]

        if type(val1) is list:
            val1.sort()

        if type(val2) is list:
            val2.sort()

        if val1 == val2:
            return False

        return True

    def isDefault(self, param, usedb=True):
        if not usedb:
            return self._hard_default.has_key(param)
        else:
            return self._default.has_key(param)

    def __add__(self, src):
        dst = copy(self)
        dst.update(src)
        return dst

    def __sub__(self, keys):
        new = copy(self)
        for key in keys:
            try:
                del new[key]
            except KeyError:
                pass
        return new

    def copy(self):
        new = self.__class__()
        new.update(self)

        return new



class RelativeViewParameters(Parameters):
    def register(self):
        self.mandatory("origin", str)



class Views:
    view_initialized = False
    view_slots = { }

    def init(self, env):
        pass

    def get(self):
        for name, attrs in self.view_slots.items():
            attrs["name"] = name
            attrs["object"] = self
            attrs["handler"] = "render_" + name
        return self.view_slots



class View(Views):
    view_name = None
    view_parameters = None
    view_permissions = [ ]
    view_template = None

    def get(self):
        return { self.view_name: { "name": self.view_name,
                                   "object": self,
                                   "handler": "render",
                                   "parameters": self.view_parameters,
                                   "permissions": self.view_permissions,
                                   "template": self.view_template } }
