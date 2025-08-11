# preprocessing/classify_attachment.py
import re

def classify_attachment(text: str, filename: str) -> str:
    """
    Классифицирует файл на основе имени и содержимого.
    Возвращает одну из меток: 'договор', 'номенклатура', 'извещение', 'неизвестно'
    """
    name = filename.lower()
    
    # Классификация по имени файла
    if any(word in name for word in ["договор", "contract", "контракт"]):
        return "договор"
    elif any(word in name for word in ["техзадание", "перечень", "форма", "номенклатура", "спецификация", "позиции", "прайс"]):
        return "номенклатура"
    elif any(word in name for word in ["извещение", "тендер", "конкурс", "котировка", "приглашение"]):
        return "извещение"
    
    # Классификация по содержимому
    lower_text = text.lower()
    
    # Проверка на извещение о тендере
    if ("извещение" in lower_text and 
        ("приглашение" in lower_text or "номер процедуры" in lower_text or 
         "участие в" in lower_text or "котировк" in lower_text)):
        return "извещение"
    
    # Проверка на договор
    elif any(phrase in lower_text for phrase in [
        "предмет договора", "настоящий договор", "стороны договора",
        "заказчик", "исполнитель", "поставщик", "условия оплаты"
    ]):
        return "договор"
    
    # Проверка на номенклатуру/техзадание
    elif any(phrase in lower_text for phrase in [
        "позиции:", "таблица поставки", "спецификация поставки",
        "наименование", "количество", "единица измерения", "цена",
        "№ п/п", "артикул", "код товара"
    ]):
        return "номенклатура"
    
    # Дополнительные проверки по ключевым словам
    contract_keywords = ["договор", "соглашение", "контракт", "сделка"]
    tender_keywords = ["тендер", "конкурс", "аукцион", "закупка"]
    goods_keywords = ["товар", "изделие", "продукция", "материал"]
    
    contract_count = sum(1 for word in contract_keywords if word in lower_text)
    tender_count = sum(1 for word in tender_keywords if word in lower_text)
    goods_count = sum(1 for word in goods_keywords if word in lower_text)
    
    if contract_count >= 2:
        return "договор"
    elif tender_count >= 2:
        return "извещение"
    elif goods_count >= 2:
        return "номенклатура"
    
    return "неизвестно"