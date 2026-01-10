from django.urls import path
from .views import delete_history, upload_resume, history, result

urlpatterns = [
    path("", upload_resume, name="upload"),
    path("history/", history, name="history"),
    path("history/delete/<int:id>/", delete_history, name="delete_history"),
     path("result/<int:id>/", result, name="result"),

]
