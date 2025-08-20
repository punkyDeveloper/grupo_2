# =============================================================================
# API SIMPLE - FUNCIONA EN LOCAL Y RENDER.COM
# Archivo: back/api/desercion_api.py
# =============================================================================

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app)  # Permitir requests desde cualquier origen

# =============================================================================
# CONFIGURACIÓN CON .ENV (OPTIMIZADA PARA RENDER)
# =============================================================================

# 🔧 DETECCIÓN AUTOMÁTICA DE ENTORNO
# Si existe PORT en las variables de entorno = Render.com
if os.getenv('PORT'):
    ENTORNO = 'servidor'
    PUERTO = int(os.getenv('PORT'))
    DEBUG = False
    print("🚀 RENDER.COM detectado automáticamente")
else:
    # Configuración local con .env
    ENTORNO = os.getenv('ENTORNO', 'local')
    PUERTO = int(os.getenv('PUERTO', 5000))
    DEBUG = os.getenv('DEBUG', 'true').lower() == 'true'

RUTA_DATOS = os.getenv('RUTA_DATOS', '')

print(f"🔧 Entorno: {ENTORNO.upper()}")
print(f"🚪 Puerto: {PUERTO}")
print(f"🐛 Debug: {DEBUG}")

# =============================================================================
# RUTAS DE ARCHIVOS CON .ENV (OPTIMIZADA PARA RENDER)
# =============================================================================

def configurar_rutas():
    """Configurar rutas usando .env"""
    
    if RUTA_DATOS:
        # Si está definida en .env, usar esa ruta
        base_dir = Path(RUTA_DATOS)
        print(f"📁 Usando ruta del .env: {base_dir}")
        
    elif ENTORNO == 'servidor':
        # 🚀 Render.com: los archivos están en /opt/render/project/src
        base_dir = Path('/opt/render/project/src')
        print(f"📁 Servidor (Render) - ruta: {base_dir}")
        
    else:
        # Local: ruta relativa desde back/api/ hacia la raíz
        base_dir = Path(__file__).parent.parent.parent
        print(f"📁 Local - ruta relativa: {base_dir}")
    
    return {
        'udea': base_dir / 'udea_datos_completos.csv',
        'udea_año': base_dir / 'udea_resumen_por_año.csv', 
        'udea_sede': base_dir / 'udea_resumen_por_sede.csv',
        'nacional': base_dir / 'desercion_consolidado_PANDAS.csv',
        'sexo': base_dir / 'desercion_por_sexo_PANDAS.csv',
        'metodologia': base_dir / 'desercion_por_metodologia_PANDAS.csv',
        'area': base_dir / 'desercion_por_area_conocimiento_PANDAS.csv'
    }

ARCHIVOS = configurar_rutas()

# =============================================================================
# FUNCIÓN SIMPLE PARA CARGAR CSV
# =============================================================================

def cargar_csv(nombre):
    """Cargar CSV de forma simple"""
    try:
        archivo = ARCHIVOS.get(nombre)
        if not archivo or not archivo.exists():
            print(f"❌ No encontrado: {archivo}")
            return None
        
        df = pd.read_csv(archivo)
        print(f"✅ Cargado {nombre}: {len(df)} registros")
        return df
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# =============================================================================
# ENDPOINTS SIMPLES
# =============================================================================

@app.route('/')
def inicio():
    """Página de inicio con información"""
    
    # Verificar qué archivos están disponibles
    archivos_ok = {}
    for nombre, ruta in ARCHIVOS.items():
        archivos_ok[nombre] = ruta.exists()
    
    return jsonify({
        "api": "Deserción Universidad de Antioquia",
        "entorno": ENTORNO.upper(),
        "puerto": PUERTO,
        "estado": "🟢 API funcionando correctamente",
        "archivos_disponibles": archivos_ok,
        "endpoints": [
            "/ - Esta información",
            "/udea - Datos completos UdeA",
            "/udea/stats - Estadísticas UdeA", 
            "/udea/años - Promedio por año",
            "/udea/sedes - Promedio por sede",
            "/udea/filtro?año=2020&sede=Principal - Filtrar datos",
            "/nacional/sexo - Deserción por sexo",
            "/nacional/metodologia - Por metodología",
            "/nacional/area - Por área de conocimiento"
        ]
    })

@app.route('/udea')
def udea_datos():
    """Todos los datos de UdeA"""
    df = cargar_csv('udea')
    if df is None:
        return jsonify({"error": "No se pudieron cargar los datos de UdeA"}), 404
    
    return jsonify({
        "universidad": "Universidad de Antioquia",
        "total_registros": len(df),
        "columnas": list(df.columns),
        "datos": df.to_dict('records')
    })

@app.route('/udea/stats')
def udea_estadisticas():
    """Estadísticas simples de UdeA"""
    df = cargar_csv('udea')
    if df is None:
        return jsonify({"error": "No se pudieron cargar los datos"}), 404
    
    return jsonify({
        "universidad": "Universidad de Antioquia",
        "desercion": {
            "promedio": round(df['desercion'].mean(), 2),
            "minimo": round(df['desercion'].min(), 2),
            "maximo": round(df['desercion'].max(), 2)
        },
        "total_registros": len(df),
        "periodo": f"{df['año'].min()}-{df['año'].max()}",
        "sedes_total": df['nombre_sede'].nunique(),
        "sedes_lista": sorted(df['nombre_sede'].unique().tolist())
    })

@app.route('/udea/años')
def udea_por_años():
    """Datos UdeA agrupados por año"""
    df = cargar_csv('udea')
    if df is None:
        return jsonify({"error": "No se pudieron cargar los datos"}), 404
    
    por_año = df.groupby('año')['desercion'].mean().round(2)
    
    return jsonify({
        "universidad": "Universidad de Antioquia",
        "tipo": "Promedio de deserción por año",
        "datos": [
            {"año": int(año), "desercion_promedio": float(desercion)} 
            for año, desercion in por_año.items()
        ]
    })

@app.route('/udea/sedes')
def udea_por_sedes():
    """Datos UdeA por sedes"""
    df = cargar_csv('udea')
    if df is None:
        return jsonify({"error": "No se pudieron cargar los datos"}), 404
    
    por_sede = df.groupby('nombre_sede')['desercion'].mean().round(2).sort_values()
    
    return jsonify({
        "universidad": "Universidad de Antioquia",
        "tipo": "Promedio de deserción por sede",
        "mejor_sede": {
            "nombre": por_sede.index[0],
            "desercion_promedio": float(por_sede.iloc[0])
        },
        "peor_sede": {
            "nombre": por_sede.index[-1], 
            "desercion_promedio": float(por_sede.iloc[-1])
        },
        "todas_sedes": {str(k): float(v) for k, v in por_sede.items()}
    })

@app.route('/nacional/sexo')
def nacional_sexo():
    """Datos nacionales por sexo"""
    df = cargar_csv('sexo')
    if df is None:
        return jsonify({"error": "No se pudieron cargar los datos de sexo"}), 404
    
    por_sexo = df.groupby('sexo')['porcentaje'].mean().round(2)
    
    return jsonify({
        "tipo": "Deserción nacional por sexo",
        "datos": {
            "hombres": float(por_sexo.get('Hombre', 0)),
            "mujeres": float(por_sexo.get('Mujer', 0)),
            "diferencia": round(float(por_sexo.get('Hombre', 0)) - float(por_sexo.get('Mujer', 0)), 2)
        }
    })

@app.route('/nacional/metodologia')
def nacional_metodologia():
    """Datos nacionales por metodología"""
    df = cargar_csv('metodologia')
    if df is None:
        return jsonify({"error": "No se pudieron cargar los datos de metodología"}), 404
    
    por_metodologia = df.groupby('metodologia')['porcentaje'].mean().round(2).sort_values(ascending=False)
    
    return jsonify({
        "tipo": "Deserción nacional por metodología",
        "mas_critica": {
            "metodologia": por_metodologia.index[0],
            "porcentaje": float(por_metodologia.iloc[0])
        },
        "mas_estable": {
            "metodologia": por_metodologia.index[-1],
            "porcentaje": float(por_metodologia.iloc[-1])  
        },
        "todas": {str(k): float(v) for k, v in por_metodologia.items()}
    })

@app.route('/nacional/area')
def nacional_area():
    """Datos nacionales por área"""
    df = cargar_csv('area')
    if df is None:
        return jsonify({"error": "No se pudieron cargar los datos de área"}), 404
    
    por_area = df.groupby('area_conocimiento')['porcentaje'].mean().round(2).sort_values(ascending=False)
    
    return jsonify({
        "tipo": "Deserción nacional por área de conocimiento", 
        "top_5_mayor_desercion": {str(k): float(v) for k, v in por_area.head(5).items()},
        "top_5_menor_desercion": {str(k): float(v) for k, v in por_area.tail(5).items()}
    })

# Endpoint para filtrar datos con parámetros
@app.route('/udea/filtro')
def udea_filtrado():
    """Filtrar datos UdeA por parámetros (año, sede)"""
    df = cargar_csv('udea')
    if df is None:
        return jsonify({"error": "No se pudieron cargar los datos"}), 404
    
    # Obtener filtros de la URL (?año=2020&sede=Principal)
    año = request.args.get('año', type=int)
    sede = request.args.get('sede')
    
    df_filtrado = df.copy()
    filtros_aplicados = {}
    
    if año:
        df_filtrado = df_filtrado[df_filtrado['año'] == año]
        filtros_aplicados['año'] = año
        
    if sede:
        df_filtrado = df_filtrado[df_filtrado['nombre_sede'].str.contains(sede, case=False)]
        filtros_aplicados['sede'] = sede
    
    return jsonify({
        "universidad": "Universidad de Antioquia",
        "filtros_aplicados": filtros_aplicados,
        "total_registros": len(df_filtrado),
        "datos": df_filtrado.to_dict('records')
    })

# =============================================================================
# CONFIGURACIÓN AUTOMÁTICA HOST Y PUERTO
# =============================================================================

def obtener_configuracion():
    """Detectar configuración automáticamente para Render.com"""
    
    # 🚀 RENDER.COM: Si existe PORT = estamos en Render
    if os.getenv('PORT'):
        return {
            'host': '0.0.0.0',  # OBLIGATORIO para Render.com
            'port': int(os.getenv('PORT')),
            'debug': False,
            'entorno': 'RENDER.COM'
        }
    
    # 💻 LOCAL: Desarrollo local
    else:
        return {
            'host': 'localhost',
            'port': PUERTO,
            'debug': DEBUG,
            'entorno': 'LOCAL'
        }

# =============================================================================
# EJECUTAR LA API
# =============================================================================

if __name__ == '__main__':
    
    # 🔧 Configuración automática
    config = obtener_configuracion()
    
    print(f"\n🚀 Iniciando API de Deserción")
    print(f"🌍 Entorno: {config['entorno']}")
    print(f"🌐 Host: {config['host']}")
    print(f"🚪 Puerto: {config['port']}")
    print(f"🐛 Debug: {config['debug']}")
    print(f"📁 Buscando datos en: {list(ARCHIVOS.values())[0].parent}")
    
    print(f"\n📊 Endpoints principales:")
    print(f"   http://{config['host']}:{config['port']}/ - Información general")
    print(f"   http://{config['host']}:{config['port']}/udea - Datos UdeA completos")
    print(f"   http://{config['host']}:{config['port']}/udea/stats - Estadísticas resumen")
    print(f"   http://{config['host']}:{config['port']}/udea/filtro?año=2020 - Filtros")
    
    # Verificar archivos al inicio
    print(f"\n📋 Verificando archivos CSV...")
    archivos_encontrados = 0
    for nombre, ruta in ARCHIVOS.items():
        if ruta.exists():
            print(f"   ✅ {nombre}: {ruta.name}")
            archivos_encontrados += 1
        else:
            print(f"   ❌ {nombre}: {ruta}")
    
    if archivos_encontrados == 0:
        print(f"\n⚠️  NO SE ENCONTRARON ARCHIVOS CSV")
        print(f"   📁 Verifica que los archivos estén en: {list(ARCHIVOS.values())[0].parent}")
    else:
        print(f"\n✅ {archivos_encontrados}/{len(ARCHIVOS)} archivos encontrados")
    
    print(f"\n🎯 ¡API lista para usar!")
    print(f"\n🔥 INICIANDO SERVIDOR...")
    
    # 🚀 EJECUTAR CON CONFIGURACIÓN AUTOMÁTICA
    app.run(
        debug=config['debug'], 
        host=config['host'], 
        port=config['port']
    )