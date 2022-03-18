from contextlib import nullcontext
from itertools import product
from django.shortcuts import render
from django.http import HttpResponse, response
# import requests
import xmlrpc.client
import json
import base64
import sys
import json 
import os
import socket

from dotenv import load_dotenv
load_dotenv()
class connectionOdoo():
    models = None
    common = None
    output = None
    uid = None
    url =  ""
    db = ""
    password = ""
    user = ""
    def __init__(self, *args):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip= s.getsockname()[0]
        s.close()

        self.url = os.getenv("URL_ODOOO")
        self.db =  os.getenv("DB_ODOO")
        self.password =  os.getenv("PASSWORD_ODOO")
        self.user =  os.getenv("USERNAME_ODOO")


        self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))

        self.common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.url))

        self.output = self.common.version()
        
        self.uid = self.common.authenticate(self.db,self.user , self.password, self.output)

        
        