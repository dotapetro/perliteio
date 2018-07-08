from rest_framework.test import APIRequestFactory, APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Solution
from django.urls import reverse
from rest_framework import status
# Create your tests here.


class TasksTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        admin = User.objects.create_user(username="administrator", email="admin@test.com",
                                         password="secret")
        admin.is_staff = True
        admin.save()
        user = User.objects.create_user(username="user", email="user@test.com", password="secret")
        self.admin_client = APIClient()  # Must have superuser permissions
        self.user_client = APIClient()  # Just a regular user
        self.anon_client = APIClient()  # Anonymous user
        self.admin_client.force_login(admin)
        self.user_client.force_login(user)
        self.global_state_dict = {}

    def taskTests(self):
        state_dict = {}
        # Admin tries to create a task
        data = {
            "title": "Write sort",
            "description": "U have faced with a difficult problem twice x2",
            "tests": "{\r\n\"1 3 2 9 8 7 6 5 4\": \"1 2 3 4 5 6  8 9\",\r\n\"4 3 2 8 9 1\": "
                     "\"1 2 3 4 8 9\",\r\n\"0 -1 90 -0 -90\": \"-90 -1 0 0 90\"\r\n}",
            "public_tests": "{\r\n\"9 8 7 6 5 4 3 2 1 0\": \"0 1 2 3 4 5 6 7 8 9\"\r\n}",
            "restrictions": "{}",
        }
        response = self.admin_client.post(reverse('task-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for i in data.keys():
            self.assertEqual(response.data[i], data[i])

        state_dict['admin_task_id'] = response.data['id']
        self.global_state_dict['task_id'] = response.data['id']
        state_dict['admin_task'] = response.data

        # Admin tries to get the task he created. Note: tests should NOT BE hidden
        response = self.admin_client.get(reverse('task-detail', kwargs={'pk': state_dict['admin_task_id']}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(state_dict['admin_task'], response.data)
        self.assertEqual(data['tests'], response.data['tests'])

        # Another user tries to get the task he didn't create. Note: tests should BE hidden
        response = self.user_client.get(reverse('task-detail', kwargs={'pk': state_dict['admin_task_id']}))
        self.assertEqual('{}', response.data['tests'])
        self.assertEqual(state_dict['admin_task']['public_tests'], response.data['public_tests'])

        # Anon user tries to get the task. Note: tests should BE hidden
        response = self.anon_client.get(reverse('task-detail', kwargs={'pk': state_dict['admin_task_id']}))
        self.assertEqual('{}', response.data['tests'])
        self.assertEqual(state_dict['admin_task']['public_tests'], response.data['public_tests'])

        # Admin tries to update the task. Checking that the task was updated
        updated_data = data.copy()
        updated_data['title'] = 'Updated title'
        state_dict['admin_task'] = updated_data
        response = self.admin_client.put(reverse('task-detail',
                                                 kwargs={'pk': state_dict['admin_task_id']}), updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(state_dict['admin_task']['title'], response.data['title'])

        # Anon tries to update the task
        response = self.user_client.put(reverse('task-detail',
                                                kwargs={'pk': state_dict['admin_task_id']}), updated_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Anon tries to update the task
        response = self.anon_client.put(reverse('task-detail',
                                                kwargs={'pk': state_dict['admin_task_id']}), updated_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Anon tries to delete the task
        response = self.user_client.delete(reverse('task-detail',
                                                   kwargs={'pk': state_dict['admin_task_id']}), updated_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Anon tries to delete the task
        response = self.anon_client.delete(reverse('task-detail',
                                                   kwargs={'pk': state_dict['admin_task_id']}), updated_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Admin wont try do delete the task because we need it later

        # Any user (say) admin tries to view the list of tasks. Tests should be hidden
        response = self.anon_client.get(reverse('task-list'))
        data = response.data['results']
        for i in data:
            self.assertEqual(i['tests'], '{}')

    def solutionsTests(self):
        task_id = self.global_state_dict['task_id']
        admin_solution = {
            "code": "print(''.join(sorted(map(int, input().split()))))",
            "task":  "http://testserver" + reverse('task-detail', kwargs={'pk': task_id})
        }

        user_solution = {
            "code": "user's code",
            "task": "http://testserver" + reverse('task-detail', kwargs={'pk': task_id})
        }

        # Admin posts a solution
        response = self.admin_client.post(reverse('solution-list'), admin_solution)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        admin_solution_id = response.data['id']

        # User posts a solution
        response = self.user_client.post(reverse('solution-list'), user_solution)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_solution_id = response.data['id']

        # Anon tries to post a solution
        response = self.anon_client.post(reverse('solution-list'), user_solution)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Admin tries to get solutions list. Should work
        response = self.admin_client.get(reverse('solution-list'), follow=True)
        self.assertEqual(response.request['PATH_INFO'], reverse('solution-list'))  # Redirection url

        # User tries to get solution list. He should be redirected to his own solutions
        response = self.user_client.get(reverse('solution-list'), follow=True)
        self.assertRedirects(response, reverse('solution-my-solutions'))

        # Admin tries to get user's solution. He should get it
        response = self.admin_client.get(reverse('solution-detail', kwargs={'pk': user_solution_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # User tries to get his own solution. He should get it
        response = self.user_client.get(reverse('solution-detail', kwargs={'pk': user_solution_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # User tries to get admin's (other user's) solution. He shouldn't get it
        response = self.user_client.get(reverse('solution-detail', kwargs={'pk': admin_solution_id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Solution.status must be equal to null (None) meaning that it is not checked yet.
        # Note: test may not work when Celery queue will be implemented
        solution = Solution.objects.get(pk=user_solution_id)
        self.assertEqual(solution.status, None)

    def test_details(self):
        self.taskTests()
        self.solutionsTests()
