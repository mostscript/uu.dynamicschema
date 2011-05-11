from hashlib import md5

from plone.supermodel import loadString
from zope import schema
from zope.interface.common.mapping import IMapping
from xml.parsers.expat import ExpatError

from uu.record.interfaces import IRecord


DEFAULT_MODEL_XML = """
<model xmlns="http://namespaces.plone.org/supermodel/schema">
  <schema />
</model>
""".strip()

DEFAULT_SIGNATURE = md5(DEFAULT_MODEL_XML.strip()).hexdigest()


def valid_xml_schema(xml):
    if not xml or xml == DEFAULT_MODEL_XML:
        return True #bypass
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
    
    def sign(schema):
        """
        Given schema as an interface object, serialize schema to XML, save
        serialization in ISchemaSaver local/persistent utility, and save
        self.signature as the MD5 hexdigest of the XML serialization 
        stripped of trailing, leading whitespace.
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

