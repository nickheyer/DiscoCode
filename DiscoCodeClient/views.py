from rest_framework import viewsets, permissions, mixins
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

import requests
import json

from DiscoCodeClient.utils import (
    update_state_sync
)


# ---------------- INDEX, ETC. ----------------

def index(request):
    update_state_sync({ 'host_url': request.get_host() })
    return render(request, "DiscoCodeClient/index.html")

def forward_runtime(request: HttpRequest):
    if request.method == 'GET':
        response = requests.get('https://emkc.org/api/v2/piston/runtimes')
        return JsonResponse(response.json(), safe=False)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def forward_execute(request):
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON format")
        
        response = requests.post('https://emkc.org/api/v2/piston/execute', json=request_data)
        return JsonResponse(response.json(), safe=False)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

# ---------------- REST API --------------------

from DiscoCodeClient import models, serializers


# Configuration / State limited to update (PUT)
class ConfigurationViewSet(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = serializers.ConfigurationSerializer
     
    def get_queryset(self):
        return models.Configuration.objects.filter(id=models.Configuration.objects.first().id)


class StateViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = serializers.StateSerializer

    def get_queryset(self):
        return models.State.objects.filter(id=models.State.objects.first().id)


class ErrLogViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    queryset = models.ErrLog.objects.all()
    serializer_class = serializers.ErrLogSerializer

class EventLogViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    queryset = models.EventLog.objects.all()
    serializer_class = serializers.EventLogSerializer

class DiscordServerViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    queryset = models.DiscordServer.objects.all()
    serializer_class = serializers.DiscordServerSerializer

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

class LangViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    queryset = models.Language.objects.all()
    serializer_class = serializers.LangSerializer