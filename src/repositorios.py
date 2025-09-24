# src/repositorios.py
from database import db
from modelos import Producto, Usuario, MovimientoStock
from typing import List, Optional
from datetime import datetime

class ProductoRepository:
    
    def crear(self, producto_data: dict) -> dict:
        nuevo_id = db.get_next_id()
        producto = {
            'id': nuevo_id,
            'nombre': producto_data['nombre'],
            'codigo': producto_data['codigo'], 
            'descripcion': producto_data.get('descripcion', ''),
            'precio': float(producto_data['precio']),
            'stock': int(producto_data.get('stock', 0)),
            'stock_minimo': int(producto_data.get('stock_minimo', 5)),
            'activo': True,
            'fecha_creacion': datetime.now().isoformat()
        }
        db.productos.append(producto)
        return producto
    
    def obtener_todos(self) -> List[dict]:
        return [p for p in db.productos if p['activo']]
    
    def obtener_por_id(self, id: int) -> Optional[dict]:
        return next((p for p in db.productos if p['id'] == id and p['activo']), None)
    
    def buscar_por_nombre(self, nombre: str) -> List[dict]:
        nombre_lower = nombre.lower()
        return [p for p in db.productos 
                if nombre_lower in p['nombre'].lower() and p['activo']]
    
    def actualizar_stock(self, producto_id: int, nuevo_stock: int):
        producto = self.obtener_por_id(producto_id)
        if producto:
            producto['stock'] = nuevo_stock
            return producto
        return None
    def busqueda_avanzada(self, filtros: dict) -> List[dict]:
        """GA.3: Búsqueda avanzada con múltiples filtros"""
        productos = [p for p in db.productos if p['activo']]
        
        # Filtro por código
        if filtros.get('codigo'):
            productos = [p for p in productos 
                        if filtros['codigo'].lower() in p['codigo'].lower()]
        
        # Filtro por nombre
        if filtros.get('nombre'):
            productos = [p for p in productos 
                        if filtros['nombre'].lower() in p['nombre'].lower()]
        
        # Filtro por descripción  
        if filtros.get('descripcion'):
            productos = [p for p in productos 
                        if filtros['descripcion'].lower() in p['descripcion'].lower()]
        
        # Filtro por categoría
        if filtros.get('categoria'):
            productos = [p for p in productos 
                        if p.get('categoria', '').lower() == filtros['categoria'].lower()]
        
        # Filtro por proveedor
        if filtros.get('proveedor'):
            productos = [p for p in productos 
                        if p.get('proveedor', '').lower() == filtros['proveedor'].lower()]
        
        # Filtro por rango de precios
        if filtros.get('precio_min'):
            productos = [p for p in productos 
                        if p['precio'] >= float(filtros['precio_min'])]
        
        if filtros.get('precio_max'):
            productos = [p for p in productos 
                        if p['precio'] <= float(filtros['precio_max'])]
        
        # Filtro por stock bajo
        if filtros.get('solo_stock_bajo'):
            productos = [p for p in productos 
                        if p['stock'] <= p['stock_minimo']]
        
        return productos
    
    def obtener_por_codigo(self, codigo: str) -> Optional[dict]:
        """Buscar producto por código exacto"""
        return next((p for p in db.productos 
                    if p['codigo'].lower() == codigo.lower() and p['activo']), None)
    
    def actualizar(self, id: int, datos: dict, usuario: str = 'sistema') -> dict:
        """Actualizar producto con log de modificaciones"""
        producto = self.obtener_por_id(id)
        if not producto:
            raise ValueError("Producto no encontrado")
        
        # Registrar modificaciones
        log_repo = LogModificacionRepository()
        
        for campo, nuevo_valor in datos.items():
            if campo in producto and str(producto[campo]) != str(nuevo_valor):
                log_repo.registrar_modificacion(
                    'productos', id, campo, 
                    producto[campo], nuevo_valor, usuario
                )
                producto[campo] = nuevo_valor
        
        return producto

class UsuarioRepository:
    
    def obtener_por_username(self, username: str) -> Optional[dict]:
        return next((u for u in db.usuarios if u['username'] == username), None)
    
    def obtener_todos(self) -> List[dict]:
        return db.usuarios

class MovimientoRepository:
    
    def crear(self, movimiento_data: dict) -> dict:
        nuevo_id = db.get_next_id()
        movimiento = {
            'id': nuevo_id,
            'producto_id': movimiento_data['producto_id'],
            'tipo': movimiento_data['tipo'],
            'cantidad': movimiento_data['cantidad'],
            'motivo': movimiento_data['motivo'],
            'fecha': datetime.now().isoformat()
        }
        db.movimientos.append(movimiento)
        return movimiento
    
    def obtener_por_producto(self, producto_id: int) -> List[dict]:
        return [m for m in db.movimientos if m['producto_id'] == producto_id]

class LogModificacionRepository:
    """GA.4: Repositorio para logs de modificaciones"""
    
    def registrar_modificacion(self, tabla: str, registro_id: int, campo: str, 
                             valor_anterior, valor_nuevo, usuario: str = 'sistema'):
        log = {
            'id': db.get_next_id(),
            'tabla': tabla,
            'registro_id': registro_id,
            'campo': campo,
            'valor_anterior': str(valor_anterior),
            'valor_nuevo': str(valor_nuevo),
            'usuario': usuario,
            'fecha': datetime.now().isoformat(),
            'tipo_operacion': 'UPDATE'
        }
        db.logs_modificaciones.append(log)
        return log
    
    def obtener_logs_por_tabla(self, tabla: str):
        return [log for log in db.logs_modificaciones if log['tabla'] == tabla]
    
    def obtener_logs_por_registro(self, tabla: str, registro_id: int):
        return [log for log in db.logs_modificaciones 
                if log['tabla'] == tabla and log['registro_id'] == registro_id]

class ReporteRepository:
    """GA.6: Repositorio para reportes mensuales"""
    
    def generar_reporte_mensual(self, año: int, mes: int):
        from calendar import monthrange
        import datetime
        
        # Fechas del mes
        primer_dia = datetime.datetime(año, mes, 1)
        ultimo_dia = datetime.datetime(año, mes, monthrange(año, mes)[1])
        
        # Obtener movimientos del mes (simulado)
        movimientos_mes = []
        productos = db.productos
        
        # Simular algunos movimientos para el reporte
        for i, producto in enumerate(productos[:3]):  # Solo primeros 3 para demo
            movimientos_mes.append({
                'producto_id': producto['id'],
                'producto_nombre': producto['nombre'],
                'entradas': (i + 1) * 10,  # Simulado
                'salidas': (i + 1) * 7,    # Simulado
                'stock_inicial': producto['stock'] + (i + 1) * 3,
                'stock_final': producto['stock'],
                'valor_entradas': (i + 1) * 10 * producto['precio'],
                'valor_salidas': (i + 1) * 7 * producto['precio']
            })
        
        reporte = {
            'id': db.get_next_id(),
            'año': año,
            'mes': mes,
            'fecha_generacion': datetime.datetime.now().isoformat(),
            'movimientos': movimientos_mes,
            'resumen': {
                'total_productos': len(productos),
                'total_entradas': sum(m['entradas'] for m in movimientos_mes),
                'total_salidas': sum(m['salidas'] for m in movimientos_mes),
                'valor_total_entradas': sum(m['valor_entradas'] for m in movimientos_mes),
                'valor_total_salidas': sum(m['valor_salidas'] for m in movimientos_mes)
            }
        }
        
        db.reportes_mensuales.append(reporte)
        return reporte