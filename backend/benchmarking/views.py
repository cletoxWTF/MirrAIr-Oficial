from rest_framework import generics
from .models import Traduction
from .serializers import TraductionSerializer

class TraductionList(generics.ListCreateAPIView):
    queryset = Traduction.objects.all()
    serializer_class = TraductionSerializer

class TraductionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Traduction.objects.all()
    serializer_class = TraductionSerializer