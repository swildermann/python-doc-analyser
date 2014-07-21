from django.db import models


class DocumentationUnit(models.Model):
    html_text = models.TextField(max_length=None)
    filename = models.CharField(max_length=500, default="None")
    length = models.IntegerField(default=0)
    offset = models.IntegerField(default=-1)
    parent_text = models.TextField(max_length=None, default="") #improve?
    file_text = models.TextField(max_length=None, default="") #improve?
    type = models.CharField(max_length=100, default="") #why not a model for its own?
    plaintext = models.TextField(max_length=None)


class KnowledgeType(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=None, default="")


class MarkedUnit(models.Model):
    user = models.ForeignKey('auth.User', null=True, blank=True) #why are null and blank true?
    documentation_unit = models.ForeignKey(DocumentationUnit)
    knowledge_type = models.IntegerField(default=0)  # should be ForeignKey #improve?
    html_text = models.TextField() #improve? #does this text differ from the original?
    range = models.TextField(max_length=500, default='')
    char_range = models.TextField(max_length=500, default='')
    timestamp = models.DateTimeField(default=0)


class MappingUnitToUser(models.Model):
    user = models.ForeignKey('auth.User', null=True, blank=True)
    documentation_unit = models.ForeignKey(DocumentationUnit)
    already_marked = models.BooleanField(default=False)
    last_change = models.DateTimeField(default=0)
    unmarked_chars = models.IntegerField(default=0)
    unmarked_percent = models.IntegerField(default=0)


class AccessLog(models.Model):
    user = models.ForeignKey('auth.User', null=True, blank=True)
    documentation_unit = models.ForeignKey(DocumentationUnit)
    timestamp = models.DateTimeField(default=0)
    filename = models.CharField(max_length=100, default='') #improve name ? filename to action?

class Agreement(models.Model):
    first = models.ForeignKey(MappingUnitToUser, related_name="first")
    second = models.ForeignKey(MappingUnitToUser, related_name="second")
    percentage_by_types = models.FloatField(default=0)
    percentage_by_chars = models.IntegerField(default=0)

class Compatibility(models.Model):
    one = models.ForeignKey(MappingUnitToUser, related_name="one", default=None)
    two = models.ForeignKey(MappingUnitToUser, related_name="two", default=None)
    compatible = models.IntegerField(default=0)
    non_compatible = models.IntegerField(default=0)
    percentage_compatible = models.FloatField(default=0)
    percentage_based_on_chars = models.FloatField(default=0)

class Confusions(models.Model):
    a = models.ForeignKey(KnowledgeType, related_name="a", default=None)
    b = models.ForeignKey(KnowledgeType, related_name="b", default=None)
    a_id = models.ForeignKey(MarkedUnit, related_name="a_id", default=0)
    b_id = models.ForeignKey(MarkedUnit, related_name="b_id", default=0)
    length = models.IntegerField(default=0)
