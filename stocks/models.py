from django.db import models

class Stock(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    moment = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

