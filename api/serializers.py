
from rest_framework import serializers

from .models import (
    Detector,
    Frame,
)

class DetectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detector
        fields = "__all__"
        read_only_fields = ("created", "updated")

# class DataSourceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DataSource
#         fields = "__all__"
#         read_only_fields = ("created", "updated")

    # def to_representation(self, instance):

    #     # self.fields['label_class'] = LabelSerializer(read_only=True)
    #     return super(self.__class__, self).to_representation(instance)

class FrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frame
        fields = "__all__"
        read_only_fields = ("created", "updated")

    def to_representation(self, instance):
        #self.fields['dataset'] = AnnotationDatasetSerializer(read_only=True)
        self.fields['detector_data'] = DetectorSerializer(read_only=True, many=True)
        self.fields['image'] = FrameSerializer(read_only=True)
        #self.fields['data_source'] = DataSourceSerializer(read_only=True, many=True)
        # self.fields['annotated_frame'] = AnnotatedFrameSerializer(read_only=True, many=True)

        return super(self.__class__, self).to_representation(instance)

