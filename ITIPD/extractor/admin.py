from django.contrib import admin
from extractor.models import DocumentationUnit, KnowledgeType, ParentElement, MarkedUnit


class KnowledgeTypesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class DocumentationUnitAdmin(admin.ModelAdmin):
    list_display = ['id', 'filename']


class ParentElementAdmin(admin.ModelAdmin):
    list_display = ['id']


class MarkedUnitAdmin(admin.ModelAdmin):
    list_display = ['id', 'knowledge_type', 'user']


admin.site.register(DocumentationUnit, DocumentationUnitAdmin)
admin.site.register(KnowledgeType, KnowledgeTypesAdmin)
admin.site.register(ParentElement, ParentElementAdmin)
admin.site.register(MarkedUnit, MarkedUnitAdmin)