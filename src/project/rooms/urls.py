from django.urls import path
from . import views
from django.conf import settings


urlpatterns = [
    path("", views.Rooms.as_view()),                            # Rooms 조회 / Room 생성
    path("<int:pk>", views.RoomDetail.as_view()),               # Room 상세 정보 조회 / Room 수정 / Room 삭제
    path("<int:pk>/reviews", views.RoomReviews.as_view()),      # Room의 reviews(페이징) / Room의 review 생성
    path("<int:pk>/amenities", views.RoomAmenities.as_view()),  # Room의 amenities(페이징) 
    path("<int:pk>/photos", views.RoomPhotos.as_view()),        # Room의 photo 생성
    path("<int:pk>/bookings", views.RoomBookings.as_view()),    # Room의 booking(예약) 조회 / Room의 booking(예약) 생성
    path('amenities/', views.Amenities.as_view()),              # Amenities 조회 / Amenity 생성
    path('amenities/<int:pk>', views.AmenityDetail.as_view()),  # Amenity 상세 정보 조회 / Amenity 수정 / Amenity 삭제
]