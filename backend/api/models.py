from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.email


class Medicine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medicines')
    title = models.TextField()
    description = models.TextField()
    dosage = models.CharField(max_length=100)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.title} - {self.id or 'unsaved id'}"


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    title = models.TextField()
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.id or 'unsaved id'}"
