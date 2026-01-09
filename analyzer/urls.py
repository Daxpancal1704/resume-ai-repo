from django.urls import path
from .views import upload_resume, history

urlpatterns = [
    path("", upload_resume, name="upload"),
    path("history/", history, name="history"),
]
