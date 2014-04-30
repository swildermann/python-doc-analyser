from django.contrib import admin
from extractor.models import DocumentationUnit, KnowledgeType


class KnowledgeTypesAdmin(admin.ModelAdmin):
    list_display = ['name'
]


class DocumentationUnitAdmin(admin.ModelAdmin):
    list_display = ['id', 'filename']


admin.site.register(DocumentationUnit,DocumentationUnitAdmin)
admin.site.register(KnowledgeType,KnowledgeTypesAdmin)
