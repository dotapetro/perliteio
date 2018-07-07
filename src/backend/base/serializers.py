from rest_framework import serializers
from .models import Task, Solution


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = ('url', 'id', 'title', 'description', 'tests', 'public_tests', 'restrictions', 'owner')


class SolutionSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    task = serializers.HyperlinkedRelatedField(many=False, view_name='task-detail', queryset=Task.objects.all())
    status = serializers.HiddenField(default=None)

    class Meta:
        model = Solution
        fields = ('url', 'id', 'created', 'code', 'status', 'task', 'owner')



