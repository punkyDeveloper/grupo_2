import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os
warnings.filterwarnings('ignore')

# Configuración de estilo para las gráficas
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (15, 10)
plt.rcParams['font.size'] = 10

print("=== ANÁLISIS DE DESERCIÓN UNIVERSITARIA EN COLOMBIA ===")
print("📊 USANDO PANDAS PARA LEER EL ARCHIVO EXCEL REAL")
print("🗓️ Periodo: 2010-2022 | Nivel: UNIVERSITARIO")
print("=" * 70)

# ===== LEER EL ARCHIVO EXCEL CON PANDAS =====
archivo_excel = os.path.join(os.path.dirname(__file__),"..", "datos", "1.ESTADÍSTICASDEDESERCIÓNYPERMANENCIAENEDUCACIÓNSUPERIOR.xlsx")

try:
    print(f"\n📂 Leyendo archivo: {archivo_excel}")
    
    # 1. LEER DATOS POR SEXO
    print("\n📊 1. EXTRAYENDO DATOS POR SEXO...")
    df_sexo_raw = pd.read_excel(archivo_excel, sheet_name='TD - sexo', header=None)
    
    # Encontrar la fila con los años y los datos
    # Según el análisis anterior: fila 12 = años, fila 13 = hombres, fila 14 = mujeres
    años = df_sexo_raw.iloc[12, 1:14].tolist()  # Columnas 1-13 (años 2010-2022)
    hombres_raw = df_sexo_raw.iloc[13, 1:14].tolist()  # Datos hombres
    mujeres_raw = df_sexo_raw.iloc[14, 1:14].tolist()  # Datos mujeres
    
    print(f"✅ Años extraídos: {len(años)} valores")
    print(f"✅ Datos hombres: {len(hombres_raw)} valores")
    print(f"✅ Datos mujeres: {len(mujeres_raw)} valores")
    
    # Crear DataFrame limpio por sexo
    datos_sexo = []
    for i, año in enumerate(años):
        if pd.notna(año) and pd.notna(hombres_raw[i]) and pd.notna(mujeres_raw[i]):
            datos_sexo.append({
                'año': int(año), 'sexo': 'Hombre', 
                'tasa_desercion': hombres_raw[i],
                'porcentaje': round(hombres_raw[i] * 100, 2),
                'nivel_formacion': 'Universitario'
            })
            datos_sexo.append({
                'año': int(año), 'sexo': 'Mujer', 
                'tasa_desercion': mujeres_raw[i],
                'porcentaje': round(mujeres_raw[i] * 100, 2),
                'nivel_formacion': 'Universitario'
            })
    
    df_sexo = pd.DataFrame(datos_sexo)
    print(f"✅ Dataset por sexo creado: {len(df_sexo)} registros")
    print("Muestra de datos por sexo:")
    print(df_sexo.head())
    
    # 2. LEER DATOS POR METODOLOGÍA
    print("\n📊 2. EXTRAYENDO DATOS POR METODOLOGÍA...")
    df_metodologia_raw = pd.read_excel(archivo_excel, sheet_name='TD - metodología', header=None)
    
    # Según análisis: fila 13 = años, filas 14-17 = metodologías
    años_metodo = df_metodologia_raw.iloc[13, 1:14].tolist()
    presencial_raw = df_metodologia_raw.iloc[14, 1:14].tolist()
    dist_tradicional_raw = df_metodologia_raw.iloc[15, 1:14].tolist()
    dist_virtual_raw = df_metodologia_raw.iloc[16, 1:14].tolist()
    dual_raw = df_metodologia_raw.iloc[17, 1:14].tolist()
    
    print(f"✅ Años metodología: {len(años_metodo)} valores")
    
    # Crear DataFrame limpio por metodología
    datos_metodologia = []
    metodologias_datos = {
        'Presencial': presencial_raw,
        'Distancia tradicional': dist_tradicional_raw,
        'Distancia virtual': dist_virtual_raw,
        'Dual': dual_raw
    }
    
    for metodologia, datos_raw in metodologias_datos.items():
        for i, año in enumerate(años_metodo):
            if pd.notna(año) and pd.notna(datos_raw[i]):
                datos_metodologia.append({
                    'año': int(año), 'metodologia': metodologia,
                    'tasa_desercion': datos_raw[i],
                    'porcentaje': round(datos_raw[i] * 100, 2),
                    'nivel_formacion': 'Universitario'
                })
    
    df_metodologia = pd.DataFrame(datos_metodologia)
    print(f"✅ Dataset por metodología creado: {len(df_metodologia)} registros")
    print("Muestra de datos por metodología:")
    print(df_metodologia.head())
    
    # 3. LEER DATOS POR ÁREA DE CONOCIMIENTO
    print("\n📊 3. EXTRAYENDO DATOS POR ÁREA DE CONOCIMIENTO...")
    df_area_raw = pd.read_excel(archivo_excel, sheet_name='TD - área de conocimiento', header=None)
    
    # Según análisis: fila 12 = años, filas 13-20 = áreas de conocimiento
    años_area = df_area_raw.iloc[12, 1:14].tolist()
    
    areas_conocimiento = [
        'Agronomía veterinaria y afines',
        'Bellas artes',
        'Ciencias de la educación',
        'Ciencias de la salud', 
        'Ciencias sociales y humanas',
        'Economía, administración, contaduría y afines',
        'Ingeniería, arquitectura, urbanismo y afines',
        'Matemáticas y ciencias naturales'
    ]
    
    print(f"✅ Años área: {len(años_area)} valores")
    print(f"✅ Áreas de conocimiento: {len(areas_conocimiento)} áreas")
    
    # Extraer datos por área
    datos_area = []
    for i, area in enumerate(areas_conocimiento):
        fila_index = 13 + i  # Filas 13-20
        area_datos_raw = df_area_raw.iloc[fila_index, 1:14].tolist()
        
        for j, año in enumerate(años_area):
            if pd.notna(año) and pd.notna(area_datos_raw[j]):
                datos_area.append({
                    'año': int(año), 'area_conocimiento': area,
                    'tasa_desercion': area_datos_raw[j],
                    'porcentaje': round(area_datos_raw[j] * 100, 2),
                    'nivel_formacion': 'Universitario'
                })
    
    df_area = pd.DataFrame(datos_area)
    print(f"✅ Dataset por área creado: {len(df_area)} registros")
    print("Muestra de datos por área:")
    print(df_area.head())
    
    # 4. ANÁLISIS: CARRERAS QUE MÁS DESERTAN
    print("\n🔥 4. ANÁLISIS: CARRERAS QUE MÁS DESERTAN...")
    areas_promedio = df_area.groupby('area_conocimiento')['porcentaje'].mean().sort_values(ascending=False)
    
    print("\n🎯 RANKING REAL - Carreras ordenadas por mayor deserción:")
    for i, (area, tasa) in enumerate(areas_promedio.items(), 1):
        print(f"{i}. {area}: {tasa:.2f}%")
    
    # 5. CREAR DATASET CONSOLIDADO
    print("\n📋 5. CREANDO DATASET CONSOLIDADO...")
    
    df_sexo['tipo_analisis'] = 'sexo'
    df_metodologia['tipo_analisis'] = 'metodologia'
    df_area['tipo_analisis'] = 'area_conocimiento'
    
    df_sexo['categoria'] = df_sexo['sexo']
    df_metodologia['categoria'] = df_metodologia['metodologia']
    df_area['categoria'] = df_area['area_conocimiento']
    
    columnas_comunes = ['año', 'categoria', 'tasa_desercion', 'porcentaje', 'nivel_formacion', 'tipo_analisis']
    
    df_consolidado = pd.concat([
        df_sexo[columnas_comunes],
        df_metodologia[columnas_comunes],
        df_area[columnas_comunes]
    ], ignore_index=True)
    
    print(f"✅ Dataset consolidado creado: {len(df_consolidado)} registros")
    
    # 6. VISUALIZACIONES
    print("\n📈 6. GENERANDO VISUALIZACIONES...")
    
    fig = plt.figure(figsize=(20, 16))
    
    # Gráfica 1: Evolución por sexo
    plt.subplot(2, 3, 1)
    df_sexo_pivot = df_sexo.pivot(index='año', columns='sexo', values='porcentaje')
    plt.plot(df_sexo_pivot.index, df_sexo_pivot['Hombre'], marker='o', linewidth=3, 
             label='Hombres', color='#1f77b4', markersize=6)
    plt.plot(df_sexo_pivot.index, df_sexo_pivot['Mujer'], marker='s', linewidth=3, 
             label='Mujeres', color='#ff7f0e', markersize=6)
    plt.title('Evolución de Deserción por Sexo\n(Datos del archivo Excel)', 
              fontsize=14, fontweight='bold')
    plt.xlabel('Año')
    plt.ylabel('Tasa de Deserción (%)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Gráfica 2: Comparación por metodología
    plt.subplot(2, 3, 2)
    metodologia_promedio = df_metodologia.groupby('metodologia')['porcentaje'].mean().sort_values(ascending=False)
    colors = ['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4']
    bars = plt.bar(range(len(metodologia_promedio)), metodologia_promedio.values, color=colors)
    plt.title('Promedio por Metodología\n(Datos del archivo)', fontsize=14, fontweight='bold')
    plt.xlabel('Metodología')
    plt.ylabel('Tasa de Deserción (%)')
    plt.xticks(range(len(metodologia_promedio)), 
               [m.replace(' ', '\n') for m in metodologia_promedio.index], rotation=0)
    plt.grid(True, alpha=0.3, axis='y')
    
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.3,
                 f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # Gráfica 3: Top 5 áreas con mayor deserción
    plt.subplot(2, 3, 3)
    top_areas = areas_promedio.head(5)
    bars = plt.barh(range(len(top_areas)), top_areas.values, color='#d62728', alpha=0.7)
    plt.title('Top 5 Carreras con Mayor Deserción\n(Del archivo Excel)', fontsize=14, fontweight='bold')
    plt.xlabel('Tasa de Deserción Promedio (%)')
    plt.yticks(range(len(top_areas)), 
               [area.replace(',', '\n') for area in top_areas.index])
    plt.grid(True, alpha=0.3, axis='x')
    
    for i, bar in enumerate(bars):
        width = bar.get_width()
        plt.text(width + 0.1, bar.get_y() + bar.get_height()/2.,
                 f'{width:.1f}%', ha='left', va='center', fontweight='bold')
    
    # Gráfica 4: Evolución temporal por metodología
    plt.subplot(2, 3, 4)
    metodologias_principales = ['Presencial', 'Distancia virtual', 'Distancia tradicional']
    for metodologia in metodologias_principales:
        data_metodo = df_metodologia[df_metodologia['metodologia'] == metodologia]
        if not data_metodo.empty:
            plt.plot(data_metodo['año'], data_metodo['porcentaje'], marker='o', 
                     linewidth=2, label=metodologia)
    
    plt.title('Evolución por Metodología\n(Del archivo)', fontsize=14, fontweight='bold')
    plt.xlabel('Año')
    plt.ylabel('Tasa de Deserción (%)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Gráfica 5: Boxplot por sexo
    plt.subplot(2, 3, 5)
    sns.boxplot(data=df_sexo, x='sexo', y='porcentaje', palette=['#1f77b4', '#ff7f0e'])
    plt.title('Distribución de Deserción por Sexo\n(Todos los años)', fontsize=14, fontweight='bold')
    plt.xlabel('Sexo')
    plt.ylabel('Tasa de Deserción (%)')
    
    # Gráfica 6: Heatmap de las 5 áreas más críticas
    plt.subplot(2, 3, 6)
    top5_areas = areas_promedio.head(5).index
    df_area_top5 = df_area[df_area['area_conocimiento'].isin(top5_areas)]
    
    if not df_area_top5.empty:
        pivot_top5 = df_area_top5.pivot(index='area_conocimiento', columns='año', values='porcentaje')
        pivot_top5 = pivot_top5.reindex(top5_areas)
        pivot_top5.index = [area.split(',')[0] for area in pivot_top5.index]
        
        sns.heatmap(pivot_top5, annot=True, fmt='.1f', cmap='Reds', 
                    cbar_kws={'label': 'Tasa (%)'})
        plt.title('Heatmap: Top 5 Áreas Críticas\n(Por Año)', fontsize=14, fontweight='bold')
        plt.xlabel('Año')
        plt.ylabel('Área de Conocimiento')
    
    plt.tight_layout()
    plt.show()
    
    # 7. ESTADÍSTICAS DESCRIPTIVAS
    print("\n📊 7. ESTADÍSTICAS DESCRIPTIVAS (DEL ARCHIVO)")
    print("="*60)
    
    print("\n🔸 RESUMEN POR SEXO:")
    resumen_sexo = df_sexo.groupby('sexo')['porcentaje'].agg(['count', 'mean', 'std', 'min', 'max']).round(2)
    print(resumen_sexo)
    
    if len(resumen_sexo) >= 2:
        brecha_genero = resumen_sexo.loc['Hombre', 'mean'] - resumen_sexo.loc['Mujer', 'mean']
        print(f"\n👥 BRECHA DE GÉNERO: {brecha_genero:.2f} puntos porcentuales")
    
    print("\n🔸 RESUMEN POR METODOLOGÍA:")
    resumen_metodologia = df_metodologia.groupby('metodologia')['porcentaje'].agg(['count', 'mean', 'std', 'min', 'max']).round(2)
    resumen_metodologia = resumen_metodologia.sort_values('mean', ascending=False)
    print(resumen_metodologia)
    
    print("\n🔸 RESUMEN POR ÁREA DE CONOCIMIENTO:")
    resumen_areas = df_area.groupby('area_conocimiento')['porcentaje'].agg(['count', 'mean', 'std', 'min', 'max']).round(2)
    resumen_areas = resumen_areas.sort_values('mean', ascending=False)
    print(resumen_areas)
    
    # 8. EXPORTAR DATOS LIMPIOS A CSV
    print("\n💾 8. EXPORTANDO DATASETS A CSV...")
    
    df_sexo.to_csv('desercion_por_sexo_PANDAS.csv', index=False, encoding='utf-8')
    df_metodologia.to_csv('desercion_por_metodologia_PANDAS.csv', index=False, encoding='utf-8')
    df_area.to_csv('desercion_por_area_conocimiento_PANDAS.csv', index=False, encoding='utf-8')
    df_consolidado.to_csv('desercion_consolidado_PANDAS.csv', index=False, encoding='utf-8')
    
    print("✅ Archivos CSV exportados con pandas:")
    print("   📄 desercion_por_sexo_PANDAS.csv")
    print("   📄 desercion_por_metodologia_PANDAS.csv") 
    print("   📄 desercion_por_area_conocimiento_PANDAS.csv")
    print("   📄 desercion_consolidado_PANDAS.csv")
    
    # 9. INSIGHTS PRINCIPALES
    print("\n🎯 9. INSIGHTS PRINCIPALES (EXTRAÍDOS CON PANDAS)")
    print("="*60)
    
    if not areas_promedio.empty:
        area_mas_critica = areas_promedio.index[0]
        area_mas_estable = areas_promedio.index[-1]
        print(f"🔥 CARRERA QUE MÁS DESERTA: {area_mas_critica} ({areas_promedio.iloc[0]:.2f}%)")
        print(f"✅ CARRERA MÁS ESTABLE: {area_mas_estable} ({areas_promedio.iloc[-1]:.2f}%)")
    
    if not resumen_metodologia.empty:
        metodologia_critica = resumen_metodologia.index[0]
        metodologia_estable = resumen_metodologia.index[-1]
        print(f"⚠️  METODOLOGÍA MÁS CRÍTICA: {metodologia_critica} ({resumen_metodologia.iloc[0]['mean']:.1f}%)")
        print(f"✅ METODOLOGÍA MÁS ESTABLE: {metodologia_estable} ({resumen_metodologia.iloc[-1]['mean']:.1f}%)")
    
    if len(resumen_sexo) >= 2:
        print(f"👥 BRECHA DE GÉNERO: Hombres desertan {brecha_genero:.2f}% más que mujeres")
    
    print(f"\n🏆 TOP 3 CARRERAS MÁS CRÍTICAS:")
    for i, (area, tasa) in enumerate(areas_promedio.head(3).items(), 1):
        print(f"   {i}. {area}: {tasa:.2f}%")
    
    print("\n" + "="*60)
    print("✨ ANÁLISIS COMPLETADO USANDO PANDAS PARA LEER EL ARCHIVO ✨")
    print("📊 Todos los datos fueron extraídos directamente del Excel")
    print("="*60)

except FileNotFoundError:
    print(f"❌ Error: No se pudo encontrar el archivo '{archivo_excel}'")
    print("📝 Asegúrate de que el archivo esté en el mismo directorio que este script")
    
except Exception as e:
    print(f"❌ Error al procesar el archivo: {str(e)}")
    print("📝 Verifica que el archivo Excel no esté corrupto y tenga las hojas esperadas")