import logging

from rest_framework import status, mixins, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from logs.log_service import events_by_date, resources_by_date, event_executions
from .models import Log
from .serializers import LogSerializer

logger = logging.getLogger(__name__)


class LogList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Log.objects.all()
    serializer_class = LogSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request):
        name = self.request.FILES['file'].name
        path = 'log_cache/' + name
        save_file(self.request.FILES['file'], path)
        log = Log.objects.create(name=name, path=path)
        serializer = LogSerializer(log)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_log_stats(request, pk, stat):
    """Get log statistics

    End URL with
    * events for event_by_date
    * resources for resources_by_date
    * executions for event_executions
    """
    try:
        log = Log.objects.get(pk=pk)
    except Log.DoesNotExist:
        return Response({'error': 'not in database'}, status=status.HTTP_404_NOT_FOUND)
    try:
        log_file = log.get_file()
    except FileNotFoundError:
        logger.error("Log id: %s, path %s not found", log.id, log.path)
        return Response({'error': 'log file not found'}, status=status.HTTP_404_NOT_FOUND)

    if stat == 'events':
        data = events_by_date(log_file)
    elif stat == 'resources':
        data = resources_by_date(log_file)
    else:
        data = event_executions(log_file)
    return Response(data)


def save_file(file, path):
    logger.info("Saving uploaded file to %s ", path)
    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)