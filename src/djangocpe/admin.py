from django.contrib import admin

from djangocpe.models import CpeData
from djangocpe.models import CpeList
from djangocpe.models import CpeItem
from djangocpe.models import Generator
from djangocpe.models import Title
from djangocpe.models import Note
from djangocpe.models import Reference
from djangocpe.models import Check
from djangocpe.models import Organization
from djangocpe.models import Deprecation
from djangocpe.models import DeprecatedBy
from djangocpe.models import ProvenanceRecord
from djangocpe.models import ChangeDescription

admin.site.register(CpeData)
admin.site.register(Generator)
admin.site.register(Title)
admin.site.register(Note)
admin.site.register(Reference)
admin.site.register(Check)
admin.site.register(Organization)
admin.site.register(DeprecatedBy)
admin.site.register(ProvenanceRecord)
admin.site.register(ChangeDescription)


# ################################################
#               INLINE MODEL ADMIN               #
# ################################################

# Help link:
# http://stackoverflow.com/questions/6034047/one-to-many-inline-select-with-django-admin

class CpeItemInline(admin.TabularInline):
    model = CpeItem
    extra = 2


class GeneratorInline(admin.TabularInline):
    model = Generator
    max_num = 1


class TitleInline(admin.TabularInline):
    model = Title
    extra = 1


class NoteInline(admin.TabularInline):
    model = Note
    extra = 1


class ReferenceInline(admin.TabularInline):
    model = Reference
    extra = 1


class CheckInline(admin.TabularInline):
    model = Check
    extra = 1


class DeprecationInline(admin.TabularInline):
    model = Deprecation
    extra = 1


class DeprecatedByInline(admin.TabularInline):
    model = DeprecatedBy
    extra = 1


class CpeListAdmin(admin.ModelAdmin):
    inlines = [
        GeneratorInline,
        CpeItemInline,
    ]


class CpeItemAdmin(admin.ModelAdmin):
    inlines = [
        TitleInline,
        NoteInline,
        ReferenceInline,
        CheckInline,
        DeprecationInline,
    ]

class DeprecationAdmin(admin.ModelAdmin):
    inlines = [
        DeprecatedByInline,
    ]

admin.site.register(CpeList, CpeListAdmin)
admin.site.register(CpeItem, CpeItemAdmin)
admin.site.register(Deprecation, DeprecationAdmin)
