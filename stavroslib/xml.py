"""XML Parsing and Manipulation Utilities"""

import io
from collections import defaultdict
from typing import Any

from lxml import etree
from lxml.etree import _Element


def xml_to_dict(xml_string: str) -> dict[str, Any]:
    """Parse XML string into a nested Python dictionary.

    Element attributes are prefixed with '@', text content uses '#text' key
    when mixed with children/attributes. Repeated elements become lists.

    Arguments:
        xml_string: The XML string to parse.

    Returns:
        A nested dictionary representing the XML structure.

    Raises:
        XMLSyntaxError: If the XML is malformed.
    """
    root = etree.fromstring(xml_string.encode("utf-8"))
    return _etree_to_dict(root)


def _etree_to_dict(t: _Element) -> dict[str, Any]:
    """Convert an ElementTree element to a dictionary (internal helper)."""
    d: dict[str, Any] = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd: defaultdict[str, list[Any]] = defaultdict(list)
        for dc in map(_etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if t.attrib:
        if d[t.tag] is None:
            d[t.tag] = {}
        d[t.tag].update(("@" + str(k), v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                if d[t.tag] is None:
                    d[t.tag] = {}
                d[t.tag]["#text"] = text
        else:
            d[t.tag] = text
    return d


def remove_namespace(xml_string: str) -> str:
    """Remove namespaces from XML document using XSLT transformation.

    Arguments:
        xml_string: The XML string with namespaces.

    Returns:
        XML string with namespaces removed, preserving structure and content.
    """
    xslt = """<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="xml" indent="no"/>

    <xsl:template match="/|comment()|processing-instruction()">
        <xsl:copy>
        <xsl:apply-templates/>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="*">
        <xsl:element name="{local-name()}">
        <xsl:apply-templates select="@*|node()"/>
        </xsl:element>
    </xsl:template>

    <xsl:template match="@*">
        <xsl:attribute name="{local-name()}">
        <xsl:value-of select="."/>
        </xsl:attribute>
    </xsl:template>
    </xsl:stylesheet>
    """

    dom = etree.fromstring(xml_string.encode("utf-8"))
    xslt_doc = etree.parse(io.BytesIO(xslt.encode("utf-8")))
    transform = etree.XSLT(xslt_doc)
    result = transform(dom)

    return etree.tostring(result, encoding="unicode")
