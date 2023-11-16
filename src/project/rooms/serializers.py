from rest_framework import serializers
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from reviews.serializers import ReviewSerializer


class AmenitySerializer(serializers.ModelSerializer):       

    class Meta:
        model = Amenity
        fields = (
            "name",
            "description", 
        )


""" 많은 데이터를 포함하는 serializer """
class RoomDetailSerializer(serializers.ModelSerializer):

    # 'read_only = True'이기 때문에 validation이 통과가 되기 때문에
    # 수동으로 validation을 해줘야 한다.
    
    owner = TinyUserSerializer(read_only=True)  # owner의 경우에는 TinyUserSerializer의 설정을 확인하여 보여줘라(보안적 요소)
    amenities = AmenitySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True) 
    # review_set = ReviewSerializer(read_only=True, many=True) # 수만개의 리뷰를 가질 수 있기 때문에 좋은 생각이 아니다. 

    # serializer에 필드를 추가.
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, room):
        # print('⭐ SELF.CONTEXT : ', self.context)
        request = self.context['request']
        return room.owner == request.user

    def get_rating(self, room):
        return room.rating()

    class Meta:
        model = Room
        fields = "__all__"
        # depth = 1 

    """ 테스트를 위해 생성시키지 않게 하기위해. """
    # def create(self, validated_data):
    #     print("⭐ VALIDATED_DATA : ", validated_data)
    #     return

    # def update(self, instance, validated_data):
    #     print("⭐ INSTANCE : ", instance)
    #     print("⭐ VALIDATED_DATA : ", validated_data)
    #     return


""" 많은 데이터를 포함하지 않은 serializer """
class RoomListSerializer(serializers.ModelSerializer):

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, room):
        # print('⭐ SELF.CONTEXT : ', self.context)
        request = self.context['request']
        return room.owner == request.user


    def get_rating(self, room):
        return room.rating()

    class Meta:
        model = Room
        fields = (
            "pk",  # ID 와 PK 는 동일하다.
            "name",
            "country",
            "city",
            "price",
            "rating",  # 메서드를 추가하면 표시할 필드에도 추가해줘야 한다.
            "is_owner",
        )
        # depth = 1  # 관계 확장