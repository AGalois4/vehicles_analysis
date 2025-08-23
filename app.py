import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# Leer los datos
car_data = pd.read_csv('vehicles_us.csv')

st.title("Análisis de Anuncios de Venta de Vehículos")

# --- Distribuciones clave ---
if st.button("Mostrar Distribuciones Clave"):
    st.subheader("Distribución de Precios")
    fig = go.Figure(data=[go.Histogram(x=car_data['price'])])
    fig.update_layout(title='', xaxis_title='Precio', yaxis_title='Frecuencia')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Distribución del Odómetro")
    fig = go.Figure(data=[go.Histogram(x=car_data['odometer'])])
    fig.update_layout(title='', xaxis_title='Kilometraje', yaxis_title='Frecuencia')
    st.plotly_chart(fig, use_container_width=True)

# --- Composición del dataset ---
if st.button("Mostrar Composición del Dataset"):
    type_counts = car_data['type'].value_counts().reset_index()
    type_counts.columns = ['type', 'count']
    st.subheader("Cantidad de Vehículos por Tipo")
    fig = go.Figure(data=[go.Bar(x=type_counts['type'], y=type_counts['count'])])
    fig.update_layout(title='', xaxis_title='Tipo', yaxis_title='Cantidad')
    st.plotly_chart(fig, use_container_width=True)

    paint_counts = car_data['paint_color'].value_counts().reset_index()
    paint_counts.columns = ['paint_color', 'count']
    st.subheader("Distribución de Colores de Pintura")
    fig = go.Figure(data=[go.Bar(x=paint_counts['paint_color'], y=paint_counts['count'])])
    fig.update_layout(title='', xaxis_title='Color', yaxis_title='Cantidad')
    st.plotly_chart(fig, use_container_width=True)

    fuel_counts = car_data['fuel'].value_counts().reset_index()
    fuel_counts.columns = ['fuel', 'count']
    st.subheader("Distribución de Combustible")
    fig = go.Figure(data=[go.Pie(labels=fuel_counts['fuel'], values=fuel_counts['count'])])
    fig.update_layout(title='')
    st.plotly_chart(fig, use_container_width=True)

# --- Relaciones clave ---
if st.button("Mostrar Relaciones Clave"):
    st.subheader("Precio contra Kilometraje")
    fig = go.Figure(data=[go.Scatter(x=car_data['odometer'], y=car_data['price'], mode='markers')])
    fig.update_layout(title='', xaxis_title='Kilometraje', yaxis_title='Precio')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Precio contra Año del Modelo")
    fig = go.Figure(data=[go.Scatter(x=car_data['model_year'], y=car_data['price'], mode='markers')])
    fig.update_layout(title='', xaxis_title='Año', yaxis_title='Precio')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Precio contra Días en Lista")
    fig = go.Figure(data=[go.Scatter(x=car_data['days_listed'], y=car_data['price'], mode='markers')])
    fig.update_layout(title='', xaxis_title='Días Listados', yaxis_title='Precio')
    st.plotly_chart(fig, use_container_width=True)

# --- Comparaciones por categoría ---
if st.button("Mostrar Comparaciones por Categoría"):
    st.subheader("Precio por Tipo de Vehículo")
    fig = go.Figure(data=[go.Box(y=car_data['price'], x=car_data['type'], boxpoints='outliers')])
    fig.update_layout(title='', xaxis_title='Tipo', yaxis_title='Precio')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Precio por Condición")
    fig = go.Figure(data=[go.Box(y=car_data['price'], x=car_data['condition'], boxpoints='outliers')])
    fig.update_layout(title='', xaxis_title='Condición', yaxis_title='Precio')
    st.plotly_chart(fig, use_container_width=True)

# --- Correlaciones ---
if st.button("Mostrar Correlaciones"):
    numeric_cols = car_data.select_dtypes(include=['float64', 'int64'])
    corr = numeric_cols.corr()

    fig = px.imshow(
        corr,
        text_auto=".2f",   # <-- ahora redondea a dos decimales
        color_continuous_scale='RdBu_r',
        title='Matriz de Correlación',
        width=900,
        height=800
    )

    # Tamaño del texto dentro de cada celda
    fig.update_traces(textfont=dict(size=16, color="black"))

    # Layout general
    fig.update_layout(
        title=dict(font=dict(size=24)),
        xaxis=dict(title_font=dict(size=18), tickfont=dict(size=14)),
        yaxis=dict(title_font=dict(size=18), tickfont=dict(size=14))
    )

    st.plotly_chart(fig, use_container_width=False)


# --- Insights temporales ---
if st.button("Mostrar Insights Temporales"):
    car_data['date_posted'] = pd.to_datetime(car_data['date_posted'])
    car_data['month_posted'] = car_data['date_posted'].dt.month
    month_counts = car_data['month_posted'].value_counts().sort_index()

    st.subheader("Publicaciones por Mes")
    fig = go.Figure(data=[go.Bar(x=month_counts.index, y=month_counts.values)])
    fig.update_layout(title='', xaxis_title='Mes', yaxis_title='Cantidad')
    st.plotly_chart(fig, use_container_width=True)