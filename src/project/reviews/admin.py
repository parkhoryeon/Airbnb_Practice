from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    
    list_display = (
        "__str__",
        "payload",
    )
    list_filter = (
        "rating",
        "user__is_host",
        "room__category",
        "room__pet_friendly",
    )