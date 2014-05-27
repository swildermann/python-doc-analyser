from django.contrib import admin
from extractor.models import DocumentationUnit, KnowledgeType, MarkedUnit, MappingUnitToUser, AccessLog


class KnowledgeTypesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class DocumentationUnitAdmin(admin.ModelAdmin):
    list_display = ['id', 'filename']


class MarkedUnitAdmin(admin.ModelAdmin):
    def unitid(self, obj):
        return obj.documentation_unit.id

    list_display = ['id', 'unitid', 'timestamp', 'knowledge_type', 'user']


class MappingUnitToUserAdmin(admin.ModelAdmin):

    def unitid(self, obj):
        return obj.documentation_unit.id

    list_display = ['user', 'unitid', 'already_marked']


class AccessLogAdmin(admin.ModelAdmin):
    def unitid(self, obj):
        return obj.documentation_unit.id

    list_display =['user', 'unitid', 'timestamp', 'filename']


admin.site.register(DocumentationUnit, DocumentationUnitAdmin)
admin.site.register(KnowledgeType, KnowledgeTypesAdmin)
admin.site.register(MarkedUnit, MarkedUnitAdmin)
admin.site.register(MappingUnitToUser,MappingUnitToUserAdmin)
admin.site.register(AccessLog, AccessLogAdmin)