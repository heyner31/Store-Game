from django.contrib import admin
from django.urls import path
from product.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('products', viewproducts, name="products"),
    path('create', createProduct, name="create"),
    path('delete/<int:id>', deleteProduct, name="delete"),
    path('uptate', updateProduct, name="update"),
    path('create/cvs', AddProductsCSV, name="addcvs"),
    path('importcsv', importProductsCSV, name="importcsv"),
]
