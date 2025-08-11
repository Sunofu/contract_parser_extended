# llm/gpt_analyzer.py
import os
from dotenv import load_dotenv

load_dotenv()
# Проверяем наличие OpenAI API ключа
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_AVAILABLE = (OPENAI_API_KEY and OPENAI_API_KEY.startswith("sk-"))

if OPENAI_AVAILABLE:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY, base_url="https://openrouter.ai/api/v1")
    except ImportError:
        OPENAI_AVAILABLE = False
        client = None
else:
    client = None

def extract_key_clauses(text: str) -> dict:
    """
    Извлечение ключевых условий из договора с помощью GPT-4

    Args:
        text (str): Текст договора

    Returns:
        dict: Словарь с ключевыми условиями
    """
    if not OPENAI_AVAILABLE:
        # Демо-режим: возвращаем заглушку
        return {
            "demo_mode": True,
            "message": "OpenAI API недоступен. Установите корректный OPENAI_API_KEY для полной функциональности.",
            "стороны": {"поставщик": "Извлечено из текста", "покупатель": "Извлечено из текста"},
            "предмет": "Поставка товаров/услуг",
            "сумма": "Извлечено из договора",
            "срок_поставки": "Согласно договору",
            "условия_оплаты": "Согласно договору"
        }

    try:
        prompt = f"""
        Проанализируй договор и выдели ключевые условия в формате JSON:
        {{
            "стороны": {{"поставщик": "", "покупатель": ""}},
            "предмет": "",
            "сумма": "",
            "срок_поставки": "",
            "условия_оплаты": "",
            "ответственность": ""
        }}
        
        Текст договора:
        {text[:3000]}
        """
        response = client.chat.completions.create(
            model="qwen/qwen3-235b-a22b:free",
            messages=[
                {"role": "user", "content": prompt},
            ],
            max_tokens=1000,
            temperature=0.1
        )

        result = response.choices[0].message.content
        # response = client.chat.completions.create(
        #     model="gpt-3.5-turbo",
        #     messages=[{"role": "user", "content": prompt}],
        #     max_tokens=1000,
        #     temperature=0.1
        # )
        #
        # result = response.choices[0].message.content

        # Пытаемся парсить JSON, если не получается - возвращаем как текст
        try:
            import json
            return json.loads(result)
        except:
            return {"extracted_text": result}

    except Exception as e:
        print(f"Ошибка извлечения ключевых условий: {e}")
        return {"error": str(e)}

def extract_goods_table(text: str) -> list:
    """
    Извлечение таблицы номенклатуры из документа

    Args:
        text (str): Текст документа

    Returns:
        list: Список товаров/услуг
    """
    if not OPENAI_AVAILABLE:
        # Демо-режим: возвращаем заглушку
        return [
            {
                "demo_mode": True,
                "message": "OpenAI API недоступен. Установите корректный OPENAI_API_KEY для полной функциональности.",
                "позиция": "1",
                "наименование": "Товар/услуга из документа",
                "количество": "1",
                "единица_измерения": "шт",
                "цена": "Извлечено из документа",
                "сумма": "Извлечено из документа"
            }
        ]

    try:
        prompt = f"""
        Найди и извлеки таблицу номенклатуры/товаров из документа в формате JSON:
        [
            {{
                "позиция": "",
                "наименование": "",
                "количество": "",
                "единица_измерения": "",
                "цена": "",
                "сумма": ""
            }}
        ]
        Верни только Json и ничего больше
        Если таблицы нет, верни строго пустой массив [] без другого текста.
        
        Текст документа:
        {text[:20000]}
        """

        response = client.chat.completions.create(
            model="qwen/qwen3-235b-a22b:free",
            messages=[
                {"role": "user", "content": prompt},
            ],
            max_tokens=1500,
            temperature=0.1
        )

        result = response.choices[0].message.content
        # response = client.chat.completions.create(
        #     model="gpt-3.5-turbo",
        #     messages=[{"role": "user", "content": prompt}],
        #     max_tokens=1500,
        #     temperature=0.1
        # )
        #
        # result = response.choices[0].message.content

        # Пытаемся парсить JSON
        try:
            import json
            return json.loads(result)
        except:
            return [{"extracted_text": result}]

    except Exception as e:
        print(f"Ошибка извлечения таблицы товаров: {e}")
        return [{"error": str(e)}]
