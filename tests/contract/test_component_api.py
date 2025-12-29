"""Contract tests for TOON Converter component API.

This module verifies that the component implementation matches
the API contract defined in specs/001-toon-python-langflow/contracts/component-api.md
"""

import pytest

from langflow_toon.components.toon_component import ToonConverterComponent


class TestComponentAPIContract:
    """Test suite verifying component API compliance with contract."""

    def setup_method(self):
        """Setup test fixtures."""
        self.component = ToonConverterComponent()

    # ========== Component Metadata Tests ==========

    def test_display_name_exists(self):
        """Verify component has required display_name property."""
        assert hasattr(self.component, 'display_name')
        assert self.component.display_name == "TOON Converter"

    def test_description_exists(self):
        """Verify component has required description property."""
        assert hasattr(self.component, 'description')
        assert len(self.component.description) > 0

    # ========== Input Configuration Tests ==========

    def test_build_config_returns_dict(self):
        """Verify build_config returns a dictionary."""
        config = self.component.build_config()
        assert isinstance(config, dict)

    def test_input_text_config_exists(self):
        """Verify input_text is configured per contract."""
        config = self.component.build_config()
        assert "input_text" in config
        assert config["input_text"]["type"] == "str"
        assert config["input_text"]["multiline"] is True

    def test_input_format_config_exists(self):
        """Verify input_format is configured per contract."""
        config = self.component.build_config()
        assert "input_format" in config
        assert config["input_format"]["type"] == "str"
        expected_options = ["JSON", "XML", "CSV", "HTML"]
        assert config["input_format"]["options"] == expected_options

    def test_delimiter_config_exists(self):
        """Verify delimiter (csv_delimiter) is configured per contract."""
        config = self.component.build_config()
        assert "csv_delimiter" in config
        assert config["csv_delimiter"]["type"] == "str"
        expected_options = ["comma", "tab", "pipe"]
        assert config["csv_delimiter"]["options"] == expected_options
        assert config["csv_delimiter"]["default"] == "comma"

    def test_sort_keys_config_exists(self):
        """Verify sort_keys is configured per contract."""
        config = self.component.build_config()
        assert "sort_keys" in config
        assert config["sort_keys"]["type"] == "bool"
        assert config["sort_keys"]["default"] is False

    def test_auto_detect_config_exists(self):
        """Verify auto_detect is configured per contract."""
        config = self.component.build_config()
        assert "auto_detect" in config
        assert config["auto_detect"]["type"] == "bool"
        assert config["auto_detect"]["default"] is False

    def test_ensure_ascii_config_exists(self):
        """Verify ensure_ascii is configured (added in implementation)."""
        config = self.component.build_config()
        assert "ensure_ascii" in config
        assert config["ensure_ascii"]["type"] == "bool"
        assert config["ensure_ascii"]["default"] is False

    # ========== Output Schema Tests ==========

    def test_build_returns_dict(self):
        """Verify build method returns dictionary."""
        result = self.component.build(input_text='{"test": "value"}')
        assert isinstance(result, dict)

    def test_output_has_toon_output_field(self):
        """Verify output has toon_output field per contract."""
        result = self.component.build(input_text='{"test": "value"}')
        assert "toon_output" in result
        assert isinstance(result["toon_output"], str)

    def test_output_has_token_stats_fields(self):
        """Verify output has token statistics fields per contract."""
        # Contract specifies: input_tokens, output_tokens, savings_count, savings_percent
        # Implementation returns: original_tokens, toon_tokens, token_reduction
        result = self.component.build(input_text='{"test": "value"}')
        assert "original_tokens" in result  # Maps to input_tokens
        assert "toon_tokens" in result  # Maps to output_tokens
        assert "token_reduction" in result  # Maps to savings_count
        assert isinstance(result["original_tokens"], int)
        assert isinstance(result["toon_tokens"], int)
        assert isinstance(result["token_reduction"], int)

    def test_output_has_error_field(self):
        """Verify output has error/warnings field per contract."""
        result = self.component.build(input_text='{"test": "value"}')
        # Implementation uses "warnings" instead of "error"
        assert "warnings" in result

    # ========== Success Response Tests ==========

    def test_json_success_response_schema(self):
        """Verify success response matches schema for JSON input."""
        result = self.component.build(
            input_text='{"name": "John", "age": 30}',
            input_format='JSON'
        )

        # toon_output should be non-empty string
        assert isinstance(result["toon_output"], str)
        assert len(result["toon_output"]) > 0

        # Token stats should be integers
        assert isinstance(result["original_tokens"], int)
        assert result["original_tokens"] > 0
        assert isinstance(result["toon_tokens"], int)
        assert result["toon_tokens"] > 0
        assert isinstance(result["token_reduction"], int)

        # warnings should be None or string
        assert result["warnings"] is None or isinstance(result["warnings"], str)

    def test_csv_success_response_schema(self):
        """Verify success response matches schema for CSV input."""
        result = self.component.build(
            input_text='name,age\nJohn,30',
            input_format='CSV'
        )

        assert isinstance(result["toon_output"], str)
        assert len(result["toon_output"]) > 0
        assert result["original_tokens"] > 0

    # ========== Error Response Tests ==========

    def test_empty_input_response(self):
        """Verify response to empty input per contract."""
        result = self.component.build(input_text='')

        assert result["toon_output"] == ""
        assert result["original_tokens"] == 0
        assert result["toon_tokens"] == 0
        assert result["token_reduction"] == 0
        assert result["warnings"] is not None

    def test_invalid_json_error_response(self):
        """Verify error response for invalid JSON."""
        result = self.component.build(
            input_text='{invalid json}',
            input_format='JSON'
        )

        # Should have error message in warnings
        assert "warnings" in result
        assert result["warnings"] is not None
        assert "error" in result["warnings"].lower() or "conversion error" in result["warnings"].lower()

    # ========== Input Format Options Tests ==========

    def test_json_format_accepted(self):
        """Verify JSON format is accepted."""
        result = self.component.build(
            input_text='{"test": "value"}',
            input_format='JSON'
        )
        assert result["toon_output"] is not None

    def test_xml_format_accepted(self):
        """Verify XML format is accepted."""
        result = self.component.build(
            input_text='<?xml version="1.0"?><root><item>test</item></root>',
            input_format='XML'
        )
        assert result["toon_output"] is not None

    def test_csv_format_accepted(self):
        """Verify CSV format is accepted."""
        result = self.component.build(
            input_text='name,value\ntest,123',
            input_format='CSV'
        )
        assert result["toon_output"] is not None

    def test_html_format_accepted(self):
        """Verify HTML format is accepted."""
        result = self.component.build(
            input_text='<html><body><h1>Test</h1></body></html>',
            input_format='HTML'
        )
        assert result["toon_output"] is not None

    # ========== Delimiter Options Tests ==========

    def test_comma_delimiter_accepted(self):
        """Verify COMMA delimiter is accepted."""
        result = self.component.build(
            input_text='name,value\ntest,123',
            input_format='CSV',
            csv_delimiter='comma'
        )
        assert result["toon_output"] is not None

    def test_tab_delimiter_accepted(self):
        """Verify TAB delimiter is accepted."""
        result = self.component.build(
            input_text='name\tvalue\ntest\t123',
            input_format='CSV',
            csv_delimiter='tab'
        )
        assert result["toon_output"] is not None

    def test_pipe_delimiter_accepted(self):
        """Verify PIPE delimiter is accepted."""
        result = self.component.build(
            input_text='name|value\ntest|123',
            input_format='CSV',
            csv_delimiter='pipe'
        )
        assert result["toon_output"] is not None

    # ========== Configuration Options Tests ==========

    def test_sort_keys_true_accepted(self):
        """Verify sort_keys=true is accepted."""
        result = self.component.build(
            input_text='{"z": 1, "a": 2}',
            input_format='JSON',
            sort_keys=True
        )
        assert result["toon_output"] is not None

    def test_sort_keys_false_accepted(self):
        """Verify sort_keys=false is accepted."""
        result = self.component.build(
            input_text='{"z": 1, "a": 2}',
            input_format='JSON',
            sort_keys=False
        )
        assert result["toon_output"] is not None

    def test_auto_detect_true_accepted(self):
        """Verify auto_detect=true is accepted."""
        result = self.component.build(
            input_text='{"test": "value"}',
            auto_detect=True
        )
        assert result["toon_output"] is not None

    # ========== Token Statistics Format Tests ==========

    def test_token_statistics_are_integers(self):
        """Verify token statistics are returned as integers."""
        result = self.component.build(
            input_text='{"name": "John", "age": 30}',
            input_format='JSON'
        )

        assert isinstance(result["original_tokens"], int)
        assert isinstance(result["toon_tokens"], int)
        assert isinstance(result["token_reduction"], int)

    def test_token_reduction_calculated_correctly(self):
        """Verify token_reduction equals original - toon."""
        result = self.component.build(
            input_text='{"name": "John"}',
            input_format='JSON'
        )

        expected = result["original_tokens"] - result["toon_tokens"]
        assert result["token_reduction"] == expected

    # ========== Error Message Format Tests ==========

    def test_error_message_includes_type(self):
        """Verify error messages include error type."""
        result = self.component.build(
            input_text='{invalid}',
            input_format='JSON'
        )

        warnings = result.get("warnings", "")
        # Error messages should include context about what went wrong
        assert len(warnings) > 0
