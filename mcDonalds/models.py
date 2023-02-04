from django.db import models
from datetime import datetime
from mcDonalds.resources import POSITIONS


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)


class Staff(models.Model):
    director = 'DI'
    admin = 'AD'
    cook = 'CO'
    cashier = 'CA'
    cleaner = 'CL'

    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=2,
                                choices=POSITIONS,
                                default=cashier)
    labor_contract = models.IntegerField()

    def get_last_name(self):
        return self.full_name.split()[0]


class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True)
    cost = models.FloatField(default=0.0)
    pickup = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, through='ProductOrder')

    def finish_order(self):
        self.time_out = datetime.now()
        self.complete = True
        self.save()

    def get_duration(self):
        return (self.time_out - self.time_in).total_seconds() if self.complete \
            else (datetime.now() - self.time_in).total_seconds()


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    _amount = models.IntegerField(default=1, db_column='amount')

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = int(value) if value >= 0 else 0
        self.save()

    def product_sum(self):
        product_price = self.product.price
        return product_price * self.amount
