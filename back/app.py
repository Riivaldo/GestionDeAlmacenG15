from flask import Flask, request, jsonify
from flask_cors import CORS
from servicios import ProductoService, AuthService, StockService, FacturacionService
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Servicios
producto_service = ProductoService()
auth_service = AuthService()
stock_service = StockService()
facturacion_service = FacturacionService()

# Variables de sesión (simplificado)
usuario_actual = None

# ========== MÓDULO 1: GESTIÓN DE ARTÍCULOS ==========

@app.route('/productos', methods=['GET'])
def obtener_productos():
    try:
        productos = producto_service.obtener_productos()
        return jsonify({'productos': productos, 'total': len(productos)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/productos', methods=['POST'])
def crear_producto():
    try:
        data = request.json
        producto = producto_service.crear_producto(data)
        return jsonify({'success': True, 'producto': producto})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/productos/buscar', methods=['GET'])
def buscar_productos():
    # GA.3: Búsqueda avanzada
    query = request.args.get('q', '')
    try:
        productos = producto_service.buscar_productos(query)
        return jsonify({'productos': productos})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/productos/alertas', methods=['GET'])
def alertas_stock():
    # GA.2: Alertas con colores
    try:
        alertas = producto_service.obtener_alertas_stock()
        return jsonify({'alertas': alertas, 'total': len(alertas)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/productos/reporte-mensual', methods=['GET'])
def reporte_mensual():
    # GA.6: Reporte mensual
    try:
        reporte = producto_service.generar_reporte_mensual()
        return jsonify({'success': True, 'reporte': reporte})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ========== MÓDULO 2: GESTIÓN DE STOCK ==========

@app.route('/stock/entrada', methods=['POST'])
def entrada_stock():
    try:
        data = request.json
        movimiento = stock_service.entrada_stock(
            data['producto_id'], 
            data['cantidad'], 
            data['motivo']
        )
        return jsonify({'success': True, 'movimiento': movimiento})
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
        return jsonify({'success': True, 'movimiento': movimiento})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ========== MÓDULO 3: AUTENTICACIÓN ==========

@app.route('/login', methods=['POST'])
def login():
    # AU.1: Login básico
    try:
        data = request.json
        usuario = auth_service.login(data['username'], data['password'])
        global usuario_actual
        usuario_actual = usuario
        return jsonify({'success': True, 'usuario': usuario})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 401

@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    # AU.2: Solo admin puede ver usuarios
    if not usuario_actual or usuario_actual['role'] != 'admin':
        return jsonify({'error': 'Permisos insuficientes'}), 403
    
    try:
        usuarios = auth_service.usuario_repo.obtener_todos()
        return jsonify({'usuarios': [{'username': u['username'], 'role': u['role']} for u in usuarios]})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/logs', methods=['GET'])
def obtener_logs():
    # AU.3 y AU.4: Logs de auditoría
    if not usuario_actual or usuario_actual['role'] != 'admin':
        return jsonify({'error': 'Solo admin puede ver logs'}), 403
    
    try:
        logs = auth_service.obtener_logs_acceso()
        return jsonify({'logs': logs})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ========== MÓDULO 4: FACTURACIÓN ==========

@app.route('/facturas', methods=['POST'])
def crear_factura():
    # F.1: Facturación diferenciada
    try:
        data = request.json
        factura = facturacion_service.crear_factura(
            data['cliente'],
            data['tipo_cliente'],
            data['productos']
        )
        
        # F.3: Generar código QR
        qr_code = facturacion_service.generar_codigo_qr(factura['id'])
        factura['codigo_qr'] = qr_code
        
        return jsonify({'success': True, 'factura': factura})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/facturas', methods=['GET'])
def obtener_facturas():
    # F.2: Reportes con filtros
    try:
        filtro = request.args.get('filtro')
        facturas = facturacion_service.obtener_reportes_facturacion(filtro)
        
        # F.4: Reporte valorizado
        total_facturado = sum(f['total'] for f in facturas)
        
        return jsonify({
            'facturas': facturas,
            'total_facturado': total_facturado,
            'cantidad_facturas': len(facturas)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ========== RUTA PRINCIPAL ==========
@app.route('/')
def home():
    return jsonify({
        'mensaje': '🏢 Sistema de Almacén - Universidad',
        'modulos': {
            'modulo_1_productos': ['GET /productos', 'POST /productos', 'GET /productos/buscar', 'GET /productos/alertas', 'GET /productos/reporte-mensual'],
            'modulo_2_stock': ['POST /stock/entrada', 'POST /stock/salida'],
            'modulo_3_auth': ['POST /login', 'GET /usuarios', 'GET /logs'], 
            'modulo_4_facturacion': ['POST /facturas', 'GET /facturas']
        },
        'usuarios_demo': {'admin': '123', 'operador': '123'}
    })

if __name__ == '__main__':
    print("🚀 Iniciando Sistema de Almacén...")
    print("📦 Módulos: Productos, Stock, Auth, Facturación")
    print("🌐 Frontend: http://localhost:5000 y abrir frontend/index.html")
    print("👤 Usuarios: admin/123, operador/123")
    app.run(debug=True)