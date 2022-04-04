from unicodedata import name
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

    path('main', main, name="main"),
    path('games', viewGames, name="view games"),
    path('add-game', add, name="add game"),
    path('add', addGame,name='addGame'),
    path('game/<int:gameid>',detailGame,name='detailGame'),
    path('edit-game/<int:gameid>',edit,name='edit game'),


    path('add-game-ajax', addGameAjax, name="addGameAjax"),
    path('edit-game-ajax', editGameAjax, name="editGameAjax"),
    path('delete-game', deleteGame, name='deleteGame'),


    path('ajax-posting/', ajax_posting, name='ajax_posting'),# ajax-posting / name = that we will use in ajax url
    path('prueba-ajax', prueba_ajax, name='ajax_prueba'),
]
