# Tools

Набор утилит для работы с файлами.

## Приложения

### Spreadsheet Converter
Конвертер данных из Excel (xlsx) в XML формат.

### XML Transform
Просмотр и преобразование XML файлов.

---

## Spreadsheet Converter

### Требования
- Python 3.8+
- openpyxl

### Установка
```bash
cd src/apps/spreadsheet_converter
pip install -r requirements.txt
```

### Запуск
```bash
cd src/apps/spreadsheet_converter
python main.py
```

### Сборка .exe
```bash
pip install pyinstaller
pyinstaller --onefile --windowed src/apps/spreadsheet_converter/main.py
```

---

## XML Transform

### Требования
- Python 3.8+

### Установка
```bash
cd src/apps/xml_transform
```

### Запуск
```bash
cd src/apps/xml_transform
python main.py
```

### Сборка .exe
```bash
pip install pyinstaller
pyinstaller --onefile --windowed src/apps/xml_transform/main.py
```

---

## Структура проекта

```
pars/
├── .gitignore
├── README.md
└── src/
    └── apps/
        ├── spreadsheet_converter/
        │   ├── config.py
        │   ├── main.py
        │   ├── requirements.txt
        │   ├── processor/
        │   │   ├── __init__.py
        │   │   ├── reader.py
        │   │   └── generator.py
        │   └── ui/
        │       └── app.py
        └── xml_transform/
            ├── main.py
            ├── processor/
            │   ├── __init__.py
            │   └── xml_processor.py
            └── ui/
                └── app.py
```
