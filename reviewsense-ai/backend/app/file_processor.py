import pandas as pd
import pdfplumber
import pytesseract
from PIL import Image
import io

class FileProcessor:
    @staticmethod
    def process_excel(file):
        df = pd.read_excel(file)
        required_columns = ['review_text', 'date', 'source']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Missing required columns in Excel file")
        return df.to_dict('records')

    @staticmethod
    def process_pdf(file):
        text = []
        with pdfplumber.open(io.BytesIO(file)) as pdf:
            for page in pdf.pages:
                if page.extract_text():
                    text.append(page.extract_text())
                else:  # Handle scanned PDFs
                    img = page.to_image(resolution=300)
                    text.append(pytesseract.image_to_string(img.original))
        return "\n".join(text)

    @staticmethod
    def generate_report(data, format='excel'):
        df = pd.DataFrame(data)
        if format == 'excel':
            output = io.BytesIO()
            df.to_excel(output, index=False)
            return output.getvalue()
        elif format == 'pdf':
            # Use ReportLab for PDF generation
            return generate_pdf(df)
