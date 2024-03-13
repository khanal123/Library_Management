from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import User
# Create your models here.
class Books(models.Model):
    title = models.CharField(max_length=100)
    quantity = models.IntegerField()
    def __str__(self):
        return self.title

class BorrowedBook(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    user = models.ForeignKey('User_Profile.MyUser', on_delete=models.CASCADE)
    # user = models.CharField(max_length=22)
    borrowed_date = models.DateField(auto_now_add=True)
    returned_date = models.DateField(null=True, blank=True)
    due_date = models.DateField()