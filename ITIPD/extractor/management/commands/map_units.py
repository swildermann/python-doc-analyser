import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ITIPD.settings")
from ITIPD.extractor.models import *


"""
get 265 elements of type exception or class
306 elements of type attribute or data
651 elements of type method, staticmethod, classmethod or function
16 elements of type describe
310 elements of type section

map each unit to 2 different users

"""


ClassOrException = DocumentationUnit.objects.filter(type='class') | DocumentationUnit.objects.filter(type='exception')
AttributeOrData = DocumentationUnit.objects.filter(type='attribute') | DocumentationUnit.objects.filter(type='data')
MethodOrFunction = DocumentationUnit.objects.filter(type='method') | \
                   DocumentationUnit.objects.filter(type='staticmethod') | \
                   DocumentationUnit.objects.filter(type='classmethod') | \
                   DocumentationUnit.objects.filter(type='function')

Describe = DocumentationUnit.objects.filter(type='describe')
Section = DocumentationUnit.objects.filter(type='section')

print(len(ClassOrException))