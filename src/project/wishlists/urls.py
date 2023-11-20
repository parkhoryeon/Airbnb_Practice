from django.urls import path
from . import views


urlpatterns = [
    path("", views.Wishlists.as_view()),                                   # Wishlists 조회 / Wishlist 생성
    path("<int:pk>", views.WishlistDetail.as_view()),                      # Wishlist 조회 / 수정 / 삭제
    path("<int:pk>/rooms/<int:room_pk>", views.WishlistToggle.as_view()),  # Wishlist.rooms 추가/제거 (toggle)
] 