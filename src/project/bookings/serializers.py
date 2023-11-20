from rest_framework import serializers
from .models import Booking
from django.utils import timezone


class CreateRoomBookingSerializer(serializers.ModelSerializer):
      
    check_in = serializers.DateField()
    check_out = serializers.DateField()

    """ 
    check_in 현재 시간보다 미래여야 한다. 
    """
    def validate_check_in(self, value):
        # print("⭐ VALUE : ", value)
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value
    
    """ 
    check_out 현재 시간보다 미래여야 한다. 
    """
    def validate_check_out(self, value):
        # print("⭐ VALUE : ", value)
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value
    
    """ 
    check_out은 check_in 날짜와 같거나 미래여야 한다.
    주어진 기간 동안에 해당하는 예약이 있는지 확인
    """
    def validate(self, data):
        if data['check_out'] <= data['check_in']:
            raise serializers.ValidationError("Check in should be smaller than check out")
        if Booking.objects.filter(
            check_in__lte=data["check_out"],
            check_out__gte=data["check_in"],
        ).exists():
            raise serializers.ValidationError("Those (or some) of those dates are already taken.")
        return data

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests", 
        )


class PublicBookingSerializer(serializers.ModelSerializer):
      
    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        ) 