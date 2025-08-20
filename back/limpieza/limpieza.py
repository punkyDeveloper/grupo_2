import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os
warnings.filterwarnings('ignore')

print("=== ANÁLISIS SIMPLE - UNIVERSIDAD DE ANTIOQUIA ===")
print("🏛️  Universidad: UNIVERSIDAD DE ANTIOQUIA")
print("📚 Nivel: UNIVERSITARIO")
print("🗓️  Periodo: 2010-2022")
print("=" * 50)

# Diccionario con nombres de sedes
nombres_sedes = {
    1201: 'Sede Principal Medellín',
    1219: 'Sede Regional Oriente',
    1220: 'Sede Regional Norte',
    1221: 'Sede Regional Occidente',
    1222: 'Sede Regional Magdalena Medio',
    1223: 'Sede Regional Urabá',
    9125: 'Sede Regional Bajo Cauca'
}

# Archivo a leer
archivo = os.path.join(os.path.dirname(__file__),"..", "datos", "2.ESTADÍSTICASDEDESERCIÓNYPERMANENCIAENEDUCACIÓNSUPERIOR.xlsx")

try:
    print(f"\n📂 Leyendo archivo: {archivo}")
    
    # Leer datos
    df = pd.read_excel(archivo, sheet_name='TDA IES Nivel Formación', header=None)
    print(f"✅ Archivo leído: {df.shape[0]} filas")
    
    # Buscar Universidad de Antioquia
    print("\n🔍 Buscando Universidad de Antioquia...")
    
    datos_limpios = []
    
    # Revisar cada fila
    for i in range(len(df)):
        try:
            fila = df.iloc[i]
            
            # Verificar si hay datos suficientes
            if len(fila) < 16:
                continue
                
            # Extraer información básica
            codigo = fila.iloc[0]
            universidad = str(fila.iloc[1]) if pd.notna(fila.iloc[1]) else ""
            nivel = str(fila.iloc[2]) if pd.notna(fila.iloc[2]) else ""
            
            # Verificar si es Universidad de Antioquia y nivel Universitario
            if 'universidad de antioquia' in universidad.lower() and 'universitario' in nivel.lower():
                
                # Obtener nombre de la sede
                nombre_sede = nombres_sedes.get(codigo, f'Sede {codigo}')
                print(f"   ✅ Encontrada: {nombre_sede}")
                
                # Extraer datos de deserción por año (columnas 3-15)
                años = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
                
                for j, año in enumerate(años):
                    col_index = 3 + j  # Columnas 3, 4, 5, ... 15
                    
                    if col_index < len(fila):
                        tasa = fila.iloc[col_index]
                        
                        # Verificar si el dato es válido
                        if pd.notna(tasa) and tasa != 'NA':
                            try:
                                porcentaje = float(tasa) * 100
                                
                                # Filtrar valores razonables (0% a 25%)
                                if 0 <= porcentaje <= 25:
                                    datos_limpios.append({
                                        'codigo_sede': codigo,
                                        'nombre_sede': nombre_sede,
                                        'año': año,
                                        'desercion': round(porcentaje, 2)
                                    })
                            except:
                                continue
                                
        except Exception as e:
            continue
    
    # Crear DataFrame limpio
    df_final = pd.DataFrame(datos_limpios)
    
    print(f"\n✅ DATOS EXTRAÍDOS:")
    print(f"   📊 Total registros: {len(df_final)}")
    print(f"   🏛️  Sedes encontradas: {df_final['nombre_sede'].nunique()}")
    print(f"   📅 Años: {df_final['año'].min()}-{df_final['año'].max()}")
    
    print(f"\n📋 Primeros datos:")
    print(df_final.head(10))
    
    # ===================================
    # GRÁFICAS CORREGIDAS
    # ===================================
    print("\n📈 Creando gráficas corregidas...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Universidad de Antioquia - Deserción Universitaria (2010-2022)', 
                 fontsize=16, fontweight='bold')
    
    # Gráfica 1: Promedio por año
    ax1 = axes[0, 0]
    promedio_año = df_final.groupby('año')['desercion'].mean()
    ax1.plot(promedio_año.index, promedio_año.values, marker='o', linewidth=3, markersize=8, color='#2E8B57')
    ax1.set_title('Evolución Promedio por Año', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Año')
    ax1.set_ylabel('Deserción (%)')
    ax1.grid(True, alpha=0.3)
    
    # Agregar valores en los puntos
    for x, y in zip(promedio_año.index, promedio_año.values):
        ax1.annotate(f'{y:.1f}%', (x, y), textcoords="offset points", 
                    xytext=(0,10), ha='center', fontsize=9)
    
    # Gráfica 2: Promedio por sede (CON NOMBRES)
    ax2 = axes[0, 1]
    promedio_sede = df_final.groupby('nombre_sede')['desercion'].mean().sort_values()
    
    # Acortar nombres para que se vean mejor
    nombres_cortos = [nombre.replace('Sede ', '').replace('Regional ', '') for nombre in promedio_sede.index]
    
    bars = ax2.barh(range(len(promedio_sede)), promedio_sede.values, color='steelblue')
    ax2.set_title('Promedio por Sede', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Deserción (%)')
    ax2.set_yticks(range(len(promedio_sede)))
    ax2.set_yticklabels(nombres_cortos, fontsize=10)
    ax2.grid(True, alpha=0.3, axis='x')
    
    # Agregar valores en las barras
    for i, (bar, valor) in enumerate(zip(bars, promedio_sede.values)):
        ax2.text(valor + 0.1, bar.get_y() + bar.get_height()/2,
                f'{valor:.1f}%', ha='left', va='center', fontweight='bold', fontsize=9)
    
    # Gráfica 3: Deserción por Año (BARRAS VERTICALES)
    ax3 = axes[1, 0]
    
    # Calcular promedio por año
    promedio_por_año = df_final.groupby('año')['desercion'].mean()
    
    # Crear gráfico de barras verticales
    bars = ax3.bar(promedio_por_año.index, promedio_por_año.values, 
                   alpha=0.7, color='skyblue', edgecolor='black', width=0.8)
    
    # LÍNEAS HORIZONTALES para promedio y mediana general
    promedio_real = df_final['desercion'].mean()
    mediana_real = df_final['desercion'].median()
    
    ax3.axhline(promedio_real, color='red', linestyle='--', linewidth=2, 
                label=f'Promedio: {promedio_real:.1f}%')
    ax3.axhline(mediana_real, color='orange', linestyle='--', linewidth=2, 
                label=f'Mediana: {mediana_real:.1f}%')
    
    ax3.set_title('Deserción por Año', fontsize=12, fontweight='bold')
    ax3.set_xlabel('Año')
    ax3.set_ylabel('Deserción (%)')
    
    # Agregar formato de porcentaje al eje Y
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0f}%'))
    
    # Rotar etiquetas del eje X para mejor legibilidad
    ax3.tick_params(axis='x', rotation=45)
    
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Gráfica 4: Boxplot por sede (CON NOMBRES CORTOS)
    ax4 = axes[1, 1]
    
    # Crear orden por promedio
    orden_sedes = df_final.groupby('nombre_sede')['desercion'].mean().sort_values().index
    
    # Crear nombres cortos para el boxplot
    df_plot = df_final.copy()
    df_plot['nombre_corto'] = df_plot['nombre_sede'].str.replace('Sede ', '').str.replace('Regional ', '')
    
    # Crear orden con nombres cortos
    orden_corto = [nombre.replace('Sede ', '').replace('Regional ', '') for nombre in orden_sedes]
    
    sns.boxplot(data=df_plot, y='nombre_corto', x='desercion', 
                order=orden_corto, ax=ax4, palette='Set2')
    ax4.set_title('Distribución por Sede', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Deserción (%)')
    ax4.set_ylabel('Sede')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # ===================================
    # ESTADÍSTICAS SIMPLES
    # ===================================
    print("\n📊 ESTADÍSTICAS CORREGIDAS")
    print("=" * 40)
    
    print(f"\n📈 GENERAL:")
    print(f"   Promedio: {df_final['desercion'].mean():.2f}%")
    print(f"   Mediana: {df_final['desercion'].median():.2f}%")
    print(f"   Mínimo: {df_final['desercion'].min():.2f}%")
    print(f"   Máximo: {df_final['desercion'].max():.2f}%")
    
    print(f"\n📅 POR AÑO:")
    for año in sorted(df_final['año'].unique()):
        datos_año = df_final[df_final['año'] == año]['desercion']
        print(f"   {año}: {datos_año.mean():.2f}%")
    
    print(f"\n🏛️  POR SEDE (CON NOMBRES):")
    resumen_sede = df_final.groupby('nombre_sede')['desercion'].agg(['mean', 'count']).sort_values('mean')
    for sede, stats in resumen_sede.iterrows():
        print(f"   {sede}: {stats['mean']:.2f}% ({stats['count']} registros)")
    
    # ===================================
    # EXPORTAR DATOS
    # ===================================
    print(f"\n💾 Exportando datos...")
    
    # Archivo principal
    df_final.to_csv('udea_datos_completos.csv', index=False, encoding='utf-8')
    
    # Resumen por año
    resumen_año = df_final.groupby('año')['desercion'].agg(['mean', 'min', 'max', 'count']).round(2)
    resumen_año.to_csv('udea_resumen_por_año.csv', encoding='utf-8')
    
    # Resumen por sede con nombres
    resumen_sede.round(2).to_csv('udea_resumen_por_sede.csv', encoding='utf-8')
    
    print("✅ Archivos creados:")
    print("   📄 udea_datos_completos.csv")
    print("   📄 udea_resumen_por_año.csv")
    print("   📄 udea_resumen_por_sede.csv")
    
    # ===================================
    # RESULTADOS PRINCIPALES
    # ===================================
    print(f"\n🎯 RESULTADOS PRINCIPALES")
    print("=" * 40)
    
    mejor_sede = df_final.groupby('nombre_sede')['desercion'].mean().idxmin()
    peor_sede = df_final.groupby('nombre_sede')['desercion'].mean().idxmax()
    mejor_año = df_final.groupby('año')['desercion'].mean().idxmin()
    peor_año = df_final.groupby('año')['desercion'].mean().idxmax()
    
    mejor_promedio = df_final.groupby('nombre_sede')['desercion'].mean().min()
    peor_promedio = df_final.groupby('nombre_sede')['desercion'].mean().max()
    
    print(f"📊 PROMEDIO GENERAL: {df_final['desercion'].mean():.2f}%")
    print(f"🏆 MEJOR SEDE: {mejor_sede} ({mejor_promedio:.2f}%)")
    print(f"⚠️  SEDE MÁS CRÍTICA: {peor_sede} ({peor_promedio:.2f}%)")
    print(f"📈 MEJOR AÑO: {mejor_año}")
    print(f"📉 AÑO MÁS CRÍTICO: {peor_año}")
    
    # Tendencia simple
    años_unicos = sorted(df_final['año'].unique())
    if len(años_unicos) >= 2:
        promedio_inicial = df_final[df_final['año'] <= 2013]['desercion'].mean()
        promedio_final = df_final[df_final['año'] >= 2020]['desercion'].mean()
        
        if promedio_final < promedio_inicial:
            print(f"✅ TENDENCIA: Mejorando (de {promedio_inicial:.1f}% a {promedio_final:.1f}%)")
        else:
            print(f"⚠️  TENDENCIA: Empeorando (de {promedio_inicial:.1f}% a {promedio_final:.1f}%)")
    
    print(f"\n📋 SEDES DE UNIVERSIDAD DE ANTIOQUIA:")
    for codigo, nombre in nombres_sedes.items():
        if codigo in df_final['codigo_sede'].values:
            promedio_sede = df_final[df_final['codigo_sede'] == codigo]['desercion'].mean()
            print(f"   {codigo}: {nombre} - {promedio_sede:.2f}%")
    
    print("\n" + "=" * 50)
    print("✨ ANÁLISIS CORREGIDO COMPLETADO ✨")
    print("📊 Línea roja del promedio corregida")
    print("🏛️  Nombres de sedes incluidos")
    print("=" * 50)

except FileNotFoundError:
    print(f"❌ No se encontró el archivo: {archivo}")
    print("📁 Verifica que el archivo esté en la carpeta correcta")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    print("🔧 Revisa el archivo Excel")