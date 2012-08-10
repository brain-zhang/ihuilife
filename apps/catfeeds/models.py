from django.db import models

# Create your models here.
class Cats(models.Model):
    num_iid = models.IntegerField(unique = True)
    title = models.CharField(max_length = 512)
    img_url = models.CharField(max_length = 256)
    cid = models.IntegerField()
    click_url = models.CharField(max_length = 256)
    price = models.FloatField()
    seller_credit_score = models.IntegerField()
    desc = models.CharField(max_length = 1024)
    
class ItemCats(models.Model):
    cid = models.IntegerField(unique = True)
    name = models.CharField(max_length = 512)
    parent_cid = models.IntegerField()