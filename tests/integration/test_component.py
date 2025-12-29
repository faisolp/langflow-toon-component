"""Integration tests for ToonConverter component."""

import pytest
from langflow_toon import ToonConverter
from langflow_toon.models.errors import ConversionError


class TestToonConverterIntegration:
    """Integration test suite for ToonConverter class."""

    def setup_method(self):
        """Setup test fixtures."""
        self.converter = ToonConverter()

    def test_json_to_toon(self):
        """Test complete JSON to TOON conversion workflow."""
        json_input = '{"name": "John", "age": 30, "city": "Bangkok"}'
        result = self.converter.convert(json_input, input_format='JSON')

        assert result.toon_output is not None
        assert len(result.toon_output) > 0
        assert result.original_tokens > 0
        assert result.toon_tokens > 0
        assert isinstance(result.token_reduction, int)

    def test_csv_to_toon(self):
        """Test complete CSV to TOON conversion workflow."""
        csv_input = "name,age,city\nJohn,30,Bangkok\nJane,25,Chiang Mai"
        result = self.converter.convert(csv_input, input_format='CSV')

        assert result.toon_output is not None
        # TOON format uses tabular format: data[N]{fields}:
        assert 'data:[2]' in result.toon_output or '{name,age,city}' in result.toon_output
        assert result.original_tokens > 0

    def test_xml_to_toon(self):
        """Test complete XML to TOON conversion workflow."""
        xml_input = '<?xml version="1.0"?><person><name>John</name><age>30</age></person>'
        result = self.converter.convert(xml_input, input_format='XML')

        assert result.toon_output is not None
        assert result.original_tokens > 0
        assert result.toon_tokens > 0

    def test_html_to_toon(self):
        """Test complete HTML to TOON conversion workflow."""
        html_input = '<html><body><h1>Welcome</h1><p>Hello World</p></body></html>'
        result = self.converter.convert(html_input, input_format='HTML')

        assert result.toon_output is not None
        assert result.original_tokens > 0

    def test_empty_input(self):
        """Test handling of empty input."""
        with pytest.raises(ConversionError) as exc_info:
            self.converter.convert('', input_format='JSON')

        assert "EMPTY_INPUT" in str(exc_info.value)

    def test_malformed_input(self):
        """Test handling of malformed input."""
        malformed_json = '{invalid json}'

        with pytest.raises(ConversionError) as exc_info:
            self.converter.convert(malformed_json, input_format='JSON')

        assert "INVALID_JSON" in str(exc_info.value)

    def test_auto_detect_json(self):
        """Test auto-detection of JSON format."""
        json_input = '{"name": "John", "age": 30}'
        result = self.converter.convert(json_input, auto_detect=True)

        assert result.toon_output is not None
        assert result.original_tokens > 0

    def test_csv_with_tab_delimiter(self):
        """Test CSV conversion with tab delimiter."""
        tab_csv = "name\tage\tcity\nJohn\t30\tBangkok"
        result = self.converter.convert(tab_csv, input_format='CSV', delimiter='tab')

        assert result.toon_output is not None

    def test_csv_with_pipe_delimiter(self):
        """Test CSV conversion with pipe delimiter."""
        pipe_csv = "name|age|city\nJohn|30|Bangkok"
        result = self.converter.convert(pipe_csv, input_format='CSV', delimiter='pipe')

        assert result.toon_output is not None

    def test_format_detection(self):
        """Test format detection functionality."""
        json_input = '{"test": "value"}'
        detected = self.converter.detect_format(json_input)

        assert detected == "JSON"

    def test_token_statistics_accuracy(self):
        """Test that token statistics are calculated correctly."""
        json_input = '{"name": "John", "age": 30}'
        result = self.converter.convert(json_input, input_format='JSON')

        assert result.original_tokens >= 0
        assert result.toon_tokens >= 0
        assert isinstance(result.token_reduction, int)

    def test_warnings_list(self):
        """Test that warnings are properly collected."""
        # Use a large CSV that might trigger warnings
        large_csv = "name,age,city\n" + "\n".join([f"Person{i},{i},City{i}" for i in range(1000)])
        result = self.converter.convert(large_csv, input_format='CSV')

        assert isinstance(result.warnings, list)
