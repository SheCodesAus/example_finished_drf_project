from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from projects.models import Exam
from .serializers import CustomUserSerializer, CustomUserDetailSerializer
from projects.serializers import ExamResultSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from projects.permissions import IsCreatorOrReadOnly

class CustomUserList(APIView):

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class CustomUserDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsCreatorOrReadOnly
    ]
    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserDetailSerializer(user)
        return Response(serializer.data)
    
    def post(self, request, pk):
        student = self.get_object(pk)

        serializer = ExamResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(examinee=student)
            return Response(serializer.data)
        return Response(serializer.errors)
    

class CustomAuthToken(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        # add more user details to response as needed
        return Response({
            'token': token.key,
            'user_id': user.id,
            'email': user.email
        })