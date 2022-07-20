from django.db import models
from django.forms import CharField
# Create your models here.


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Annotator(BaseModel):
    name=models.CharField(max_length=100)


class Frame(BaseModel):
    image = models.ImageField(upload_to="annotation/")
    annotated = models.BooleanField(default=False)
    # dataset = models.ForeignKey('AnnotationDataset', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.image.name}"




class Detector(BaseModel):
    # ANNOTATION_BY = (
    #     ('p', 'PERSON'),
    #     ('m', 'MODEL'),
    # )
    label_class = models.PositiveSmallIntegerField()
    x = models.DecimalField(max_digits=50, decimal_places=20)
    y = models.DecimalField(max_digits=50, decimal_places=20)
    w = models.DecimalField(max_digits=50, decimal_places=20)
    h = models.DecimalField(max_digits=50, decimal_places=20)
    # verified = models.BooleanField(default=False)
    #annotated_by = models.CharField(max_length=5, choices=ANNOTATION_BY, default=None)

    annotated_by = models.ForeignKey(Annotator, on_delete=models.SET_NULL, null=True, blank=True)
    frame_obj = models.ForeignKey(Frame, on_delete=models.CASCADE, related_name="detector_data")
    

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"X: {self.x}, Y: {self.y}, W: {self.w}, H: {self.h}"
    


