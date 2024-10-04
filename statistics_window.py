import customtkinter as ctk
from database_repair import DatabaseRepair
from datetime import datetime

class StatisticsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Статистика")
        self.geometry("900x600") 
        self.resizable(False, False)
        self.attributes("-topmost", True)

        # Instance of DatabaseRepair
        self.database = DatabaseRepair()

        # Header Label
        self.title_label = ctk.CTkLabel(self, text="Статистика по заявкам", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=10)

        # Frame for main table with scrollbar
        self.table_frame = ctk.CTkScrollableFrame(self, width=860, height=300)
        self.table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Table headers
        headers = ["ID", "Фамилия", "Имя", "Отчество", "Телефон", "Email", "Статус", "Дата создания", "Дата выполнения", "Время выполнения"]
        for idx, header in enumerate(headers):
            label = ctk.CTkLabel(self.table_frame, text=header, font=("Arial", 12, "bold"), anchor="w")
            label.grid(row=0, column=idx, padx=5, pady=5, sticky='ew')

        # Load all orders
        self.load_data()  # Assuming this method is defined elsewhere

        self.component_count_frame = ctk.CTkScrollableFrame(self, width=860, height=200)

                # Frame for component counts table with scrollbar
        self.component_count_frame = ctk.CTkScrollableFrame(self, width=860, height=200)
        self.component_count_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Table headers for component counts
        component_headers = ["Комплектующие", "Количество выполненных заявок"]
        for idx, header in enumerate(component_headers):
            label = ctk.CTkLabel(self.component_count_frame, text=header, font=("Arial", 12, "bold"), anchor="w")
            label.grid(row=0, column=idx, padx=5, pady=5, sticky="ew")

        
        # Load and display completed component counts
        self.load_component_counts()

        

        # Close button
        self.close_button = ctk.CTkButton(self, text="Закрыть", command=self.destroy)
        self.close_button.pack(pady=10)

    def load_component_counts(self):
        # Load component counts data from the database
        component_counts = self.database.get_all_repair_orders()

        # Display the component counts data in the table
        for i, component in enumerate(component_counts, start=1):
            ctk.CTkLabel(self.component_count_frame, text=component["component"], anchor="w").grid(row=i, column=0, padx=5, pady=2)
            ctk.CTkLabel(self.component_count_frame, text=str(component["count"]), anchor="w").grid(row=i, column=1, padx=5, pady=2)

    def load_data(self):
        """ Method to load and display order data in the table. """
        repair_orders = self.database.get_all_repair_orders()
        for i, order in enumerate(repair_orders, start=1):
            # Define text color based on status
            text_color = "green" if order['status'] == "Выполнено" else "black"
            ctk.CTkLabel(self.table_frame, text=str(order['id']), anchor="w", text_color=text_color).grid(row=i, column=0, padx=5, pady=2)
            ctk.CTkLabel(self.table_frame, text=order["surname"], anchor="w", text_color=text_color).grid(row=i, column=1, padx=5, pady=2)
            ctk.CTkLabel(self.table_frame, text=order["first_name"], anchor="w", text_color=text_color).grid(row=i, column=2, padx=5, pady=2)
            ctk.CTkLabel(self.table_frame, text=order["patronymic"], anchor="w", text_color=text_color).grid(row=i, column=3, padx=5, pady=2)
            ctk.CTkLabel(self.table_frame, text=order["phone"], anchor="w", text_color=text_color).grid(row=i, column=4, padx=5, pady=2)
            ctk.CTkLabel(self.table_frame, text=order["email"], anchor="w", text_color=text_color).grid(row=i, column=5, padx=5, pady=2)
            ctk.CTkLabel(self.table_frame, text=order["status"], anchor="w", text_color=text_color).grid(row=i, column=6, padx=5, pady=2)
            
            # Format dates
            created_date = datetime.strptime(order["created_date"], "%Y-%m-%d%H:%M:%S").strftime("%d.%m.%Y") if order["created_date"] != "Не указано" else "Не указано"
            completed_date = datetime.strptime(order["completed_date"], "%Y-%m-%d%H:%M:%S").strftime("%d.%m.%Y") if order["completed_date"] else "Не завершено"
            
            ctk.CTkLabel(self.table_frame, text=created_date, anchor="w", text_color=text_color).grid(row=i, column=7, padx=5, pady=2)
            ctk.CTkLabel(self.table_frame, text=completed_date, anchor="w", text_color=text_color).grid(row=i, column=8, padx=5, pady=2)
            
            if order["completed_date"]:
                time_spent = datetime.strptime(order["completed_date"], "%Y-%m-%d%H:%M:%S") - datetime.strptime(order["created_date"], "%Y-%m-%d%H:%M:%S")
                time_spent_days = time_spent.days
                time_spent_hours, remainder = divmod(time_spent.seconds, 3600)
                time_spent_minutes, time_spent_seconds = divmod(remainder, 60)
                time_spent_str = f"{time_spent_days} д {time_spent_hours} ч {time_spent_minutes} мин"
            else:
                time_spent_str = "Не завершено"
            
            ctk.CTkLabel(self.table_frame, text=time_spent_str, anchor="w", text_color=text_color).grid(row=i, column=9, padx=5, pady=2)
