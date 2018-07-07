from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


# Create your models here.


# TODO: only teacher can create tasks
class Task(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, blank=False)
    description = models.TextField()  # Markdown description
    tests = models.TextField()  # Json: input -> output, Visible: CreatorOnly
    public_tests = models.TextField()  # Json: input -> output, Visible: Everyone
    restrictions = models.TextField()  # Json: Ram limit, cpu time, ect...
    owner = models.ForeignKey('auth.User', related_name='tasks', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.title


class Solution(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    code = models.TextField()  # Code itself
    status = models.NullBooleanField(null=True)
    task = models.ForeignKey(Task, related_name='solutions', on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='solutions', on_delete=models.CASCADE)
