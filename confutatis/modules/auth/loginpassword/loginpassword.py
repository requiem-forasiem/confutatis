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


import md5
from confutatis import Auth, User, Database


class MyLoginPasswordAuth(Auth.LoginPasswordAuth):
    def __init__(self, env, config):
        user = config.getOptionValue("initial_admin_user", User.ADMIN_LOGIN)
        passwd = config.getOptionValue("initial_admin_pass", User.ADMIN_LOGIN)

        expiration = int(config.getOptionValue("expiration", 60)) * 60
        Auth.LoginPasswordAuth.__init__(self, env, expiration)

        has_user_manager = False
        for login in self.getUserLogins():
            permissions = self.db.getPermissions(login)
            if User.PERM_USER_MANAGEMENT in permissions:
                has_user_manager = True
                break

        if not has_user_manager:
            if not self.db.hasUser(user):
                self.db.createUser(user)

            if not self.db.hasPassword(user):
                self.setPassword(user, passwd)

            self.db.setPermissions(user, User.ALL_PERMISSIONS)

    def _hash(self, data):
        return md5.new(data.encode("utf8")).hexdigest()

    def createUser(self, login):
        return self.db.createUser(login)

    def deleteUser(self, login):
        return self.db.deleteUser(login)

    def checkPassword(self, login, password):
        try:
            real_password = self.db.getPassword(login)
        except Database.DatabaseError:
            raise Auth.AuthError()

        if real_password == None or self._hash(password) != real_password:
            raise Auth.AuthError()

    def setPassword(self, login, password):
        self.db.setPassword(login, self._hash(password))


def load(env, config):
    return MyLoginPasswordAuth(env, config)
