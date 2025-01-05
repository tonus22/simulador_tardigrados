import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random

# Título de la Aplicación
st.title("Simulador de Supervivencia de Tardígrados")

# Sección de Entradas del Usuario
st.header("Parámetros de Simulación")
temperatura = st.number_input("Temperatura (°C)", min_value=-150, max_value=150, value=25)
humedad = st.number_input("Humedad (%)", min_value=0, max_value=100, value=50)
radiacion = st.number_input("Radiación (%)", min_value=0, max_value=100, value=10)

# Función para calcular la probabilidad de supervivencia
def calcular_probabilidad_supervivencia(temperatura, humedad, radiacion):
    peso_temperatura = 0.6
    peso_humedad = 0.2
    peso_radiacion = 0.2

    def penalizacion_temperatura(temp):
        if temp < -150 or temp > 150:
            return 0.0
        return 1 - abs(temp - 25) / 175

    puntuacion = (
        peso_temperatura * penalizacion_temperatura(temperatura) +
        peso_humedad * (humedad / 100) +
        peso_radiacion * (1 - radiacion / 100)
    )
    probabilidad = puntuacion * 100
    return max(0, min(probabilidad, 100))

# Función para interpretar las variables
def interpretar_variables(temp, humedad, radiacion):
    if temp <= 20:
        temp_exp = "La temperatura es demasiado baja. Los tardígrados entran en criptobiosis para sobrevivir."
    elif temp <= 50:
        temp_exp = "La temperatura es óptima para el metabolismo activo de los tardígrados."
    else:
        temp_exp = "La temperatura es demasiado alta y puede causar daños celulares irreversibles."

    if humedad <= 30:
        humedad_exp = "La humedad es muy baja, lo que puede inducir criptobiosis."
    elif humedad <= 70:
        humedad_exp = "La humedad es adecuada para el metabolismo activo."
    else:
        humedad_exp = "La humedad es excesiva y puede afectar la respiración celular."

    if radiacion <= 30:
        radiacion_exp = "La radiación es segura para los tardígrados."
    elif radiacion <= 70:
        radiacion_exp = "La radiación es moderada, con un impacto mínimo."
    else:
        radiacion_exp = "La radiación es peligrosa y puede dañar el ADN."

    return temp_exp, humedad_exp, radiacion_exp

# Calcular la probabilidad
probabilidad = calcular_probabilidad_supervivencia(temperatura, humedad, radiacion)
st.subheader(f"Probabilidad de Supervivencia: {probabilidad:.2f}%")

# Mostrar gráfico de parámetros
st.header("Gráfico de Parámetros")
fig, ax = plt.subplots()
ax.bar(["Temperatura", "Humedad", "Radiación"], [temperatura, humedad, radiacion], color=['blue', 'green', 'red'])
ax.set_ylabel("Valores")
st.pyplot(fig)

# Tabla Explicativa de las Variables
st.header("Tabla Explicativa de las Variables")
temp_exp, humedad_exp, radiacion_exp = interpretar_variables(temperatura, humedad, radiacion)
datos = {
    "Variable": ["Temperatura (°C)", "Humedad (%)", "Radiación (%)"],
    "Valor": [temperatura, humedad, radiacion],
    "Interpretación": [temp_exp, humedad_exp, radiacion_exp]
}
df = pd.DataFrame(datos)
st.table(df)

# Gráfico de Supervivencia
st.header("Gráfico de Supervivencia")
fig, ax = plt.subplots()
ax.pie([probabilidad, 100 - probabilidad], labels=["Supervivencia", "Riesgo"], colors=['skyblue', 'lightcoral'], autopct='%1.1f%%')
ax.axis('equal')
st.pyplot(fig)

# Histograma de Distribución de Probabilidades
st.header("Distribución de Probabilidad")
probabilidades = [
    calcular_probabilidad_supervivencia(
        random.uniform(-150, 150),
        random.uniform(0, 100),
        random.uniform(0, 100)
    ) for _ in range(1000)
]

fig, ax = plt.subplots()
ax.hist(probabilidades, bins=20, color='skyblue', edgecolor='black')
ax.set_title("Distribución de la Probabilidad de Supervivencia")
ax.set_xlabel("Probabilidad de Supervivencia (%)")
ax.set_ylabel("Frecuencia")
st.pyplot(fig)

# Tabla Explicativa del Histograma
st.header("Tabla Explicativa del Histograma")
mean = sum(probabilidades) / len(probabilidades)
std_dev = (sum((x - mean) ** 2 for x in probabilidades) / len(probabilidades)) ** 0.5

interpretacion_histograma = f"""
- **Media:** {mean:.2f}%  
- **Desviación Estándar:** {std_dev:.2f}  
"""

if std_dev < 10:
    interpretacion_histograma += "La distribución está muy concentrada cerca de la media, indicando estabilidad en las condiciones."
elif std_dev < 30:
    interpretacion_histograma += "La distribución es moderada, lo que indica variabilidad controlada."
else:
    interpretacion_histograma += "La distribución es muy dispersa, lo que sugiere condiciones variables."

st.write(interpretacion_histograma)

# Conclusión Final
st.header("Conclusión Final")
st.write("""
El simulador ha analizado los datos proporcionados sobre la temperatura, humedad y radiación, 
y ha generado una representación visual y descriptiva de la probabilidad de supervivencia de los tardígrados. 
Recuerda que estos organismos son increíblemente resistentes, pero sus límites tienen un rango claro.
""")
