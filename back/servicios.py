from repositorios import ProductoRepository, UsuarioRepository, MovimientoRepository, LogRepository, FacturaRepository
from datetime import datetime

class ProductoService:
    def __init__(self):
        self.repo = ProductoRepository()
        self.log_repo = LogRepository()
    
    def obtener_productos(self):
        return self.repo.obtener_todos()
    
    def crear_producto(self, data):
        # GA.5: Validar código duplicado
        productos = self.repo.obtener_todos()
        if any(p['codigo'] == data['codigo'] for p in productos):
            raise ValueError(f"Código {data['codigo']} ya existe")
        
        # GA.1: Validaciones
        if not data.get('nombre') or not data.get('codigo'):
            raise ValueError("Nombre y código son obligatorios")
        
        producto = self.repo.crear(data)
        
        # GA.4: Log de modificación
        self.log_repo.registrar('sistema', 'CREAR_PRODUCTO', f"Producto {producto['nombre']} creado")
        
        return producto
    
    def buscar_productos(self, query):
        # GA.3: Búsqueda avanzada
        return self.repo.buscar(query)
    
    def obtener_alertas_stock(self):
        # GA.2: Alertas de stock
        alertas = self.repo.obtener_alertas_stock()
        for alerta in alertas:
            if alerta['stock'] <= 1:
                alerta['color'] = 'rojo'
                alerta['nivel'] = 'CRÍTICO'
            else:
                alerta['color'] = 'naranja' 
                alerta['nivel'] = 'BAJO'
        return alertas
    
    def generar_reporte_mensual(self):
        # GA.6: Reporte mensual
        productos = self.repo.obtener_todos()
        return {
            'total_productos': len(productos),
            'valor_inventario': sum(p['precio'] * p['stock'] for p in productos),
            'productos_bajo_stock': len(self.repo.obtener_alertas_stock()),
            'fecha': datetime.now().isoformat()
        }

class AuthService:
    def __init__(self):
        self.usuario_repo = UsuarioRepository()
        self.log_repo = LogRepository()
    
    def login(self, username, password):
        # AU.1: Autenticación
        usuario = self.usuario_repo.obtener_por_credenciales(username, password)
        if not usuario:
            # AU.4: Log de intento fallido
            self.log_repo.registrar(username, 'LOGIN_FALLIDO', 'Credenciales incorrectas')
            raise ValueError("Credenciales incorrectas")
        
        # AU.4: Log de acceso exitoso  
        self.log_repo.registrar(usuario['username'], 'LOGIN_EXITOSO', f"Acceso como {usuario['role']}")
        return usuario
    
    def verificar_permisos(self, usuario, accion):
        # AU.2: Control por roles
        permisos = {
            'admin': ['crear', 'editar', 'eliminar', 'ver_usuarios', 'auditoria'],
            'operador': ['crear', 'editar', 'ver']
        }
        return accion in permisos.get(usuario['role'], [])
    
    def obtener_logs_acceso(self):
        # AU.3: Logs de acceso
        return self.log_repo.obtener_logs()

class StockService:
    def __init__(self):
        self.producto_repo = ProductoRepository()
        self.movimiento_repo = MovimientoRepository()
    
    def entrada_stock(self, producto_id, cantidad, motivo):
        producto = self.producto_repo.obtener_por_id(producto_id)
        if not producto:
            raise ValueError("Producto no encontrado")
        
        # Actualizar stock
        producto['stock'] += cantidad
        
        # Registrar movimiento
        return self.movimiento_repo.crear({
            'producto_id': producto_id,
            'tipo': 'entrada',
            'cantidad': cantidad,
            'motivo': motivo
        })
    
    def salida_stock(self, producto_id, cantidad, motivo):
        producto = self.producto_repo.obtener_por_id(producto_id)
        if not producto:
            raise ValueError("Producto no encontrado")
        
        if producto['stock'] < cantidad:
            raise ValueError("Stock insuficiente")
        
        # Actualizar stock
        producto['stock'] -= cantidad
        
        # Registrar movimiento
        return self.movimiento_repo.crear({
            'producto_id': producto_id,
            'tipo': 'salida', 
            'cantidad': cantidad,
            'motivo': motivo
        })

class FacturacionService:
    def __init__(self):
        self.factura_repo = FacturaRepository()
        self.producto_repo = ProductoRepository()
    
    def crear_factura(self, cliente, tipo_cliente, productos):
        # F.1: Facturación diferenciada
        descuento = 0.1 if tipo_cliente == 'mayorista' else 0.05
        
        total = 0
        for item in productos:
            producto = self.producto_repo.obtener_por_id(item['producto_id'])
            subtotal = producto['precio'] * item['cantidad']
            subtotal_con_descuento = subtotal * (1 - descuento)
            total += subtotal_con_descuento
        
        factura_data = {
            'cliente': cliente,
            'tipo': tipo_cliente,
            'productos': productos,
            'total': total
        }
        
        return self.factura_repo.crear(factura_data)
    
    def obtener_reportes_facturacion(self, filtro=None):
        # F.2: Reportes con filtros
        facturas = self.factura_repo.obtener_todas()
        if filtro:
            facturas = [f for f in facturas if filtro in f['cliente'] or f['tipo'] == filtro]
        return facturas
    
    def generar_codigo_qr(self, factura_id):
        # F.3: Código QR (simulado)
        return f"QR-{factura_id}-{datetime.now().strftime('%Y%m%d')}"