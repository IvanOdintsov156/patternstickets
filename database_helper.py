import sqlite3

class DatabaseHelper:
    def __init__(self, db_name='db_name'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        tables = {'processors': '(name TEXT, specs TEXT, price REAL, quantity INTEGER)',
                  'motherboards': '(name TEXT, specs TEXT, price REAL, quantity INTEGER)',
                  'graphics_cards': '(name TEXT, specs TEXT, price REAL, quantity INTEGER)',
                  'ram': '(name TEXT, specs TEXT, price REAL, quantity INTEGER)',
                  'hard_drives': '(name TEXT, specs TEXT, price REAL, quantity INTEGER)',
                  'keyboards': '(name TEXT, specs TEXT, price REAL, quantity INTEGER)',
                  'mice': '(name TEXT, specs TEXT, price REAL, quantity INTEGER)',
                  'monitor': '(name TEXT, specs TEXT, price REAL, quantity INTEGER)',
                  'power_supplies': '(name TEXT, specs TEXT, price REAL, quantity INTEGER)',
                  'cases': '(name TEXT, specs TEXT, price REAL, quantity INTEGER)',
                  'orders': '(id INTEGER PRIMARY KEY AUTOINCREMENT, last_name TEXT, first_name TEXT, middle_name TEXT, phone TEXT, email TEXT, total_price REAL)',
                  'order_items': '(id INTEGER PRIMARY KEY AUTOINCREMENT, order_id INTEGER, component_name TEXT, price REAL, quantity INTEGER, FOREIGN KEY(order_id) REFERENCES orders(id))'}
        
        for table, columns in tables.items():
            self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {table} {columns}')
        self.conn.commit()

    def add_component_info(self, table_name, name, specs, price, quantity):
        try:
            self.cursor.execute(f"INSERT INTO {table_name} (name, specs, price, quantity) VALUES (?, ?, ?, ?)", (name, specs, float(price), int(quantity)))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении компонента в таблицу {table_name}: {e}")
            return False
        
    def add_order(self, last_name, first_name, middle_name, phone, email, total_price):
        try:
            self.cursor.execute(f"INSERT INTO orders (last_name, first_name, middle_name, phone, email, total_price) VALUES (?, ?, ?, ?, ?, ?)", (last_name, first_name, middle_name, phone, email, float(total_price)))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении заказа: {e}")
            return None
        
    def add_order_item(self, order_id, component_name, price, quantity):
        try:
            self.cursor.execute(f"INSERT INTO order_items (order_id, component_name, price, quantity) VALUES (?, ?, ?, ?)", (order_id, component_name, float(price), int(quantity)))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении элемента заказа: {e}")
            return None
    
    def create_order_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS orders 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             last_name TEXT, 
                             first_name TEXT, 
                             middle_name TEXT, 
                             phone TEXT, 
                             email TEXT, 
                             total_price REAL)"""
                            )
        self.conn.commit()

    def create_order_items_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS order_items 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             order_id INTEGER, 
                             component_name TEXT, 
                             price REAL, 
                             quantity INTEGER, 
                             FOREIGN KEY(order_id) REFERENCES orders(id))"""
                            )
        self.conn.commit()

    def get_component_names(self, table_name):
        self.cursor.execute(f"SELECT name FROM {table_name}")
        return [row[0] for row in self.cursor.fetchall()]

