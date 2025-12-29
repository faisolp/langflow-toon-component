"""Pytest configuration and fixtures for TOON Converter tests."""

import pytest

from langflow_toon import ToonConverter
from langflow_toon.models.data import ConversionConfig


@pytest.fixture
def converter():
    """Fixture providing ToonConverter instance."""
    return ToonConverter()


@pytest.fixture
def sample_json():
    """Fixture providing sample JSON input."""
    return '{"name": "John", "age": 30, "city": "Bangkok"}'


@pytest.fixture
def sample_xml():
    """Fixture providing sample XML input."""
    return '<?xml version="1.0"?><person><name>John</name><age>30</age></person>'


@pytest.fixture
def sample_csv():
    """Fixture providing sample CSV input."""
    return "name,age,city\nJohn,30,Bangkok\nJane,25,Chiang Mai"


@pytest.fixture
def sample_html():
    """Fixture providing sample HTML input."""
    return "<html><body><h1>Welcome</h1><p>Hello World</p></body></html>"
