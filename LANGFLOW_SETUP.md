# วิธีการติดตั้งและใช้งาน TOON Converter ใน Langflow

## ขั้นตอนที่ 1: ติดตั้ง Package

### วิธี A: ติดตั้งจาก Source (แนะนำ)

```bash
# Clone หรือไปที่โฟลเดอร์โปรเจกต์
cd /path/to/toon_langflow

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
pip install langflow-toon-component
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

```python
from langflow_toon import ToonConverter
from langflow_toon.models.data import ConversionConfig, Delimiter

# สร้าง converter
converter = ToonConverter()

# แปลง JSON → TOON
json_data = '{"users": [{"id": 1, "name": "Alice"}]}'
result = converter.convert(json_data, input_format='JSON')

print(result.toon_output)
# users[1]{id,name}:
#   1,Alice

print(f"Token reduction: {result.token_reduction} tokens")
```

---

## เอกสารอ้างอิง

- [TOON Format Specification](https://github.com/toon-format/toon)
- [Langflow Documentation](https://langflow.org)
- [Project README](./README.md)

