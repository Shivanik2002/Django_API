from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .helpers import *
import datetime 

# Create your views here.
print("_____________________________________________>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

# class GeneratePdf(APIView):
#     def get(self,request):
#         Student_objs = Student.objects.all()
#         params = {
#             'today' : datetime.date.today(),
#             'student_objs' : Student_objs,
#         }
#         file_name , status = save_pdf(params)
#         if not status:
#             return Response({'status':400})

#         return Response({"status":200 , 'path':f'/media/{file_name}.pdf'})
        

class GeneratePdf(APIView):
    def get(self, request):
        try:
            student_objs = Student.objects.all()
            
            params = {
                'today': datetime.date.today(),
                'student_objs': student_objs
            }
            
            # Generate the PDF
            file_name, status = save_pdf(params)
            
            if not status:
                print("PDF generation failed")
                return Response({'status': 400, 'error': 'PDF generation failed'})
            
            return Response({"status": 200, 'path': f'/static/{file_name}.pdf'})
        except Exception as e:
            print("Exception in GeneratePdf view:", e)
            return Response({'status': 500, 'error': 'Internal Server Error'})        

print("_____________________________________________>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

from rest_framework import generics

class StudentGeneric(generics.ListAPIView,generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = Studentserializer

class GenericUpdate(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = Studentserializer
    lookup_field = 'id'




@api_view(['GET'])
def get_book(request):
    book_objs = Book.objects.all()
    serializer = Bookserializer(book_objs, many=True)
    return Response({'status':200 , 'payload':serializer.data})

print("_____________________________________________>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

from rest_framework_simplejwt.tokens import RefreshToken

class RegisterUser(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            # print(serializer.errors)
            return Response({'state':403,'errors':serializer.errors, 'message':'Something went wrong'})
        
        serializer.save()

        user = User.objects.get(username = serializer.data['username'])
        refresh = RefreshToken.for_user(user)

        return Response({'status':200 ,
        'payload':serializer.data ,  
        'refresh': str(refresh),
        'access': str(refresh.access_token), 'message': 'your data is saved !!'})


print("_____________________________________________>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class StudentAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self,request):
        student_objs  = Student.objects.all()
        serializer = Studentserializer(student_objs,many=True)
        print(request.user)
        return Response({'status':200,'payload': serializer.data})

    def post(self,request):
        data = request.data
        print("--------------------------------->>>>>>>",data)
        serializer = Studentserializer(data=request.data)
        if not serializer.is_valid():
                print(serializer.errors)
                return Response({'state':403,'errors':serializer.errors, 'message':'Something went wrong'})
        
        serializer.save()
        return Response({'status':200 , 'payload':serializer.data , 'message': 'your data is saved !!'})


    def put(self,request):
        try:
            student_objs = Student.objects.get(id=request.data['id'])

            serializer = Studentserializer(student_objs , data=request.data)
            if not serializer.is_valid():
                print(serializer.errors)
                return Response({'state':403,'errors':serializer.errors, 'message':'Something went wrong'})
            
            serializer.save()
            return Response({'status':200 , 'payload':serializer.data , 'message': 'your data is saved !!'})
    
        except Exception as e:
            return Response({'status':403 , 'message':'invalid id'})

    def patch(self,request):
        try:
            student_objs = Student.objects.get(id=request.data['id'])

            serializer = Studentserializer(student_objs , data=request.data , partial=True)
            if not serializer.is_valid():
                print(serializer.errors)
                return Response({'state':403,'errors':serializer.errors, 'message':'Something went wrong'})
            
            serializer.save()
            return Response({'status':200 , 'payload':serializer.data , 'message': 'your data is saved !!'})
        
        except Exception as e:
            return Response({'status':403 , 'message':'invalid id'})
        
    def delete(self,request):
        try:
            Student_obj = Student.objects.get(id=request.data['id'])
            Student_obj.delete()
            return Response({'status':200 , 'message':'deleted'})
        except Exception as e:
            print(e)
            return(Response({'status':403 , 'message':'invalid id'}))



print("_____________________________________________>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

import uuid
import os
import pandas as pd
from django.conf import settings

class ExportImportExcel(APIView):
    def get(self,request):
        Student_objs = Student.objects.all()
        serializer = Studentserializer(Student_objs,many=True)
        df = pd.DataFrame(serializer.data)
        print(df)
        df.to_csv(f"public/static/excel/{uuid.uuid4}.csv",encoding = "UTF-8")
        return Response({'status' : 200})


# class ExportImportExcel(APIView):
#     def get(self, request):
#         try:
#             student_objs = Student.objects.all()
#             data = [{"id": obj.id, "name": obj.name, "age": obj.age, "father_name": obj.father_name} for obj in student_objs]
#             df = pd.DataFrame(data)
            
#             directory = os.path.join(settings.BASE_DIR, 'public', 'static', 'excel')
#             os.makedirs(directory, exist_ok=True)
            
#             file_name = str(uuid.uuid4())
#             file_path = os.path.join(directory, f'{file_name}.csv')
            
#             df.to_csv(file_path, encoding="UTF-8")
            
#             return Response({"status": 200, 'path': f'/static/excel/{file_name}.csv'})
#         except Exception as e:
#             print("Exception in GenerateCsv view:", e)
            # return Response({'status': 500, 'error': 'Internal Server Error'})


# @api_view(['GET'])
# def home(request):
#     student_objs  = Student.objects.all()
#     serializer = Studentserializer(student_objs,many=True)

#     return Response({'status':200,'payload': serializer.data})


# @api_view(['POST'])
# def post_student(request):
#     data = request.data
#     print("--------------------------------->>>>>>>",data)
#     serializer = Studentserializer(data=request.data)
#     if not serializer.is_valid():
#             print(serializer.errors)
#             return Response({'state':403,'errors':serializer.errors, 'message':'Something went wrong'})
    
#     serializer.save()
#     return Response({'status':200 , 'payload':serializer.data , 'message': 'your data is saved !!'})

# @api_view(['PUT'])
# def update_student(request,id):
#     try:
#         student_objs = Student.objects.get(id=id)

#         serializer = Studentserializer(student_objs , data=request.data , partial=True)
#         if not serializer.is_valid():
#             print(serializer.errors)
#             return Response({'state':403,'errors':serializer.errors, 'message':'Something went wrong'})
        
#         serializer.save()
#         return Response({'status':200 , 'payload':serializer.data , 'message': 'your data is saved !!'})
    
#     except Exception as e:
#         return Response({'status':403 , 'message':'invalid id'})

# @api_view(['DELETE'])
# def delete_student(request,id):
#     try:
#         Student_obj = Student.objects.get(id=id)
#         Student_obj.delete()
#         return Response({'status':200 , 'message':'deleted'})
#     except Exception as e:
#         print(e)
#         return(Response({'status':403 , 'message':'invalid id'}))

     