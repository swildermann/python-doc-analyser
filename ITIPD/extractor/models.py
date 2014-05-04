from django.db import models


class ParentElement(models.Model):
        html_text = models.TextField(max_length=None)


class DocumentationUnit(models.Model):
    html_text = models.TextField(max_length=None)
    filename = models.CharField(max_length=500, default="None")
    length = models.IntegerField(default=0)


class KnowledgeType(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=None, default="")


class MarkedUnit(models.Model):
    user = models.ForeignKey('auth.User', null=True, blank=True)
    documentation_unit = models.ForeignKey(DocumentationUnit)
    #documentation_unit = models.IntegerField(default=0)
    knowledge_type = models.IntegerField(default=0)
    html_text = models.TextField()


class MappingUnitToUser(models.Model):
    user = models.ForeignKey('auth.User', null=True, blank=True)
    documentation_unit = models.ForeignKey(DocumentationUnit)
    already_marked = models.BooleanField(default=False)
