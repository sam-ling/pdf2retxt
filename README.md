# PDF to Redacted Text Converter

A Python-based tool for extracting text from PDF documents while redacting sensitive information for data privacy and security purposes. The redacted .txt file is optimized for uploading to external tools like LLMs to recreate content in HTML or other structured formats.

## 🎯 Purpose

This tool addresses the need to:
- Extract text content from PDF documents
- Automatically redact sensitive information (names, numbers, emails, etc.)
- Prepare sanitized text for external processing
- Enable safe document transformation and restructuring
- Maintain document privacy when using AI/cloud services

The redaction method used is cryptographically secure against reversal because:

1. Information Destruction: The original text is completely replaced with [REDACTED] - the original data is not preserved anywhere in the output file
2. No Encoding/Encryption: It's true replacement, not encoding or encryption that could be reversed
3. Regex Substitution: Uses re.sub() which overwrites the matched text entirely

✅ Secure against reversal: No computational method can recover the original text from [REDACTED] markers alone

⚠️ Potential vulnerabilities to consider:
- Context clues from surrounding text
- Partial matches that weren't caught
- Formatting patterns that might reveal information structure
- Metadata in the original PDF that isn't redacted

Recommendations for stronger security:
- Review redacted output manually before sharing
- Use broad redaction terms to catch variations
- Consider redacting surrounding context for highly sensitive data
- Ensure the original PDF files are securely deleted after processing

## 🛠️ Technology Stack

### Core Technologies
- **PyMuPDF (fitz)**: Primary PDF processing library for text extraction
- **Python 3.8+**: Core runtime environment
- **Regular Expressions**: Pattern matching for text redaction
- **UTF-8 Encoding**: Full Unicode support for international character sets

### Methods Used

#### Text Extraction
- **Plain Text Extraction**: Uses PyMuPDF's `get_text()` method to extract raw text content
- **Page-by-Page Processing**: Maintains document structure with page separators
- **Character Encoding**: Native UTF-8 support for international documents

#### Redaction Process
- **Pattern-Based Redaction**: Uses regex to identify and replace sensitive terms
- **Case-Insensitive Matching**: Flexible matching regardless of capitalization
- **Term Escaping**: Safely handles special characters in redaction terms
- **Replacement Strategy**: Replaces sensitive content with `[REDACTED]` markers

#### Output Generation
- **Structured Text Files**: Outputs `.txt` files with metadata headers
- **Timestamped Processing**: Includes processing timestamps for audit trails
- **Batch Processing**: Handles multiple PDF files simultaneously

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone or download the repository**
   ```bash
   git clone <repository-url>
   cd pdf2retxt
   ```

2. **Install dependencies**
   ```bash
   pip install PyMuPDF
   ```

3. **Create directory structure**
   ```bash
   mkdir -p input output
   ```

4. **Configure redaction terms**
   ```bash
   touch terms_to_redact.txt
   ```

## ⚙️ Configuration

### Directory Structure
```
pdf2retxt/
├── input/                   # Place PDF files here
├── output/                  # Redacted text files saved here
├── text_redact.py           # Main program
├── terms_to_redact.txt      # Keywords to be redacted
└── README.md                # This file
```

### Redaction Terms Configuration

Create `terms_to_redact.txt` with one term per line:

```
John Doe
jane.smith@company.com
555-123-4567
Social Security Number
Account Number
Confidential
Private
Internal Use Only
```

**Configuration Tips:**
- **Case Insensitive**: Terms match regardless of capitalization
- **Exact Matching**: Use specific terms rather than broad categories
- **Special Characters**: The tool safely handles regex special characters
- **Empty Lines**: Blank lines are automatically ignored
- **Unicode Support**: Full support for international characters

## 🚀 Usage

### Basic Usage
```bash
python text_redact.py
```

### Workflow
1. Place PDF files in the `input/` directory
2. Configure sensitive terms in `terms_to_redact.txt`
3. Run the script
4. Find redacted text files in `output/` directory
5. Upload `.txt` files to LLMs for further processing

### Output Format
Generated files follow this naming convention:
```
text_redacted_[original_filename]_[timestamp].txt
```

Example output file header:
```
# Redacted Content from document.pdf
# Extraction Method: plain text
# Processed: 2024-01-15 14:30:25

--- Page 1 ---

[Document content with sensitive information replaced by [REDACTED]]
```

## 🔧 Character Set Support

### Unicode Compatibility
- **Full UTF-8 Support**: Handles all Unicode characters including:
  - Latin scripts (English, French, German, Spanish, etc.)
  - Cyrillic scripts (Russian, Bulgarian, Serbian, etc.)
  - Asian scripts (Chinese, Japanese, Korean)
  - Arabic and Hebrew scripts
  - Mathematical symbols and special characters

### Encoding Handling
- **Input**: Automatically detects PDF text encoding
- **Processing**: Maintains Unicode integrity during redaction
- **Output**: Saves files in UTF-8 encoding for maximum compatibility

## ⚠️ Known Limitations

### PDF Processing Limitations
- **Text-Only Extraction**: Cannot process text embedded in images
- **Complex Layouts**: May not preserve complex formatting or table structures
- **Scanned Documents**: Requires OCR preprocessing for image-based PDFs
- **Encrypted PDFs**: Cannot process password-protected documents

### Redaction Limitations
- **Exact Term Matching**: Only redacts exact matches of specified terms
- **Context Awareness**: Cannot understand semantic context of sensitive information
- **Partial Matching**: Does not handle partial or fuzzy matching
- **Pattern Recognition**: Cannot automatically detect PII patterns (SSNs, credit cards) without explicit configuration

### Performance Considerations
- **Memory Usage**: Large PDFs may require significant memory
- **Processing Speed**: Text extraction speed depends on document complexity
- **Batch Processing**: No parallel processing for multiple files

## 🔄 LLM Integration Workflow

### Recommended Process
1. **Extract and Redact**: Use this tool to create sanitized text files
2. **Upload to LLM**: Upload `.txt` files to Claude, ChatGPT, or similar services
3. **Prompt for Conversion**: Request HTML, Markdown, or structured format conversion
4. **Review Output**: Verify the LLM maintains redaction markers
5. **Final Processing**: Apply additional formatting or styling as needed

### Example LLM Prompt
```
Convert this redacted text to HTML format while:
- Preserving all [REDACTED] markers
- Creating appropriate heading structures
- Maintaining document flow and organization
- Adding semantic HTML tags for better structure
```

## 🛡️ Security Considerations

- **Local Processing**: All processing happens locally, no data sent to external services
- **Redaction Verification**: Always verify redacted output before sharing
- **Term Management**: Keep `terms_to_redact.txt` updated with current sensitive terms
- **Output Review**: Manually review outputs for any missed sensitive information

## 🤝 Contributing

When contributing to this project:
1. Test with various PDF types and character sets
2. Verify redaction accuracy with sample sensitive data
3. Ensure Unicode compatibility is maintained
4. Add appropriate error handling for edge cases

## 📝 License

Copyright (c) 2025 Sam Ling

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

---

*This tool is designed for defensive security and privacy protection purposes. Always verify redaction results before sharing processed documents.*
