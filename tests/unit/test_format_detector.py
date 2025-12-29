"""Unit tests for format detector."""

import pytest
from langflow_toon.detectors.format_detector import FormatDetector


class TestFormatDetector:
    """Test suite for FormatDetector class."""

    def setup_method(self):
        """Setup test fixtures."""
        self.detector = FormatDetector()

    def test_json_detection(self):
        """Test detection of JSON format."""
        json_object = '{"name": "John", "age": 30}'
        json_array = '[1, 2, 3, 4, 5]'

        assert self.detector.detect(json_object) == "JSON"
        assert self.detector.detect(json_array) == "JSON"

    def test_xml_detection(self):
        """Test detection of XML format."""
        xml_with_decl = '<?xml version="1.0"?><root></root>'
        xml_simple = '<root><item>value</item></root>'
        xml_custom = '<data><nested>value</nested></data>'

        assert self.detector.detect(xml_with_decl) == "XML"
        assert self.detector.detect(xml_simple) == "XML"
        assert self.detector.detect(xml_custom) == "XML"

    def test_csv_detection(self):
        """Test detection of CSV format."""
        csv_comma = "name,age,city\nJohn,30,Bangkok"
        csv_tab = "name\tage\tcity\nJohn\t30\tBangkok"
        csv_pipe = "name|age|city\nJohn|30|Bangkok"

        assert self.detector.detect(csv_comma) == "CSV"
        assert self.detector.detect(csv_tab) == "CSV"
        assert self.detector.detect(csv_pipe) == "CSV"

    def test_html_detection(self):
        """Test detection of HTML format."""
        html_simple = '<html><body></body></html>'
        html_with_doctype = '<!DOCTYPE html><html></html>'
        html_divs = '<div><span>Content</span></div>'

        assert self.detector.detect(html_simple) == "HTML"
        assert self.detector.detect(html_with_doctype) == "HTML"
        assert self.detector.detect(html_divs) == "HTML"

    def test_fallback_to_json(self):
        """Test that JSON-like content falls back to JSON detection."""
        json_like = '{"key": "value"}'

        result = self.detector.detect(json_like)
        assert result == "JSON"

    def test_empty_input(self):
        """Test detection with empty input."""
        empty = ""
        whitespace = "   \n\t   "

        assert self.detector.detect(empty) is None
        assert self.detector.detect(whitespace) is None

    def test_invalid_json(self):
        """Test that invalid JSON doesn't get detected as JSON."""
        invalid_json = '{not valid json}'

        # Should not detect as JSON
        result = self.detector.detect(invalid_json)
        # May return None or another format
        assert result != "JSON"

    def test_mixed_content(self):
        """Test detection with mixed/ambiguous content."""
        # Content that looks like JSON but has HTML-like parts
        mixed = '{"html": "<div>content</div>"}'

        # Should detect as JSON (starts with {)
        assert self.detector.detect(mixed) == "JSON"

    def test_xml_vs_html_distinction(self):
        """Test that XML and HTML are properly distinguished."""
        xml_custom = '<customtag>data</customtag>'
        html_tag = '<div>data</div>'

        xml_result = self.detector.detect(xml_custom)
        html_result = self.detector.detect(html_tag)

        # Custom tags should be XML
        assert xml_result == "XML"
        # Standard HTML tags should be HTML
        assert html_result == "HTML"

    def test_csv_with_quotes(self):
        """Test CSV detection with quoted fields containing commas."""
        csv_quoted = 'name,description\n"John, Doe","Developer, AI"'

        assert self.detector.detect(csv_quoted) == "CSV"

    def test_number_alone(self):
        """Test that plain numbers are not detected as any format."""
        number = "12345"

        # Should return None for plain numbers
        result = self.detector.detect(number)
        assert result is None
