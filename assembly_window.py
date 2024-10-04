import customtkinter as ctk
from tkinter import ttk, messagebox
from database_helper import DatabaseHelper

class AssemblyWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Окно сборки")

        self.geometry("600x400")

        self.db_helper = DatabaseHelper()

        self.title_label = ctk.CTkLabel(self, text="Сборка компьютера", font=("Arial", 16))
        self.title_label.pack(pady=20)

        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.frame = ctk.CTkFrame(self.scrollable_frame)
        self.frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.selected_components = []

        self.create_component_selector("Процессор", "processors")

        self.create_component_selector("Материнская плата", "motherboards")

        self.create_component_selector("Видеокарта", "graphics_cards")

        self.create_component_selector("Оперативная память", "ram")

        self.create_component_selector("Жесткий диск", "hard_drives")

        self.create_component_selector("Блок питания", "power_supplies")

        self.create_component_selector("Корпус компьютера", "cases")

        self.create_contact_fields()

        self.total_price_label = ctk.CTkLabel(self, text="Общая цена: 0 рублей", font=("Arial", 14))
        self.total_price_label.pack(pady=10)

        self.assemble_button = ctk.CTkButton(self, text="Собрать", command=self.complete_order)
        self.assemble_button.pack(pady=10)

    def create_component_selector(self, component_name, table_name):
        ctk.CTkLabel(self.frame, text=f"{component_name}:").pack(anchor="w")
        component_options = self.db_helper.get_component_names(table_name)
        component_combobox = ctk.CTkComboBox(self.frame, values=component_options)
        component_combobox.pack(pady=5, fill = "x")
        component_combobox.bind("<<ComboboxSelected>>", lambda event, combobox=component_combobox: self.select_component(combobox))
        

    def component_options(self, table_name):
        self.db_helper.cursor.execute(f"SELECT name FROM {table_name}")

        components = self.db_helper.cursor.fetchall()

        return [component[0] for component in components]
    
    def update_total_price(self):
        self.selected_components = []

        for widget in self.frame.winfo_children():
            if isinstance(widget, ctk.CTkComboBox):
                selected_component = widget.get()
                if selected_component:
                    self.selected_components.append(selected_component)
                    self.check_last_unit(selected_component)

        total_price = 0
        for component in self.selected_components:
            for table_name in ["processors", "motherboards", "graphics_cards", "ram", "hard_drives", "power_supplies", "cases"]:
                self.db_helper.cursor.execute(f"SELECT price FROM {table_name} WHERE name = ?", (component,))
                price = self.db_helper.cursor.fetchone()
                if price:
                    total_price += price[0]

        self.total_price_label.configure(text=f"Общая цена: {total_price} рублей")

    def check_last_unit(self, component):
            for table_name in ["processors", "motherboards", "graphics_cards", "ram", "hard_drives", "power_supplies", "cases"]:
                self.db_helper.cursor.execute(f"SELECT price FROM {table_name} WHERE name = ?", (component,))
                result = self.db_helper.cursor.fetchone()
                if result:
                    quantity = result[0]

                    if quantity == 1:
                        messagebox.showinfo("Внимание", f"Последняя единица товара: {component}")

    def create_contact_fields(self):
        contact_frame = ctk.CTkFrame(self)
        contact_frame.pack(padx=20, pady=10,fill = "x")

        contact_frame.grid_rowconfigure(0, weight=1)

        contact_frame.grid_rowconfigure(1, weight=1)

        contact_frame.grid_rowconfigure(2, weight=1)

        contact_frame.grid_rowconfigure(3, weight=1)

        contact_frame.grid_rowconfigure(4, weight=1)


        self.last_name_entry = ctk.CTkEntry(contact_frame, placeholder_text="Фамилия")
        self.last_name_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.first_name_entry = ctk.CTkEntry(contact_frame, placeholder_text="Имя")
        self.first_name_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.patronymic_entry = ctk.CTkEntry(contact_frame, placeholder_text="Отчество")
        self.patronymic_entry.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.phone_number_entry = ctk.CTkEntry(contact_frame, placeholder_text="Номер телефона")
        self.phone_number_entry.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.email_entry = ctk.CTkEntry(contact_frame, placeholder_text="Email")
        self.email_entry.grid(row=4, column=0, padx=10, pady=10, sticky="ew")


    def complete_order(self):
        last_name = self.last_name_entry.get()
        first_name = self.first_name_entry.get()
        middle_name = self.middle_name_entry.get()
        phone_number = self.phone_number_entry.get()
        email = self.email_entry.get()

        if not self.selected_components:
            messagebox.showinfo("Внимание", "Выберите хотя бы один компонент")
            return
        
        order_data =[]
        total_price = 0

        for component in self.selected_components:
            for table_name in ["processors", "motherboards", "graphics_cards", "ram", "hard_drives", "power_supplies", "cases"]:
                self.db_helper.cursor.execute(f"SELECT price FROM {table_name} WHERE name = ?", (component,))
                result = self.db_helper.cursor.fetchone()
                if result:
                    name, price, quantity = result

                    if quantity > 0:
                        order_data.append((name, price, 1))
                        total_price += price
                        self.db_helper.cursor.execute(f"UPDATE {table_name} SET quantity = quantity - 1 WHERE name = ?", (component,))
                    else:
                        messagebox.showinfo("Внимание", f"Компонент {component} недоступен")
                        return
                    
        self.db_helper.conn.commit()

        order_id = self.db_helper.add_order(last_name, first_name, middle_name, phone_number, email, order_data, total_price)

        if order_id is not None:
            for component_name, price, quantity in order_data:
                self.db_helper.add_order_item(order_id, component_name, price, quantity)

            self.db_helper.conn.commit()
            messagebox.showinfo("Успех", "Компоненты оформлены. Количество комплектующих обновлено")


        else:
            messagebox.showerror("Ошибка", "Не удалось оформить заказ")

    