import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from database_repair import DatabaseRepair

class RepairRequestsWindow(ctk.CTk):
    def __init__(self, on_close_callback):
        super().__init__()
        self.on_close_callback = on_close_callback
        self.title("Оформление заявки на ремонт")
        self.geometry("800x600")

        self.database_repair = DatabaseRepair()

        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.surname_label = ctk.CTkLabel(self.form_frame,  text="Фамилия:", font=("Arial", 12))
        self.surname_label.grid(row=0, column=0, padx =10, pady=10,  sticky="e")
        self.surname_entry = ctk.CTkEntry(self.form_frame)
        self.surname_entry.grid(row=0,  column=1, padx =10, pady=5)

        self.first_name_label =  ctk.CTkLabel(self.form_frame,  text="Имя:")
        self.first_name_label.grid(row=1, column=0, padx =10, pady=5, sticky="e")
        self.first_name_entry =  ctk.CTkEntry(self.form_frame)
        self.first_name_entry.grid(row=1, column=1, padx =10, pady=5)

        self.patronimic_label =  ctk.CTkLabel(self.form_frame,  text="Отчество:")
        self.patronimic_label.grid(row=2, column=0, padx =10, pady=5, sticky="e")
        self.patronymic_entry =  ctk.CTkEntry(self.form_frame)
        self.patronymic_entry.grid(row=2, column=1, padx =10, pady=5)

        self.components_label =  ctk.CTkLabel(self.form_frame,  text="Комплектующие")
        self.components_label.grid(row=3, column=0, padx =10, pady=5, sticky="e")
        self.components_combobox =  ctk.CTkComboBox(self.form_frame, values=["Процессоры",  "Материнские платы", "Видеокарты", "Оперативные памяти", "Жесткие диски", "Клавиатуры", "Мыши", "Мониторы", "Блоки питания", "Корпусы компьютеров"])

        self.components_combobox.grid(row=3, column=1, padx =10, pady=5)

        self.problem_description_label =  ctk.CTkLabel(self.form_frame,  text="Описание проблемы:")
        self.problem_description_label.grid(row=4, column=0, padx =10, pady=5, sticky="e")
        self.problem_description_text =  ctk.CTkTextbox(self.form_frame, height=180)
        self.problem_description_text.grid(row=4, column=1, padx =10, pady=5)

        self.phone_label = ctk.CTkLabel(self.form_frame, text="Телефон:")
        self.phone_label.grid(row=5, column=0, padx =10, pady=5, sticky="e")
        self.phone_entry = ctk.CTkEntry(self.form_frame)
        self.phone_entry.grid(row=5, column=1, padx =10, pady=5)

        self.email_label = ctk.CTkLabel(self.form_frame, text="Email:")
        self.email_label.grid(row=6, column=0, padx =10, pady=5, sticky="e")
        self.email_entry =  ctk.CTkEntry(self.form_frame)
        self.email_entry.grid(row=6, column=1, padx =10, pady=5)

        self.expected_completion_date_label = ctk.CTkLabel(self.form_frame, text="Ожидаемая дата выполнения:")
        self.expected_completion_date_label.grid(row=7, column=0, padx =10, pady=5, sticky="e")
        self.expected_completion_date_entry = ctk.CTkEntry(self.form_frame)
        self.expected_completion_date_entry.grid(row=7, column=1, padx =10, pady=5)

        self.submit_button = ctk.CTkButton(self.form_frame, text="Отправить заявку", command=self.submit_request)
        self.submit_button.grid(row=8, column=0, columnspan=2, pady=20)

    def submit_request(self):
        surname = self.surname_entry.get()
        first_name = self.first_name_entry.get()
        patronymic = self.patronymic_entry.get()
        components = self.components_combobox.get()
        problem_description = self.problem_description_text.get("1.0", 'end-1c')
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        expected_completion_date = self.expected_completion_date_entry.get()
        
        self.database_repair.add_repair_order(
            surname, first_name, patronymic, components, problem_description, phone, email, expected_completion_date, status = "В работе"
        )

        self.surname_entry.delete(0, 'end')
        self.first_name_entry.delete(0, 'end')
        self.patronymic_entry.delete(0, 'end')
        self.components_combobox.set("")
        self.problem_description_text.delete("1.0", 'end')
        self.phone_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.expected_completion_date_entry.delete(0, 'end')
        
        self.destroy()

        if self.on_close_callback:
            self.on_close_callback()

