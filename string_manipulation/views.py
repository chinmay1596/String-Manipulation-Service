from rest_framework import generics, status
from .serializers import StringSerializer, StringOperationSerializer, AllStringOperationsSerializer
from .models import StringModel, OperationModel
from rest_framework.response import Response


class StringAPI(generics.ListCreateAPIView):
    queryset = StringModel.objects.all()
    serializer_class = StringSerializer

    def list(self, request, *args, **kwargs):
        """
        API which returns a list of all the strings added to the DB and their IDs.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            queryset = StringModel.objects.all()
            serializer = self.serializer_class(queryset, many=True)
            return Response({'message': 'Data fetch Successfully.', 'data': serializer.data},
                            status=status.HTTP_200_OK)
        except:
            return Response({'message': 'No Data Found', 'data': []}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        API which accepts a string and stores it in the DB and returns an ID corresponding to it.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            params = request.data
            serializer = self.serializer_class(data=params)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = {'id': serializer.data['id']}
            return Response({'message': 'String Saved Successfully', 'success': True, 'data': data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': 'Oops! Something is wrong. Please retry again after sometime', 'success': False,
                             'error': e.args[0]},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StringOperationsAPI(generics.ListCreateAPIView):
    queryset = OperationModel.objects.all()
    serializer_class = StringOperationSerializer

    def get_string_object(self, params):
        try:
            obj = StringModel.objects.get(id=params['string_id'])
            return obj
        except StringModel.DoesNotExist:
            return None

    def reverse_string(self, params):
        string_obj = self.get_string_object(params)
        string = string_obj.string_name
        return string[::-1]

    def reverse_word(self, params):
        string_obj = self.get_string_object(params)
        string = string_obj.string_name
        split_string = string.split()
        split_string.reverse()
        res = ' '.join(split_string)
        return res

    def flip_string(self, params):
        string_obj = self.get_string_object(params)
        string = string_obj.string_name
        string_len = len(string) // 2
        first = string[0:string_len]
        second = string[string_len:]
        res = second + first
        return res

    def sort_string(self, params):
        string_obj = self.get_string_object(params)
        string = string_obj.string_name
        string = list(string)
        res = ''.join(string)
        return res

    def create(self, request, *args, **kwargs):
        """
        API which accepts an operation name and an ID of the string, performs the operation on the string, stores the transformed string in the DB and returns its ID.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        result = None
        try:
            params = request.data
            possible_operations = ['reverse', 'reverse_word', 'flip', 'sort']
            if params['operation_name'] not in possible_operations:
                return Response({'message': 'Please Select a Valid Possible operations',
                                 'possible_operations': possible_operations}, status=status.HTTP_400_BAD_REQUEST)
            if params['operation_name'] == 'reverse':
                string_reverse = self.reverse_string(params)
                result = string_reverse
            elif params['operation_name'] == 'reverse_word':
                result = self.reverse_word(params)
            elif params['operation_name'] == 'flip':
                result = self.flip_string(params)
            elif params['operation_name'] == 'sort':
                result = self.sort_string(params)
            serializer = self.serializer_class(data=params, context={'result': result})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = {'string_id': serializer.data['string_id']}
            return Response(
                {'message': 'String Transformed successfully', 'success': True, 'data': data},
                status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': 'Oops! Something is wrong. Please retry again after sometime', 'success': False,
                             'error': e.args[0]},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        """
        API which accepts an ID of the string and returns a list of all the operations performed on it and the corresponding transformed strings.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            params = request.data
            queryset = OperationModel.objects.filter(string_id=params['string_id'])
            serializer = AllStringOperationsSerializer(queryset, many=True)
            if queryset:
                return Response({'message': 'Data fetch Successfully.', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No Data Found', 'data': []}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Oops! Something is wrong. Please retry again after sometime', 'success': False,
                             'error': e.args[0]},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
