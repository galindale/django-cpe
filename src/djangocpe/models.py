from cpe import CPE
from cpe.cpe2_3_wfn import CPE2_3_WFN
from cpe.comp.cpecomp import CPEComponent

from django.core.exceptions import ValidationError
from django.db import models
from fields import URIField, LanguageField

# South intrspection of custom fields of Django models
from south.modelsinspector import add_introspection_rules

add_introspection_rules([], ["^djangocpe\.fields\.URIField"])
add_introspection_rules([], ["^djangocpe\.fields\.LanguageField"])


# Used when the name is first added to the dictionary
CHANGE_ORIGINAL_RECORD = 1

# Used when the authority behind the name is modified
CHANGE_AUTHORITY_CHANGE = 2

# Used when the name is first deprecated
CHANGE_DEPRECATION = 3

# Used when additional deprecation entries are recorded for a deprecated name
CHANGE_DEPRECATION_MODIFICATION = 4

CHANGE_TYPE_CHOICES = (
    (CHANGE_ORIGINAL_RECORD, 'Original record'),
    (CHANGE_AUTHORITY_CHANGE, 'Authority change'),
    (CHANGE_DEPRECATION, 'Deprecation'),
    (CHANGE_DEPRECATION_MODIFICATION, 'Deprecation modification')
)


def get_change_type_str(value):
    """
    Returns the text associated with the input change type.

    :param int value: The change type to get
    :returns: Text associated with the change type
    :rtype: string
    """

    for k, v in CHANGE_TYPE_CHOICES:
        if k == value:
            return v

    # Type not found
    errormsg = "Invalid change type: {0}".format(value)
    raise ValueError(errormsg)


def get_change_type_int(value):
    """
    Returns the integer value associated with the input change type.

    :param int value: The change type to get
    :returns: Integer value associated with the change type
    :rtype: int
    """

    for k, v in CHANGE_TYPE_CHOICES:
        if v.upper().replace(" ", "_") == value:
            return k

    # Type not found
    errormsg = "Invalid change type: {0}".format(value)
    raise ValueError(errormsg)

# The curator of the dictionary discovered information that led to a change
EVIDENCE_CURATOR_UPDATE = 1

# The vendor of the product identified in the name released or
# submitted information that led to a change
EVIDENCE_VENDOR_FIX = 2

# A third party released or submitted information that led to a change
EVIDENCE_THIRD_PARTY_FIX = 3

EVIDENCE_TYPE_CHOICES = (
    (EVIDENCE_CURATOR_UPDATE, 'Curator update'),
    (EVIDENCE_VENDOR_FIX, 'Vendor fix'),
    (EVIDENCE_THIRD_PARTY_FIX, 'Third party fix')
)


def get_evidence_type_str(value):
    """
    Returns the text associated with the input evidence type.

    :param int value: The evidence type to get
    :returns: Text associated with the evidence type
    :rtype: string
    """

    for k, v in EVIDENCE_TYPE_CHOICES:
        if k == value:
            return v

    # Type not found
    errormsg = "Invalid evidence type: {0}".format(value)
    raise ValueError(errormsg)


def get_evidence_type_int(value):
    """
    Returns the integer value associated with the input evidence type.

    :param string value: The evidence type to get
    :returns: Integer value associated with the evidence type
    :rtype: int
    """

    for k, v in EVIDENCE_TYPE_CHOICES:
        if v.upper().replace(" ", "_") == value:
            return k

    # Type not found
    errormsg = "Invalid evidence type: {0}".format(value)
    raise ValueError(errormsg)

# Deprecation is of type Identifier Name Correction
DEPRECATED_BY_NAME_CORRECTION = 1

# Deprecation is of type Identifier Name Removal
DEPRECATED_BY_NAME_REMOVAL = 2

# Deprecation is of type Additional Information Discovery
DEPRECATED_BY_ADDITIONAL_INFO = 3

DEPRECATED_BY_CHOICES = (
    (DEPRECATED_BY_NAME_CORRECTION, 'Name correction'),
    (DEPRECATED_BY_NAME_REMOVAL, 'Name removal'),
    (DEPRECATED_BY_ADDITIONAL_INFO, 'Additional information')
)


def get_deprecatedby_type_str(value):
    """
    Returns the text associated with the input deprecated-by type.

    :param int value: The deprecated-by type to get
    :returns: Text associated with the deprecated-by type
    :rtype: string
    """

    for k, v in DEPRECATED_BY_CHOICES:
        if k == value:
            return v

    # Type not found
    errormsg = "Invalid deprecated-by type: {0}".format(value)
    raise ValueError(errormsg)


def get_deprecatedby_type_int(value):
    """
    Returns the integer value associated with the input deprecated-by type.

    :param string value: The deprecated-by type to get
    :returns: Integer value associated with the deprecated-by type
    :rtype: int
    """

    for k, v in DEPRECATED_BY_CHOICES:
        if v.upper().replace(" ", "_") == value:
            return k

    # Type not found
    eRRORmsg = "Invalid deprecated-by type: {0}".format(value)
    raise ValueError(errormsg)

# ################################
#    MODEL CLASSES OF CPE DICT   #
# ################################


class CpeData(models.Model):
    """
    Stores data related to the CPE Names of the dictionary.
    """

    #: The system type of CPE Name
    part = models.CharField(max_length=10, null=True, blank=True)
    #: The vendor name of CPE Name
    vendor = models.CharField(max_length=100, null=True, blank=True)
    #: The product name of CPE Name
    product = models.CharField(max_length=100, null=True, blank=True)
    #: The version of product of CPE Name
    version = models.CharField(max_length=50, null=True, blank=True)
    #: The update or service pack information of CPE Name
    update = models.CharField(max_length=100, null=True, blank=True)
    #: The edition of product of CPE Name
    edition = models.CharField(max_length=100, null=True, blank=True)
    #: The software edition of CPE Name
    sw_edition = models.CharField(max_length=100, null=True, blank=True)
    #: The software computing environment of CPE Name within
    #: which the product operates
    target_sw = models.CharField(max_length=100, null=True, blank=True)
    #: The arquitecture of CPE Name
    target_hw = models.CharField(max_length=100, null=True, blank=True)
    #: The extra information about CPE Name
    other = models.CharField(max_length=150, null=True, blank=True)
    #: The internationalization information of CPE Name
    language = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        unique_together = (("part", "vendor", "product", "version", "update",
                            "edition", "sw_edition", "target_sw", "target_hw",
                            "other", "language"),)

         # Only >= django 1.5
#        index_together = [["part", "vendor", "product", "version", "update",
#                           "edition", "sw_edition", "target_sw", "target_hw",
#                           "other", "language"], ]

    def clean(self):
        """
        Validates the input CPE Name values which are CPE Names with WFN style
        (Well-Formed Name).

        :exception: ValidationError - Invalid CPE Name
        """

        # Compose a CPE Name with WFN style
        cpe_name = ['wfn:[']

        for att in CPEComponent.CPE_COMP_KEYS_EXTENDED:
            value = getattr(self, att)
            if (value != "") and (value is not None):
                cpe_name.append('{0}={1}'.format(att, value))
                cpe_name.append(', ')

        if len(cpe_name) > 1:
            # Delete the last separator
            cpe_name = cpe_name[:-1]

        # Append the WFN suffix
        cpe_name.append(']')
        wfn = "".join(cpe_name)

        try:
            # Try to create a CPE Name with the input data.
            CPE2_3_WFN(wfn)
        except ValueError as e:
            raise ValidationError(message=e.message, code='invalid')
        else:
            super(CpeData, self).clean()

    def __unicode__(self):
        """
        Human-readable representation of model objects.
        Returns each object as CPE name string with WFN style.

        :returns: CPE data as string
        :rtype: string
        """

        cpe_name = ['wfn:[']

        for att in CPEComponent.CPE_COMP_KEYS_EXTENDED:
            value = getattr(self, att)
            if value != "":
                cpe_name.append('{0}={1}'.format(att, value))
                cpe_name.append(', ')

        if len(cpe_name) > 1:
            # Delete the last separator
            cpe_name = cpe_name[:-1]

        # Append the WFN suffix
        cpe_name.append(']')
        cpe_wfn = CPE("".join(cpe_name), CPE.VERSION_2_3)

        return cpe_wfn.as_fs()

    #def save(self, *args, **kwargs):
    #    # If object exists, save operation not executed
    #    if CpeData.objects.get(part__iexact = self.part,
    #                           vendor__iexact = self.vendor,
    #                           product__iexact = self.product,
    #                           version__iexact = self.version,
    #                           update__iexact = self.update,
    #                           edition__iexact = self.edition,
    #                           sw_edition__iexact = self.sw_edition,
    #                           target_sw__iexact = self.target_sw,
    #                           target_hw__iexact = self.target_hw,
    #                           other__iexact = self.other,
    #                           language__iexact = self.language):
    #        # Object ignored
    #        return
    #    else:
    #        super(CpeData, self).save(*args, **kwargs)


class CpeList(models.Model):
    """
    Acts as a top-level container for CPE Name items.
    Each individual item must be unique.
    """

    #: CPE list name
    name = models.CharField(max_length=255, null=True, blank=True,
                            help_text=u'CPE list name')

    def __unicode__(self):
        """
        Human-readable representation of model objects.

        :returns: CPE list as string
        :rtype: string
        """

        num_cpes = len(self.cpeitem_set.all())
        return u'{0} ({1} elementos)'.format(self.name, num_cpes)


class CpeItem(models.Model):
    """
    Contains all of the information for a single dictionary entry
    (identifier name), including metadata.
    """

    #: The identifier name bound in CPE 2.2 format
    name = models.ForeignKey(
        CpeData, null=False,
        related_name="name_cpeitem")

    #: Whether or not the name has been deprecated
    deprecated = models.NullBooleanField(
        blank=True, default=False,
        help_text=u'Whether or not the name has been deprecated')

    #: The name that deprecated this name, bound in CPE 2.2 format
    deprecated_by = models.ForeignKey(
        CpeData, null=True, blank=True,
        related_name="deprecatedby_cpeitem")

    #: When the name was deprecated
    deprecation_date = models.DateTimeField(
        null=True, blank=True,
        help_text=u'When the name was deprecated')

    #: CPE list that includes the cpe item
    cpelist = models.ForeignKey(CpeList, null=False)

    class Meta:
        unique_together = (("name", "cpelist"),)

    def __unicode__(self):
        """
        Human-readable representation of model objects.

        :returns: CPE item as string
        :rtype: string
        """

        depre_str = ""
        if self.deprecated == 1:
            depre_str = "anulado"
        else:
            depre_str = "no anulado"

        if self.deprecation_date is None:
            return u'{0} ({1})'.format(self.name, depre_str)
        else:
            return u'{0} ({1}) [{2}]'.format(self.name,
                                             depre_str,
                                             self.deprecation_date)


class Generator(models.Model):
    """
    Defines an element that is used to hold information about
    when a particular document was compiled,
    what version of the schema was used,
    what tool compiled the document,
    and what version of that tool was used.
    """

    #: The name of the application used to generate the file
    product_name = models.CharField(
        max_length=255, null=True, blank=True,
        help_text=u'The name of the application used to generate the file')

    #: The version of the application used to generate the file
    product_version = models.CharField(
        max_length=255, null=True, blank=True,
        help_text=u'The version of the application used to generate the file')

    #: The version of the schema that the document has been written against
    #: and that should be used for validation
    schema_version = models.DecimalField(
        max_digits=4, decimal_places=2, null=False,
        help_text=u'The version of the schema that the document has been\
            written against and that should be used for validation')

    #: When the particular document was compiled
    timestamp = models.DateTimeField(
        null=False,
        help_text=u'When the particular document was compiled')

    #: Cpe list associated with the generator data
    cpelist = models.ForeignKey(CpeList, null=False)

    def __unicode__(self):
        """
        Human-readable representation of model objects.

        :returns: Generator as string
        :rtype: string
        """

        return u'Version CPE {0} ({1})'.format(
            self.schema_version, self.timestamp)


class Title(models.Model):
    """
    Stores the titles associated with cpe items together with the language in
    which they are defined.
    """

    #: Human-readable title of the CPE Name
    title = models.CharField(
        max_length=255, null=False,
        help_text=u'Human-readable title of the CPE Name')

    #: Language associated with the title
    language = LanguageField(
        null=False,
        help_text=u'Language associated with the title')

    #: Cpe item associated with the title
    cpeitem = models.ForeignKey(CpeItem, null=False)

    def __unicode__(self):
        """
        Human-readable representation of model objects.

        :returns: Title as string
        :rtype: string
        """

        return u'{0} (lang={1})'.format(self.title, self.language)


class Note(models.Model):
    """
    Stores the notes associated with cpe items together with the language in
    which they are defined.
    """

    #: Note associated with the CPE Name
    note = models.TextField(
        null=False,
        help_text=u'Note associated with the CPE Name')

    #: Language associated with the note
    language = LanguageField(
        null=False,
        help_text=u'Language associated with the note')

    #: Cpe item associated with the note
    cpeitem = models.ForeignKey(CpeItem, null=False)

    def __unicode__(self):
        """
        Human-readable representation of model objects.

        :returns: Note as string
        :rtype: string
        """

        return u'{0} (lang={1})'.format(self.note, self.language)


class Reference(models.Model):
    """
    Stores the references associated with the CPE Name checks, such as,
    an OVAL definition, that can confirm or reject an IT system
    as an isntance of the named platfom.
    """

    #: Human-readable title of the reference
    name = models.CharField(
        max_length=255, null=False,
        help_text=u'Human-readable title of the reference')

    #: URL pointing to a real resource of reference
    href = URIField(
        null=False,
        help_text=u'URL pointing to a real resource of reference')

    #: Cpe item associated with the reference
    cpeitem = models.ForeignKey(CpeItem, null=False)

    def __unicode__(self):
        """
        Human-readable representation of model objects.

        :returns: Reference as string
        :rtype: string
        """

        return u'{0} ({1})'.format(self.name, self.href)


class Check(models.Model):
    """
    Holds information about an individual check, such as an OVAL definition,
    that can confirm or reject an IT system as an instance
    of the named platform.
    """

    #: Check identifier
    check_id = models.CharField(
        max_length=255, null=False,
        help_text=u'The check identifier')

    #: The pointer to the file where the check is defined
    href = URIField(
        null=True, blank=True,
        help_text=u'The pointer to the file where the check is defined')

    #: The checking system specification URI of the reference, that is,
    #: a URI for a particular version of OVAL or
    #: a related system testing language
    system = URIField(
        null=False,
        help_text=u'Check system specification URI of the reference')

    #: Cpe item associated with the check
    cpeitem = models.ForeignKey(CpeItem, null=False)

    class Meta:
        unique_together = (("system", "cpeitem"),)

    def __unicode__(self):
        """
        Human-readable representation of model objects.

        :returns: Check as string
        :rtype: string
        """

        return u'{0}'.format(self.check_id)


# ################################################
#    MODEL CLASSES OF CPE DICTIONARY EXTENSION   #
# ################################################


class Organization(models.Model):
    """
    Stores information about organizations of CPE dictionary.
    """

    system_id = URIField(
        null=False,
        help_text=u'Unique URI representing the organization')
    name = models.CharField(
        max_length=255, null=False,
        help_text=u'Human readable name of the organization')
    action_datetime = models.DateTimeField(
        null=False,
        help_text=u'The date the organization performed an action \
            relative to an identifier name')
    description = models.TextField(
        max_length=255, null=True, blank=True,
        help_text=u'A high-level description of the organization')

    def __unicode__(self):
        """
        Human-readable representation of model objects.

        :returns: Organization as string
        :rtype: string
        """

        return u'{0} ({1})'.format(self.name, self.system_id)


class Deprecation(models.Model):
    """
    Stores information about deprecations of CPE Names.
    """

    #: When the deprecation occurred
    dep_datetime = models.DateTimeField(
        null=True, blank=True,
        help_text=u'When the deprecation occurred')

    #: Cpe item associated with the check
    cpeitem = models.ForeignKey(CpeItem, null=False)

    def __unicode__(self):
        """
        Human-readable representation of model objects.

        :returns: Deprecation as string
        :rtype: string
        """

        name = ""
        try:
            name = self.cpeitem.name
        except:
            name = "SIN ASIGNAR CPE"
        finally:
            return u'{0} ({1})'.format(self.cpeitem.name, self.dep_datetime)


class DeprecatedBy(models.Model):
    """
    Stores information about the type of deprecation and the the name
    that is deprecating the identifier name.
    """

    #: The type of deprecation
    dep_type = models.IntegerField(
        null=False, choices=DEPRECATED_BY_CHOICES,
        help_text=u'The type of deprecation')

    #: The name that is deprecating the identifier name
    name = models.ForeignKey(
        CpeData, null=False,
        related_name="name_deprecatedby")

    #: Information about deprecation
    deprecation = models.ForeignKey(Deprecation, null=False)

    def __unicode__(self):
        """
        Human-readable representation of model objects.

        :returns: Information about the name that is deprecating as string
        :rtype: string
        """

        dep_type_text = DEPRECATED_BY_CHOICES[self.dep_type][1]
        return u'{0} ({1})'.format(self.name, dep_type_text)


class ProvenanceRecord(models.Model):
    """
    Stores information about a provenance record.
    """

    submitter = models.ForeignKey(
        Organization, null=False, related_name='submitter',
        help_text=u'The organization responsible for submitting \
            the identifier name')
    authorities = models.ManyToManyField(
        Organization, null=False, related_name='authority',
        help_text=u'The authority or authorities responsible for \
            endorsing the identifier name')
    cpeitem = models.ForeignKey(CpeItem, null=False)

    def __unicode__(self):
        """
        Human-readable representation of model objects.

        :returns: Provenance record as string
        :rtype: string
        """

        return u'{0} ({1})'.format(self.cpeitem.name, self.submitter)


class EvidenceReference(models.Model):
    """
    Stores information about change evidences.
    """

    ref = URIField(
        null=False,
        help_text=u'Unique URI representing the evidence reference')
    evidence = models.IntegerField(
        null=False, choices=EVIDENCE_TYPE_CHOICES,
        help_text=u'Supporting evidence for any change to a name or \
            associated metadata')

    def __unicode__(self):
        """
        Human-readable representation of model objects.

        :returns: Evidence reference as string
        :rtype: string
        """

        evidence_text = EVIDENCE_TYPE_CHOICES[self.evidence][1]
        return u'{0} - {1}'.format(self.ref, evidence_text)


class ChangeDescription(models.Model):
    """
    Stores information about change information of a provenance record.
    """

    change_type = models.IntegerField(
        null=False, choices=CHANGE_TYPE_CHOICES,
        default=CHANGE_ORIGINAL_RECORD,
        help_text=u'The type of change that occurred')
    change_datetime = models.DateTimeField(
        null=False,
        help_text=u'When the change occurred')
    comment = models.TextField(
        max_length=255, null=True, blank=True,
        help_text=u'Comments explaining the rationale for the change')
    prov_record = models.ForeignKey(ProvenanceRecord, null=False)
    evidence = models.ForeignKey(EvidenceReference, null=True, blank=True)

    def __unicode__(self):
        """
        Human-readable representation of model objects.

        :returns: Change description as string
        :rtype: string
        """

        change_type_text = CHANGE_TYPE_CHOICES[self.change_type][1]
        return u'{0} - {1}'.format(self.change_datetime, change_type_text)
