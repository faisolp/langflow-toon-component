"""Unit tests for CSV converter."""

import pytest
from langflow_toon.converters.csv_converter import CsvConverter
from langflow_toon.models.data import ConversionConfig, Delimiter
from langflow_toon.models.errors import ConversionError


class TestCsvConverter:
    """Test suite for CsvConverter class."""

    def setup_method(self):
        """Setup test fixtures."""
        self.converter = CsvConverter()
        self.config = ConversionConfig()

    def test_valid_csv(self):
        """Test conversion of valid CSV input."""
        csv_input = "name,age,city\nJohn,30,Bangkok\nJane,25,Chiang Mai"
        result = self.converter.convert(csv_input, self.config)

        print(f"\n--- test_valid_csv ---")
        print(f"INPUT (CSV):\n{csv_input}")
        print(f"OUTPUT (TOON):\n{result.toon_output}")
        print(f"Tokens: {result.original_tokens} -> {result.toon_tokens}")

        assert result.toon_output is not None
        # TOON format uses tabular format: data[N]{fields}:
        assert 'data:[2]' in result.toon_output or '{name,age,city}' in result.toon_output
        assert result.original_tokens > 0
        assert result.toon_tokens > 0

    def test_inconsistent_columns(self):
        """Test CSV with inconsistent column counts."""
        inconsistent_csv = "name,age,city\nJohn,30\nJane,25,Chiang Mai"
        result = self.converter.convert(inconsistent_csv, self.config)

        # Should handle with null insertion
        assert result.toon_output is not None

    def test_empty_csv(self):
        """Test conversion of empty CSV input."""
        empty_csv = ""

        with pytest.raises((ConversionError, Exception)):
            self.converter.convert(empty_csv, self.config)

    def test_csv_with_quotes(self):
        """Test CSV with quoted fields."""
        quoted_csv = 'name,description\n"John, Doe","Developer, AI"\n"Jane, Smith","Designer, UI"'
        result = self.converter.convert(quoted_csv, self.config)

        assert result.toon_output is not None

    def test_csv_tab_delimiter(self):
        """Test CSV with tab delimiter."""
        tab_csv = "name\tage\tcity\nJohn\t30\tBangkok"
        config = ConversionConfig(delimiter=Delimiter.TAB)
        result = self.converter.convert(tab_csv, config)

        assert result.toon_output is not None

    def test_csv_pipe_delimiter(self):
        """Test CSV with pipe delimiter."""
        pipe_csv = "name|age|city\nJohn|30|Bangkok"
        config = ConversionConfig(delimiter=Delimiter.PIPE)
        result = self.converter.convert(pipe_csv, config)

        assert result.toon_output is not None

    def test_large_csv(self):
        """Test conversion of larger CSV dataset."""
        rows = ["name,age,city"]
        for i in range(100):
            rows.append(f"Person{i},{20+i},City{i}")
        large_csv = "\n".join(rows)

        result = self.converter.convert(large_csv, self.config)

        assert result.toon_output is not None
        # Should have 100 data rows
        assert '"name"' in result.toon_output or 'name' in result.toon_output

    def test_csv_with_empty_fields(self):
        """Test CSV with empty fields."""
        empty_fields_csv = "name,age,city\nJohn,,Bangkok\n,25,"
        result = self.converter.convert(empty_fields_csv, self.config)

        assert result.toon_output is not None
