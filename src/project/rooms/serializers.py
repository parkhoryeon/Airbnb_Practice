from rest_framework import serializers
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer


class AmenitySerializer(serializers.ModelSerializer):       

    class Meta:
        model = Amenity
        fields = (
            "name",
            "description", 
        )


""" 많은 데이터를 포함하는 serializer """
class RoomDetailSerializer(serializers.ModelSerializer):

    owner = TinyUserSerializer()  # owner의 경우에는 TinyUserSerializer의 설정을 확인하여 보여줘라(보안적 요소)
    amenities = AmenitySerializer(many=True)
    category = CategorySerializer() 

    class Meta:
        model = Room
        fields = "__all__"
        # depth = 1 


""" 많은 데이터를 포함하지 않은 serializer """
class RoomListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = (
            "pk",  # ID 와 PK 는 동일하다.
            "name",
            "country",
            "city",
            "price"
        )
        # depth = 1  # 관계 확장