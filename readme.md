# Perlite.io (Basil need to read all)
## Installation

- Clone this repository
- Build docker environment using `docker-compose build`, it will take a while
- Run built container: `docker-compose up -d`
- Get a list of currently running detached containers: `docker ps`
- Get a console instance of the container `sudo docker exec -i -t perliteio_web_1 /bin/bash`. Note: if it doesn't work, change `perliteio_web_1` to the listed above
- Make sure everything works fine by running some tests: `python manage.py test base.tests`
- Deploy the server: `python manage.py runserver 0.0.0.0:8000`
- Now you can change the code. Docker-compose file system is shared with yours and all changes will be applied instantly
## Tips

- No need to build you container over and over. Changing `Dockerfile` or `docker-compose.yml` doesn't require that
- Testing is broken. `python manage.py test` will result in some weird error. run `python manage.py test appName.tests` instead, it  will work out just fine.
- Changing the port in code (or cmd) is not enough. Also check `port` in docker-compose
- Docker console is a **shithole**. Need to think of something else.
## Architecture
### Db: PostgreSQL

### App: base
It comes without saying that I am genius. Naming god. Whatever. This app contains Task, Solution and some interactions. For example:
- Admin tries to get the task he created. Note: tests should NOT BE hidden
- Another user tries to get the task he didn't create. Note: tests should BE hidden
- Any user (say, admin) tries to get the list of tasks. Tests should be hidden
- Admin tries to get ALL solutions list. Should work
- User tries to get solution list. He should be redirected to his own solutions
- Admin tries to get user's solution. He should get it
- User tries to get admin's (other user's) solution. He should NOT get it
- Once created, Solution.status must be equal to null (None) meaning that it is not checked yet. (Will be changed)
These were most the notable interactions. For all look in base.test.
Thus, **no need to worry** if you try to peep other user's solution using a non-staff account and get `403_FORBIDDEN` or try to get all solution list  and get redirected to your own (solution list), using the same non-staff account.
> **Note:** Name refractor is a good thing and needs to be done


## App: users
Just  a Serializer with a small ViewWet using the native User model. Needs to be changed. Later. Probably...

## Celery instance

[Celery: first steps with django](http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html)
Main problem: whether to use [Redis](https://redis.io/) or (  [Memchached](https://memcached.org/) as backend + [RabbitMQ](https://www.rabbitmq.com/) as a message broker )
Need more studying.
### That seems to be all. For a while... For now...

Copyright (c) 2018 **dotapetro**

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE X CONSORTIUM BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
