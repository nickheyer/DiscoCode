from rest_framework import serializers
from .models import Configuration, State, ErrLog, EventLog, DiscordServer, User, Language

class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = '__all__'

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

class ErrLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrLog
        fields = '__all__'

class EventLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventLog
        fields = '__all__'

class DiscordServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscordServer
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class LangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'
