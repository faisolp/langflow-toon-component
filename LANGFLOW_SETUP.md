# วิธีการติดตั้งและใช้งาน TOON Converter ใน Langflow

## ขั้นตอนที่ 1: ติดตั้ง Package

### วิธี A: ติดตั้งจาก Source (แนะนำ)

```bash
# Clone หรือไปที่โฟลเดอร์โปรเจกต์
cd /path/to/langflow-toon-component

# ติดตั้งในโหมด development
pip install -e .

# ติดตั้งในโหมด production
pip install .

# หรือติดตั้งจาก requirements.txt
pip install -r requirements.txt
```

### วิธี B: ติดตั้งจาก PyPI

```bash
# ติดตั้งจาก PyPI (เมื่อ publish แล้ว)
pip install langflow-toon
```

### วิธี C: ติดตั้งแบบรันไทม์ใน Langflow

```bash
# เมื่อ Langflow กำลังทำงานอยู่
pip install tiktoken xmltodict
```

---

## ขั้นตอนที่ 2: ลงทะเบียน Custom Component ใน Langflow

### สร้างไฟล์ Custom Component

สร้างไฟล์ใหม่: `~/.langflow/custom_components/toon_converter.py`

```python
"""TOON Converter Custom Component for Langflow."""

import sys
sys.path.insert(0, '/path/to/toon_langflow')  # ระบุ path ของโปรเจกต์

from langflow_toon.components.toon_component import ToonConverterComponent

# Export component สำหรับ Langflow
__all__ = ['ToonConverterComponent']
```

---

## ขั้นตอนที่ 3: รีสตาร์ท Langflow

```bash
# หยุด Langflow ถ้ากำลังทำงาน
# แล้วเริ่มใหม่
langflow run
```

---

## ขั้นตอนที่ 4: ใช้งานใน Langflow UI

### 4.1 เปิด Langflow

เปิด browser ไปที่ `http://localhost:7860`

### 4.2 สร้าง Flow ใหม่

1. คลิก **"New Project"**
2. เลือก **"Blank Flow"**

### 4.3 เพิ่ม TOON Converter Component

1. ค้นหา **"TOON Converter"** ใน Component Palette
2. ลาก component มาวางบน canvas

### 4.4 เชื่อมต่อ Flow

ตัวอย่าง Flow: **HTTP Request → TOON Converter → LLM**

```
┌─────────────┐      ┌──────────────┐      ┌──────────┐
│   HTTP      │─────▶│   TOON       │─────▶│   LLM    │
│  Request    │      │  Converter   │      │          │
└─────────────┘      └──────────────┘      └──────────┘
```

---

## ขั้นตอนที่ 5: กำหนดค่า Component (Configuration)

### Input Ports

| Port | ค่า | คำอธิบาย |
|------|------|-----------|
| `input_text` | `{{input_data}}` | ข้อมูลจาก HTTP Request หรือ Input อื่นๆ |
| `input_format` | `JSON` | รูปแบบข้อมูล (JSON, XML, CSV, HTML) |
| `csv_delimiter` | `comma` | Delimiter สำหรับ CSV (comma, tab, pipe) |
| `auto_detect` | `false` | ตรวจหา format อัตโนมัติ |
| `sort_keys` | `false` | เรียง key ตามตัวอักษร |
| `ensure_ascii` | `false` | แปลง non-ASCII เป็น escape sequence |

### Output Ports

| Port | ใช้สำหรับ |
|------|-----------|
| `toon_output` | ส่งเข้า LLM Prompt |
| `original_tokens` | แสดงสถิติ |
| `toon_tokens` | แสดงสถิติ |
| `token_reduction` | แสดงสถิติ |
| `warnings` | แสดง warning ถ้ามี |

---

## ตัวอย่างการใช้งานจริง

### Example 1: JSON API → TOON → LLM

**สถานการณ์**: ดึงข้อมูลจาก API และส่งให้ LLM

```
1. HTTP Request Component
   - URL: https://api.example.com/users
   - Output: ต่อเข้า input_text ของ TOON Converter

2. TOON Converter Component
   - input_format: JSON
   - input_text: {{http_request_output}}
   - Output: toon_output ต่อเข้า LLM

3. LLM Component
   - Prompt: "Analyze this user data:\n{{toon_output}}"
```

### Example 2: CSV → TOON → LLM

**สถานการณ์**: อัปโหลด CSV และให้ LLM วิเคราะห์

```
1. File Loader Component
   - โหลดไฟล์ CSV
   - Output: ต่อเข้า TOON Converter

2. TOON Converter Component
   - input_format: CSV
   - csv_delimiter: comma
   - Output: toon_output

3. LLM Component
   - Prompt: "สรุปข้อมูลจากตารางนี้:\n{{toon_output}}"
```

### Example 3: HTML → TOON → LLM

**สถานการณ์**: ดึงข้อมูลจากเว็บและสรุปเนื้อหา

```
1. HTTP Request Component
   - URL: https://example.com/page.html
   - Output: HTML content

2. TOON Converter Component
   - input_format: HTML
   - auto_detect: true
   - Output: toon_output

3. LLM Component
   - Prompt: "สรุปเนื้อหาจากหน้าเว็บนี้:\n{{toon_output}}"
```

---

## ตัวอย่าง Prompt Template

```python
# ใน LLM Component หรือ Prompt Component

# Basic
prompt = """Analyze the following data:
{toon_output}

Provide insights and summaries."""

# With statistics
prompt = """Data Analysis Report
─────────────────────
Original tokens: {original_tokens}
TOON tokens: {toon_tokens}
Saved: {token_reduction} tokens

Data:
{toon_output}

Please analyze this data."""

# Thai prompt
prompt = """วิเคราะห์ข้อมูลต่อไปนี้:
{toon_output}

โปรดให้ข้อมูลเชิงลึกและสรุปผล"""
```

---

## การ Debug และ Troubleshooting

### Component ไม่ปรากฏใน Palette

```bash
# ตรวจสอบการติดตั้ง
pip list | grep toon

# ตรวจสอบ path
python -c "import langflow_toon; print(langflow_toon.__file__)"

# รีสตาร์ท Langflow และล้าง cache
rm -rf ~/.langflow/cache
langflow run --refresh
```

### Error: ImportError

```bash
# ติดตั้ง dependencies ที่ขาดหาย
pip install tiktoken xmltodict

# หรือติดตั้งทั้งหมดจาก requirements
pip install -r requirements.txt
```

---

## Python API Usage (นอก Langflow)

### Method 1: ใช้ Core Modules โดยตรง

```python
from langflow_toon.detectors.format_detector import FormatDetector
from langflow_toon.converters.json_converter import JsonConverter
from langflow_toon.converters.xml_converter import XmlConverter
from langflow_toon.converters.csv_converter import CsvConverter
from langflow_toon.converters.html_converter import HtmlConverter
from langflow_toon.models.data import ConversionConfig, Delimiter

# ตั้งค่า configuration
config = ConversionConfig(
    delimiter=Delimiter.COMMA,
    sort_keys=False,
    ensure_ascii=False
)

# ตัวอย่าง JSON
json_data = '{"name": "Faisolp", "age": 30, "courses": ["Math", "Science"]}'

# Auto-detect format
detector = FormatDetector()
detected_format = detector.detect(json_data)
print(f"Detected format: {detected_format}")

# แปลง JSON → TOON
converter = JsonConverter()
result = converter.convert(json_data, config)

print("TOON Output:")
print(result.toon_output)
print(f"Token reduction: {result.token_reduction} tokens")
print(f"Savings: {result.token_reduction/result.original_tokens*100:.1f}%")

# Output:
# name: Faisolp
# age: 30
# courses:[2]: "Math","Science"
```

### Method 2: ใช้ ToonConverterComponent แบบ Standalone

```python
from langflow_toon.components.toon_component import ToonConverterComponent

# สร้าง component instance
component = ToonConverterComponent()

# กำหนดค่า inputs
component.input_text = '{"name": "Faisolp", "age": 30, "courses": ["Math", "Science"]}'
component.input_format = "JSON"
component.csv_delimiter = "comma"
component.auto_detect = True
component.sort_keys = False
component.ensure_ascii = False

# รัน conversion
data_result = component.convert_to_toon()

# ดึงผลลัพธ์
result = data_result.value
print("TOON Output:")
print(result["toon_output"])
print(f"Original tokens: {result['original_tokens']}")
print(f"TOON tokens: {result['toon_tokens']}")
print(f"Token reduction: {result['token_reduction']}")

# ดึง text output
text_result = component.get_text_output()
print("Text Output:")
print(text_result.text)
```

### Method 3: ใช้ในรูปแบบ Function

```python
def convert_to_toon(input_text, input_format="AUTO", csv_delimiter="comma", 
                   sort_keys=False, ensure_ascii=False):
    """
    Convert input text to TOON format.
    
    Args:
        input_text: Input content to convert
        input_format: Format type (AUTO, JSON, XML, CSV, HTML)
        csv_delimiter: CSV delimiter (comma, tab, pipe)
        sort_keys: Sort object keys alphabetically
        ensure_ascii: Encode non-ASCII characters
    
    Returns:
        dict: Conversion result with toon_output and statistics
    """
    from langflow_toon.detectors.format_detector import FormatDetector
    from langflow_toon.converters.json_converter import JsonConverter
    from langflow_toon.models.data import ConversionConfig, Delimiter
    
    # Detect format
    if input_format == "AUTO":
        detector = FormatDetector()
        detected_format = detector.detect(input_text)
    else:
        detected_format = input_format
    
    # Create config
    delimiter_map = {
        "comma": Delimiter.COMMA,
        "tab": Delimiter.TAB,
        "pipe": Delimiter.PIPE
    }
    
    config = ConversionConfig(
        delimiter=delimiter_map.get(csv_delimiter, Delimiter.COMMA),
        sort_keys=sort_keys,
        ensure_ascii=ensure_ascii
    )
    
    # Convert based on format
    if detected_format == "JSON":
        converter = JsonConverter()
        result = converter.convert(input_text, config)
        
        return {
            "toon_output": result.toon_output,
            "original_tokens": result.original_tokens,
            "toon_tokens": result.toon_tokens,
            "token_reduction": result.token_reduction,
            "warnings": list(result.warnings) if result.warnings else []
        }
    else:
        return {
            "toon_output": input_text,
            "original_tokens": len(input_text.split()),
            "toon_tokens": len(input_text.split()),
            "token_reduction": 0,
            "warnings": [f"Format {detected_format} not supported in this example"]
        }

# ใช้งาน
json_data = '{"name": "Faisolp", "age": 30, "courses": ["Math", "Science"]}'
result = convert_to_toon(json_data)
print(result["toon_output"])
```

### Method 4: Batch Processing

```python
from langflow_toon.converters.json_converter import JsonConverter
from langflow_toon.models.data import ConversionConfig

def batch_convert(data_list, config=None):
    """Convert multiple JSON objects to TOON format."""
    if config is None:
        config = ConversionConfig()
    
    converter = JsonConverter()
    results = []
    
    for data in data_list:
        try:
            result = converter.convert(data, config)
            results.append({
                "input": data,
                "output": result.toon_output,
                "tokens_saved": result.token_reduction
            })
        except Exception as e:
            results.append({
                "input": data,
                "output": None,
                "error": str(e)
            })
    
    return results

# ใช้งาน
data_list = [
    '{"name": "Alice", "age": 25}',
    '{"name": "Bob", "age": 30, "skills": ["Python", "JavaScript"]}',
    '{"users": [{"id": 1}, {"id": 2}]}'
]

results = batch_convert(data_list)
for i, result in enumerate(results):
    print(f"Data {i+1}:")
    print(f"  Output: {result['output']}")
    if 'tokens_saved' in result:
        print(f"  Tokens saved: {result['tokens_saved']}")
    print()
```

---

## เอกสารอ้างอิง

- [TOON Format Specification](https://github.com/toon-format/toon)
- [Langflow Documentation](https://langflow.org)
- [Project README](./README.md)

