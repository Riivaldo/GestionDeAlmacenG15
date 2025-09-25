from datetime import datetime

class InMemoryDB:
    def __init__(self):
        self.productos = [
            {'id': 1, 'nombre': 'Laptop HP', 'codigo': 'LAP001', 'precio': 899.99, 'stock': 25, 'stock_minimo': 5, 'activo': True, 'categoria': 'Computadoras'},
            {'id': 2, 'nombre': 'Mouse Logitech', 'codigo': 'MOU001', 'precio': 29.99, 'stock': 3, 'stock_minimo': 5, 'activo': True, 'categoria': 'Periféricos'},
            {'id': 3, 'nombre': 'Teclado Gaming', 'codigo': 'TEC001', 'precio': 89.99, 'stock': 1, 'stock_minimo': 3, 'activo': True, 'categoria': 'Periféricos'}
        ]
        self.usuarios = [
            {'id': 1, 'username': 'admin', 'password': '123', 'role': 'admin'},
            {'id': 2, 'username': 'operador', 'password': '123', 'role': 'operador'}
        ]
        self.movimientos = []
        self.logs_acceso = []
        self.facturas = []
        self.next_id = 4
    
    def get_next_id(self):
        current = self.next_id
        self.next_id += 1
        return current

db = InMemoryDB()