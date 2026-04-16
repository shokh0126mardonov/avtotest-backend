from rest_framework.viewsets import ModelViewSet

from .models import RoadSign,RoadSignFolder
from .serializers import RoadSignFolderSerializer,RoadSignSerializer


class RoadSignViewsets(ModelViewSet):
    queryset = RoadSign.objects.all()
    serializer_class = RoadSignSerializer


class RoadSignFolderViewsets(ModelViewSet):
    queryset = RoadSignFolder.objects.all()
    serializer_class = RoadSignFolderSerializer
