from django.db import models


# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class StringModel(BaseModel):
    string_name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.string_name


class OperationModel(BaseModel):
    string_id = models.ForeignKey(StringModel, on_delete=models.CASCADE)
    operation_name = models.CharField(max_length=200, null=True)
    transformed_string = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f'{self.operation_name}->{self.transformed_string}'
