from django.urls import path, include
from .import views

urlpatterns = [
    path('', views.index),
    path('registration', views.register_user),
    path('login', views.login_user),
    path('logout', views.logout),
    path('quotes', views.show_dashboard),
    path('add_quote', views.add_quote),
    path('user/<int:quote_id>', views.view_quote),   #view page
    path('quotes/<int:quote_id>', views.remove),   #view page
    path('remove/<int:quote_id>',views.remove),
    path('liked_quote/<int:quote_id>', views.liked),
    path('unlike_quote/<int:quote_id>', views.unlike),
    path('myaccount/<int:user_id>', views.edit_user),
    

]