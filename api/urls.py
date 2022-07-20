from django.urls import path, include
from rest_framework.routers import SimpleRouter
from api import views


from .views import (
    DetectorViewSet,
    FrameViewSet,
)

router = SimpleRouter()
router.register(r'detector', DetectorViewSet, basename='annotation_detector')
router.register(r'frame', FrameViewSet, basename='annotation_frame')

urlpatterns = [
    
    path('', include(router.urls)),
]