from django.contrib import admin
from extractor.models import DocumentationUnit, KnowledgeType, ParentElement, MarkedUnit, MappingUnitToUser


class KnowledgeTypesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class DocumentationUnitAdmin(admin.ModelAdmin):
    list_display = ['id', 'filename']


class ParentElementAdmin(admin.ModelAdmin):
    list_display = ['id']


class MarkedUnitAdmin(admin.ModelAdmin):
    list_display = ['id', 'knowledge_type', 'user']


class MappingUnitToUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'documentation_unit', 'already_marked']


admin.site.register(DocumentationUnit, DocumentationUnitAdmin)
admin.site.register(KnowledgeType, KnowledgeTypesAdmin)
admin.site.register(ParentElement, ParentElementAdmin)
admin.site.register(MarkedUnit, MarkedUnitAdmin)
admin.site.register(MappingUnitToUser,MappingUnitToUserAdmin)