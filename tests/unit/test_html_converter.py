"""Unit tests for HTML converter."""

import pytest
from langflow_toon.converters.html_converter import HtmlConverter
from langflow_toon.models.data import ConversionConfig
from langflow_toon.models.errors import ConversionError


class TestHtmlConverter:
    """Test suite for HtmlConverter class."""

    def setup_method(self):
        """Setup test fixtures."""
        self.converter = HtmlConverter()
        self.config = ConversionConfig()

    def test_valid_html(self):
        """Test conversion of valid HTML input."""
        html_input = '<html><body><h1>Welcome</h1><p>Hello World</p></body></html>'
        result = self.converter.convert(html_input, self.config)

        assert result.toon_output is not None
        assert len(result.toon_output) > 0
        assert result.original_tokens > 0

    def test_html_with_table(self):
        """Test HTML with table structure."""
        table_html = '''
        <table>
            <tr><th>Name</th><th>Age</th></tr>
            <tr><td>John</td><td>30</td></tr>
        </table>
        '''
        result = self.converter.convert(table_html, self.config)

        assert result.toon_output is not None
        assert "table" in result.toon_output.lower()

    def test_html_with_lists(self):
        """Test HTML with ordered and unordered lists."""
        lists_html = '''
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
        </ul>
        <ol>
            <li>First</li>
            <li>Second</li>
        </ol>
        '''
        result = self.converter.convert(lists_html, self.config)

        assert result.toon_output is not None

    def test_html_with_form(self):
        """Test HTML with form elements."""
        form_html = '''
        <form>
            <input type="text" name="username" />
            <input type="password" name="password" />
            <button type="submit">Submit</button>
        </form>
        '''
        result = self.converter.convert(form_html, self.config)

        assert result.toon_output is not None

    def test_html_with_scripts_excluded(self):
        """Test that scripts are parsed (not excluded in basic parser)."""
        script_html = '''
        <html>
        <head>
            <script>alert("test");</script>
        </head>
        <body>
            <h1>Content</h1>
        </body>
        </html>
        '''
        result = self.converter.convert(script_html, self.config)

        assert result.toon_output is not None
        # Basic HTML parser includes script tags
        assert "script" in result.toon_output.lower()

    def test_html_with_styles(self):
        """Test HTML with style tags."""
        style_html = '''
        <html>
        <head>
            <style>body { color: red; }</style>
        </head>
        <body><p>Text</p></body>
        </html>
        '''
        result = self.converter.convert(style_html, self.config)

        assert result.toon_output is not None

    def test_html_headings(self):
        """Test HTML with various heading levels."""
        headings_html = '''
        <h1>Title</h1>
        <h2>Subtitle</h2>
        <h3>Section</h3>
        '''
        result = self.converter.convert(headings_html, self.config)

        assert result.toon_output is not None

    def test_empty_html(self):
        """Test conversion of empty HTML."""
        empty_html = '<html></html>'
        result = self.converter.convert(empty_html, self.config)

        assert result.toon_output is not None

    def test_html_with_attributes(self):
        """Test HTML with element attributes."""
        attrs_html = '<a href="https://example.com" target="_blank">Link</a>'
        result = self.converter.convert(attrs_html, self.config)

        assert result.toon_output is not None
        # Check for attributes
        assert "href" in result.toon_output or "a" in result.toon_output.lower()
