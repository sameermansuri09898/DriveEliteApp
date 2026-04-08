from rest_framework import serializers
from Account.models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    image = serializers.ImageField(required=False, allow_null=True) 

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password','confirm_password', 'phone_number', 'address','image','role']
        extra_kwargs = {    
            'password': {'write_only': True},
            'confirm_password': {'write_only': True},
            'image': {'required': False, 'allow_null': True}, 
        } 

    def validate(self, data):
     password = data.get('password')
     confirm_password = data.get('confirm_password')

     if password != confirm_password:
        raise serializers.ValidationError("Passwords do not match")

     return data
    
    def validate_phone_number(self, value):
        if not value.isdigit() or len(value) != 10:
          if CustomUser.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number already exists")
          raise serializers.ValidationError("Phone number must be 10 digits")
        return value  

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_image(self, value):
        if value is not None:
            if not value.name.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                raise serializers.ValidationError("Image must be a valid image file")
        return value  

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return value  

    def create(self, validated_data):
     validated_data.pop("confirm_password")
     user = CustomUser.objects.create_user(**validated_data)
     user.set_password(validated_data["password"])
     user.save()  
     return user  


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password']