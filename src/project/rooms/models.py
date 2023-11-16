from django.db import models
from common.models import CommonModel


class Room(CommonModel):

    """ Model Definition for rooms """

    class RoomKindChoices(models.TextChoices):
        ENTIRE_PRICE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = ("shared_room", "Shared Room")

    name = models.CharField(max_length=180, default="",)
    country = models.CharField(max_length=50, default="한국")
    city = models.CharField(max_length=80, default="서울")
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=250)
    pet_friendly = models.BooleanField(default=True)
    kind = models.CharField(max_length=20, choices=RoomKindChoices.choices)
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)
    amenities = models.ManyToManyField("rooms.Amenity")
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.name   
    
    def total_amenities(room):
        return room.amenities.count() 
    
    def rating(room):
        count = room.review_set.count()
        if count == 0:
            return "No Reviews"  # "0"
        else:
            total_rating = 0
            for review in room.review_set.all().values("rating"):
                total_rating += review["rating"]
            return round(total_rating / count, 2) 


class Amenity(CommonModel):

    """ Amenity Definition """

    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Amenities"