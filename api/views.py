from ast import Return
from functools import partial
from rest_framework import status
from django.shortcuts import render
from rest_framework.response import Response
from api.models import Detector, Frame
from rest_framework.viewsets import ModelViewSet

from rest_framework.decorators import action
from .serializers import (
    FrameSerializer,
    DetectorSerializer,
)
class DetectorViewSet(ModelViewSet): 
    
        # permission_classes = (GenericObjectPermissions,)
    queryset = Detector.objects.all()
    serializer_class = DetectorSerializer
    

    perms_map = {
        'GET': ['annotation.view_detector'],
        'POST': ['annotation.add_detector'],
        'PATCH': ['annotation.change_detector'],
        'PUT': ['annotation.change_detector'],
        'DELETE': ['annotation.delete_detector'],
    }

    
    def perform_create(self, serializer):
        #serializer.save(annotated_by=self.request.user.administration.annotated_by)
        serializer.save()
        

    def perform_update(self, serializer):
        #serializer.save(annotated_by=self.request.user.administration.annotated_by)
        serializer.save()
        
    
    """


    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    def perform_destroy(self,serializer):
        self.data['objs'] = [serializer.annotation]
        serializer.delete()


    def retrieve(self, request, pk=None):
        id=pk
        if id is not None:
            queryset = Detector.objects.get(id=id)
            serializer = DetectorSerializer(queryset)
            return Response(serializer.data)

    def create(self,request):
        serializer = DetectorSerializer(data=request.data)
        if serializer.is_valid():
            # 
            serializer.save()
            return Response({'msg':'Annotation created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def update(self,request,pk):
        id = pk
        queryset = Detector.objects.get(pk=id)
        serializer = DetectorSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Update'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk):
        id = pk
        queryset = Detector.objects.get(pk=id)
        serializer = DetectorSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Partial Data Update'})
        return Response(serializer.errors)
        ====================================================================================
        """

class FrameViewSet(ModelViewSet):
    serializer_class = FrameSerializer
    # permission_classes = (GenericObjectPermissions,)
    perms_map = {
        'GET': ['annotation.view_frame'],
        'POST': ['annotation.add_frame'],
        'PATCH': ['annotation.change_frame'],
        'PUT': ['annotation.change_frame'],
        'DELETE': ['annotation.delete_frame'],
    }

    def paginate_queryset(self, queryset):
        if self.request.query_params.get('no_page'):
            return None
        return super().paginate_queryset(queryset)

    def get_queryset(self):
        dataset_id = self.request.GET.get("dataset")
        queryset = Frame.objects.all()
        if dataset_id:
            queryset = queryset.filter(dataset_id=dataset_id)
        return queryset

    @action(
        methods=['PATCH'], detail=True
    )
    def update_frame(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.dataset.model_type == "d":
            instance.detector_data.filter().delete()
            for data in self.request.data.get("detector_data"):
                Detector.objects.create(**data, frame_obj=instance)
        return Response(self.serializer_class(instance).data)


    @action(
        methods=['POST'], detail=False
    )
    def update_frames(self, request, *args, **kwargs):
        frame_list = []
        frames = self.request.data.get("frames", [])
        for data in frames:
            instance = Frame.objects.get(pk=data["frame"])
            frame_list.append(data["frame"])
            if instance.dataset.model_type == "d":
                instance.detector_data.filter().delete()
                for d_data in data["detector_data"]:
                    Detector.objects.create(**d_data, frame_obj=instance)
            

            # elif instance.sourcedata.model_id== "so":
            #     instance.source_data.filter().delete()
            #     for label in self.request.data.get("source_data"):
            #         Sourcedata.objects.create(model_id=id, frame_obj=instance)
            
            if instance.detector_data.exists():

                instance.annotated = True
            else:
                instance.annotated = False
            instance.save()

        return Response(self.serializer_class(Frame.objects.filter(id__in=frame_list), many=True).data)


    

















        





