import tkinter as tk
import customtkinter as ctk
from datetime import datetime

# Import windows
from database_window import DatabaseWindow
from assembly_window import AssemblyWindow
from completion_window import CompletionWindow
from edit_order_window import OrdersWindow
from repair_requests_window import RepairRequestsWindow

# Import utilities
from database_repair import DatabaseRepair
from pdf_generator import generate_report

# Import additional windows
from contacts_window import ContactsWindow
from calendar_window import CalendarWindow
from document_window import DocumentationWindow
from statistics_window import StatisticsWindow


class CustomWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.theme = "light"

        self.title("Базовая система")
        self.geometry("800x600")
        self.resizable(False, False)

        self.database_repair = DatabaseRepair()

        self.time_frame = ctk.CTkFrame(self)
        self.time_frame.pack(pady=10, fill="x")

        self.time_label = ctk.CTkLabel(self.time_frame, text="", font=("Arial", 12))
        self.time_label.pack(side="bottom")

        self.calendar_icon = ctk.CTkLabel(self.time_frame, text="", font=("Arial", 25), cursor="hand2")
        self.calendar_icon.pack(side="bottom", padx=(10, 0))

        self.calendar_icon.bind("<Enter>", self.show_task_info)
        self.calendar_icon.bind("<Leave>", self.hide_task_info)

        self.these = "light"
        ctk.set_appearance_mode(self.these)

        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.pack(pady=10, fill="x")

        self.toggle_theme_button = ctk.CTkButton(self.buttons_frame, text="Переключить тему", command=self.toggle_theme)
        self.toggle_theme_button.pack(side="left", padx=5)

        self.contacts_button = ctk.CTkButton(self.buttons_frame, text="Контакты", command=self.show_contacts)
        self.contacts_button.pack(side='left', padx=5)

        self.calendar_button = ctk.CTkButton(self.buttons_frame, text="Календарь", command=self.show_calendar)
        self.calendar_button.pack(side="left", padx=5)

        self.statistics_button = ctk.CTkButton(self.buttons_frame, text="Статистика", command=self.show_statistics)
        self.statistics_button.pack(side="left", padx=5)

        self.documentation_button = ctk.CTkButton(self.buttons_frame, text="Документация", command=self.show_documentation)
        self.documentation_button.pack(side="left", padx=5)

        self.generate_button = ctk.CTkButton(self.buttons_frame, text="Формировать", command=self.generate_report,
                                            fg_color="#0e7bff", border_width=0, width=120)
        self.generate_button.pack(side="top", padx=5, pady=2)

        self.repair_scrollable_frame = ctk.CTkScrollableFrame(self, corner_radius=0, width=300, height=300)
        self.repair_scrollable_frame.pack(fill="both", expand=True)

        self.load_repair_data()

    def show_task_info(self, event):
        current_date = datetime.now().strftime("%d.%m.%Y")
        tasks = self.database_repair.get_all_tasks()
        tasks_today = [task for task in tasks if task['task_date'] == current_date]

        self.task_info_label = ctk.CTkFrame(self)
        self.task_info_label.place(x=290, y=-100)
        self.task_info_label.pack_propagate(False)

        if tasks_today:
            for task in tasks_today:
                color = "green" if task["status"] == "Выполнено" else "black"
                task_label = ctk.CTkLabel(self.task_info_label, text=f"{task['task_date']} - {task['task']} (Статус: {task['status']})", text_color=color)
                task_label.pack(anchor="w", padx=5, pady=2)
        else:
            task_label = ctk.CTkLabel(self.task_info_label, text="Нет задач", fg_color="transparent")
            task_label.pack(anchor="w", padx=5, pady=2)

        self.task_info_label.lift()

    def hide_task_info(self, event):
        self.task_info_label.place_forget()

    def create_button(self, text, command):
        return ctk.CTkButton(self.buttons_frame, text=text, command=command)

    def update_time(self):
        now = datetime.now()
        formatted_time = now.strftime("Дата: %d.%m.%Y Время: %H:%M:%S")
        self.time_label.configure(text=formatted_time)
        self.after(1000, self.update_time)

    def open_database_window(self):
        database_window = DatabaseWindow(self)
        database_window.mainloop()

    def open_assembly_window(self):
        assembly_window = AssemblyWindow(self)
        assembly_window.mainloop()

    def open_completion_window(self):
        completion_window = CompletionWindow(self)
        completion_window.mainloop()

    def open_orders_window(self):
        orders_window = OrdersWindow()
        orders_window.mainloop()

    def open_repair_window(self):
        def on_repair_window_close():
            self.load_repair_data()

        repair_window = RepairRequestsWindow(on_close_callback=on_repair_window_close)
        repair_window.mainloop()

    def load_repair_data(self):
        repair_orders = self.database_repair.get_all_repair_orders()
        
        for idx, order in enumerate(repair_orders, start=1):
            order_frame = ctk.CTkFrame(self.repair_scrollable_frame, border_width=8)
            order_frame.pack(pady=5, fill='x', padx=10)

            order_info = (
                f"Заявка #{idx}\n"
                f"Фамилия: {order['surname']}\n"
                f"Имя: {order['first_name']}\n"
                f"Отчество: {order['patronymic']}\n"
                f"Комплектующие: {order['components']}\n"
                f"Описание проблемы: {order['problem_description']}\n"
                f"Телефон: {order['phone']}\n"
                f"Email: {order['email']}\n"
                f"Ожидаемая дата завершения: {order['expected_completion_date']}\n"
                f"Статус: {order['status']}"
            )

            info_label = ctk.CTkLabel(order_frame, text=order_info, anchor="w", justify="left")
            info_label.pack(side='left', fill="x", expand=True)

            button_frame = ctk.CTkFrame(order_frame)
            button_frame.pack(side="right")

            button_color = "#28a745" if order["status"] == "Выполнено" else "#007bff"
            button_text = "Выполнено" if order["status"] == "Выполнено" else "Выполнить"
            execute_button = ctk.CTkButton(button_frame, text=button_text, command=lambda o=order: self.execute_order(o),
                                           fg_color=button_color, border_width=0, width=120)
            execute_button.pack(side="top", padx=5, pady=2)

            delete_button = ctk.CTkButton(button_frame, text="Удалить", command=lambda o=order: self.delete_order(o),
                                          fg_color="#dc3545", border_width=0, width=120)
            delete_button.pack(side="top", padx=5, pady=2)

            edit_button = ctk.CTkButton(button_frame, text="Редактировать", command=lambda o=order: self.edit_order(o),
                                        fg_color="#ffc107", border_width=0, width=120)
            edit_button.pack(side="top", padx=5, pady=2)

            generate_button = ctk.CTkButton(button_frame, text="Формировать", command=lambda o=order: self.generate_report(o),
                                            fg_color="#0e7bff", border_width=0, width=120)
            generate_button.pack(side="top", padx=5, pady=2)

    def execute_order(self, order):
        self.database_repair.cursor.execute(
            "UPDATE repair_orders SET status = ? WHERE id = ?", ("Выполнено", order["id"])
        )
        self.database_repair.conn.commit()
        self.load_repair_data()

    def delete_order(self, order):
        self.database_repair.delete_repair_order(order["id"])
        self.load_repair_data()

    def edit_order(self, order):
        edit_window = EditOrderWindow(order, self.database_repair, on_close_callback=self.load_repair_data)
        edit_window.mainloop()

    def generate_report(self, order):
        pdf_filename = generate_report(order, self.database_repair)
        print(f"Отчет для заявки №{order['id']} успешно создан: {pdf_filename}")

    def toggle_theme(self):
        if self.theme == "light":
            self.theme = "dark"
        else:
            self.theme = "light"
        ctk.set_appearance_mode(self.theme)

    def show_contacts(self):
        ContactsWindow(self)

    def show_calendar(self):
        CalendarWindow(self)
        

    def show_statistics(self):
        stats_window = StatisticsWindow(self)

    def show_documentation(self):
        DocumentationWindow(self)

    def filter_orders(self):
        search_query = self.search_entry.get().strip()
        if search_query.startswith("#"):
            # Remove "#" from the query, if it exists
            search_query = search_query[1:].strip()

        # Clear current orders
        for widget in self.repair_scrollable_frame.winfo_children():
            widget.destroy()

        # Load filtered orders
        all_orders = self.database_repair.get_all_repair_orders()
        if not search_query:
            self.load_repair_data()
            return

        filtered_orders = [order for order in all_orders if
                           search_query.lower() in order['surname'].lower() or
                           search_query.lower() in order['first_name'].lower() or
                           search_query.lower() in order["patronymic"].lower() or
                           search_query == str(order['id']) or
                           search_query in order['phone'] or
                           search_query in order['expected_completion_date']
                           ]

        if filtered_orders:
            for order in filtered_orders:
                order_frame = ctk.CTkFrame(self.repair_scrollable_frame, borderwidth=0)
                order_frame.pack(pady=5, fill="x", padx=10)

                order_info = (
                    f"ID заявки: {order['id']}\n"
                    f"Фамилия: {order['surname']}\n"
                    f"Имя: {order['first_name']}\n"
                    f"Отчество: {order['patronymic']}\n"
                    f"Комплектующие: {order['components']}\n"
                    f"Описание проблемы: {order['problem_description']}\n"
                    f"Телефон: {order['phone']}\n"
                    f"Email: {order['email']}\n"
                    f"Ожидаемая дата завершения: {order['expected_completion_date']}\n"
                    f"Статус: {order['status']}\n"
                )

                info_label = ctk.CTkLabel(order_frame, text=order_info, anchor="w", justify="left")
                info_label.pack(side="left", fill="x", expand=True)

                button_frame = ctk.CTkFrame(order_frame)
                button_frame.pack(side="right")

                button_color = "#28a745" if order["status"] == "Выполнено" else "#007bff"
                button_text = "Выполнено" if order["status"] == "Выполнено" else "Выполнить"
                execute_button = ctk.CTkButton(button_frame, text=button_text, command=lambda o=order: self.execute_order(o),
                                               fg_color=button_color, border_width=0, width=120)
                execute_button.pack(side="top", padx=5, pady=2)

                delete_button = ctk.CTkButton(button_frame, text="Удалить", command=lambda o=order: self.delete_order(o),
                                              fg_color="#dc3545", border_width=0, width=120)
                delete_button.pack(side="top", padx=5, pady=2)

                edit_button = ctk.CTkButton(button_frame, text="Редактировать", command=lambda o=order: self.edit_order(o),
                                            fg_color="#ffc107", border_width=0, width=120)
                edit_button.pack(side="top", padx=5, pady=2)

                generate_button = ctk.CTkButton(button_frame, text="Формировать", command=lambda o=order: self.generate_report(o),
                                                fg_color="#0e7bff", border_width=0, width=120)
                generate_button.pack(side="top", padx=5, pady=2)

                if not filtered_orders:
                    no_results_label = ctk.CTkLabel(self.repair_scrollable_frame, text="Отсутствуют заявки, соответствующие критериям поиска.", anchor="w", justify="left")
                    no_results_label.pack(pady=5, padx=10)
class EditOrderWindow(ctk.CTk):
    def __init__(self, order, database_repair, on_close_callback):
        super().__init__()
        self.title("Редактировать заявку")
        self.geometry("400x400")
        self.order = order
        self.database_repair = database_repair
        self.on_close_callback = on_close_callback

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        ctk.CTkLabel(self, text="Фамилия").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.surname_entry = ctk.CTkEntry(self, placeholder_text="Фамилия")
        self.surname_entry.insert(0, order["surname"])
        self.surname_entry.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(self, text="Имя").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.first_name_entry = ctk.CTkEntry(self, placeholder_text="Имя")
        self.first_name_entry.insert(0, order["first_name"])
        self.first_name_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(self, text="Отчество").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.patronimic_entry = ctk.CTkEntry(self, placeholder_text="Отчество")
        self.patronimic_entry.insert(0, order["patronymic"])
        self.patronimic_entry.grid(row=2, column=1, padx=10, pady=5)

        ctk.CTkLabel(self, text="Комплектующие").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.components_combobox = ctk.CTkComboBox(self, values=["Материнская плата", "Процессор", "Оперативная память", "Жесткий диск", "Видеокарта"])
        self.components_combobox.set(order["components"])
        self.components_combobox.grid(row=3, column=1, padx=10, pady=5)

        ctk.CTkLabel(self, text="Описание проблемы").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.problem_description_entry = ctk.CTkEntry(self, placeholder_text="Описание проблемы")
        self.problem_description_entry.insert(0, order["problem_description"])
        self.problem_description_entry.grid(row=4, column=1, padx=10, pady=5)

        ctk.CTkLabel(self, text="Телефон").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.phone_entry = ctk.CTkEntry(self, placeholder_text="Телефон")
        self.phone_entry.insert(0, order["phone"])
        self.phone_entry.grid(row=5, column=1, padx=10, pady=5)

        ctk.CTkLabel(self, text="Email").grid(row=6, column=0, padx=10, pady=5, sticky="e")
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email")
        self.email_entry.insert(0, order["email"])
        self.email_entry.grid(row=6, column=1, padx=10, pady=5)

        ctk.CTkLabel(self, text="Ожидаемая дата завершения").grid(row=7, column=0, padx=10, pady=5, sticky="e")
        self.expected_completion_date_entry = ctk.CTkEntry(self, placeholder_text="Ожидаемая дата завершения")
        self.expected_completion_date_entry.insert(0, order["expected_completion_date"])
        self.expected_completion_date_entry.grid(row=7, column=1, padx=10, pady=5)

        # Save button
        save_button = ctk.CTkButton(self, text="Сохранить", command=self.save_order)
        save_button.grid(row=8, column=0, columnspan=2, pady=10)

    def save_order(self):
        # Update the order in the database
        self.database_repair.cursor.execute("""
            UPDATE repair_orders
            SET surname=?, first_name=?, patronymic=?, components=?, problem_description=?, phone=?, email=?, expected_completion_date=?
            WHERE id=?""",
            (self.surname_entry.get(), self.first_name_entry.get(), self.patronimic_entry.get(), self.components_combobox.get(),
             self.problem_description_entry.get(), self.phone_entry.get(), self.email_entry.get(), self.expected_completion_date_entry.get(),
             self.order["id"]))
        self.database_repair.conn.commit()
        self.on_close_callback()
        self.destroy()
