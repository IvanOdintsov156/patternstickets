from datetime import datetime
import customtkinter as ctk
from tkcalendar import Calendar
from database_repair import DatabaseRepair # Импортируем класс базы данных
class CalendarWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Календарь")
        self.geometry("600x600")
        self.resizable(False, False)
        self.attributes("-topmost", True)

        today = datetime.today()
        current_year = today.year
        current_month = today.month
        current_day = today.day

        self.calendar = Calendar(self, selectmode="day", year=current_year, month=current_month, day=current_day)
        self.calendar.pack(padx=10, pady=10)

        self.task_entry = ctk.CTkEntry(self, placeholder_text="Введите задачу")
        self.task_entry.pack(pady=10)

        save_button = ctk.CTkButton(self, text="Добавить задачу", command=self.add_task)
        save_button.pack(pady=(0, 5))

        close_button = ctk.CTkButton(self, text="Закрыть", command=self.destroy)
        close_button.pack(pady=(0, 10))

        self.tasks_frame = ctk.CTkFrame(self)
        self.tasks_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.database = DatabaseRepair() # Создаем экземпляр базы данных
        self.load_tasks() # Загружаем задачи из базы данных

    def load_tasks(self, event=None):
        """ Метод для загрузки задач из базы данных для выбранной даты и отображения их в списке. """
        for widget in self.tasks_frame.winfo_children():
            widget.destroy() # Очищаем предыдущие задачи
        selected_date = self.calendar.get_date() # Получаем выбранную дату
        tasks = self.database.get_all_tasks() # Получаем все задачи из базы данных
        for task in tasks:
            if task["task_date"] == selected_date: # Фильтруем задачи по выбранной дате
                task_frame = ctk.CTkFrame(self.tasks_frame) 
                task_frame.pack(pady=5, fill="x")
                text_color = "green" if task["status"] == "Выполнено" else "black"
                task_label = ctk.CTkLabel(task_frame, text=f"{task['task_date']} - {task['task']} (Статус: {task['status']})", anchor="w", text_color=text_color)
                task_label.pack(side="left", fill="x", expand=True)
                complete_button = ctk.CTkButton(task_frame, text="Выполнить", command=lambda t=task: self.complete_task(t))
                complete_button.pack(side='right', padx=5)
                delete_button = ctk.CTkButton(task_frame, text="Удалить", command=lambda t=task: self.delete_task(t))
                delete_button.pack(side="right", padx=5)
    def add_task(self):
        """ Метод для добавления задачи и отображения ее в списке. """
        task = self.task_entry.get()
        selected_date = self.calendar.get_date()
        if task:
            self.database.add_task(task, selected_date) # Сохраняем задачу в базе данных
            self.load_tasks(None) # Обновляем список задач для выбранной даты
            self.task_entry.delete(0, "end") # Очищаем поле ввода

    def delete_task(self, task):
        """ Метод для удаления выбранной задачи. """
        task_id = task["id"]
        self.database.delete_task(task_id) # Удаляем задачу из базы данных
        self.load_tasks(None) # Обновляем список задач для выбранной даты

    def complete_task(self, task):
        """ Метод для изменения статуса задачи на "Выполнено" """
        task_id = task["id"]
        self.database.cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", ("Выполнено", task_id))
        self.database.conn.commit() # Cохраняем изменения
        self.load_tasks(None) # Обновляем список задач для выбранной даты

class TaskWindow(ctk.CTkToplevel):
    def __init__(self, parent, date, database):
        super().__init__(parent)
        self.title("Создание задачи")
        self.geometry("300x200")
        self.resizable(False, False)
        # Установка метки с выбранной датой
        date_label = ctk.CTkLabel(self, text=f"Выбранная дата: {date}")
        date_label.pack(pady=10)
        # Поле для ввода задачи
        self.task_entry = ctk.CTkEntry(self, placeholder_text="Введите задачу")
        self.task_entry.pack(pady=10)
        # Кнопка для сохранения задачи
        save_button = ctk.CTkButton(self, text="Cохpанить", command=lambda: self.save_task(date))
        save_button.pack(pady=(0, 10))

        self.database = database # Сохраняем ссылку на базу данных

    def save_task(self, date):
        """ Метод для сохранения задачи """
        task = self.task_entry.get()
        if task:
            self.database.add_task(task, date) # Сохраняем задачу в базе данных
            print(f"Задача на {date}: {task} создана!")
        self.destroy()

