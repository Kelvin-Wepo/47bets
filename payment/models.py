from django.db import models

class Transaction(models.Model):
    phone_number = models.CharField(max_length = 13, null = True, blank = True )
    amount = models.DecimalField(max_digits = 10,decimal_places=2, null =True, blank = True )

    def __str__(self):
        return self.phone_number