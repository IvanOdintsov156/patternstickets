import customtkinter as ctk
from tkinter import messagebox
from database_helper import DatabaseHelper

class DatabaseWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Окно базы данных")

        self.geometry("500x400")

        self.db_helper = DatabaseHelper()

        self.scrollable_frame = ctk.CTkScrollableFrame(self, corner_radius=0)
        self.scrollable_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.frame = ctk.CTkFrame(self.scrollable_frame)
        self.frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.title_label = ctk.CTkLabel(self, text="Введите информацию о комплектующих", font=("Arial", 16))
        self.title_label.pack(pady=10)

        self.create_component_inputs("Процессор", "processors")

        self.create_component_inputs("Материнская плата", "motherboards")

        self.create_component_inputs("Видеокарта", "graphics_cards")

        self.create_component_inputs("Оперативная память", "ram")

        self.create_component_inputs("Жесткий диск", "hard_drives")
        self.create_component_inputs("Клавиатура", "keyboards")
        self.create_component_inputs("Мышка", "mice")
        self.create_component_inputs("Монитор", "monitor")

        self.create_component_inputs("Блок питания", "power_supplies")
        self.create_component_inputs("Корпус компьютера", "cases")


    def create_component_inputs(self, component_name, table_name):
        ctk.CTkLabel(self.frame, text=f"{component_name}:").pack(anchor="w")
        name_entry = ctk.CTkEntry(self.frame, placeholder_text=f"Название {component_name.lower()}")
        name_entry.pack(pady=5, fill = "x")

        specs_entry = ctk.CTkEntry(self.frame, placeholder_text=f"Характеристики {component_name.lower()}")
        specs_entry.pack(pady=5, fill = "x")

        price_entry = ctk.CTkEntry(self.frame, placeholder_text=f"Цена {component_name.lower()}")
        price_entry.pack(pady=5, fill = "x")

        quantity_entry = ctk.CTkEntry(self.frame, placeholder_text=f"Количество {component_name.lower()}")
        quantity_entry.pack(pady=5, fill = "x")

        add_button = ctk.CTkButton(self.frame, text="Добавить", command=lambda: self.add_component_info(table_name, name_entry.get(), specs_entry.get(), price_entry.get(), quantity_entry.get()))
        add_button.pack(pady=10)


    def add_component_info(self, table_name, name, specs, price, quantity):
        if not all([name, specs, price, quantity]):
            messagebox.showwarning("Предупреждение", "Пожалуйста, заполните все поля")
            return
        
        if not self.db_helper.add_component_info(table_name, name, specs, price, quantity):
            messagebox.showinfo("Успех", "Данные успешно внесены")
        else:
            messagebox.showerror("Ошибка", "Не удалось добавить информацию о комплектующем")
