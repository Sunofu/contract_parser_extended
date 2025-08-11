# Contract Parser Extended

Система автоматической обработки деловой корреспонденции для анализа договоров, технических заданий и извещений о тендерах.

## 🎯 Возможности

- 📬 Автоматическое получение писем с вложениями через IMAP
- 🤖 Анализ документов с помощью GPT-4
- 📄 Поддержка форматов: PDF, DOCX, XLSX, TXT
- 🔍 Автоматическая классификация документов
- 🔗 Интеграция с Bitrix24 CRM
- ⏰ Запуск по расписанию

## 🏗️ Структура проекта

```
contract_parser_extended/
├── main/                     # Основная логика
│   └── handle_email_request.py
├── preprocessing/            # Предобработка
│   └── classify_attachment.py
├── ingestion/               # Извлечение текста
│   └── extract_text_universal.py
├── llm/                     # ИИ анализ
│   └── gpt_analyzer.py
├── bitrix24/               # CRM интеграция
│   └── bitrix_sender.py
├── email_reader.py         # Чтение почты
├── run_scheduled.py        # Запуск по расписанию
└── requirements.txt        # Зависимости
```

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка переменных окружения

Скопируйте `.env.example` в `.env` и заполните:

```bash
cp .env.example .env
```

Отредактируйте `.env`:

```env
# Почта
EMAIL_HOST=imap.gmail.com
EMAIL_PORT=993
EMAIL_LOGIN=your@email.com
EMAIL_PASSWORD=your_app_password

# OpenAI
OPENAI_API_KEY=sk-your-openai-key

# Bitrix24
BITRIX_WEBHOOK=https://yourcompany.bitrix24.ru/rest/1/webhook_key
```

### 3. Запуск

```bash
python run_scheduled.py
```

## ⚙️ Настройка автоматического запуска

### Windows (Планировщик заданий)

1. Откройте Планировщик заданий
2. Создайте новую задачу
3. Укажите триггер (например, каждый час)
4. Действие: запуск программы `python.exe`
5. Аргументы: путь к `run_scheduled.py`

### Linux/macOS (cron)

```bash
# Каждый час
0 * * * * /usr/bin/python3 /path/to/run_scheduled.py

# Каждые 30 минут
*/30 * * * * /usr/bin/python3 /path/to/run_scheduled.py
```

## 📋 Типы обрабатываемых документов

1. **Договоры** - извлечение ключевых условий
2. **Номенклатура** - извлечение таблиц товаров/услуг
3. **Извещения** - информация о тендерах и котировках

## 🔧 Разработка

### Добавление нового типа документов

1. Обновите `classify_attachment.py`
2. Добавьте обработчик в `handle_email_request.py`
3. При необходимости создайте новый анализатор в `llm/`

### Тестирование

```bash
# Тест классификации
python -c "from preprocessing.classify_attachment import classify_attachment; print(classify_attachment('текст договора', 'contract.pdf'))"

# Тест извлечения текста
python -c "from ingestion.extract_text_universal import extract_text_from_file; print(extract_text_from_file('test.pdf')[:100])"
```

## 🛠️ Устранение неполадок

### Ошибки подключения к почте

- Проверьте настройки IMAP
- Убедитесь, что используете пароль приложения (для Gmail)
- Проверьте настройки безопасности почтового ящика

### Ошибки OpenAI

- Проверьте корректность API ключа
- Убедитесь в наличии средств на счету
- Проверьте лимиты запросов

### Ошибки извлечения текста

- Убедитесь, что установлены все зависимости
- Проверьте права доступа к файлам
- Для PDF может потребоваться дополнительная настройка

## 📝 Логи

Результаты обработки сохраняются в:
- `output/email_parsed.json` - структурированные данные
- Консольный вывод с детальной информацией

## 🔒 Безопасность

- Никогда не коммитьте `.env` файл
- Используйте пароли приложений вместо основных паролей
- Регулярно обновляйте API ключи
- Ограничьте права доступа к файлам проекта