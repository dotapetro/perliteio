from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework import renderers, viewsets
from .models import Task, Solution
from .serializers import TaskSerializer, SolutionSerializer
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly, IsOwnerOrStaff


class TasksViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        task = get_object_or_404(queryset, pk=kwargs['pk'])
        if request.user.username != task.owner.username:
            task.tests = "{}"

        serializer = self.get_serializer(task, context={'request': request})
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            for i in range(len(page)):
                page[i].tests = "{}"
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer()(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class SolutionsViewSet(viewsets.ModelViewSet):
    queryset = Solution.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrStaff)
    serializer_class = SolutionSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super(SolutionsViewSet, self).list(request, *args, **kwargs)

        if request.user:
            return HttpResponseRedirect(reverse('solution-my-solutions'))

        return Response({'details': 'You need to login first.'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['GET', 'POST'])
    def my_solutions(self, request, *args, **kwargs):
        if request.method == 'GET':
            queryset = Solution.objects.filter(owner__username=request.user.username)
            serializer = SolutionSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)
        elif request.method == 'POST':
            return self.create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        return Response({'details': 'Solutions can not be updated.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # Commented out for testing purposes
    # def destroy(self, request, *args, **kwargs):
        # return Response({'details': 'Don`t worry we use cron for that purpose :)'},
        #               status=status.HTTP_405_METHOD_NOT_ALLOWED)





