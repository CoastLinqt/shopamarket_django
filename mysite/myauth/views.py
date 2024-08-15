import json

from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import (
    SignUpSerializer,
    SignInSerializer,
    ProfileEditSerializer,
    ProfileImagesSerializer,
    ProfilePasswordSerializer,

)
from .models import Profile
from .utils import GetProfile
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import FormParser, MultiPartParser
from .openapi import (avatar,
                      password,
                      passwordReply,
                      passwordCurrent,
                      profile_schema_response,
                      profile_schema
                      )


class SignUpView(APIView):


    @swagger_auto_schema(request_body=SignUpSerializer, responses={201:  "successfully, you entered",
                                                                   404: 'ERRORS'})
    def post(self, request):

        # dict_string = list(request.data.keys())[0]
        # dict_new = json.loads(dict_string)

        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            username = request.data.get("username")
            password = request.data.get("password")

            user = authenticate(username=username, password=password)

            login(request, user)
            return Response(
                {"messages": "successfully, you entered"},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignOutView(APIView):
    @swagger_auto_schema(responses={200: "successfully"})
    def post(self, request):
        logout(request)
        return Response({"message": "successfully"}, status=status.HTTP_200_OK)


class SignInView(APIView):

    @swagger_auto_schema(request_body=SignInSerializer, responses={201: "successfully, you entered",
                                                                   404: "user not found",
                                                                   400: "ERRORS"})
    def post(self, request):

        dict_string = list(request.data.keys())[0]

        dict_new = json.loads(dict_string)

        serializer = SignInSerializer(data=dict_new)
        if serializer.is_valid():

            username = dict_new.get("username")
            password = dict_new.get("password")

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                return Response(
                    {"messages": "successfully, you entered"},
                    status=status.HTTP_201_CREATED,
                )

            return Response(
                {"messages": "user not found"}, status=status.HTTP_404_NOT_FOUND
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileEditView(APIView):
    @swagger_auto_schema(request_body=ProfileEditSerializer, responses={201: '',
                                                                        400: ''})
    def post(self, request):
        if request.user.is_authenticated:
            serializer = ProfileEditSerializer(
                data=request.data, instance=request.user.profile
            )
            if serializer.is_valid(raise_exception=True):

                serializer.save()

                return Response(
                    GetProfile(
                        object_name=Profile.objects.filter(user_id=request.user.pk).defer(
                            "src", "alt"
                        )
                    ),
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return  Response(status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(responses=profile_schema)
    def get(self, request):
        if request.user.is_authenticated:

            return Response(
                GetProfile(object_name=Profile.objects.filter(user_id=request.user.pk)),
                status=status.HTTP_200_OK,
            )
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ProfileAvatar(APIView):
    parser_classes = [FormParser, MultiPartParser,]

    @swagger_auto_schema(manual_parameters=[avatar,], responses={200: '',
                                                                 400: ''})
    def post(self, request):

        obj = Profile.objects.filter(user_id=request.user.pk)[0]

        obj.src = request.FILES["avatar"]
        obj.alt = request.FILES["avatar"]
        obj.save()

        serializer = ProfileImagesSerializer(
            data={"src": request.FILES["avatar"], "alt": f"{obj.alt}"},
            instance=request.user.profile,
        )

        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class ProfileEditPassword(APIView):

    @swagger_auto_schema(manual_parameters=[passwordCurrent, password, passwordReply],
                         responses=profile_schema_response)
    def post(self, request):
        user = User.objects.filter(pk=request.user.pk)[0]

        passwordCurrent = request.data['passwordCurrent']
        password = request.data['password']
        passwordReply = request.data['passwordReply']

        serializer = ProfilePasswordSerializer(data=request.data)

        if user.check_password(passwordCurrent) and (password == passwordReply):
            if serializer.is_valid():

                user.set_password(password)
                user.save()

                user = authenticate(username=request.user.username, password=password)
                login(request, user)

                return Response(
                    GetProfile(object_name=Profile.objects.filter(user_id=request.user.pk)),
                    status=status.HTTP_200_OK,
                )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "the password does not match"}, status=status.HTTP_400_BAD_REQUEST)

