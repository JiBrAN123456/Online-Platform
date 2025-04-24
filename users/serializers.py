from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email', 'role', 'is_active', 'date_joined')



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)

    class Meta:
        model = User 
        fields = ('email','role','password')

    def create(self, validated_data):

        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            role=validated_data['role']
        )              
        return user
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self,data):
        email = data.get("email")
        password = data.get("password")


        if email and password:
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                return user
            raise serializers.ValidationError("Invalid credentials")
        raise serializers.ValidationError("Email and password are required")
    


class JWTTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only = True)
    

    class Meta:
        model = User
        fields = ("access_token","refresh_token")

    def create(self, validated_data):
        
        user = validated_data
        refresh = RefreshToken.for_user(user)
        
        return   { 
            'access_token' : str(refresh.access_token),
            "refresh_token" : str(refresh),
        }  