from rest_framework import views, response, generics
from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from apps.users.serializers import InputRegisterUserSerializer, OutputRegisterUserSerializer, InputLoginUserSerializer, \
    InputChangePasswordSerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

User = get_user_model()

class TestView(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        print(request.user.username)
        print(request.auth)

        return response.Response("ok")

class RegisterUserView(views.APIView):

    def post(self, request):

        input_serializer = InputRegisterUserSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        print(input_serializer.data)
        u = User.objects.create(
            first_name=input_serializer.data['first_name'],
            last_name=input_serializer.data['last_name'],
            username=input_serializer.data['username'],
            email=input_serializer.data['email']
        )

        u.set_password(input_serializer.data['password'])
        u.save()

        output_serializer = OutputRegisterUserSerializer(u)

        return response.Response(output_serializer.data)

class LoginUserView(views.APIView):
    def post(self, request):
        input_serializer = InputLoginUserSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        if User.objects.filter(username=input_serializer.data['username']).exists():
            u = User.objects.get(username=input_serializer.data['username'])
            if u.check_password(input_serializer.data['password']):
                if Token.objects.filter(user=u).exists():
                    token = Token.objects.get(user=u)
                else:
                    token = Token.objects.create(user=u)
                print(token.key)
                return response.Response({'token': token.key})

        return response.Response({'error': 'Bad Credentials'}, status=400)

class LogoutUserView(views.APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.filter(key=request.auth).delete()
        return response.Response("ok")

class ChangePasswordView(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        input_serializer = InputChangePasswordSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        if request.user.check_password(input_serializer.data['old_password']):
            if input_serializer.data['new_password'] != input_serializer.data['confirm_new_password']:
                return response.Response({'confirm_new_password': 'confirmation failed'})
            else:
                request.user.set_password(input_serializer.data['new_password'])
                request.user.save()
                return response.Response("ok")
        else:
            return response.Response({'old_password': 'incorrect password'})
        return response.Response("ok")

class ProfileView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user