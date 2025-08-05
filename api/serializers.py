from rest_framework import serializers
from .models import Job, Application
from django.contrib.auth.models import User

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # display username
    job = serializers.ReadOnlyField(source='job.title')       # show job title

    class Meta:
        model = Application
        fields = ['id', 'user', 'job', 'cover_letter', 'resume', 'applied_at']
        read_only_fields = ['id', 'applied_at']
