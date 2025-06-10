from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Traduction
from .serializers import TraductionSerializer


class TraductionViewSet(viewsets.ModelViewSet):
    queryset = Traduction.objects.all()
    serializer_class = TraductionSerializer

# class TraductionList(generics.ListCreateAPIView):
#     queryset = Traduction.objects.all()
#     serializer_class = TraductionSerializer

# class TraductionDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Traduction.objects.all()
#     serializer_class = TraductionSerializer