# src/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from servicios import ProductoService, StockService, AuthService
from repositorios import LogModificacionRepository, ReporteRepository

app = Flask(__name__)
CORS(app)

# Servicios
producto_service = ProductoService()
stock_service = StockService()
auth_service = AuthService()

# ===== RUTAS DE PRODUCTOS =====
@app.route('/productos', methods=['GET'])
def obtener_productos():
    try:
        productos = producto_service.obtener_productos()
        return jsonify(productos)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/productos', methods=['POST'])
def crear_producto():
    try:
        producto = producto_service.crear_producto(request.json)
        return jsonify(producto), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/productos/buscar', methods=['GET'])
def buscar_productos():
    query = request.args.get('q', '')
    try:
        productos = producto_service.buscar_productos(query)
        return jsonify(productos)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ===== RUTAS DE STOCK =====
@app.route('/stock/entrada', methods=['POST'])
def entrada_stock():
    try:
        data = request.json
        movimiento = stock_service.entrada_stock(
            data['producto_id'],
            data['cantidad'], 
            data['motivo']
        )
        return jsonify(movimiento), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/stock/salida', methods=['POST'])
def salida_stock():
    try:
        data = request.json
        movimiento = stock_service.salida_stock(
            data['producto_id'],
            data['cantidad'],
            data['motivo']
        )
        return jsonify(movimiento), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ===== RUTAS DE AUTH =====
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        usuario = auth_service.login(data['username'], data['password'])
        return jsonify(usuario)
    except Exception as e:
        return jsonify({'error': str(e)}), 401

@app.route('/productos/alertas-stock', methods=['GET'])
def alertas_stock():
    """GA.2: Alertas de stock con color naranja/rojo"""
    try:
        resultado = producto_service.obtener_alertas_stock()
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ===== GA.3: BÚSQUEDA AVANZADA =====
@app.route('/productos/busqueda-avanzada', methods=['POST'])
def busqueda_avanzada():
    """GA.3: Búsqueda por código, descripción, categoría, proveedor"""
    try:
        filtros = request.json or {}
        resultado = producto_service.busqueda_avanzada(filtros)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ===== GA.4: LOGS DE MODIFICACIONES =====
@app.route('/productos/<int:producto_id>/historial', methods=['GET'])
def historial_modificaciones(producto_id):
    """GA.4: Ver historial de modificaciones de un producto"""
    try:
        log_repo = LogModificacionRepository()
        logs = log_repo.obtener_logs_por_registro('productos', producto_id)
        
        return jsonify({
            'producto_id': producto_id,
            'modificaciones': logs,
            'total_modificaciones': len(logs)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/productos/<int:producto_id>', methods=['PUT'])
def actualizar_producto(producto_id):
    """GA.4: Actualizar producto con registro automático"""
    try:
        datos = request.json
        usuario = datos.pop('usuario', 'sistema')  # Usuario que hace la modificación
        
        resultado = producto_service.actualizar_producto(producto_id, datos, usuario)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ===== GA.5: DETECCIÓN DE CÓDIGOS DUPLICADOS =====
@app.route('/productos/crear-con-validacion', methods=['POST'])
def crear_producto_con_validacion():
    """GA.5: Crear producto con detección de códigos duplicados"""
    try:
        datos = request.json
        usuario = datos.pop('usuario', 'sistema')
        
        resultado = producto_service.crear_producto_con_validacion(datos, usuario)
        
        if resultado['success']:
            return jsonify(resultado), 201
        else:
            return jsonify(resultado), 409  # Conflict
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ===== GA.6: REPORTE MENSUAL =====
@app.route('/productos/reporte-mensual', methods=['GET'])
def reporte_mensual():
    """GA.6: Generar reporte mensual de movimientos"""
    try:
        año = request.args.get('año', type=int)
        mes = request.args.get('mes', type=int)
        
        resultado = producto_service.generar_reporte_mensual(año, mes)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ===== RUTA PARA VER TODOS LOS LOGS =====
@app.route('/logs/productos', methods=['GET'])
def todos_los_logs_productos():
    """Ver todos los logs de productos"""
    try:
        log_repo = LogModificacionRepository()
        logs = log_repo.obtener_logs_por_tabla('productos')
        
        return jsonify({
            'logs': logs,
            'total': len(logs)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ===== RUTA DE PRUEBA =====
@app.route('/')
def home():
    return jsonify({
        'mensaje': '🚀 Sistema de Almacén - MÓDULO 1 COMPLETO!',
        'modulo_1_endpoints': [
            'GET /productos - Ver todos los productos',
            'POST /productos - Crear producto básico',
            'POST /productos/crear-con-validacion - GA.5: Crear con detección duplicados',
            'PUT /productos/<id> - GA.4: Actualizar con logs',
            'GET /productos/buscar?q=nombre - Búsqueda básica',
            'POST /productos/busqueda-avanzada - GA.3: Búsqueda avanzada',
            'GET /productos/alertas-stock - GA.2: Alertas de stock',
            'GET /productos/<id>/historial - GA.4: Ver modificaciones',
            'GET /productos/reporte-mensual - GA.6: Reporte mensual',
            'GET /logs/productos - Ver todos los logs'
        ],
        'otros_endpoints': [
            'POST /stock/entrada - Entrada de stock',
            'POST /stock/salida - Salida de stock', 
            'POST /login - Iniciar sesión'
        ]
    })

if __name__ == '__main__':
    app.run(debug=True)
    
