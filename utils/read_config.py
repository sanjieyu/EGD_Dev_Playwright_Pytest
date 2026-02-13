# Author:Yi Sun(Tim) 2022-09-13

'''Read Config function'''

import configparser
import os
from pathlib import Path

class ReadConfig():
    def __init__(self):
        project_root = Path(__file__).parent.parent
        configfile_path = project_root / "Config" / "config.ini"
        self.cf = configparser.ConfigParser()
        self.cf.read(configfile_path)

    def get_url(self):
        url = self.cf.get('config','url')
        print(url)
        return url

    def admin_username(self):
        username_admin = self.cf.get('admin','username')
        print(username_admin)
        return username_admin

    def admin_password(self):
        password_admin = self.cf.get('admin','password')
        print(password_admin)
        return password_admin

    def dealer_username(self):
        username_dealer = self.cf.get('dealer','username')
        # print(username_rep)
        return username_dealer

    def dealer_password(self):
        password_dealer = self.cf.get('dealer','password')
        # print(password_rep)
        return password_dealer
