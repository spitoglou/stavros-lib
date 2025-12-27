"""Tests for XML utilities"""

import pytest
from lxml.etree import XMLSyntaxError

from stavroslib.xml import remove_namespace, xml_to_dict


class TestXmlToDict:
    def test_simple_xml(self):
        xml = "<root><item>value</item></root>"
        result = xml_to_dict(xml)
        assert result == {"root": {"item": "value"}}

    def test_xml_with_attributes(self):
        xml = '<root id="123"><item>value</item></root>'
        result = xml_to_dict(xml)
        assert result == {"root": {"@id": "123", "item": "value"}}

    def test_nested_xml(self):
        xml = "<root><parent><child>value</child></parent></root>"
        result = xml_to_dict(xml)
        assert result == {"root": {"parent": {"child": "value"}}}

    def test_repeated_elements(self):
        xml = "<items><item>1</item><item>2</item><item>3</item></items>"
        result = xml_to_dict(xml)
        assert result == {"items": {"item": ["1", "2", "3"]}}

    def test_mixed_content_with_attributes(self):
        xml = '<root id="1">text<child>value</child></root>'
        result = xml_to_dict(xml)
        assert result == {"root": {"@id": "1", "#text": "text", "child": "value"}}

    def test_empty_element(self):
        xml = "<root><empty/></root>"
        result = xml_to_dict(xml)
        assert result == {"root": {"empty": None}}

    def test_element_with_only_attributes(self):
        xml = '<root><item id="1" name="test"/></root>'
        result = xml_to_dict(xml)
        assert result == {"root": {"item": {"@id": "1", "@name": "test"}}}

    def test_complex_nested_structure(self):
        xml = """
        <catalog>
            <book id="1">
                <title>Book One</title>
                <author>Author A</author>
            </book>
            <book id="2">
                <title>Book Two</title>
                <author>Author B</author>
            </book>
        </catalog>
        """
        result = xml_to_dict(xml)
        assert "catalog" in result
        assert "book" in result["catalog"]
        assert isinstance(result["catalog"]["book"], list)
        assert len(result["catalog"]["book"]) == 2

    def test_invalid_xml_raises_error(self):
        xml = "<root><unclosed>"
        with pytest.raises(XMLSyntaxError):
            xml_to_dict(xml)

    def test_whitespace_handling(self):
        xml = "<root>  value with spaces  </root>"
        result = xml_to_dict(xml)
        assert result == {"root": "value with spaces"}


class TestRemoveNamespace:
    def test_simple_namespace(self):
        xml = '<root xmlns="http://example.com"><item>value</item></root>'
        result = remove_namespace(xml)
        assert "xmlns" not in result
        assert "<root>" in result
        assert "<item>value</item>" in result

    def test_multiple_namespaces(self):
        xml = """<root xmlns="http://example.com" xmlns:custom="http://custom.com">
                    <custom:item>value</custom:item>
                 </root>"""
        result = remove_namespace(xml)
        assert "xmlns" not in result
        assert "<item>value</item>" in result

    def test_preserve_content(self):
        xml = '<root xmlns="http://example.com"><item attr="test">value</item></root>'
        result = remove_namespace(xml)
        assert 'attr="test"' in result
        assert "<item" in result
        assert "value</item>" in result

    def test_no_namespace(self):
        xml = "<root><item>value</item></root>"
        result = remove_namespace(xml)
        assert "<root>" in result
        assert "<item>value</item>" in result

    def test_nested_namespaced_elements(self):
        xml = """<root xmlns="http://example.com">
                    <parent xmlns:ns="http://ns.com">
                        <ns:child>value</ns:child>
                    </parent>
                 </root>"""
        result = remove_namespace(xml)
        assert "xmlns" not in result
        assert "<child>value</child>" in result

    def test_preserve_element_structure(self):
        xml = '<root xmlns="http://example.com"><a><b><c>deep</c></b></a></root>'
        result = remove_namespace(xml)
        assert "<a><b><c>deep</c></b></a>" in result
