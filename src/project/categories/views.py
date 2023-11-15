from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render
from .models import Category

from .serializers import CategorySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_202_ACCEPTED
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet


class CategoryViewSet(ModelViewSet):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()

# ############################################################################
"""
class Categories(APIView):
   
    def get(self, request):
        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            new_category = serializer.save()
            serializer = CategorySerializer(new_category)
            return Response(serializer.data)
        else:
            return Response(serializer.errors) 
        
    
class  CategoryDetail(APIView):

    def get_object(self, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound
        return category

    def get(self, request, pk):
        serializer = CategorySerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = CategorySerializer(self.get_object(pk), data=request.data, partial=True,)     
        if serializer.is_valid():
            updated_category = serializer.save()
            serializer = CategorySerializer(updated_category)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=HTTP_202_ACCEPTED)
"""
# ############################################################################
"""
@api_view([ "GET", "POST" ])
def categories(request):
    try:
        all_categories = Category.objects.all()
    except Category.DoesNotExist:
        raise NotFound
    
    if request.method == "GET":
        serializer = CategorySerializer(all_categories, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            new_category = serializer.save()
            serializer = CategorySerializer(new_category)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)    


@api_view([ "GET", "PUT", "DELETE" ])
def category(request, pk):
    
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        raise NotFound
    
    if request.method == "GET":
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer = CategorySerializer(category, data=request.data, partial=True,)     
        if serializer.is_valid():
            updated_category = serializer.save()
            serializer = CategorySerializer(updated_category)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    elif request.method == "DELETE":
        category.delete()
        return Response(status=HTTP_202_ACCEPTED)
"""