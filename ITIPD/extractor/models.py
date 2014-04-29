from django.db import models

class DocumentationUnit(models.Model):
    html_text = models.TextField(max_length=None)
    parentElement = models.IntegerField(default=0)
    filename = models.CharField(max_length=500, default=None)
    start_offset = models.IntegerField(default=0)
    end_offset = models.IntegerField(default=0)

class KnowledgeType(models.Model):
    name = models.CharField(max_length=200)
    desription = models.TextField(max_length=None, default="")


