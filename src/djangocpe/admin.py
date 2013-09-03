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
admin.site.register(CpeList)
admin.site.register(CpeItem)
admin.site.register(Generator)
admin.site.register(Title)
admin.site.register(Note)
admin.site.register(Reference)
admin.site.register(Check)
admin.site.register(Organization)
admin.site.register(Deprecation)
admin.site.register(DeprecatedBy)
admin.site.register(ProvenanceRecord)
admin.site.register(ChangeDescription)
