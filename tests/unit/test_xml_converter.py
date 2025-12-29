"""Unit tests for XML converter."""

import pytest
from langflow_toon.converters.xml_converter import XmlConverter
from langflow_toon.models.data import ConversionConfig
from langflow_toon.models.errors import ConversionError


class TestXmlConverter:
    """Test suite for XmlConverter class."""

    def setup_method(self):
        """Setup test fixtures."""
        self.converter = XmlConverter()
        self.config = ConversionConfig()

    def test_valid_xml(self):
        """Test conversion of valid XML input."""
        xml_input = '<?xml version="1.0"?><person><name>John</name><age>30</age></person>'
        result = self.converter.convert(xml_input, self.config)

        print(f"\n--- test_valid_xml ---")
        print(f"INPUT (XML): {xml_input}")
        print(f"OUTPUT (TOON): {result.toon_output}")
        print(f"Tokens: {result.original_tokens} -> {result.toon_tokens}")

        assert result.toon_output is not None
        assert len(result.toon_output) > 0
        assert result.original_tokens > 0
        assert result.toon_tokens > 0

    def test_malformed_xml(self):
        """Test handling of malformed XML input."""
        malformed_xml = '<person><name>John</age></person>'

        # xmltodict will raise exception for malformed XML
        with pytest.raises(Exception):
            self.converter.convert(malformed_xml, self.config)

    def test_nested_xml(self):
        """Test conversion of nested XML structure."""
        nested_xml = '''
        <root>
            <user>
                <name>John</name>
                <address>
                    <city>Bangkok</city>
                    <country>Thailand</country>
                </address>
            </user>
        </root>
        '''
        result = self.converter.convert(nested_xml, self.config)

        assert result.toon_output is not None
        assert result.original_tokens > 0

    def test_xml_with_attributes(self):
        """Test XML with element attributes."""
        xml_with_attrs = '<person id="1" active="true"><name>John</name></person>'
        result = self.converter.convert(xml_with_attrs, self.config)

        assert result.toon_output is not None

    def test_xml_mixed_content(self):
        """Test XML with mixed content (text and elements)."""
        mixed_xml = '<p>Hello <b>World</b>!</p>'
        result = self.converter.convert(mixed_xml, self.config)

        assert result.toon_output is not None

    def test_xml_with_cdata(self):
        """Test XML with CDATA sections."""
        cdata_xml = '<data><![CDATA[Special <characters> here]]></data>'
        result = self.converter.convert(cdata_xml, self.config)

        assert result.toon_output is not None

    def test_empty_xml(self):
        """Test conversion of empty XML element."""
        empty_xml = '<root></root>'
        result = self.converter.convert(empty_xml, self.config)

        assert result.toon_output is not None
