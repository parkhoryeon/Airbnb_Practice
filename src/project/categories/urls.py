from django.urls import path
from . import views


urlpatterns = [
    path('', views.CategoryViewSet.as_view(          # Categories 조회 / Category 생성
        {
            'get': 'list',
            'post': 'create',
        }
    )),
    path('<int:pk>', views.CategoryViewSet.as_view(  # Category 조회/수정/삭제
        {
            'get': 'retrieve',
            'put': 'partial_update',
            'delete': 'destroy',
        }
    )),

    # path('', views.Categories.as_view()),
    # path('<int:pk>', views.CategoryDetail.as_view()),
    
    # path('', views.categories),
    # path('<int:pk>', views.category),
]