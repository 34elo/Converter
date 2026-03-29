import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

from processor import parse, transform
from config import DEFAULTS


class App:
    """Главное окно приложения."""
    
    def __init__(self, root):
        self.root = root
        self.root.title('XML Transform')
        self.root.geometry('1200x800')
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(True, True)

        self.input_path = None
        self.data = []

        main_frame = ttk.Frame(root, padding='20')
        main_frame.pack(fill='both', expand=True)

        file_frame = ttk.LabelFrame(
            main_frame,
            text='Выберите .xml файл (формат 1)',
            padding='10'
        )
        file_frame.pack(fill='x', pady=(0, 15))

        file_row = ttk.Frame(file_frame)
        file_row.pack(fill='x')

        self.file_btn = ttk.Button(
            file_row, text='Выбрать файл',
            command=self.select_file, width=20
        )
        self.file_btn.pack(side='left')

        self.file_label = ttk.Label(
            file_row, text='Файл не выбран',
            foreground='gray'
        )
        self.file_label.pack(side='left', padx=15, fill='x', expand=True)

        preview_frame = ttk.LabelFrame(main_frame, text='Предпросмотр', padding='10')
        preview_frame.pack(fill='both', expand=True, pady=(0, 15))

        columns = ('#', 'Pack Code', 'Длина')
        self.tree = ttk.Treeview(preview_frame, columns=columns, show='headings', height=12)

        self.tree.heading('#', text='#')
        self.tree.heading('Pack Code', text='Pack Code')
        self.tree.heading('Длина', text='Длина')

        self.tree.column('#', width=50, anchor='center')
        self.tree.column('Pack Code', width=400)
        self.tree.column('Длина', width=80, anchor='center')

        scrollbar = ttk.Scrollbar(preview_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.count_label = ttk.Label(
            preview_frame, text='Pack count: 0',
            font=('Segoe UI', 9, 'italic')
        )
        self.count_label.pack(anchor='e', pady=(5, 0))

        params_frame = ttk.LabelFrame(main_frame, text='Параметры (формат 2)', padding='10')
        params_frame.pack(fill='x', pady=(0, 15))

        self.entries = {}
        params = [
            ('document_id', 'Document ID:'),
            ('ver_form', 'VerForm:'),
            ('ver_prog', 'VerProg:'),
            ('operation_date_time', 'Operation Date:'),
            ('document_number', 'Document Number:'),
            ('org_name', 'Org Name:'),
            ('rrc', 'RRC:'),
            ('phone_number', 'Phone:'),
            ('email', 'Email:'),
            ('country_code', 'Country Code:'),
            ('text_address', 'Text Address:'),
        ]

        for key, label in params:
            row = ttk.Frame(params_frame)
            row.pack(fill='x', pady=2)
            ttk.Label(row, text=label, width=20).pack(side='left')
            entry = ttk.Entry(row, width=40)
            entry.insert(0, DEFAULTS.get(key, ''))
            entry.pack(side='left', padx=5, fill='x', expand=True)
            self.entries[key] = entry

        self.save_btn = ttk.Button(
            main_frame, text='Сохранить как .xml',
            command=self.save_file
        )
        self.save_btn.pack(pady=5)

    def select_file(self):
        """Выбор xml файла."""
        path = filedialog.askopenfilename(
            title='Выберите .xml файл',
            filetypes=[('XML files', '*.xml'), ('All files', '*.*')]
        )
        if path:
            self.input_path = path
            self.file_label.config(text=os.path.basename(path))

            try:
                self.data = parse(path)
                self.update_preview()
            except Exception as e:
                messagebox.showerror('Ошибка', f'Не удалось прочитать файл:\n{e}')
                self.file_label.config(text='Ошибка чтения', foreground='red')

    def update_preview(self):
        """Обновление таблицы предпросмотра."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        import xml.etree.ElementTree as ET
        try:
            tree = ET.parse(self.input_path)
            root = tree.getroot()
            
            pack_contents = root.findall('.//pack_content')
            for i, pc in enumerate(pack_contents, 1):
                pack_code = pc.find('pack_code')
                pack_code_text = pack_code.text.strip() if pack_code is not None and pack_code.text else ''
                self.tree.insert('', 'end', values=(i, pack_code_text, len(pack_code_text)))
            
            self.count_label.config(text=f'Pack count: {len(pack_contents)}')
        except Exception as e:
            self.count_label.config(text=f'Error: {e}')

    def save_file(self):
        """Сохранение данных в XML файл."""
        if not self.input_path:
            messagebox.showerror('Ошибка', 'Сначала выберите .xml файл')
            return

        output_path = filedialog.asksaveasfilename(
            title='Сохранить как',
            defaultextension='.xml',
            filetypes=[('XML files', '*.xml'), ('All files', '*.*')]
        )
        if not output_path:
            return

        try:
            params = {key: entry.get() for key, entry in self.entries.items()}
            params['file_date_time'] = ''
            
            content = transform(self.input_path, params)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            messagebox.showinfo('Готово', 'Файл сохранён.')

        except Exception as e:
            messagebox.showerror('Ошибка', str(e))
