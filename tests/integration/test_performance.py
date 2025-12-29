"""Performance benchmark tests for TOON Converter.

This module contains tests that verify performance targets:
- <5s for 10,000 records conversion
- <2s for token statistics calculation
"""

import json
import time
import pytest

from langflow_toon import ToonConverter
from langflow_toon.models.data import ConversionConfig


class TestPerformanceBenchmarks:
    """Performance benchmark test suite."""

    def setup_method(self):
        """Setup test fixtures."""
        self.converter = ToonConverter()

    def test_json_10k_records_under_5_seconds(self):
        """Benchmark: Convert 10,000 JSON records in under 5 seconds."""
        # Generate 10,000 records
        large_data = [
            {"id": i, "name": f"Person{i}", "age": 20 + (i % 50), "city": f"City{i % 100}"}
            for i in range(10000)
        ]
        json_input = json.dumps(large_data)

        # Measure conversion time
        start_time = time.time()
        result = self.converter.convert(json_input, input_format='JSON')
        elapsed = time.time() - start_time

        # Assertions
        assert result.toon_output is not None
        assert elapsed < 5.0, f"Conversion took {elapsed:.2f}s, expected <5s"
        print(f"✓ 10k JSON records converted in {elapsed:.2f}s")

    def test_csv_10k_records_under_5_seconds(self):
        """Benchmark: Convert 10,000 CSV records in under 5 seconds."""
        # Generate 10,000 CSV rows
        header = "id,name,age,city\n"
        rows = [
            f"{i},Person{i},{20 + (i % 50)},City{i % 100}\n"
            for i in range(10000)
        ]
        csv_input = header + "".join(rows)

        # Measure conversion time
        start_time = time.time()
        result = self.converter.convert(csv_input, input_format='CSV')
        elapsed = time.time() - start_time

        # Assertions
        assert result.toon_output is not None
        assert elapsed < 5.0, f"Conversion took {elapsed:.2f}s, expected <5s"
        print(f"✓ 10k CSV records converted in {elapsed:.2f}s")

    def test_xml_10k_records_under_5_seconds(self):
        """Benchmark: Convert 10,000 XML records in under 5 seconds."""
        # Generate 10,000 XML records
        records = []
        for i in range(10000):
            records.append(f'<person><id>{i}</id><name>Person{i}</name><age>{20 + (i % 50)}</age></person>')
        xml_input = f'<?xml version="1.0"?><root>{"".join(records)}</root>'

        # Measure conversion time
        start_time = time.time()
        result = self.converter.convert(xml_input, input_format='XML')
        elapsed = time.time() - start_time

        # Assertions
        assert result.toon_output is not None
        assert elapsed < 5.0, f"Conversion took {elapsed:.2f}s, expected <5s"
        print(f"✓ 10k XML records converted in {elapsed:.2f}s")

    def test_token_stats_under_2_seconds(self):
        """Benchmark: Calculate token statistics in under 2 seconds."""
        # Large JSON input for stats calculation
        large_data = [
            {"id": i, "name": f"Person{i}", "data": "x" * 100}
            for i in range(5000)
        ]
        json_input = json.dumps(large_data)

        # Measure conversion time (includes token stats)
        start_time = time.time()
        result = self.converter.convert(json_input, input_format='JSON')
        elapsed = time.time() - start_time

        # Assertions - stats are part of conversion, so total should be reasonable
        assert result.original_tokens > 0
        assert result.toon_tokens > 0
        # Token stats calculation is fast; 2s for 5k records is reasonable
        assert elapsed < 2.0, f"Stats calculation took {elapsed:.2f}s, expected <2s"
        print(f"✓ Token stats calculated in {elapsed:.2f}s for 5k records")

    def test_nested_json_performance(self):
        """Benchmark: Convert deeply nested JSON structure."""
        # Create deeply nested structure (depth 10)
        nested = {"value": "root"}
        for i in range(10):
            nested = {"level": i, "child": nested}

        json_input = json.dumps(nested)

        # Measure conversion time
        start_time = time.time()
        result = self.converter.convert(json_input, input_format='JSON')
        elapsed = time.time() - start_time

        # Assertions - deeply nested should still be fast
        assert result.toon_output is not None
        assert elapsed < 1.0, f"Nested conversion took {elapsed:.2f}s, expected <1s"
        print(f"✓ Deeply nested JSON (depth 10) converted in {elapsed:.2f}s")

    def test_memory_estimation_performance(self):
        """Benchmark: Memory estimation should be fast."""
        # Large input
        large_input = "x" * 1_000_000  # 1MB string

        # Measure estimation time
        start_time = time.time()
        estimate = self.converter.estimate_memory(large_input)
        elapsed = time.time() - start_time

        # Assertions
        assert estimate is not None
        assert elapsed < 0.1, f"Memory estimation took {elapsed:.2f}s, expected <0.1s"
        print(f"✓ Memory estimation for 1MB took {elapsed:.4f}s")

    def test_format_detection_performance(self):
        """Benchmark: Format detection should be fast."""
        json_input = '{"test": "value"}' * 10000  # Large JSON

        # Measure detection time
        start_time = time.time()
        detected = self.converter.detect_format(json_input)
        elapsed = time.time() - start_time

        # Assertions - detection may return None for complex cases
        # Just verify it completes quickly
        assert elapsed < 0.5, f"Format detection took {elapsed:.2f}s, expected <0.5s"
        print(f"✓ Format detection took {elapsed:.4f}s (result: {detected})")

    def test_config_options_performance(self):
        """Benchmark: Conversion with various config options."""
        large_data = [{"id": i, "name": f"Person{i}"} for i in range(5000)]
        json_input = json.dumps(large_data)

        # Test with sorted keys
        config_sorted = ConversionConfig(sort_keys=True)
        start_time = time.time()
        result = self.converter.convert(json_input, input_format='JSON', config=config_sorted)
        elapsed_sorted = time.time() - start_time

        assert result.toon_output is not None
        assert elapsed_sorted < 3.0, f"Sorted keys took {elapsed_sorted:.2f}s"

        # Test with ASCII encoding
        config_ascii = ConversionConfig(ensure_ascii=True)
        start_time = time.time()
        result = self.converter.convert(json_input, input_format='JSON', config=config_ascii)
        elapsed_ascii = time.time() - start_time

        assert result.toon_output is not None
        assert elapsed_ascii < 3.0, f"ASCII encoding took {elapsed_ascii:.2f}s"
        print(f"✓ Config options: sorted={elapsed_sorted:.2f}s, ascii={elapsed_ascii:.2f}s")
