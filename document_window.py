import customtkinter as ctk
from tkinter import filedialog, messagebox
import os

class DocumentationWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Документация")
        self.geometry("900x500")
        self.resizable(False, False)

        # Создайте базовую папку и подпапки, если они не существуют
        self.datasheet_folder = "Datasheet"
        self.subfolders = [
            "Процессоры", "Видеокарты", "Материнские платы", "Оперативная память",
            "Жесткие диски", "Клавиатуры", "Мышки", "Блоки питания",
            "Мониторы", "Корпуса компьютеров"
        ]
        if not os.path.exists(self.datasheet_folder):
            os.makedirs(self.datasheet_folder)
        for folder in self.subfolders:
            os.makedirs(os.path.join(self.datasheet_folder, folder), exist_ok=True)
        
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=10)
        for index, folder in enumerate(self.subfolders):
            button = ctk.CTkButton(self.button_frame, text=f"{folder}", command=lambda f=folder: self.load_document(f))
            button.grid(row=index // 3, column=index % 3, padx=10, pady=5)
        
        # Фрейм для поиска
        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.pack(pady=18)
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Введите название файла для поиска", width=300)
        self.search_entry.pack(side="left", padx=(10, 0), fill="x", expand=True)
        self.search_button = ctk.CTkButton(self.search_frame, text="Поиск", command=self.search_files)
        self.search_button.pack(side="right", padx=(5, 10))
        
        # Фрейм для отображения загруженных файлов
        self.file_list_frame = ctk.CTkScrollableFrame(self, width=380, height=300)
        self.file_list_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Заголовки для таблицы
        self.headers_label = ctk.CTkLabel(self.file_list_frame, text="ID Название файла", anchor="w", font=("Arial", 12, "bold"))
        self.headers_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        
        # Обновлять список файлов при инициализации
        self.update_file_list()
    
    def load_document(self, category):
        """Загрузите документ для указанной категории и сохраните его в соответствующей подпапке."""
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            file_name = os.path.basename(file_path)
            # Определите путь для указанной категории
            destination_path = os.path.join(self.datasheet_folder, category, file_name)
            # Сохраните файл в соответствующей подпапке
            with open(file_path, "rb") as source_file:
                with open(destination_path, "wb") as dest_file:
                    dest_file.write(source_file.read())
            messagebox.showinfo("Успех", f"Документ {file_name} успешно загружен в {category} !")
            self.update_file_list()  # Обновите список файлов

    def update_file_list(self):
        """Обновите список загруженных файлов в зависимости от выбранной категории."""
        for widget in self.file_list_frame.winfo_children():
            widget.destroy()

        # Изблекать файлы из всех подпапок
        all_files = []

        for folder in self.subfolders:
            path = os.path.join(self.datasheet_folder, folder)
            all_files.extend([(folder, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])

        if all_files:
            for index, (folder, file) in enumerate(all_files, start=1):
                file_label = ctk.CTkLabel(self.file_list_frame, text=f"{index} {file} (Категория: {folder})", anchor="w")
                file_label.grid(row=index, column=0, padx=5, pady=2, sticky='w')

                delete_button = ctk.CTkButton(self.file_list_frame, text="Удалить", command=lambda f=file, cat=folder: self.delete_file(cat, f))
                delete_button.grid(row=index, column=1, padx=5, pady=2)

                open_button = ctk.CTkButton(self.file_list_frame, text="Открыть", command=lambda f=file, cat=folder: self.open_file(cat, f))
                open_button.grid(row=index, column=2, padx=5, pady=2)
        else:
            empty_label = ctk.CTkLabel(self.file_list_frame, text="Папка пуста", anchor="e")

    def search_files(self):
        """Выполняйте поиск файлов во всех подпапках на основе поискового запроса."""
        search_query = self.search_entry.get().strip().lower()
        for widget in self.file_list_frame.winfo_children():
            widget.destroy()
        # Извлекать файлы из всех блаженных папок
        all_files = []
        for folder in self.subfolders:
            path = os.path.join(self.datasheet_folder, folder)
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            all_files.extend([(folder, f) for f in files])
        if all_files:
            for index, (folder, file) in enumerate(all_files, start=1):
                if search_query in file.lower():  # Check if search query is in the filename
                    file_label = ctk.CTkLabel(self.file_list_frame, text=f"{index} {file} (Категория: {folder})", anchor="w")
                    file_label.grid(row=index, column=0, padx=5, pady=2, sticky="w")
                    delete_button = ctk.CTkButton(self.file_list_frame, text="Удалить", command=lambda f=file, cat=folder: self.delete_file(cat, f))
                    delete_button.grid(row=index, column=1, padx=5, pady=2)
                    open_button = ctk.CTkButton(self.file_list_frame, text="Открыть", command=lambda f=file, cat=folder: self.open_file(cat, f))
                    open_button.grid(row=index, column=2, padx=5, pady=2)
        else:
            empty_label = ctk.CTkLabel(self.file_list_frame, text="Нет файлов, соответствующих запросу.", anchor="w")
            empty_label.grid(row=1, column=0, padx=5, pady=2)

    def delete_file(self, category, file_name):
        """Удалите выбранный файл из соответствующей подпапки."""
        if os.path.exists(file_path):
            file_path = os.path.join(self.datasheet_folder, category, file_name)
            os.remove(file_path)
            messagebox.showinfo("Успех", f"Файл {file_name} успешно удален!")
            self.update_file_list()  # Обновите список файлов после удаления
        else:
            messagebox.showerror("Ошибка", f"Файл {file_name} не найден!")

    def search_files(self):
        """Выполняйте поиск файлов во всех подпапках на основе поискового запроса."""
        search_query = self.search_entry.get().strip().lower()
        for widget in self.file_list_frame.winfo_children():
            widget.destroy()
        # Извлекать файлы из всех блаженных папок
        all_files = []
        for folder in self.subfolders:
            path = os.path.join(self.datasheet_folder, folder)
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            all_files.extend([(folder, f) for f in files])
        if all_files:
            for index, (folder, file) in enumerate(all_files, start=1):
                if search_query in file.lower():  # Check if search query is in the filename
                    file_label = ctk.CTkLabel(self.file_list_frame, text=f"{index} {file} (Категория: {folder})", anchor="w")
                    file_label.grid(row=index, column=0, padx=5, pady=2, sticky="w")
                    delete_button = ctk.CTkButton(self.file_list_frame, text="Удалить", command=lambda f=file, cat=folder: self.delete_file(cat, f))
                    delete_button.grid(row=index, column=1, padx=5, pady=2)
                    open_button = ctk.CTkButton(self.file_list_frame, text="Открыть", command=lambda f=file, cat=folder: self.open_file(cat, f))
                    open_button.grid(row=index, column=2, padx=5, pady=2)
        else:
            empty_label = ctk.CTkLabel(self.file_list_frame, text="Нет файлов, соответствующих запросу.", anchor="w")
            empty_label.grid(row=1, column=0, padx=5, pady=2)

    def delete_file(self, category, file_name):
        """Удалите выбранный файл из соответствующей подпапки."""
        file_path = os.path.join(self.datasheet_folder, category, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            messagebox.showinfo("Успех", f"Файл {file_name} успешно удален!")
            self.update_file_list()  # Обновите список файлов после удаления
        else:
            messagebox.showerror("Ошибка", f"Файл {file_name} не найден!")

    def open_file(self, category, file_name):
        """Open the selected file with the default PDF viewer."""
        file_path = os.path.join(self.datasheet_folder, category, file_name)
        if os.path.exists(file_path):
            os.startfile(file_path)  # Use os.startfile to open the file
        else:
            messagebox.showerror("Ошибка", f"Файл {file_name} не найден!")

