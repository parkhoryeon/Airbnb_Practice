from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied
from rest_framework.status import HTTP_202_ACCEPTED, HTTP_204_NO_CONTENT
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from reviews.serializers import ReviewSerializer
from .models import Amenity, Room
from categories.models import Category
from django.db import transaction


class Amenities(APIView):

    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            serializer = AmenitySerializer(amenity)
            return Response(serializer.data)
        else:
            return Response(serializer.errors) 


class AmenityDetail(APIView):

    def get_object(self, pk):
        try:
            amenity = Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound
        return amenity

    def get(self, request, pk):
        serializer = AmenitySerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = AmenitySerializer(self.get_object(pk), data=request.data, partial=True,)
        if serializer.is_valid():
            updated_amenity = serializer.save()
            serializer = AmenitySerializer(updated_amenity)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=HTTP_202_ACCEPTED)
        

class Rooms(APIView):
    
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_rooms, 
            many=True,
            context={
                "request": request,
            }
        )
        return Response(serializer.data)
    
    def post(self, request):
        
        # print( dir(request.user) )  
         
        # 요청한 사용자의 로그인 유무 확인.
        if request.user.is_authenticated:
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():
                # print("⭐ REQUEST.DATA : ", request.data)
                category_pk = request.data.get("category")
                if not category_pk:
                    raise ParseError("Category is required")
                try: 
                    category = Category.objects.get(pk=category_pk)
                    # 카테고리는 Room을 위한 것과 Experiences를 위한 카티고리 두 종류이끼 때문에
                    # Room을 위한 카테고리인지 체크를 해줘야 한다.
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be 'rooms'")
                except Category.DoesNotExist:
                    raise ParseError("Category not found")
                
                try:
                    # 트랜잭션 Start
                    with transaction.atomic():
                        # owner, category, amenity는 read_only 이며 수동으로 보내줘야 한다.
                        room = serializer.save(owner=request.user, category=category)    
                        amenities = request.data.get('amenities')
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)
                        serializer = RoomDetailSerializer(room)
                        return Response(serializer.data)
                # 트랜잭션 End
                except Exception:
                    raise ParseError("Amenity not found")
                
                # 트랜잭션을 사용하지 않을 경우,( ID 낭비 )
                """
                # owner, category, amenity는 read_only 이며 수동으로 보내줘야 한다.
                room = serializer.save(owner=request.user, category=category)
                amenities = request.data.get('amenities')
                for amenity_pk in amenities:
                    try:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                    except Amenity.DoesNotExist:
                        room.delete()
                        raise ParseError(f"Amenity with id { amenity_pk } not found")
                    room.amenities.add(amenity)
                serializer = RoomDetailSerializer(room)
                return Response(serializer.data)
                # """

            else:
                return Response(serializer.errors)
        else: 
            raise NotAuthenticated
            

class RoomDetail(APIView):

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(
            room,
            context={
                "request": request,
            }
        )
        return Response(serializer.data)
    
    def put(self, request, pk):
        room = self.get_object(pk)
        # 로그인 여부 확인
        if not request.user.is_authenticated:
            raise NotAuthenticated
        # 방을 생성한 사람과 request한 사용자가 일치 여부 확인
        if room.owner != request.user:
            raise PermissionDenied
        
        # Assignment
        serializer = RoomDetailSerializer(room, data=request.data, partial=True)
        if serializer.is_valid():
            # print("⭐ REQUEST.DATA : ", request.data)
            category_pk = request.data.get("category")

            if not category_pk:
                raise ParseError("Category is required")   
             
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("The catdegory kind should be 'rooms'")
            except Category.DoesNotExist:
                raise ParseError("Category not found")
             
            try:
                with transaction.atomic():
                    room = serializer.save(owner=request.user, category=category)

                    amenities = request.data.get('amenities')
                    if amenities:
                        for amenity_pk in amenities:
                            try:
                                amenity = Amenity.objects.get(pk=amenity_pk)
                            except Amenity.DoesNotExist:
                                raise ParseError(f"Amenity with id {amenity_pk} not found")
                        room.amenities.set(amenities)
                serializer = RoomDetailSerializer(room)
                return Response(serializer.data)
            except Exception:
                raise ParseError("Transaction Error")    
        else:
            return Response(serializer.errors)


    def delete(self, request, pk):
        room = self.get_object(pk)
        # 로그인 여부 확인
        if not request.user.is_authenticated:
            raise NotAuthenticated
        # 방을 생성한 사람과 request한 사용자가 일치 여부 확인
        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)

        
class RoomReviews(APIView):

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = ReviewSerializer(
            room.review_set.all(),
            many = True,
        )
        return Response(serializer.data)