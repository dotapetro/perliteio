from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)
    tasks = serializers.HyperlinkedRelatedField(many=True, view_name='task-detail', read_only=True)
    solutions = serializers.HyperlinkedRelatedField(many=True, view_name='solution-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'base', 'tasks', 'solutions')
