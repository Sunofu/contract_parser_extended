# main/handle_email_request.py
import os
import json
from typing import List, Dict, Any
from preprocessing.classify_attachment import classify_attachment
from ingestion.extract_text_universal import extract_text_from_file
from llm.gpt_analyzer import extract_key_clauses, extract_goods_table
from bitrix24.bitrix_sender import send_to_bitrix24

def handle_email_request(files: List[str], output_dir: str = "output") -> Dict[str, Any]:
    """
    Основной обработчик запроса покупателя с вложениями:
    - классифицирует файлы
    - направляет в соответствующие LLM-модули
    - сохраняет результат в JSON
    - отправляет данные в Bitrix24
    """
    print("make files")
    os.makedirs(output_dir, exist_ok=True)
    print("finish")
    
    results = {
        "key_clauses": {},
        "goods": [],
        "metadata": [],
        "processed_files": []
    }
    
    print(f"🔄 Обработка {len(files)} файлов...")
    
    for file_path in files:
        try:
            print(f"📄 Обрабатываю: {os.path.basename(file_path)}")
            
            # Извлечение текста из файла
            text = extract_text_from_file(file_path)
            if not text.strip():
                print(f"⚠️ Пустой файл: {file_path}")
                continue
            
            # Классификация документа
            doc_type = classify_attachment(text, os.path.basename(file_path))
            print(f"➡️ Тип: {doc_type}")
            
            # Обработка в зависимости от типа
            if doc_type == "договор":
                clauses = extract_key_clauses(text)
                results["key_clauses"][os.path.basename(file_path)] = clauses
                
            elif doc_type == "номенклатура":
                goods = extract_goods_table(text)
                results["goods"].append({
                    "file": os.path.basename(file_path),
                    "items": goods
                })
                
            elif doc_type == "извещение":
                results["metadata"].append({
                    "type": "Извещение",
                    "file": os.path.basename(file_path),
                    "content": text[:1000] + "..." if len(text) > 1000 else text
                })
                
            else:
                results["metadata"].append({
                    "type": "Неопределённый файл",
                    "file": os.path.basename(file_path),
                    "content": text[:500] + "..." if len(text) > 500 else text
                })
            
            results["processed_files"].append({
                "file": os.path.basename(file_path),
                "type": doc_type,
                "size": len(text)
            })
            
        except Exception as e:
            print(f"❌ Ошибка при обработке {file_path}: {str(e)}")
            results["metadata"].append({
                "type": "Ошибка обработки",
                "file": os.path.basename(file_path),
                "error": str(e)
            })
    
    # Сохранение результатов
    output_file = os.path.join(output_dir, "email_parsed.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Результаты сохранены в: {output_file}")
    
    # Отправка в Bitrix24
    try:
        summary = f"Обработано файлов: {len(results['processed_files'])}"
        if results["key_clauses"]:
            summary += f", Договоров: {len(results['key_clauses'])}"
        if results["goods"]:
            summary += f", Номенклатур: {len(results['goods'])}"
        
        bitrix_response = send_to_bitrix24(
            title=f"Новый запрос на поставку - {len(files)} файлов",
            description=summary + f"\n\nДетали в файле: {output_file}"
        )
        print(f"📤 Отправлено в Bitrix24: {bitrix_response}")
        
    except Exception as e:
        print(f"⚠️ Ошибка отправки в Bitrix24: {str(e)}")
    
    return results