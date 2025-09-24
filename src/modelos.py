# src/modelos.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Producto:
    id: int
    nombre: str
    codigo: str
    descripcion: str
    precio: float
    stock: int
    stock_minimo: int
    activo: bool = True
    fecha_creacion: str = None
    
    def __post_init__(self):
        if self.fecha_creacion is None:
            self.fecha_creacion = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'codigo': self.codigo,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'stock': self.stock,
            'stock_minimo': self.stock_minimo,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion
        }

@dataclass  
class Usuario:
    id: int
    username: str
    password: str
    role: str
    active: bool = True
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'active': self.active
            # NO incluir password en respuesta
        }

@dataclass
class MovimientoStock:
    id: int
    producto_id: int
    tipo: str  # 'entrada' o 'salida'
    cantidad: int
    motivo: str
    fecha: str = None
    
    def __post_init__(self):
        if self.fecha is None:
            self.fecha = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            'id': self.id,
            'producto_id': self.producto_id,
            'tipo': self.tipo,
            'cantidad': self.cantidad,
            'motivo': self.motivo,
            'fecha': self.fecha
        }