# -*- coding: utf-8 -*-

"""
This file is part of django-cpe package.

This module implements the importation of CPE Dictionaries version 2.3,
specified as XML files, in the models of package django-cpe.

Copyright (C) 2013  Alejandro Galindo Garcí Roberto Abdelkader Martíz Péz

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

For any problems using the django-cpe package, or general questions and
feedback about it, please contact:

- Alejandro Galindo Garcí galindo.garcia.alejandro@gmail.com
- Roberto Abdelkader Martíz Péz: robertomartinezp@gmail.com
"""

from iso8601 import iso8601
from xml.sax.handler import ContentHandler

from cpe import CPE
from djangocpe.models import CpeList, Generator, CpeData, CpeItem, Title, Note
from djangocpe.models import Reference, Check, Deprecation, DeprecatedBy
from djangocpe.models import ProvenanceRecord, Organization
from djangocpe.models import ChangeDescription, EvidenceReference
from djangocpe.models import get_deprecatedby_type_int
from djangocpe.models import get_change_type_int
from djangocpe.models import get_evidence_type_int
from djangocpe.cpedict_parser_error import ParserError


class Cpedict23Handler(ContentHandler):
    """
    A handler to deal with CPE Dictionaries defined in XML format.
    """

    # CPE-LIST ------------------------

    TAG_CPELIST = "cpe-list"

    ATT_CPELIST_NAME = "name"

    # GENERATOR -----------------------

    TAG_GEN = "generator"

    TAG_PROD_NAME = "product_name"
    TAG_PROD_VER = "product_version"
    TAG_SCHEMA_VER = "schema_version"
    TAG_TIMESTAMP = "timestamp"

    # CPE-ITEM ------------------------

    TAG_CPEITEM = "cpe-item"

    ATT_CPEITEM_NAME = "name"
    ATT_CPEITEM_DEPRECATEDBY = "deprecated_by"
    ATT_CPEITEM_DEPRECATED = "deprecated"
    ATT_CPEITEM_DEPDATE = "deprecation_date"

    # CPE23-ITEM ----------------------

    TAG_CPEITEM_23 = "cpe-23:cpe23-item"

    ATT_CPEITEM_23_NAME = "name"

    # TITLE ---------------------------

    TAG_TITLE = "title"
    ATT_TITLE_LANG = "xml:lang"

    # NOTES ---------------------------

    TAG_NOTE_LIST = "notes"
    TAG_NOTE = "note"
    ATT_NOTES_LANG = "xml:lang"

    # REFERENCE -----------------------

    TAG_REF_LIST = "references"
    TAG_REF = "reference"
    ATT_REF_HREF = "href"

    # CHECK ---------------------------

    TAG_CHECK = "check"
    ATT_CHECK_SYSTEM = "system"
    ATT_CHECK_HREF = "href"

    # DEPRECATION ---------------------

    TAG_DEPRECATION = "cpe-23:deprecation"
    ATT_DEPRECATION_DATE = "date"

    # DEPRECATED-BY -------------------

    TAG_DEPRECATEDBY = "cpe-23:deprecated-by"
    ATT_DEPRECATEDBY_TYPE = "type"
    ATT_DEPRECATEDBY_NAME = "name"

    # PROVENANCE-RECORD ---------------

    TAG_PROVRECORD = "cpe-23:provenance-record"
    ATT_PROVRECORD_DATE = "date"

    # CHANGE-DESCRIPCION --------------

    TAG_CHANGEDESC = "cpe-23:change-description"
    ATT_CHANGEDESC_TYPE = "change-type"
    ATT_CHANGEDESC_DATE = "date"

    # EVIDENCE-REFERENCE --------------

    TAG_EVIDENCEREF = "cpe-23:evidence-reference"
    ATT_EVIDENCEREF_EVIDENCE = "evidence"

    # COMMENTS ------------------------

    TAG_COMMENTS = "cpe-23:comments"

    # ORGANIZATION --------------------

    TAG_SUBMITTER = "cpe-23:submitter"
    TAG_AUTHORITY = "cpe-23:authority"
    ATT_ORG_SYSTEMID = "system-id"
    ATT_ORG_NAME = "name"
    ATT_ORG_DATE = "date"

    # DESCRIPTION ---------------------

    TAG_DESCRIPTION = "cpe-23:description"

    def __init__(self, *args, **kwargs):
        """
        Initialization of condition variables and objects to store input
        values.
        """

        self.inCpelist = False

        self.inGenerator = False

        self.inGenProdName = False

        self.inGenProdVer = False

        self.inGenSchemaVer = False

        self.inGenTimestamp = False

        self.inCpeitem = False

        self.inCpeitem23 = False

        self.inTitle = False

        self.inNote = False
        self.inNotelist = False

        self.inRef = False
        self.inReflist = False

        self.inCheck = False

        # Only in CPE Dictionary 2.3 ----------------------

        self.inDeprecation = False

        self.inProvrecord = False

        self.inChangedesc = False

        self.inEvidenceref = False

        self.inComment = False

        self.inAuthority = False

        self.inSubmitter = False

        self.inDescription = False

    def _startCpeList(self):
        """
        Analyzes the input opening tag corresponds to a cpe-list element.

        :returns: None
        """

        self.cpelist = CpeList()

        timenow = iso8601.datetime.now().isoformat()
        self.cpelist.name = timenow

        self.cpelist.save()

        self.inCpelist = True
        self.hasCpeitem23 = False

    def _startGenerator(self):
        """
        Analyzes the input opening tag corresponds to a generator element.

        :returns: None
        """

        self.generator = Generator()

        # Initializes the optional attributes of generator element
        self.generator.product_name = ""
        self.generator.product_version = ""

        self.inGenerator = True

    def _startCpeItem(self, attributes):
        """
        Analyzes the input opening tag corresponds to a cpe-item element.

        :param Atributes attributes: List of element attributes
        :returns: None
        """

        # Initialize variables associated with cpeitem element and
        # its subelements
        self.cpeitem_att = dict()
        self.titleList = []
        self.notesList = []
        self.refsList = []
        self.checkList = []
        self.deprecationList = []
        self.provrecord = None

        name = attributes.get(self.ATT_CPEITEM_NAME)
        self.cpeitem_att[self.ATT_CPEITEM_NAME] = name

        depby = attributes.get(self.ATT_CPEITEM_DEPRECATEDBY)
        self.cpeitem_att[self.ATT_CPEITEM_DEPRECATEDBY] = depby

        deprecated = attributes.get(self.ATT_CPEITEM_DEPRECATED)
        if deprecated is None:
            deprecated = False
        self.cpeitem_att[self.ATT_CPEITEM_DEPRECATED] = deprecated

        depdate = attributes.get(self.ATT_CPEITEM_DEPDATE)
        self.cpeitem_att[self.ATT_CPEITEM_DEPDATE] = depdate

        self.cpeitem_db = None
        self.inCpeitem = True

    def _startCpeItem23(self, attributes):
        """
        Analyzes the input opening tag corresponds to a cpe23-item element.

        :param Atributes attributes: List of element attributes
        :returns: None
        """

        self.cpeitem23_att = dict()

        # Save CPE Name version 2.2 only when not exist cpe23-item element.
        # If this element exist then only save CPE Name version 2.3
        self.hasCpeitem23 = True

        name = attributes.get(self.ATT_CPEITEM_23_NAME)
        self.cpeitem23_att[self.ATT_CPEITEM_23_NAME] = name

        self.provrecord = None

        self.inCpeitem23 = True

    def _startTitle(self, attributes):
        """
        Analyzes the input opening tag corresponds to a title element.

        :param Atributes attributes: List of element attributes
        :returns: None
        """

        language = attributes.get(self.ATT_TITLE_LANG)
        title_values = Title()
        title_values.language = language

        self.titleList.append(title_values)

        self.inTitle = True

    def _startNoteList(self, attributes):
        """
        Analyzes the input opening tag corresponds to a notes element.

        :param Atributes attributes: List of element attributes
        :returns: None
        """

        language = attributes.get(self.ATT_NOTES_LANG)

        self.notes_att = dict()
        self.notes_att[self.ATT_NOTES_LANG] = language

        self.inNotelist = True

    def _startNote(self):
        """
        Analyzes the input opening tag corresponds to a note element.

        :returns: None
        """

        note_values = Note()
        note_values.language = self.notes_att[self.ATT_NOTES_LANG]

        self.notesList.append(note_values)

        self.inNote = True

    def _startRef(self, attributes):
        """
        Analyzes the input opening tag corresponds to a reference element.

        :param Atributes attributes: List of element attributes
        :returns: None
        """

        href = attributes.get(self.ATT_REF_HREF)

        ref_values = Reference()
        ref_values.href = href

        self.refsList.append(ref_values)

        self.inRef = True

    def _startCheck(self, attributes):
        """
        Analyzes the input opening tag corresponds to a check element.

        :param Atributes attributes: List of element attributes
        :returns: None
        """

        system = attributes.get(self.ATT_CHECK_SYSTEM)
        href = attributes.get(self.ATT_CHECK_HREF)

        check_values = Check()
        check_values.system = system
        check_values.href = href

        self.checkList.append(check_values)

        self.inCheck = True

    def _startDeprecation(self, attributes):
        """
        Analyzes the input opening tag corresponds to a deprecation element.

        :param Atributes attributes: List of element attributes
        :returns: None
        """

        # Initialize variables associated with deprecation element and its
        # subelements
        self.deprecatedbyList = []

        depdate = attributes.get(self.ATT_DEPRECATION_DATE)

        dep_values = Deprecation()
        dep_values.dep_datetime = depdate
        self.deprecationList.append(dep_values)

        self.inDeprecation = True

    def _startDeprecatedBy(self, attributes):
        """
        Analyzes the input opening tag corresponds to a deprecated-by element.

        :param Atributes attributes: List of element attributes
        :returns: None
        """

        deptype = attributes.get(self.ATT_DEPRECATEDBY_TYPE)
        depname = attributes.get(self.ATT_DEPRECATEDBY_NAME)

        cpedata = self._saveCpe(depname, CPE.VERSION_2_3)

        depby_values = DeprecatedBy()
        depby_values.dep_type = get_deprecatedby_type_int(deptype)
        depby_values.name = cpedata

        # The last deprecation element read in XML file
        # because parser is analyzing it when read the deprecated-by element
        depby_values.deprecation = self.deprecationList[-1]

        self.deprecatedbyList.append(depby_values)

    def _startProvRecord(self):
        """
        Analyzes the input opening tag corresponds to a provenance record
        element.

        :returns: None
        """

        self.provrecord = ProvenanceRecord()

        # Initialize variables associated with subelements
        self.changedescList = []
        self.authorityList = []
        self.submitter = None

        self.inProvrecord = True

    def _startChangeDesc(self, attributes):
        """
        Analyzes the input opening tag corresponds
        to a change-description element.

        :param Atributes attributes: List of element attributes
        :returns: None
        """

        change_type = attributes.get(self.ATT_CHANGEDESC_TYPE)
        change_date = attributes.get(self.ATT_CHANGEDESC_DATE)

        changedesc_values = ChangeDescription()
        changedesc_values.change_type = get_change_type_int(change_type)
        changedesc_values.change_datetime = change_date

        self.changedescList.append(changedesc_values)

        self.evidenceref = None

        self.inChangedesc = True

    def _startEvidenceRef(self, attributes):
        """
        Analyzes the input opening tag corresponds
        to an evidence-reference element.

        :param Atributes attributes: List of element attributes
        :returns: None
        """

        evidence = attributes.get(self.ATT_EVIDENCEREF_EVIDENCE)

        self.evidenceref = EvidenceReference()
        self.evidenceref.evidence = get_evidence_type_int(evidence)

        self.inEvidenceref = True

    def _startSubmitter(self, attributes):
        """
        Analyzes the input opening tag corresponds
        to a submitter element.

        :param Atributes attributes: List of element attributes
        :returns: None
        """

        system_id = attributes.get(self.ATT_ORG_SYSTEMID)
        name = attributes.get(self.ATT_ORG_NAME)
        dt = attributes.get(self.ATT_ORG_DATE)

        self.submitter = Organization()
        self.submitter.system_id = system_id
        self.submitter.name = name
        self.submitter.action_datetime = dt

        self.inSubmitter = True

    def _startAuthority(self, attributes):
        """
        Analyzes the input opening tag corresponds to an authority element.

        :param Atributes attributes: List of element attributes
        :returns: None
        """

        system_id = attributes.get(self.ATT_ORG_SYSTEMID)
        name = attributes.get(self.ATT_ORG_NAME)
        dt = attributes.get(self.ATT_ORG_DATE)

        authority_values = Organization()
        authority_values.system_id = system_id
        authority_values.name = name
        authority_values.action_datetime = dt

        self.authorityList.append(authority_values)

        self.inAuthority = True

    def startElement(self, name, attributes):
        """
        Analyzes the input opening tag of an element.

        :param string name: The opening tag name of element
        :param Attributes attributes: List of element attributes
        :returns: None
        """

        # CPE-LIST --------------------

        if name == self.TAG_CPELIST:
            self._startCpeList()

        elif self.inCpelist:

            # GENERATOR ---------------

            if name == self.TAG_GEN:
                self._startGenerator()

            elif self.inGenerator:
                if name == self.TAG_PROD_NAME:
                    self.inGenProdName = True

                elif name == self.TAG_PROD_VER:
                    self.inGenProdVer = True

                elif name == self.TAG_SCHEMA_VER:
                    self.inGenSchemaVer = True

                elif name == self.TAG_TIMESTAMP:
                    self.inGenTimestamp = True

            # CPE-ITEM ----------------

            elif name == self.TAG_CPEITEM:
                self._startCpeItem(attributes)

            elif self.inCpeitem:

                # CPE23-ITEM ----------

                if name == self.TAG_CPEITEM_23:
                    self._startCpeItem23(attributes)

                elif self.inCpeitem23:

                    # DEPRECATION -----

                    if name == self.TAG_DEPRECATION:
                        self._startDeprecation(attributes)

                    elif self.inDeprecation:

                        # DEPRECATED-BY

                        if name == self.TAG_DEPRECATEDBY:
                            self._startDeprecatedBy(attributes)

                    # PROVENANCE-RECORD

                    elif name == self.TAG_PROVRECORD:
                        self._startProvRecord()

                    elif self.inProvrecord:

                        # CHANGE-DESCRIPCION

                        if name == self.TAG_CHANGEDESC:
                            self._startChangeDesc(attributes)

                        elif self.inChangedesc:

                            # EVIDENCE-REFERENCE

                            if name == self.TAG_EVIDENCEREF:
                                self._startEvidenceRef(attributes)

                            # COMMENTS

                            elif name == self.TAG_COMMENTS:
                                self.inComment = True

                        # SUBMITTER ---

                        elif name == self.TAG_SUBMITTER:
                            self._startSubmitter(attributes)

                        elif self.inSubmitter:

                            # DESCRIPTION

                            if name == self.TAG_DESCRIPTION:
                                self.inDescription = True

                        # AUTHORITY ---

                        elif name == self.TAG_AUTHORITY:
                            self._startSubmitter(attributes)

                        elif self.inAuthority:

                            # DESCRIPTION

                            if name == self.TAG_DESCRIPTION:
                                self.inDescription = True

                # TITLE ---------------

                elif name == self.TAG_TITLE:
                    self._startTitle(attributes)

                # NOTES ---------------

                elif name == self.TAG_NOTE_LIST:
                    self._startNoteList(attributes)

                elif self.inNotelist:

                    if name == self.TAG_NOTE:
                        self._startNote()

                # REFERENCE -----------

                elif name == self.TAG_REF_LIST:
                    self.inReflist = True

                elif self.inReflist:

                    if name == self.TAG_REF:
                        self._startRef(attributes)

                # CHECK ---------------

                elif name == self.TAG_CHECK:
                    self._startCheck(attributes)

    def characters(self, chars):
        """
        Analyzes the content of a XML element.

        :param string chars: The content of element as string
        :returns: None
        """

        print "CHAR: ", chars
        # GENERATOR -------------------

        if self.inGenerator:
            if self.inGenProdName:
                self.generator.product_name = chars
            if self.inGenProdVer:
                self.generator.product_version = chars
            if self.inGenSchemaVer:
                self.generator.schema_version = chars
            if self.inGenTimestamp:
                self.generator.timestamp = chars

        # TITLE -----------------------

        elif self.inTitle:
            # Set the content of last title element found
            self.titleList[-1].title = chars

        # NOTES -----------------------

        elif self.inNote:
            # Set the content of last note element found
            self.notesList[-1].note = chars

        # REFERENCE -------------------

        elif self.inRef:
            # Set the content of last reference element found
            self.refsList[-1].name = chars

        # CHECK -----------------------

        elif self.inCheck:
            # Set the content of last check element found
            self.checkList[-1].check_id = chars

        # EVIDENCE-REFERENCE ----------

        elif self.inEvidenceref:
            self.evidenceref.ref = chars

        # COMMENTS --------------------

        elif self.inComment:
            # Set the content of last change description element found
            self.changedescList[-1].comment = chars

        # DESCRIPTION -----------------

        elif self.inSubmitter:
            if self.inDescription:
                self.submitter.description = chars
                print "DESC SUB   ", self.submitter

        elif self.inAuthority:
            if self.inDescription:
                self.authorityList[-1].description = chars

    def _endGenerator(self):
        """
        Analyzes the input ending tag corresponds to a generator element.

        :returns: None
        """

        self.inGenerator = False

        # Generator element depends on cpe-list element
        self.generator.cpelist = self.cpelist
        self.generator.save()

    def _endChangeDescription(self):
        """
        Analyzes the input ending tag corresponds to a change description
        element.

        :returns: None
        """

        # Change description element depends on evidence reference element.
        # Assign the evidence reference to the last change description read
        # from XML file
        self.changedescList[-1].evidence = self.evidenceref

        self.inChangedesc = False

    def _endEvidenceReference(self):
        """
        Analyzes the input ending tag corresponds to an evidence reference
        element.

        :returns: None
        """

        self.evidenceref.save()
        self.inEvidenceref = False

    def _endSubmitter(self):
        """
        Analyzes the input ending tag corresponds to a submitter reference
        element.

        :returns: None
        """

        self.submitter.save()
        self.inSubmitter = False

    def _endAuthority(self):
        """
        Analyzes the input ending tag corresponds to an authority reference
        element.

        :returns: None
        """

        self.authorityList[-1].save()
        self.inAuthority = False

    def _saveCpe(self, cpe_str, version):
        """
        Save the input cpe name string into the database if not exist already.

        :param string cpe_str: The CPE Name to save
        :version string version: The CPE Name version
        :returns: The CPE Name saved or existing one
        :rtype: CpeData
        :raises:
            :NotImplementedError: invalid CPE Name with input version
        """

        try:
            cpe = CPE(cpe_str, version)
        except NotImplementedError:
            raise
        else:
            # Convert CPE Name to WFN style
            # because it is the default style in database

            cpe_wfn = CPE(cpe.as_wfn(), version)

            part = cpe_wfn.get_part()[0]
            vendor = cpe_wfn.get_vendor()[0]
            product = cpe_wfn.get_product()[0]
            version = cpe_wfn.get_version()[0]
            update = cpe_wfn.get_update()[0]
            edition = cpe_wfn.get_edition()[0]
            sw_edition = cpe_wfn.get_software_edition()[0]
            target_sw = cpe_wfn.get_target_software()[0]
            target_hw = cpe_wfn.get_target_hardware()[0]
            other = cpe_wfn.get_other()[0]
            language = cpe_wfn.get_language()[0]

            # Find out if CPE Name exists already
            cpe_list = CpeData.objects.filter(part=part,
                                              vendor=vendor,
                                              product=product,
                                              version=version,
                                              update=update,
                                              edition=edition,
                                              sw_edition=sw_edition,
                                              target_sw=target_sw,
                                              target_hw=target_hw,
                                              other=other,
                                              language=language)
            cpedata = None

            if len(cpe_list) == 0:
                # Save the new cpedata element

                cpedata = CpeData(part=part,
                                  vendor=vendor,
                                  product=product,
                                  version=version,
                                  update=update,
                                  edition=edition,
                                  sw_edition=sw_edition,
                                  target_sw=target_sw,
                                  target_hw=target_hw,
                                  other=other,
                                  language=language)

                cpedata.save()
            else:
                # Get the cpedata stored in the database
                cpedata = cpe_list[0]

            return cpedata

    def _endCpeItem(self):
        """
        Analyzes the input ending tag corresponds to a cpe-item element.

        :returns: None
        """

        self.inCpeitem = False

        # This name corresponds to version 2.2 of CPE.
        # It is necessary to check valid name and
        # save it only when not exist cpe23-item element.
        # If this element exist then only save CPE Name version 2.3
        cpe_str = self.cpeitem_att[self.ATT_CPEITEM_NAME]
        try:
            CPE(cpe_str, CPE.VERSION_2_2)
        except:
            errormsg = "Invalid CPE Name version 2.2 in cpe-item element: \
                {0}".format(cpe_str)
            raise ParserError(errormsg)
        else:
            cpedata = None

            depre = self.cpeitem_att[self.ATT_CPEITEM_DEPRECATED]
            depdate = self.cpeitem_att[self.ATT_CPEITEM_DEPDATE]

            if self.hasCpeitem23:

                # Check if CPE Name version 2.3 is valid
                cpe23_str = self.cpeitem23_att[self.ATT_CPEITEM_23_NAME]

                try:
                    cpedata = self._saveCpe(cpe23_str, CPE.VERSION_2_3)
                except:
                    errormsg = "Invalid CPE Name version 2.3 in cpe23-item \
                        element: {0}".format(cpe23_str)
                    raise ParserError(errormsg)
            else:
                cpedata = self._saveCpe(cpe_str, CPE.VERSION_2_2)

            # Save the cpeitem element
            self.cpeitem_db = CpeItem(deprecated=depre,
                                      deprecation_date=depdate,
                                      name=cpedata,
                                      cpelist=self.cpelist)
            self.cpeitem_db.save()

            if len(self.titleList) > 0:
                # Title elements must be saved after cpe-item element
                # because of the dependency between each other
                for tit in self.titleList:
                    tit.cpeitem = self.cpeitem_db
                    tit.save()

            if len(self.notesList) > 0:
                # Note elements must be saved after cpe-item element
                # because of the dependency between each other
                for note in self.notesList:
                    note.cpeitem = self.cpeitem_db
                    note.save()

            if len(self.refsList) > 0:
                # Reference elements must be saved after cpe-item element
                # because of the dependency between each other
                for ref in self.refsList:
                    ref.cpeitem = self.cpeitem_db
                    ref.save()

            if len(self.checkList) > 0:
                # Check elements must be saved after cpe-item element
                # because of the dependency between each other
                for check in self.checkList:
                    check.cpeitem = self.cpeitem_db
                    check.save()

            if self.hasCpeitem23:

                if len(self.deprecationList) > 0:
                    # Deprecation elements must be saved after cpe-item element
                    # because of the dependency between each other
                    for dep in self.deprecationList:
                        dep.cpeitem = self.cpeitem_db
                        dep.save()

                        # Save all deprecated-by element associated with
                        # the deprecation element saved

                        if len(self.deprecatedbyList) > 0:
                            # Deprecated-by elems must be saved after cpe-item
                            # elem because of the dependency with deprecation
                            # element
                            for depby in self.deprecatedbyList:
                                depby.deprecation = dep
                                depby.save()

                if self.provrecord is not None:
                    # Provenance Record element exists. Assign cpe23-item and
                    # submitter
                    self.provrecord.cpeitem = self.cpeitem_db
                    self.provrecord.submitter = self.submitter

                    # Save prov record
                    self.provrecord.save()

                    # Change Description elements must be saved after
                    # provenance record element
                    # because of the dependency between each other
                    for chandesc in self.changedescList:
                        chandesc.prov_record = self.provrecord
                        chandesc.save()

                    # Set many-to-many relationship between authority element
                    # and provenance record element
                    for auth in self.authorityList:
                        self.provrecord.authorities.add(auth)

            self.hasCpeitem23 = False

    def endElement(self, name):
        """
        Analyzes the input ending tag of an element.

        :param string name: The ending tag name
        :returns: None
        """

        # CPE-LIST --------------------

        if name == self.TAG_CPELIST:
            self.inCpelist = False

        elif self.inCpelist:

            # GENERATOR ---------------

            if name == self.TAG_GEN:
                self._endGenerator()

            elif self.inGenerator:

                if name == self.TAG_PROD_NAME:
                    self.inGenProdName = False

                elif name == self.TAG_PROD_VER:
                    self.inGenProdVer = False

                elif name == self.TAG_SCHEMA_VER:
                    self.inGenSchemaVer = False

                elif name == self.TAG_TIMESTAMP:
                    self.inGenTimestamp = False

            # CPE-ITEM ----------------

            elif name == self.TAG_CPEITEM:
                self._endCpeItem()

            elif self.inCpeitem:

                # CPE23-ITEM ----------

                if name == self.TAG_CPEITEM_23:
                    self.inCpeitem23 = False

                elif self.inCpeitem23:

                    # DEPRECATION -----

                    if name == self.TAG_DEPRECATION:
                        self.inDeprecation = False

                    # PROVENANCE-RECORD

                    elif name == self.TAG_PROVRECORD:
                        self.inProvrecord = False

                    elif self.inProvrecord:

                        # CHANGE-DESCRIPCION

                        if name == self.TAG_CHANGEDESC:
                            self._endChangeDescription()

                        elif self.inChangedesc:

                            # EVIDENCE-REFERENCE

                            if name == self.TAG_EVIDENCEREF:
                                self._endEvidenceReference()

                            # COMMENTS

                            if name == self.TAG_COMMENTS:
                                self.inComment = False

                        # SUBMITTER ---

                        elif name == self.TAG_SUBMITTER:
                            self._endSubmitter()

                        elif self.inSubmitter:

                            # DESCRIPTION

                            if name == self.TAG_DESCRIPTION:
                                self.inDescription = False

                        # AUTHORITY ---

                        elif name == self.TAG_AUTHORITY:
                            self._endAuthority()

                        elif self.inAuthority:

                            # DESCRIPTION

                            if name == self.TAG_DESCRIPTION:
                                self.inDescription = False

                # TITLE ---------------

                elif name == self.TAG_TITLE:
                    self.inTitle = False

                # NOTES ---------------

                elif name == self.TAG_NOTE_LIST:
                    self.inNotelist = False

                elif self.inNotelist:

                    if name == self.TAG_NOTE:
                        self.inNote = False

                # REFERENCE -----------

                elif name == self.TAG_REF_LIST:
                    self.inReflist = False

                elif self.inReflist:

                    if name == self.TAG_REF:
                        self.inRef = False

                # CHECK ---------------

                elif name == self.TAG_CHECK:
                    self.inCheck = False
