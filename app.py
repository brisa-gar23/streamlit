import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

nba_data = pd.read_csv("nba_all_elo.csv")
st.title("Práctica 3 - Dashboard NBA")

# valores únicos para cada componente en la barra lateral
year_list = sorted(nba_data['year_id'].unique().tolist())
team_list = sorted(nba_data['team_id'].unique().tolist())

with st.sidebar:
    # selectbox para el año
    year = st.selectbox('Seleccionar año', year_list, 0)
    
    # selectbox para el equipo
    team = st.selectbox('Seleccionar equipo', team_list, 0)
    
    # pills para seleccionar tipo de juegos
    game_type = st.radio("Seleccionar juegos de:",["Temporada regular", "Playoffs", "Ambos"])

# filtro por equipo y año
team_year_filter = (nba_data['team_id'] == team) & (nba_data['year_id'] == year)

# filtro adicional para el tipo de juego
if game_type == "Temporada regular":
    filtered_data = nba_data[team_year_filter & (nba_data['is_playoffs'] == 0)]
elif game_type == "Playoffs":
    filtered_data = nba_data[team_year_filter & (nba_data['is_playoffs'] == 1)]
else:
    filtered_data = nba_data[team_year_filter]

# ordenar datos por fecha
filtered_data = filtered_data.sort_values(by='date_game')

if not filtered_data.empty:
    filtered_data['win'] = (filtered_data['game_result'] == 'W').astype(int)
    filtered_data['loss'] = (filtered_data['game_result'] == 'L').astype(int)
    
    filtered_data['wins_cumsum'] = filtered_data['win'].cumsum()
    filtered_data['losses_cumsum'] = filtered_data['loss'].cumsum()
    
    total_wins = filtered_data['win'].sum()
    total_losses = filtered_data['loss'].sum()
    
    # gráficas
    st.write(f"### Estadísticas de {team} en {year}")
    
    # gráfico de líneas 
    st.write("#### Acumulado de juegos ganados y perdidos")
    
    fig1 = plt.figure(figsize=(10, 6))
    
    plt.plot(range(1, len(filtered_data) + 1), filtered_data['wins_cumsum'], 'g-', label='Victorias (W)')
    plt.plot(range(1, len(filtered_data) + 1), filtered_data['losses_cumsum'], 'r-', label='Derrotas (L)')
    plt.xlabel('Número de juego')
    plt.ylabel('Acumulado')
    plt.title(f'Acumulado de victorias y derrotas - {team} ({year})')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    st.pyplot(fig1)
    
    # gráfico de pastel
    st.write("#### Porcentaje de juegos ganados y perdidos en la temporada")
    
    fig2 = plt.figure(figsize=(8, 8))
    
    labels = ['Victorias', 'Derrotas']
    sizes = [total_wins, total_losses]
    colors = ['green', 'red']
    
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.axis('equal')
    
    st.pyplot(fig2)
else:
    st.warning("No hay datos disponibles para los filtros seleccionados.")