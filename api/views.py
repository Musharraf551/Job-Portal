from rest_framework import viewsets, permissions, status, generics,filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import JobSerializer, ApplicationSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    
class ApplyJobAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, job_id):
        job = get_object_or_404(Job, id = job_id)

        if Application.objects.filter(user = request.user, job = job).exists():
            return Response({"detail": "you have already applied for this job."}, status= status.HTTP_400_BAD_REQUEST)
        
        data = request.data.copy()
        data['user'] = request.user.id
        data['job'] = job.id
        
        serializer = ApplicationSerializer(data = data)
        if serializer.is_valid():
            serializer.save(user = request.user, job = job)
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MyApplicationsAPIView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [filters.SearchFilter]
    search_fields = ['job__title', 'job__company', 'job__location']        
    
    def get_queryset(self):
        return Application.objects.filter(user = self.request.user).order_by('-applied_at')    