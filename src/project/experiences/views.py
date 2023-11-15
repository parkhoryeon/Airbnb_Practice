from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_202_ACCEPTED
from .serializers import PerkSerializer
from .models import Perk


class Perks(APIView):

    def get(self, request):
        all_perks = Perk.objects.all()
        serializer = PerkSerializer(all_perks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            serializer = PerkSerializer(perk)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):

    def get_object(self, pk):
        try:
            perk = Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound
        return perk

    def get(self, request, pk):
        serializer = PerkSerializer(self.get_object(pk)) 
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = PerkSerializer(self.get_object(pk), data=request.data, partial=True)
        if serializer.is_valid():
            updated_perk = serializer.save()
            serializer = PerkSerializer(updated_perk)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=HTTP_202_ACCEPTED)
