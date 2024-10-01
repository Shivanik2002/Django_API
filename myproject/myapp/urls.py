from django.contrib import admin
from django.urls import path,include
from .views import *



urlpatterns = [
    path('student/',StudentAPI.as_view()),
    path('register/',RegisterUser.as_view()),
    # path('api-token-auth/', views.obtain_auth_token),
    # path('',home),
    # path('student/',post_student),
    # path('update_student/<id>/',update_student),
    # path('delete_student/<id>/',delete_student),
    path('get_book/',get_book),
    path('generic/',StudentGeneric.as_view()),
    path('GenericUpdate/<id>/',GenericUpdate.as_view()),
    path('generate_pdf/',GeneratePdf.as_view()),
    path('excel/',ExportImportExcel.as_view()),
]
