from django.db import models
from customer.models import Customer

# Create your models here.
class Order(models.Model):
    item = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    description = models.TextField()
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return str(self.owner) + 's order'
    