from django.db import models
from django.dispatch import receiver
from .tasks import check_solution

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

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Solution, self).save(force_insert, force_update, using, update_fields)


@receiver(models.signals.post_save, sender=Solution)
def solution_execute_after_save(sender, instance, created, *args, **kwargs):
    if created:
        check_solution(instance.id)
