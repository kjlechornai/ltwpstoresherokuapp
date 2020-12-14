from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django import template

register = template.Library()

STATUS_CHOICES = (
    ('in stock', 'primary'),
    ('out of stock', 'danger'),
    ('reorder now', 'warning')
)

class Category(models.Model):
    name = models.CharField(max_length = 50)
    slug = models.SlugField(unique=True)
    summary = models.CharField(max_length=250, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
            
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class Location(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    summary = models.TextField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Location, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Shelf(models.Model):
    name = models.CharField(max_length=50)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Shelves'

class Item(models.Model):
    name = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    item_sage_id = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=20, default='pcs')
    sub_category = models.CharField(max_length=50, blank=True)
    slug = models.SlugField(unique=True)
    shelf_lbl = models.ForeignKey(Shelf, on_delete=models.CASCADE, blank=True)
    reorder_quantity = models.IntegerField(default=0)
    status = models.CharField(max_length=50, default='in stock', choices=STATUS_CHOICES)
    recent = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Item, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name


    @property    
    def get_total_received(self):
        item = Item.objects.filter(name__exact=self.name).get()
        received_qty = item.receive_set.all().aggregate(Sum('quantity'))['quantity__sum']
        if received_qty is not None:
            return received_qty
        return 0

    @property    
    def get_total_returned_to_supplier(self):
        returned_qty = ReturnToSupplier.objects.filter(item__item__name=self.name).aggregate(Sum('quantity'))['quantity__sum']
        if returned_qty is not None:
            return returned_qty
        return 0

    @property    
    def get_total_issued(self):
        item = Item.objects.filter(name__exact=self.name).get()
        issued_qty = item.issue_set.all().aggregate(Sum('quantity'))['quantity__sum']
        if issued_qty is not None:
            return issued_qty
        return 0

    @property    
    def get_total_returned_to_store(self):
        returned_qty = ReturnToStore.objects.filter(item__item__name=self.name).aggregate(Sum('quantity'))['quantity__sum']
        if returned_qty is not None:
            return returned_qty
        return 0

    @property
    def get_total_balance(self):
        total = self.get_total_received - self.get_total_issued + self.get_total_returned_to_store - self.get_total_returned_to_supplier
        if total > 0:
            return total
        return 0

    def project_balance(self, project):
        project_rcv = Receive.objects.filter(item__name=self.item, project__name=project).aggregate(Sum('quantity'))['quantity__sum']
        project_iss = Issue.objects.filter(item__name=self.item, project__name=project).aggregate(Sum('quantity'))['quantity__sum']
        if project_iss is not None:
            return project_rcv - project_iss
        else:
            return project_rcv
        
    def is_in_stock(self):
        return self.get_total_balance > 0


    def get_absolute_url(self):
        return reverse('item:detail', kwargs={'slug' : self.slug})

    def get_add_to_cart_url(self):
        return reverse('cart:add-to-cart', kwargs={'slug':self.slug})

    def get_remove_from_cart_url(self):
        return reverse('cart:remove-from-cart', kwargs={'slug':self.slug})

    
class Image(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', blank=True)
    featured = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.item.name

class Receive(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField()
    receive_date = models.DateTimeField(default=timezone.datetime(2020,1,1))
    status = models.CharField(max_length=50, default='in good condition')
    delivery_mode = models.CharField(max_length=100)
    requestor = models.CharField(max_length=100)
    receive_by = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.item} - {self.quantity}'

    @property
    def project_received(self):
        project_qty = Receive.objects.filter(item__name=self.item, project__name=self.project).aggregate(Sum('quantity'))['quantity__sum']
        return project_qty

    class Meta:
        verbose_name_plural = 'Received'

class Issue(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField()
    purpose = models.CharField(max_length=200, blank=True, null=True)
    issued_to = models.CharField(max_length=100)
    issue_date = models.DateTimeField()
    issue_type = models.CharField(max_length=50, default='direct')

    def __str__(self):
        return f'{self.item} - {self.quantity}'

    class Meta:
        verbose_name_plural = 'Issued'

class ReturnToStore(models.Model):
    item = models.ForeignKey(Issue, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    reason = models.TextField()
    return_by = models.CharField(max_length=100)
    return_date = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return f'{self.item.item} - {self.quantity}'        

class ReturnToSupplier(models.Model):
    item = models.ForeignKey(Receive, on_delete=models.CASCADE)
    reason = models.TextField()
    quantity = models.IntegerField()
    return_by = models.CharField(max_length=100)
    return_date = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return f'{self.item.item} - {self.quantity}'

    class Meta:
        verbose_name_plural = 'Returned to supplier'        

class Department(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    hod = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Department, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True, auto_now=False) 
    completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def project_items(self):
        proj = Project.objects.get(name=self.name)
        pitems = Item.objects.filter(receive__project=proj)
        return pitems
        

    



    

        


    
