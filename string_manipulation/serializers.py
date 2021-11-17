from rest_framework import serializers
from .models import StringModel, OperationModel


class StringSerializer(serializers.ModelSerializer):
    class Meta:
        model = StringModel
        fields = ['id', 'string_name']


class StringOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationModel
        fields = ['string_id', 'operation_name', 'transformed_string']

    def create(self, validated_data):
        transformed_string = self.context.get('result')
        string_operation = OperationModel.objects.create(string_id=validated_data.get('string_id'),
                                                         operation_name=validated_data.get('operation_name'),
                                                         transformed_string=transformed_string)
        return string_operation


class AllStringOperationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationModel
        fields = ['operation_name', 'transformed_string']
