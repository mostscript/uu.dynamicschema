from hashlib import md5

from plone.supermodel import loadString
from zope import schema
from zope.interface import Interface
from zope.interface.common.mapping import IMapping
from xml.parsers.expat import ExpatError

from uu.record.interfaces import IRecord

# various package globals:

PKGNAME = 'uu.dynamicschema'

DEFAULT_MODEL_XML = (
    '<model xmlns:security="http://namespaces.plone.org/supermodel/security" '
    'xmlns:marshal="http://namespaces.plone.org/supermodel/marshal" '
    'xmlns:form="http://namespaces.plone.org/supermodel/form" '
    'xmlns="http://namespaces.plone.org/supermodel/schema">\n'
    '  <schema/>\n'
    '</model>'
    ).strip()

DEFAULT_SIGNATURE = md5(DEFAULT_MODEL_XML.strip()).hexdigest()


def valid_xml_schema(xml):
    if not xml or xml == DEFAULT_MODEL_XML:
        return True  # bypass
    try:
        return loadString(xml)
    except ExpatError:
        raise schema.ValidationError('could not parse field schema xml')
    return True


class ISchemaSignedEntity(IRecord):
    """
    An entity that is signed with the signature of a persisted dynamic
    interface/schema object.  The signature is the md5 hexidecimal digest
    of the XML serialization of the schema provided by plone.supermodel.

    Entity is also:

      * a location with __name__ and __parent__ attributes of
        ILocation ancestor interface (via IRecord).

        __parent__ should normatively be the content-ish container of
        the entity records, but may be some other context.

      * A record with a string-representation UUID attribute record_uid
        (via IRecord).

    """

    signature = schema.BytesLine(
        title=u'Schema signature',
        description=u'MD5 hex-digest signature of XML serialized schema',
        required=False,
        )

    def sign(schema, usedottedname=False):
        """
        Given schema as an interface object, serialize schema to XML, save
        serialization in ISchemaSaver local/persistent utility, and save
        self.signature as the MD5 hexdigest of the XML serialization
        stripped of trailing, leading whitespace.

        If usedottedname is true, and schema has a proper identifier NOT
        sourced from a dynamic module namespace (that is, it can be
        resolved in a real python module namespace), then the signature
        will be stored as a resolvable dotted name instead of an MD5
        signature.
        """


class ISchemaSaver(IMapping):
    """
    Mapping to persist xml schema from plone.supermodel. Values are
    xml stripped of trailing/leading whitespace, keys are md5 hexidecimal
    digest signatures of the XML serialization of the schema.

    Meant for use as a persistent (local) utility to save and lookup
    schema xml by md5 signature.
    """

    def signature(schema):
        """
        Return md5 signature for xml or interface object provided as
        schema (resulting xml will have leading/trailing whitespace
        stripped prior to obtaining a digest).
        """

    def add(schema):
        """
        given schema as xml or interface, save to mapping, return md5
        signature for the saved xml serialization.  XML value will
        have leading/trailing whitespace stripped prior to saving and
        obtaining a digest via signature().
        """

    def load(xml):
        """Given xml for schema, load/return interface/schema object"""

    def invalidate(schema):
        """invalidate transient cached/loaded interface/schema object"""


class ISchemaImportExport(Interface):
    """
    Adapter interface for export of all schemas to/from zip file.  Should
    adapt schema saver, but may be constructed to get a default schema saver
    on construction (implementation-specific).

    Key/value conventions:

     * File name is [MD5sum].xml
     * File content is supermodel-parsable XML of schema.
    """

    def load(stream):
        """
        Given stream or filename to a zip file, import contained
        schemas from it.  Filenames and contents must match conventions
        described above.
        """

    def dump(stream=None):
        """
        Return a stream, or write to an existing one.
        """

