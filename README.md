# XLSX → XML Converter

Конвертер данных из Excel (xlsx) в XML формат.

## Требования

- Python 3.8+
- openpyxl
- pyinstaller

## Установка

```bash
cd src
pip install -r requirements.txt
pip install pyinstaller
```

## Запуск

```bash
cd src
python main.py
```

## Использование

1. Запустите программу: `python main.py`
2. Нажмите **"Выбрать .xlsx файл"** и укажите файл Excel.
   > **Важно:** данные должны быть в первом столбце таблицы.
3. Проверьте список в предпросмотре данных.
4. При необходимости измените параметры XML:
   - `action_id` — идентификатор операции
   - `version` — версия формата
   - `inn` — ИНН участника
5. Нажмите **"Сохранить как .xml"** и выберите место сохранения.
6. XML файл создан.

## Сборка .exe

```bash
pyinstaller --onefile --windowed src/main.py
```

## Структура проекта

```
pars/
├── .gitignore
├── README.md
└── src/
    ├── config.py          # настройки по умолчанию
    ├── main.py            # точка входа
    ├── processor/         # логика обработки
    │   ├── __init__.py
    │   ├── reader.py      # чтение xlsx
    │   └── generator.py   # генерация xml
    └── ui/                # интерфейс
        ├── __init__.py
        └── app.py         # приложение
```
