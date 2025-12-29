"""Unit tests for JSON converter."""

import pytest
from langflow_toon.converters.json_converter import JsonConverter
from langflow_toon.models.data import ConversionConfig
from langflow_toon.models.errors import ConversionError


class TestJsonConverter:
    """Test suite for JsonConverter class."""

    def setup_method(self):
        """Setup test fixtures."""
        self.converter = JsonConverter()
        self.config = ConversionConfig()

    def test_valid_json(self):
        """Test conversion of valid JSON input."""
        json_input = '{"name": "John", "age": 30, "city": "Bangkok"}'
        result = self.converter.convert(json_input, self.config)

        print(f"\n--- test_valid_json ---")
        print(f"INPUT:  {json_input}")
        print(f"OUTPUT: {result.toon_output}")
        print(f"Tokens: {result.original_tokens} -> {result.toon_tokens} (reduction: {result.token_reduction})")

        assert result.toon_output is not None
        assert len(result.toon_output) > 0
        assert result.original_tokens > 0
        assert result.toon_tokens > 0
        assert isinstance(result.warnings, list)

    def test_malformed_json(self):
        """Test handling of malformed JSON input."""
        malformed_json = '{invalid json}'

        with pytest.raises(ConversionError) as exc_info:
            self.converter.convert(malformed_json, self.config)

        assert "INVALID_JSON" in str(exc_info.value)

    def test_nested_json(self):
        """Test conversion of nested JSON structure."""
        nested_json = '''
        {
            "user": {
                "name": "John",
                "address": {
                    "city": "Bangkok",
                    "country": "Thailand"
                }
            },
            "tags": ["developer", "python"]
        }
        '''
        result = self.converter.convert(nested_json, self.config)

        print(f"\n--- test_nested_json ---")
        print(f"INPUT (nested):  {{...}}")
        print(f"OUTPUT: {result.toon_output}")
        print(f"Tokens: {result.original_tokens} -> {result.toon_tokens}")

        assert result.toon_output is not None
        assert result.original_tokens > 0
        assert result.toon_tokens > 0

    def test_empty_json(self):
        """Test conversion of empty JSON object."""
        empty_json = '{}'
        result = self.converter.convert(empty_json, self.config)

        print(f"\n--- test_empty_json ---")
        print(f"INPUT: {empty_json}")
        print(f"OUTPUT: '{result.toon_output}'")

        # Empty dict produces empty or minimal output
        assert result.toon_output == '' or result.toon_output == '{}'

    def test_json_array(self):
        """Test conversion of JSON array."""
        array_json = '[1, 2, 3, 4, 5]'
        result = self.converter.convert(array_json, self.config)

        assert result.toon_output is not None
        assert result.toon_output.startswith('[')

    def test_json_with_special_characters(self):
        """Test JSON with special characters."""
        special_json = r'{"text": "Hello\nWorld\t!"}'
        result = self.converter.convert(special_json, self.config)

        assert result.toon_output is not None

    def test_json_with_unicode(self):
        """Test JSON with Unicode characters."""
        unicode_json = '{"name": "สมชาย", "city": "กรุงเทพฯ"}'
        result = self.converter.convert(unicode_json, self.config)

        assert result.toon_output is not None
        assert "สมชาย" in result.toon_output or "name" in result.toon_output
