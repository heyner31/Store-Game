from ast import If
from itertools import product
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponse, response, JsonResponse
from django.contrib.auth import logout
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
def ajax_posting(request):
    if request.is_ajax():
        first_name = request.POST.get('first_name', None) # getting data from first_name input 
        last_name = request.POST.get('last_name', None)  # getting data from last_name input
        if first_name and last_name: #cheking if first_name and last_name have value
            response = {
                         'msg':'Your form has been submitted successfully ' + first_name # response message
            }
            return JsonResponse(response) # return response as JSON

def prueba_ajax(request):
    return render(request, 'prueba-ajax.html')

def addGameAjax(request):

    #try:
        #request.is_ajax()
    #    if request.is_ajax():
    #        return JsonResponse("EXITO")
    #except:
    #    responseData = {}
    #    responseData['success'] = 'false'
    #    responseData['message'] = 'Error: Request is not Ajax'
    #    return JsonResponse(responseData, status=422)

    try:
        json_object = request.POST
        #json_object = json.loads(request.body)
    except:
        responseData = {}
        responseData['success'] = 'false'
        responseData['message'] = 'Error: Json not obtained'
        return JsonResponse(responseData, status=422)

    try:
        odoo = connectionOdoo()
        id = odoo.models.execute_kw(odoo.db, odoo.uid, odoo.password, 'product.template', 'create', [{
        'name': json_object['name'],
        'description': json_object['description'],
        'description_purchase': json_object['description_purchase'],
        'description_sale': json_object['description_sale'],
        'type': "product",
        'barcode': json_object['barcode'],
        'default_code': json_object['default_code'],
        'categ_id': "1",
        'list_price': json_object['list_price'],
        'standard_price': json_object['standard_price'],
        #'active' : json_object['active'],
        "company_id": 4
        }])
    except:
        responseData = {}
        responseData['success'] = 'false'
        responseData['message'] = 'Error: Game not inserted'
        return JsonResponse(responseData, status=422)

    response = {
        'msg':'El videojuego ha sido agregado correctamente a la base de datos' # response message
    }
    return JsonResponse(response) # return response as JSON

@login_required
def editGameAjax(request):

    try:
        json_object = request.POST
        #json_object = json.loads(request.body)
    except:
        responseData = {}
        responseData['success'] = 'false'
        responseData['message'] = 'Error: Json not obtained'
        return JsonResponse(responseData, status=422)

    try:
        odoo = connectionOdoo()
        odoo.models.execute_kw(odoo.db, odoo.uid, odoo.password, 'product.template', 'write', [[int(json_object['id'])], {
        'name': json_object['name'],
        'description': json_object['description'],
        'description_purchase': json_object['description_purchase'],
        'description_sale': json_object['description_sale'],
        'barcode': json_object['barcode'],
        'default_code': json_object['default_code'],
        'list_price': json_object['list_price'],
        'standard_price': json_object['standard_price'],
        #'active' : json_object['active'],
        }])
    except:
        responseData = {}
        responseData['success'] = 'false'
        responseData['message'] = 'Error: Game not updated'
        responseData['num'] = int(json_object['id'])
        return JsonResponse(responseData, status=422)

    response = {
        'msg':'El videojuego ha sido actualizado correctamente en la base de datos' # response message
    }
    return JsonResponse(response) # return response as JSON

@login_required
def edit(request, gameid):
    odoo = connectionOdoo()
    products =  odoo.models.execute_kw(
    odoo.db,
    odoo.uid,
    odoo.password,
    'product.template','search_read',
    [
        [
            [ "id" ,"=", gameid]
        ]
    ],
    {'fields': []}
)

    data = {
        "products": products
    }
        
    return render(request ,"edit.html", data)

@login_required
def deleteGame(request):

    try:
        json_object = request.POST
        #json_object = json.loads(request.body)
    except:
        responseData = {}
        responseData['success'] = 'false'
        responseData['message'] = 'Error: Json not obtained'
        return JsonResponse(responseData, status=422)

    try:
        odoo = connectionOdoo()

        odoo.models.execute_kw(
            odoo.db,
            odoo.uid,
            odoo.password,
            'product.template', 
            'unlink', 
            [[int(json_object['id'])]])

    except:
        responseData = {}
        responseData['success'] = 'false'
        responseData['message'] = 'Error: Game not deleted'
        return JsonResponse(responseData, status=422)

    data = {
            'deleted': True
        }

    return JsonResponse(data)

@login_required
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
            [ "company_id" ,"=", 4]
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

@login_required
def viewGames(request):
    #return HttpResponse(socket.gethostbyname(socket.gethostname()))
    
    odoo = connectionOdoo()
    products =  odoo.models.execute_kw(
    odoo.db
    ,odoo.uid,
    odoo.password,
    'product.template','search_read',
    [
        [
            [ "company_id" ,"=", 4]
            # [ "id" ,"=", 2]
        ]
    ],
    {'fields': []}
)
    
    cuantos = len(products)

    data = {
        "products": products,
        "cuantos": cuantos
    }
        
    # return HttpResponse(xx)
    return render(request ,"table.html", data)

@login_required
def main(request):
    return render(request, 'base.html')

@login_required
def add(request):
    return render(request, 'add.html')

@login_required
def addGame(request):

    try:
        json_object = request.POST
        #json_object = json.loads(request.body)
    except:
        responseData = {}
        responseData['success'] = 'false'
        responseData['message'] = 'Error: Json not obtained'
        return JsonResponse(responseData, status=422)

    try:
        odoo = connectionOdoo()
        id = odoo.models.execute_kw(odoo.db, odoo.uid, odoo.password, 'product.template', 'create', [{
        'name': json_object['name'],
        'description': json_object['description'],
        'description_purchase': json_object['description_purchase'],
        'description_sale': json_object['description_sale'],
        'type': "product",
        'barcode': json_object['barcode'],
        'default_code': json_object['default_code'],
        'categ_id': "1",
        'list_price': json_object['list_price'],
        "company_id": 4
        }])
    except:
        responseData = {}
        responseData['success'] = 'false'
        responseData['message'] = 'Error: Game not inserted'
        return JsonResponse(responseData, status=422)

    return render(request, 'add.html')

@login_required
def detailGame(request, gameid):
    odoo = connectionOdoo()
    products =  odoo.models.execute_kw(
    odoo.db
    ,odoo.uid,
    odoo.password,
    'product.template','search_read',
    [
        [
            #[ "company_id" ,"=", 4]
            [ "id" ,"=", gameid]
        ]
    ],
    {'fields': []}
)

    data = {
        "products": products
    }
        
    return render(request ,"detail-table.html", data)
    #return HttpResponse(gameid)

@login_required 
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

@login_required
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

@login_required 
def updateProduct(request):
    odoo = connectionOdoo()
    odoo.models.execute_kw(odoo.db, odoo.uid, odoo.password, 'product.template', 'write', [[43], {
    'name': "Newer partner",
    "price":"4567"
        }])
    return HttpResponse("updated")

@login_required    
def AddProductsCSV(request):
    df = pd.read_csv('product/productos.csv')
    if(df != null):
        print(df.to_numpy()[0])
        for i in range(len(df.to_numpy())):
            self.createCsvProducts(df.to_numpy()[i][0], df.to_numpy()[i][1], df.to_numpy()[i][2], df.to_numpy()[i][3])    
        return HttpResponse("CVS agregado")
    else:
        return HttpResponse("No hay archivo")

@login_required
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

def LogoutView(request):
    logout(request)
    return redirect('/login')