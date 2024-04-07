from rest_framework import serializers
from .models import CustomUser
from projects.serializers import ExamResultSerializer, ExamSerializer, TutorPledgeSerializer, TutorProjectSerializer

class CustomUserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
    
class CustomUserDetailSerializer(CustomUserSerializer):
    owned_exams = ExamSerializer(many=True, read_only=True)
    studied_exams=ExamSerializer(many=True, read_only=True)
    exam_results = ExamResultSerializer(many=True, read_only=True)
    owned_projects = TutorProjectSerializer(many=True, read_only=True)
    supporter_pledges = TutorPledgeSerializer(many=True, read_only=True)
