from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Exam, ExamResult, TutorProject, TutorPledge
from .serializers import ExamSerializer, TutorProjectSerializer, TutorProjectDetailSerializer, TutorPledgeSerializer
from django.http import Http404
from rest_framework import status, permissions
from .permissions import ProjectDetailPerms, IsCreatorOrReadOnly, IsPledgerOrPledgeeOrReadOnly

class ExamList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        exams = Exam.objects.all()
        serializer = ExamSerializer(exams, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ExamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class ExamDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsCreatorOrReadOnly
    ]

    def get_object(self, pk):
        try:
            exam = Exam.objects.get(pk=pk)
            self.check_object_permissions(self.request, exam)
            return exam
        except Exam.DoesNotExist:
            raise Http404

    def post(self, request, pk):
        exam=self.get_object(pk=pk)
        serializer = TutorProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                created_by=request.user,
                tutor_for=exam
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class ProjectList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        projects = TutorProject.objects.all()
        serializer = TutorProjectSerializer(projects, many=True)
        return Response(serializer.data)

class ProjectDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        ProjectDetailPerms
    ]

    def get_object(self, pk):
        try:
            project = TutorProject.objects.get(pk=pk)
            self.check_object_permissions(self.request, project)
            return project
        except TutorProject.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = TutorProjectDetailSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = self.get_object(pk)
        data = request.data
        serializer = TutorProjectDetailSerializer(
            instance=project,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        
    def post(self, request, pk):
        project = self.get_object(pk)
        serializer = TutorPledgeSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save(
            pledged_to=project,
            pledged_by=request.user
        )

        return Response(serializer.data)       

class PledgeList(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def get(self, request):
        pledges = TutorPledge.objects.all()
        serializer=TutorPledgeSerializer(pledges, many=True)
        return Response(serializer.data)
    
class PledgeDetailView(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsPledgerOrPledgeeOrReadOnly
    ]

    def get_object(self, pk):
        try:
            project = TutorPledge.objects.get(pk=pk)
            self.check_object_permissions(self.request, project)
            return project
        except TutorPledge.DoesNotExist:
            raise Http404
        
    def delete(self, request, pk):
        pledge = self.get_object(pk)
        pledge.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class HelloWorld(APIView):
    def get(self, request):
        return Response({"hello": "world"})