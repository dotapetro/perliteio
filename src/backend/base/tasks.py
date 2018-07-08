from celery import shared_task
from . import models
import json
import epicbox
import pprint

@shared_task
def check_solution(pk):
    solution_object = models.Solution.objects.get(pk=pk)
    print(solution_object.id, 'Code is:')
    print(solution_object.code)
    print('EXECUTING TASK')
    print('Task tests are:')
    tests = json.loads(solution_object.task.tests)
    print(tests)
    '''
    code = str.encode(solution_object.code)
    epicbox.configure(
        profiles=[
            epicbox.Profile('python', 'python:3.6.5-alpine')
        ]
    )
    files = [{'name': 'main.py', 'content': code}]
    limits = {'cputime': 1, 'memory': 64}

    result = epicbox.run('python', 'python3 main.py', stdin=list(tests.keys())[0], files=files, limits=limits)
    pprint.pprint(result)
    '''
