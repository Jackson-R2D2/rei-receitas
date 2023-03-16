from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializer import SerializerRevenue


'''@api_view(['GET'])
def get_user(request, pk):
    user = get_user_model().objects.get(id = pk)
    serializer = SerializerRevenue(user, many=False)
    return Response(serializer.data)'''


class ViewUser(APIView):

    def get(self, request, pk, format=None):
        user = get_user_model().objects.get(id = pk)
        serializer = SerializerRevenue(user, many=False)
        return Response(serializer.data)