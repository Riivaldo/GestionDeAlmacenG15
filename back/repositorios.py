from database import db
from datetime import datetime

class ProductoRepository:
    def obtener_todos(self):
        return [p for p in db.productos if p['activo']]
    
    def obtener_por_id(self, id):
        return next((p for p in db.productos if p['id'] == id), None)
    
    def crear(self, data):
        producto = {
            'id': db.get_next_id(),
            'nombre': data['nombre'],
            'codigo': data['codigo'],
            'precio': float(data['precio']),
            'stock': int(data['stock']),
            'stock_minimo': int(data.get('stock_minimo', 5)),
            'activo': True,
            'categoria': data.get('categoria', ''),
            'fecha': datetime.now().isoformat()
        }
        db.productos.append(producto)
        return producto
    
    def buscar(self, query):
        return [p for p in db.productos if query.lower() in p['nombre'].lower() or query.lower() in p['codigo'].lower()]
    
    def obtener_alertas_stock(self):
        return [p for p in db.productos if p['stock'] <= p['stock_minimo']]

class UsuarioRepository:
    def obtener_por_credenciales(self, username, password):
        return next((u for u in db.usuarios if u['username'] == username and u['password'] == password), None)
    
    def obtener_todos(self):
        return db.usuarios

class MovimientoRepository:
    def crear(self, data):
        movimiento = {
            'id': db.get_next_id(),
            'producto_id': data['producto_id'],
            'tipo': data['tipo'],
            'cantidad': data['cantidad'],
            'motivo': data['motivo'],
            'fecha': datetime.now().isoformat()
        }
        db.movimientos.append(movimiento)
        return movimiento

class LogRepository:
    def registrar(self, usuario, accion, detalle=''):
        log = {
            'id': db.get_next_id(),
            'usuario': usuario,
            'accion': accion,
            'detalle': detalle,
            'fecha': datetime.now().isoformat()
        }
        db.logs_acceso.append(log)
        return log
    
    def obtener_logs(self):
        return db.logs_acceso[-50:]  # Últimos 50

class FacturaRepository:
    def crear(self, data):
        factura = {
            'id': db.get_next_id(),
            'cliente': data['cliente'],
            'tipo': data['tipo'],
            'productos': data['productos'],
            'total': data['total'],
            'fecha': datetime.now().isoformat()
        }
        db.facturas.append(factura)
        return factura
    
    def obtener_todas(self):
        return db.facturas