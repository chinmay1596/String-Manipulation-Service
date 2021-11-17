from django.contrib import admin
from .models import StringModel, OperationModel

admin.site.register(StringModel)
admin.site.register(OperationModel)
