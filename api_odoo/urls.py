from unicodedata import name
from django.contrib import admin
from django.urls import path
from product.views import *
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


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

    path('login', LoginView.as_view(template_name='Login.html'), name='login'),
    path('logout', LogoutView, name="logout"),
    

    path('password_reset', PasswordResetView.as_view(template_name='password_reset_form.html', html_email_template_name='password_reset_email.html'), name='password_reset'),
    path('password_reset_done',PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('P<uidb64>[0-9A-Za-z\-]'+'/P<token>'+'/',PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
    path('password_reset_complete',PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),
]
