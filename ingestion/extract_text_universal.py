# ingestion/extract_text_universal.py
import os
import pandas as pd

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

try:
    import docx2txt
    DOCX2TXT_AVAILABLE = True
except ImportError:
    DOCX2TXT_AVAILABLE = False

try:
    from docx import Document
    PYTHON_DOCX_AVAILABLE = True
except ImportError:
    PYTHON_DOCX_AVAILABLE = False

def extract_text_from_pdf(file_path: str) -> str:
    """Извлечение текста из PDF файла"""
    try:
        if not PDFPLUMBER_AVAILABLE:
            raise ImportError("pdfplumber не установлен")
        
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        print(f"Ошибка извлечения текста из PDF {file_path}: {e}")
        return ""

def extract_text_from_docx(file_path: str) -> str:
    """Извлечение текста из DOCX файла"""
    try:
        if DOCX2TXT_AVAILABLE:
            text = docx2txt.process(file_path)
            if text:
                return text.strip()
        
        if PYTHON_DOCX_AVAILABLE:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        
        raise ImportError("Ни docx2txt, ни python-docx не установлены")
    except Exception as e:
        print(f"Ошибка извлечения текста из DOCX {file_path}: {e}")
        return ""

def extract_text_from_excel(file_path: str) -> str:
    """Извлечение текста из Excel файла"""
    try:
        # Читаем все листы Excel файла
        excel_file = pd.ExcelFile(file_path)
        all_text = []
        
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            # Преобразуем все данные в строки и объединяем
            sheet_text = df.astype(str).apply(lambda x: ' '.join(x), axis=1).str.cat(sep='\n')
            all_text.append(f"=== Лист: {sheet_name} ===\n{sheet_text}")
        
        return '\n\n'.join(all_text)
    except Exception as e:
        print(f"Ошибка при извлечении текста из Excel {file_path}: {e}")
        return ""

def extract_text_from_txt(file_path: str) -> str:
    """Извлечение текста из TXT файла"""
    try:
        encodings = ['utf-8', 'cp1251', 'latin-1']
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        
        # Если все кодировки не сработали
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"Ошибка при извлечении текста из TXT {file_path}: {e}")
        return ""



def extract_text_from_file(file_path: str) -> str:
    """
    Универсальная функция извлечения текста из файлов различных форматов
    
    Args:
        file_path (str): Путь к файлу
        
    Returns:
        str: Извлеченный текст
    """
    if not os.path.exists(file_path):
        print(f"Файл не найден: {file_path}")
        return ""
    
    file_extension = os.path.splitext(file_path)[1].lower()
    
    try:
        if file_extension == '.pdf':
            return extract_text_from_pdf(file_path)
        elif file_extension in ['.docx', '.doc']:
            return extract_text_from_docx(file_path)
        elif file_extension in ['.xlsx', '.xls']:
            return extract_text_from_excel(file_path)
        elif file_extension == '.txt':
            return extract_text_from_txt(file_path)
        else:
            print(f"Неподдерживаемый формат файла: {file_extension}")
            return ""
    except Exception as e:
        print(f"Общая ошибка извлечения текста из {file_path}: {e}")
        return ""