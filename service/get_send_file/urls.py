from django.urls import path
from .views import FileUploadView


urlpatterns = [
    path('upload_file/', FileUploadView.as_view(), name='file-upload'),
]