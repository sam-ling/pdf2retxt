import fitz  # PyMuPDF
import logging
import sys
import re
from pathlib import Path
from datetime import datetime

INPUT_DIR = "input"
OUTPUT_DIR = "output"
TERMS_FILE = "terms_to_redact.txt"

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_terms(terms_file):
    """Load redaction terms from file with error handling."""
    try:
        with open(terms_file, "r", encoding="utf-8") as f:
            terms = [line.strip() for line in f if line.strip()]
        logger.info(f"Loaded {len(terms)} redaction terms")
        return terms
    except FileNotFoundError:
        logger.error(f"Terms file not found: {terms_file}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error loading terms file: {e}")
        sys.exit(1)

def validate_directories():
    """Validate input and output directories."""
    input_path = Path(INPUT_DIR)
    output_path = Path(OUTPUT_DIR)
    
    if not input_path.exists() or not input_path.is_dir():
        logger.error(f"Input directory does not exist or is not a directory: {INPUT_DIR}")
        sys.exit(1)
    
    try:
        output_path.mkdir(exist_ok=True)
        logger.info("Directories validated")
    except Exception as e:
        logger.error(f"Cannot create output directory: {e}")
        sys.exit(1)


def redact_text(text, terms, case_sensitive=False):
    """Redact sensitive terms in text."""
    if not text or not terms:
        return text
    
    redacted_text = text
    flags = 0 if case_sensitive else re.IGNORECASE
    
    for term in filter(None, terms):  # Filter out empty terms
        pattern = re.escape(term)
        redacted_text = re.sub(pattern, "[REDACTED]", redacted_text, flags=flags)
    
    return redacted_text

def extract_and_redact_text(filepath, terms):
    """Extract text and redact sensitive information."""
    try:
        doc = fitz.open(filepath)

        # Default: plain text
        full_text = ""
        for page_num, page in enumerate(doc):
            page_text = page.get_text()
            if page_text:
                full_text += f"\n\n--- Page {page_num + 1} ---\n\n"
                full_text += page_text
        
        doc.close()
        
        # Redact the extracted text
        redacted_text = redact_text(full_text, terms)
        
        return redacted_text
        
    except Exception as e:
        logger.error(f"Error extracting text from {filepath}: {e}")
        return None

def text_redact_pdf(filepath, terms, output_path):
    """Main text redaction function - extracts and saves redacted text."""
    try:
        logger.info(f"Starting text redaction for: {filepath.name}")
        
        # Extract and redact text
        logger.info("Extracting text...")
        redacted_text = extract_and_redact_text(filepath, terms)
        
        if redacted_text and redacted_text.strip():
            # Save as text file for LLM processing
            txt_output = output_path.with_suffix('.txt')
            with open(txt_output, 'w', encoding='utf-8') as f:
                f.write(f"# Redacted Content from {filepath.name}\n")
                f.write(f"# Extraction Method: plain text\n")
                f.write(f"# Processed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(redacted_text)
            
            logger.info(f"Text redaction completed: {txt_output}")
            return True
        
        logger.error("Text extraction failed")
        return False
        
    except Exception as e:
        logger.error(f"Error in text redaction: {e}")
        return False

def main():
    """Main text redaction workflow."""
    logger.info("Starting text-based PDF redaction workflow")
    
    # Validate setup
    validate_directories()
    terms = load_terms(TERMS_FILE)
    
    if not terms:
        logger.warning("No redaction terms found - nothing to redact")
        return
    
    # Process PDFs
    input_path = Path(INPUT_DIR)
    output_path = Path(OUTPUT_DIR)
    
    pdf_files = list(input_path.glob("*.pdf"))
    if not pdf_files:
        logger.warning(f"No PDF files found in {INPUT_DIR}")
        return
    
    logger.info(f"Found {len(pdf_files)} PDF files to process")
    
    successful = 0
    failed = 0
    
    # Generate timestamp for this batch
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for pdf_file in pdf_files:
        # Create filename with timestamp
        base_name = pdf_file.stem
        output_file = output_path / f"text_redacted_{base_name}_{timestamp}.txt"
        
        logger.info(f"Processing: {pdf_file.name}")
        
        if text_redact_pdf(pdf_file, terms, output_file):
            successful += 1
        else:
            failed += 1
    
    logger.info(f"Text redaction complete: {successful} successful, {failed} failed")
    logger.info("Upload the .txt files to external tools with preserved document structure")

if __name__ == "__main__":
    main()