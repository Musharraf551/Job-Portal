from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, ApplyJobAPIView, MyApplicationsAPIView

router = DefaultRouter()
router.register(r'jobs', JobViewSet, basename='job')

urlpatterns = [
    path('', include(router.urls)),
    path('jobs/<int:job_id>/apply/', ApplyJobAPIView.as_view(), name='apply-job'),
    path('my-applications/', MyApplicationsAPIView.as_view(), name='my-applications'),
]
