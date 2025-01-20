from rest_framework import status
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import *

User = get_user_model()


# Create your views here.
class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        data = self.request.data
        print(data)
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        company_name = data.get("company_name")
        email = data.get("email")
        phone_no = data.get("phone_no")
        password = data.get("password")
        password2 = data.get("password2")

        if password == password2:
            user = User.objects.filter(email=email).exists()
            if user:
                res = {
                    "created": False,
                    "mail_already_exist": True,
                    "active_user": User.objects.get(email=email).is_active,
                    "message": f"User with {email} email already exists!",
                }
                return Response(res)
            else:
                if len(password) < 5:
                    res = {"created": False, "message": "Password is too short!"}
                    return Response(res)

                user = User.objects.create_user(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    company_name=company_name,
                    phone_no=phone_no,
                    password=password,
                )

                user.is_active = True  # Set the user as active immediately
                user.save()

                res = {
                    "created": True,
                    "mail_already_exist": False,
                    "active_user": True,
                    "message": "Account created successfully!",
                }
                return Response(res)
        else:
            res = {"created": False, "message": "Passwords do not match!"}
            return Response(res)


# user view to get profile data
class UserView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=self.request.user.email)
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except UserAccount.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        try:
            user = UserAccount.objects.get(email=self.request.user.email)
            data = request.data

            # Handle optional fields
            phone_no = data.get("phone_no")
            city = data.get("city")
            country = data.get("country", "Pakistan")  # Default to "Pakistan"
            about = data.get("about")
            gender = data.get("gender")
            date_of_birth = data.get("date_of_birth")

            # Update user instance
            serializer = UserSerializer(user, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except UserAccount.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
