from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string

from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user) 

                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response({
                    "status": "success",
                    "data": {
                        "access": access_token,
                        "refresh": str(refresh)
                    }
                })

            return Response({
                "status": "fail",
                "message": "Invalid credentials"
            })

        return Response({
            "status": "fail",
            "message": "Validation errors occurred",
            "errors": serializer.errors
        })

@api_view(['POST'])
def register(request):
    data = request.data
    user_serializer = CreateAccountSerializer(data=data)

    if user_serializer.is_valid():
        if not User.objects.filter(email=data['email']).exists():
            user = User.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                username=data['email'],
                email=data['email'],
                password=make_password(data['password']),
            )
            response_serializer = UserSerializer(user)
            return Response({
                "status": "success",
                "data": response_serializer.data
            }, status= status.HTTP_201_CREATED)
        else:
            return Response({
                "status": "failed",
                "message": "Email address already exists"
            }, status= status.HTTP_302_FOUND)
    else:
        return Response({
            "status": "failed",
            "message": "Validation errors occurred",
            "errors": user_serializer.errors
            }, status= status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def currentUser(request):
    user = UserSerializer(request.user, many=False)
    return Response({
        "status": "success",
        "data": user.data
    })


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateCurrentUser(request):
    user = request.user
    user_data = request.data

    serializer = UserSerializer(user, data=user_data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": "success",
            "data": serializer.data
        })

    return Response({
        "status": "error",
        "message": "Failed to update user data",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updatePassword(request):
    user = request.user
    data = request.data

    required_fields = ['currentPassword', 'newPassword', 'confirmPassword']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return Response({
            "status": "error",
            "message": f"Missing fields: {', '.join(missing_fields)}"
        }, status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(data['currentPassword']):
        return Response({
            "status": "error",
            "message": "Current password is incorrect."
        }, status=status.HTTP_400_BAD_REQUEST)

    if data['newPassword'] != data['confirmPassword']:
        return Response({
            "status": "error",
            "message": "New password and confirm password do not match."
        }, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(data['newPassword'])
    user.save()

    return Response({
        "status": "success",
        "data": {
            "newPassword": data['newPassword'],
            "confirmPassword": data['confirmPassword'],
        }
    }, status=status.HTTP_200_OK)


def getCurrentHost(request):
    protocol = request.is_secure() and 'https' or 'http'
    host = request.get_host()
    return "{protocol}://{host}".format(protocol = protocol , host = host)



@api_view(['POST'])
def UserForgotPassword(request):
    data = request.data
    try:
        user = get_object_or_404(User, email=data['email'])
    
        otp = get_random_string(6, allowed_chars='0123456789')
        expire_date = timezone.now() + timedelta(minutes=2)
        
        user.profile.password_reset_otp = otp
        user.profile.password_reset_expire = expire_date
        user.profile.save()

        # host = getCurrentHost(request)
        # link = f'{host}/api/v1/resetPassword/{token}'
        body = f"Your Password Reset OTP is: {otp}. It is valid for 30 minutes."

        send_mail(
            "Password Reset From TASKY App",
            body,
            "tasky24@info.com",
            [data['email']]
        )

        return Response({
            "status": "success",
            "message": f"Password Reset OTP sent to {data['email']}"
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            "status": "failed",
            "message": f"your email: {data['email']} is invalid",
            "error" : f"{e}"
        }, status=status.HTTP_200_OK)



@api_view(['POST'])
def UserResetPassword(request):
    data = request.data

    user = get_object_or_404(User, profile__password_reset_otp=data.get('otp'))

    if user.profile.password_reset_expire < timezone.now():
        return Response({
            "status": "error",
            "message": "OTP is expired!"
        }, status=status.HTTP_400_BAD_REQUEST)

    if data['password'] != data['confirmPassword']:
        return Response({
            "status": "error",
            "message": "Passwords do not match!"
        }, status=status.HTTP_400_BAD_REQUEST)

    user.password = make_password(data['password'])
    user.profile.password_reset_otp = ""
    user.profile.password_reset_expire = None
    user.profile.save()
    user.save()

    return Response({
        "status": "success",
        "message": "Password has been successfully reset"
    }, status=status.HTTP_200_OK)
