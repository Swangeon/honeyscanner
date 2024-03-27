#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This is the module for handling the Amun honeypot.
"""

from .base_honeypot import BaseHoneypot

class Amun(BaseHoneypot):
    def __init__(self,
                 version: str,
                 ip: int,
                 port: int,
                 username: str ='',
                 password: str =''):
        if username is None:
            username = ''
        if password is None:
            password = ''
        super().__init__("amun", version, ip, port, username, password)

    def set_source_code_url(self):
        return "https://github.com/zeroq/amun"
    #"https://downloads.sourceforge.net/project/amunhoney/amun/amun-v0.2.2/amun-v0.2.2.tar.gz?ts=gAAAAABmAaF12M8Wyez6J4YTMoqMgz5sWvqdv_w8lx5b20Vbc9vQDbqN5ve5ZkvYysL83l5C0CdlccQgejWUrfsSTi0PVo5whA%3D%3D&use_mirror=master&r="

    def set_versions_list(self):
        return [
            {
                "version": "0.1.0",
                "requirements_url": "python2.7"
            }
        ]

    def set_owner(self):
        return "Jan Goebel"