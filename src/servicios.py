# src/servicios.py
from repositorios import ProductoRepository, UsuarioRepository, MovimientoRepository, LogModificacionRepository, ReporteRepository
from datetime import datetime

class ProductoService:
    def __init__(self):
        self.repo = ProductoRepository()
    
    def crear_producto(self, data: dict):
        # Validaciones básicas
        if not data.get('nombre'):
            raise ValueError("El nombre es obligatorio")
        if not data.get('codigo'):
            raise ValueError("El código es obligatorio") 
        if not data.get('precio'):
            raise ValueError("El precio es obligatorio")
            
        return self.repo.crear(data)
    
    def obtener_productos(self):
        return self.repo.obtener_todos()
    
    def buscar_productos(self, query: str):
        if not query:
            return self.obtener_productos()
        return self.repo.buscar_por_nombre(query)
    def crear_producto_con_validacion(self, data: dict, usuario: str = 'sistema'):
        """GA.5: Crear producto con detección de códigos duplicados"""
        # Validaciones básicas existentes...
        if not data.get('nombre'):
            raise ValueError("El nombre es obligatorio")
        if not data.get('codigo'):
            raise ValueError("El código es obligatorio") 
        if not data.get('precio'):
            raise ValueError("El precio es obligatorio")
        
        # GA.5: Detectar código duplicado
        producto_existente = self.repo.obtener_por_codigo(data['codigo'])
        
        if producto_existente:
            return {
                'success': False,
                'error': 'CÓDIGO_DUPLICADO',
                'mensaje': f"⚠️ ALERTA: Ya existe un producto con el código '{data['codigo']}'",
                'producto_existente': {
                    'id': producto_existente['id'],
                    'nombre': producto_existente['nombre'],
                    'precio': producto_existente['precio']
                },
                'sugerencias': [
                    f"{data['codigo']}_V2",
                    f"{data['codigo']}_NUEVO",
                    f"{data['codigo']}_{datetime.now().strftime('%m%d')}"
                ]
            }
        
        # Crear producto si no hay duplicados
        producto = self.repo.crear(data)
        
        # Log de creación
        log_repo = LogModificacionRepository()
        log_repo.registrar_modificacion(
            'productos', producto['id'], 'CREACION', 
            'NULL', f"Producto creado: {producto['nombre']}", usuario
        )
        
        return {
            'success': True,
            'producto': producto,
            'mensaje': f"✅ Producto '{producto['nombre']}' creado exitosamente"
        }
    
    def busqueda_avanzada(self, filtros: dict):
        """GA.3: Búsqueda avanzada con múltiples criterios"""
        productos = self.repo.busqueda_avanzada(filtros)
        
        return {
            'productos': productos,
            'total_encontrados': len(productos),
            'filtros_aplicados': filtros,
            'mensaje': f"Se encontraron {len(productos)} productos con los filtros aplicados"
        }
    
    def obtener_alertas_stock(self):
        """GA.2: Obtener productos con alertas de stock"""
        productos = self.repo.obtener_todos()
        alertas = []
        
        for producto in productos:
            if producto['stock'] <= producto['stock_minimo']:
                nivel_alerta = 'CRÍTICO' if producto['stock'] <= 1 else 'BAJO'
                color = 'rojo' if producto['stock'] <= 1 else 'naranja'
                
                alertas.append({
                    'id': producto['id'],
                    'nombre': producto['nombre'],
                    'codigo': producto['codigo'],
                    'stock_actual': producto['stock'],
                    'stock_minimo': producto['stock_minimo'],
                    'diferencia': producto['stock_minimo'] - producto['stock'],
                    'nivel_alerta': nivel_alerta,
                    'color': color,
                    'categoria': producto.get('categoria', 'Sin categoría'),
                    'proveedor': producto.get('proveedor', 'Sin proveedor')
                })
        
        return {
            'alertas': sorted(alertas, key=lambda x: x['stock_actual']),
            'total_alertas': len(alertas),
            'criticas': len([a for a in alertas if a['nivel_alerta'] == 'CRÍTICO']),
            'bajas': len([a for a in alertas if a['nivel_alerta'] == 'BAJO'])
        }
    
    def actualizar_producto(self, id: int, datos: dict, usuario: str = 'sistema'):
        """GA.4: Actualizar producto con registro de modificaciones"""
        try:
            producto_actualizado = self.repo.actualizar(id, datos, usuario)
            return {
                'success': True,
                'producto': producto_actualizado,
                'mensaje': f"✅ Producto actualizado exitosamente"
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def generar_reporte_mensual(self, año: int = None, mes: int = None):
        """GA.6: Generar reporte mensual de movimientos"""
        if not año:
            año = datetime.now().year
        if not mes:
            mes = datetime.now().month
        
        reporte_repo =  ()
        reporte = reporte_repo.generar_reporte_mensual(año, mes)
        
        return {
            'success': True,
            'reporte': reporte,
            'mensaje': f"✅ Reporte generado para {mes}/{año}"
        }

class StockService:
    def __init__(self):
        self.producto_repo = ProductoRepository()
        self.movimiento_repo = MovimientoRepository()
    
    def entrada_stock(self, producto_id: int, cantidad: int, motivo: str):
        producto = self.producto_repo.obtener_por_id(producto_id)
        if not producto:
            raise ValueError("Producto no encontrado")
        
        # Crear movimiento
        movimiento_data = {
            'producto_id': producto_id,
            'tipo': 'entrada',
            'cantidad': cantidad,
            'motivo': motivo
        }
        movimiento = self.movimiento_repo.crear(movimiento_data)
        
        # Actualizar stock
        nuevo_stock = producto['stock'] + cantidad
        self.producto_repo.actualizar_stock(producto_id, nuevo_stock)
        
        return movimiento
    
    def salida_stock(self, producto_id: int, cantidad: int, motivo: str):
        producto = self.producto_repo.obtener_por_id(producto_id)
        if not producto:
            raise ValueError("Producto no encontrado")
        
        if producto['stock'] < cantidad:
            raise ValueError("Stock insuficiente")
        
        # Crear movimiento
        movimiento_data = {
            'producto_id': producto_id,
            'tipo': 'salida', 
            'cantidad': cantidad,
            'motivo': motivo
        }
        movimiento = self.movimiento_repo.crear(movimiento_data)
        
        # Actualizar stock
        nuevo_stock = producto['stock'] - cantidad
        self.producto_repo.actualizar_stock(producto_id, nuevo_stock)
        
        return movimiento

class AuthService:
    def __init__(self):
        self.usuario_repo = UsuarioRepository()
    
    def login(self, username: str, password: str):
        usuario = self.usuario_repo.obtener_por_username(username)
        if usuario and usuario['password'] == password:
            return {
                'username': usuario['username'],
                'role': usuario['role']
            }
        raise ValueError("Credenciales inválidas")
   