from django.db import models

class DocumentationUnit(models.Model):
 name = models.CharField(max_length=500)
 checked = models.BooleanField()
