
from django.contrib import admin
from django.urls import path

from .yasg import urlpatterns as swagger_url
from get_send_file.urls import urlpatterns as url_file


urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += swagger_url
urlpatterns += url_file
