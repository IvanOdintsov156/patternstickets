import customtkinter as ctk
from tkinter import messagebox
from database_helper import DatabaseHelper

class CompletionWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Окно докомплектации")
        self.geometry("600x400")

        self.db_helper = DatabaseHelper()

        self.title_label = ctk.CTkLabel(self, text="Введите информацию о комплектующих", font=("Arial", 16))
        self.title_label.pack(pady=20)

        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.frame = ctk.CTkFrame(self.scrollable_frame)
        self.frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.component_quantities = {}

        self.display_components()


    def display_components(self):
        component_tables = {"processors": "Процессоры",
                            "motherboards": "Материнские платы",
                            "graphics_cards": "Видеокарты",
                            "ram": "Оперативные памяти",
                            "hard_drives": "Жесткие диски",
                            "power_supplies": "Блоки питания",
                            "cases": "Корпусы компьютеров"}

        self.component_frames = {} # Хранение ссылок на фреймы компонентов

        for table_name, category in component_tables.items():
            ctk.CTkLabel(self.frame, text=category, font=("Arial", 14, "bold")).pack(anchor="w", pady=(10,5))

            # Получаем компоненты из базы данных
            self.db_helper.cursor.execute(f"SELECT name, specs, price, quantity FROM {table_name}")
            components = self.db_helper.cursor.fetchall()

            for component in components:
                name, specs, price, quantity = component
                component_info = f"{name}: {specs}, {price} рублей, Количество: {quantity}"

                # Создаем фрейм для размещения информации о компоненте и кнопок
                component_frame = ctk.CTkFrame(self.frame)
                component_frame.pack(pady=5, fill="x")

                # Создаем метку для найменования компонента
                component_label = ctk.CTkLabel(component_frame, text=component_info, font=("Arial", 12))
                component_label.pack(side = "left", padx = 5)

                # Кнопка "+" для увеличения количества
                increase_button = ctk.CTkButton(component_frame, text="+", command=lambda name=name: self.increase_quantity(name, component_label), width=40, height=20)
                increase_button.pack(side="right", padx=5)

                # Кнопка "-" для уменьшения количества
                decrease_button = ctk.CTkButton(component_frame, text="-", command=lambda name=name, component_label=component_label: self.decrease_quantity(name, component_label), fg_color="red", hover_color="darkred")
                decrease_button.pack(side="right", padx=5)

                # Добавляем компонент в словарь
                self.component_quantities[name] = quantity
                self.component_frames[name] = component_label


    def increase_quantity(self, component_name, component_label):
        # Увеличиваем количество компонента на 1
        if component_name in self.component_quantities:
            self.component_quantities[component_name] += 1
            self.update_component_label(component_name, component_label)

    def decrease_quantity(self, component_name, component_label):
        # Уменьшаем количество компонента на 1
        if component_name in self.component_quantities:
            if self.component_quantities[component_name] > 0:
                self.component_quantities[component_name] -= 1
                self.update_component_label(component_name, component_label)

    def update_component_label(self, component_name, component_label):
        # Обновляем метку компонента
        new_quantity = self.component_quantities[component_name]
        table_name = self.get_table_name(component_name)
        component_label.configure(text=f"{component_name}: {self.get_specs(table_name, component_name)}, {self.get_price(table_name, component_name)} рублей, Количество: {new_quantity}")


    def get_table_name(self, component_name):
        # Определяем таблицу компонента по имени
        component_tables = {"processors": "Процессоры",
                            "motherboards": "Материнские платы",
                            "graphics_cards": "Видеокарты",
                            "ram": "Оперативные памяти",
                            "hard_drives": "Жесткие диски",
                            "power_supplies": "Блоки питания",
                            "cases": "Корпусы компьютеров"}

        for table_name, name in component_tables.items():
            self.db_helper.cursor.execute(f"SELECT specs FROM {table_name} WHERE name = ?", (component_name,))
            specs = self.db_helper.cursor.fetchone()
            if specs:
                return table_name
        return None
    def get_specs(self, table_name, component_name):
            self.db_helper.cursor.execute(f"SELECT specs FROM {table_name} WHERE name = ?", (component_name,))
            specs = self.db_helper.cursor.fetchone()
            return specs[0] if specs else "Неизвестно"
        

    def get_price(self, table_name, component_name):
            self.db_helper.cursor.execute(f"SELECT price FROM {table_name} WHERE name = ?", (component_name,))
            price = self.db_helper.cursor.fetchone()
            return price[0] if price else "Неизвестно"
        
    def save_changes(self):
            # Обновляем количество компонентов в базе данных
            for component_name, quantity in self.component_quantities.items():
                table_name = self.get_table_name(component_name)
                if table_name:
                    self.db_helper.cursor.execute(f"UPDATE {table_name} SET quantity = ? WHERE name = ?", (quantity, component_name))

            self.db_helper.conn.commit()
            messagebox.showinfo("Успех", "Изменения успешно сохранены")
        
        
