from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password']

    def create(self, validated_data):
        user = User.objects.create(username = validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user    

class Studentserializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        # fields = ['name','age']
        # exclude = ['id']
        fields = '__all__'

    def validate(self, data):
        if data['age'] < 18:
            raise serializers.ValidationError({'error':"age cannot be less than 18"})
        
        if data['name']:
            for n in data['name']:
                if n.isdigit():
                    raise serializers.ValidationError({'error':"Name cannot be numeric or special Symbols"})
        return data
    

class Categoryserializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # fields = '__all__'    
        fields = ['category_name',]


class Bookserializer(serializers.ModelSerializer):
    category = Categoryserializer()
    class Meta:
        model = Book
        fields = '__all__'            