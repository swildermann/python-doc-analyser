from django.db import models


class DocumentationUnit(models.Model):
    html_text = models.TextField(max_length=None)
    filename = models.CharField(max_length=500, default="None")
    length = models.IntegerField(default=0)
    offset = models.IntegerField(default=-1)
    parent_text = models.TextField(max_length=None, default="")
    file_text = models.TextField(max_length=None, default="")
    type = models.CharField(max_length=100, default="")


class KnowledgeType(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=None, default="")


class MarkedUnit(models.Model):
    user = models.ForeignKey('auth.User', null=True, blank=True)
    documentation_unit = models.ForeignKey(DocumentationUnit)
    #documentation_unit = models.IntegerField(default=0)
    knowledge_type = models.IntegerField(default=0)  # should be ForeignKey
    html_text = models.TextField()
    range = models.TextField(max_length=500, default='')
    timestamp = models.TimeField(default=0)


class MappingUnitToUser(models.Model):
    user = models.ForeignKey('auth.User', null=True, blank=True)
    documentation_unit = models.ForeignKey(DocumentationUnit)
    already_marked = models.BooleanField(default=False)