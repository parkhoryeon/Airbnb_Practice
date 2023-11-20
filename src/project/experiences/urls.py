from django.urls import path
from . import views


urlpatterns = [
    path("perks/", views.Perks.as_view()),               # Perks 조회 / Perk 생성
    path("perks/<int:id>", views.PerkDetail.as_view()),  # Perk 상세 조회/수정/삭제
]