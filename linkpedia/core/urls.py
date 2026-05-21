from django.urls import path
from core.views import login, logout, home, create, all, delete


urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('index/', home, name='index'),
    path('', home,name='home'),
    path('create/', create, name='create'),
    path('table/', all, name='table'),
    path('delete/<int:id>/', delete, name='delete')
]