# src/database.py - BASE DE DATOS EN MEMORIA
from datetime import datetime
from typing import List, Optional

# "BASE DE DATOS" (solo listas en memoria)
# src/database.py - REEMPLAZAR COMPLETO
from datetime import datetime

class InMemoryDB:
    def __init__(self):
        # Tablas como listas
        self.productos = []
        self.usuarios = []
        self.movimientos = []
        self.logs_modificaciones = []  # NUEVO
        self.reportes_mensuales = []   # NUEVO
        self.next_id = 1
        
        # Cargar datos iniciales
        self._cargar_datos_iniciales()
        self._cargar_productos_demo()  # NUEVO
    
    def get_next_id(self):
        current = self.next_id
        self.next_id += 1
        return current
    
    def _cargar_datos_iniciales(self):
        # Usuarios iniciales
        self.usuarios = [
            {
                'id': 1,
                'username': 'admin',
                'password': '123',
                'role': 'admin',
                'active': True
            },
            {
                'id': 2, 
                'username': 'operador',
                'password': '123',
                'role': 'operador',
                'active': True
            }
        ]
        
        # Productos iniciales para demo
        self.productos = [
            {
                'id': 1,
                'nombre': 'Laptop HP',
                'codigo': 'LAP001',
                'descripcion': 'Laptop HP Core i5',
                'precio': 899.99,
                'stock': 25,
                'stock_minimo': 5,
                'categoria': 'Computadoras',
                'proveedor': 'HP',
                'activo': True,
                'fecha_creacion': datetime.now().isoformat()
            },
            {
                'id': 2,
                'nombre': 'Mouse Logitech', 
                'codigo': 'MOU001',
                'descripcion': 'Mouse inalámbrico Logitech',
                'precio': 29.99,
                'stock': 100,
                'stock_minimo': 10,
                'categoria': 'Periféricos',
                'proveedor': 'Logitech',
                'activo': True,
                'fecha_creacion': datetime.now().isoformat()
            }
        ]
        
        self.next_id = 3  # Próximo ID disponible

    def _cargar_productos_demo(self):
        """Productos adicionales para demostración"""
        productos_demo = [
            {
                'id': 3,
                'nombre': 'Teclado Mecánico',
                'codigo': 'TEC001',
                'descripcion': 'Teclado mecánico RGB gaming',
                'precio': 89.99,
                'stock': 3,  # Stock bajo para alertas
                'stock_minimo': 5,
                'categoria': 'Periféricos',
                'proveedor': 'Corsair',
                'activo': True,
                'fecha_creacion': datetime.now().isoformat()
            },
            {
                'id': 4,
                'nombre': 'Monitor 4K',
                'codigo': 'MON001',
                'descripcion': 'Monitor 27 pulgadas 4K',
                'precio': 299.99,
                'stock': 1,  # Stock crítico
                'stock_minimo': 3,
                'categoria': 'Monitores',
                'proveedor': 'Samsung',
                'activo': True,
                'fecha_creacion': datetime.now().isoformat()
            },
            {
                'id': 5,
                'nombre': 'Auriculares Gaming',
                'codigo': 'AUR001',
                'descripcion': 'Auriculares con micrófono',
                'precio': 79.99,
                'stock': 15,
                'stock_minimo': 10,
                'categoria': 'Audio',
                'proveedor': 'HyperX',
                'activo': True,
                'fecha_creacion': datetime.now().isoformat()
            }
        ]
        
        self.productos.extend(productos_demo)
        self.next_id = 6

# Instancia global (nuestra "base de datos")
db = InMemoryDB()

