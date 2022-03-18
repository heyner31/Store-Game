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
import pandas as pd
import logging
 
from .connectionOdoo import * 
 
from dotenv import load_dotenv
load_dotenv()
# from dotenv import load_dotenv
 
# Create your views here.
def viewproducts(request):
    #return HttpResponse(socket.gethostbyname(socket.gethostname()))
    
    odoo = connectionOdoo()
    products =  odoo.models.execute_kw(
    odoo.db
    ,odoo.uid,
    odoo.password,
    'product.template','search_read',
    [
        [
            [ "company_id" ,"=", 1]
            # [ "id" ,"=", 2]
        ]
    ],
    {'fields': []}
)
 
    data = {
        "products":products
    }
        
    # return HttpResponse(xx)
    return render(request ,"products/list.html",data)
 
def createProduct(request):
    url = os.getenv("URL_ODOO")
    db =  os.getenv("DB_ODOO")
    password =  os.getenv("PASSWORD_ODOO")
 
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    output = common.version()
    uid = common.authenticate(db, os.getenv("USERNAME_ODOO"), password, output)
 
    id = models.execute_kw(db, uid, password, 'product.template', 'create', [{
    'name': "Producto DJANGO companyID",
    'default_code':"test_default_code_DJANGO",
    'list_price':"100",
    "company_id":1
    }])
    return HttpResponse(id)
 
def deleteProduct(request, id):
    url = os.getenv("URL_ODOO")
    db =  os.getenv("DB_ODOO")
    password =  os.getenv("PASSWORD_ODOO")
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    output =  common.version()
    uid = common.authenticate(db, os.getenv("USERNAME_ODOO"), password, output)
    models.execute_kw(db, uid, password, 'product.template', 'unlink', [[id]])
    return HttpResponse("deleted")
 
def updateProduct(request):
    odoo = connectionOdoo()
    odoo.models.execute_kw(odoo.db, odoo.uid, odoo.password, 'product.template', 'write', [[43], {
    'name': "Newer partner",
    "price":"4567"
        }])
    return HttpResponse("updated")
    
def AddProductsCSV(request):
    df = pd.read_csv('product/productos.csv')
    if(df != null):
        print(df.to_numpy()[0])
        for i in range(len(df.to_numpy())):
            self.createCsvProducts(df.to_numpy()[i][0], df.to_numpy()[i][1], df.to_numpy()[i][2], df.to_numpy()[i][3])    
        return HttpResponse("CVS agregado")
    else:
        return HttpResponse("No hay archivo")

def importProductsCSV(request):
    odoo = connectionOdoo()
    df = pd.read_csv("product/products.csv", sep=',', delimiter=None, header="infer", names=None, index_col=False)
    info = []

    for i in range(0, len(df)):
        logging.debug("---Product {}---\n".format(i+1))
        product = {}
        for item in df:
            logging.debug("" + item + ":") 
            data = df[item][i]
            logging.debug(data)
            logging.debug(type(data))
            
            if item == "list_price":
                if data <= 0:
                    raise Exception("El producto {} tiene que tener un valor válido".format(df["name"][i]))
            
            if isinstance(data, str):
                product[item] = data
            else:
                product[item] = data.item()
                
        info.append(product)
            
        product["barcode"] = str(product["barcode"])
        logging.debug(product)
        logging.debug(type(product))
        #sys.exit()
        id = None
        try:
            id = odoo.models.execute_kw(odoo.db, odoo.uid, odoo.password, 'product.template', 'create',
                [
                    product
                ])
        except Exception as e:
            return HttpResponse("Error")
        logging.debug(id)

    return HttpResponse(info)


# check if the deleted record is still in the database
    # models.execute_kw(db, uid, password,
    #     'res.partner', 'search', [[['id', '=', id]]])
   