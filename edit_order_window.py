import customtkinter as ctk
from tkinter import messagebox
from database_helper import DatabaseHelper

class OrdersWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Окно заказов")

        self.geometry("1200x600")

        self.db_helper = DatabaseHelper()

        self.title_label = ctk.CTkLabel(self, text="Заказы", font=("Arial", 16))
        self.title_label.pack(pady=20)

        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(pady=20, padx=20, fill="both", expand=True)


        self.x_scroll = ctk.CTkScrollableFrame(self.table_frame)
        self.x_scroll.pack(side="bottom", fill="x")

        self.y_scroll = ctk.CTkScrollableFrame(self.table_frame)
        self.y_scroll.pack(side="right", fill="y")


        self.header_table = ctk.CTkFrame(self.table_frame)
        self.header_table.pack(fill="x")

        headers = ["ID", "Фамилия", "Имя", "Отчество", "Телефон", "E-mail", "Компоненты", "Итоговая сумма"]

        for header in headers:
            ctk.CTkLabel(self.header_table, text=header, font=("Arial", 12, "bold"), width=150, anchor="w").pack(side="left", padx=5, pady=5)

        self.load_button = ctk.CTkButton(self, text="Загрузить данные", command=self.load_data())
        self.load_button.pack(pady=10)

    def load_data(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        query = """
        SELECT o.id as order_id, o.last_name, o.first_name, o.middle_name, o.phone, o.email, o.total_price
        FROM orders o"""

        self.db_helper.cursor.execute(query)

        orders = self.db_helper.cursor.fetchall()

        for order in orders:
            order_id, last_name, first_name, middle_name, phone, email, total_price = order

            item_query = """
            SELECT component_name, price, quantity
            FROM order_items WHERE order_id = ?"""
            self.db_helper.cursor.execute(item_query, (order_id,))

            items = self.db_helper.cursor.fetchall()

            components_str = "\n".join([f"{item[0]} - Цена: {item[1]}, Кол-во: {item[2]}" for item in items])

            total_price = str(item[1] * item[2] for item in items)

            self.add_row(order_id, last_name, first_name, middle_name, phone, email, components_str, total_price)

    def add_row(self, order_id, last_name, first_name, middle_name, phone, email, components_str, total_price):
        row_frame = ctk.CTkFrame(self.data_frame)
        row_frame.pack(fill="x", padx=2, pady=5)

        data = [order_id, last_name, first_name, middle_name, phone, email, components_str, total_price]

        for item in data:
            ctk.CTkLabel(row_frame, text=item, font=("Arial", 12), anchor="w", wraplength=150).pack(side="left", padx=5, pady=2)

