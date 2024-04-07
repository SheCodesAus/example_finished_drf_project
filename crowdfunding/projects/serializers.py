from rest_framework import serializers
from .models import Exam, ExamResult, TutorProject, TutorPledge


class TutorPledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorPledge
        fields = ['id', 'hours_pledged', 'comment', 'pledged_to', 'pledged_by']
        read_only_fields = ['id', 'pledged_by', 'pledged_to']

    def create(self, validated_data):
        return TutorPledge.objects.create(**validated_data)

class TutorProjectSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=200)
    created_by = serializers.ReadOnlyField(source='created_by.id')
    tutor_for = serializers.ReadOnlyField(source='tutor_for.id')
    description = serializers.CharField(max_length=None)
    image = serializers.URLField()
    required_grade = serializers.FloatField()
    required_tutoring_hours = serializers.IntegerField()
    is_open = serializers.BooleanField()
    created_date = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return TutorProject.objects.create(**validated_data)

class TutorProjectDetailSerializer(TutorProjectSerializer):
    pledges = TutorPledgeSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.required_grade = validated_data.get('required_grade', instance.required_grade)
        instance.required_tutoring_hours = validated_data.get('required_tutoring_hours', instance.required_tutoring_hours)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        instance.save()
        return instance
    
class ExamResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamResult
        fields = ['id', 'examinee', 'exam', 'score', 'date_recorded']
        read_only_fields = ['id', 'examinee', 'date_recorded']

    def create(self, validated_data):
        return ExamResult.objects.create(**validated_data)
    
class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'name', 'created_by', 'created_date']
        read_only_fields = ['id', 'created_by', 'created_date']

    def create(self, validated_data):
        return Exam.objects.create(**validated_data)