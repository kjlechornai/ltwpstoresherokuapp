from django.db import models
from django.conf import settings
from item.models import Item, Department, Project, Location

ISSUER = (
    ('KJ', 'kizito'),
    ('CG', 'celestine'),
    ('JP', 'jesire')
)

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username}"

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    order_purpose = models.ForeignKey('OrderPurpose', on_delete=models.SET_NULL, null=True, blank=True)
    order_issued = models.ForeignKey('OrderIssued', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

class OrderPurpose(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    purpose = models.CharField(max_length=200)
    project_name = models.ForeignKey(Project, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    collected_by = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.purpose}'

class OrderIssued(models.Model):
    issuer = models.CharField(max_length=100, choices=ISSUER)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'from {self.location.name} issued by {self.issuer}'