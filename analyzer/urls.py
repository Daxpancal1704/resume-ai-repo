from django.urls import path
from .views import delete_history, upload_resume, history

urlpatterns = [
    path("", upload_resume, name="upload"),
    path("history/", history, name="history"),
    path("history/delete/<int:id>/", delete_history, name="delete_history"),
    

]
