from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField()
    description = models.TextField()
    type = models.CharField(max_length=2, choices=[('1', 'Pemasukan'), ('2', 'Pengeluaran')])
    transaction_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.description}"
    
    class Meta:
        ordering = ['-transaction_date']

class TransactionImage(models.Model):
    transaction = models.ForeignKey(Transaction, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    image_name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"image_{self.id}" if self.image_name is None else self.image_name
