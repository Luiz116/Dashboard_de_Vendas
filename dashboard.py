import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Carregar os dados
df = pd.read_excel("1 - Base de Dados.xlsx")

# Iniciar a aplicação Dash
app = dash.Dash(__name__)

# Layout do Dashboard
app.layout = html.Div([
    dcc.Graph(id='total-vendas-mes'),
    dcc.Graph(id='total-vendas-representante'),
    dcc.Graph(id='total-vendas-regional'),
    dcc.Graph(id='total-vendas-estado'),
    dcc.Dropdown(id='estado-dropdown', options=[{'label': estado, 'value': estado} for estado in df['Estado_Cliente'].unique()]),
    dcc.Dropdown(id='cidade-dropdown'),
])

# Callback para atualizar as cidades quando o estado é selecionado
@app.callback(
    Output('cidade-dropdown', 'options'),
    [Input('estado-dropdown', 'value')]
)
def update_cidades(estado_selecionado):
    if estado_selecionado:
        cidades = df[df['Estado_Cliente'] == estado_selecionado]['Cidade_Cliente'].unique()
        return [{'label': cidade, 'value': cidade} for cidade in cidades]
    else:
        return []

# Callbacks para atualizar os gráficos com base nos filtros selecionados
@app.callback(
    Output('total-vendas-mes', 'figure'),
    Output('total-vendas-representante', 'figure'),
    Output('total-vendas-regional', 'figure'),
    Output('total-vendas-estado', 'figure'),
    Input('estado-dropdown', 'value'),
    Input('cidade-dropdown', 'value')
)
def update_graphs(estado_selecionado, cidade_selecionada):
    filtered_df = df.copy()
    if estado_selecionado:
        filtered_df = filtered_df[filtered_df['Estado_Cliente'] == estado_selecionado]
    if cidade_selecionada:
        filtered_df = filtered_df[filtered_df['Cidade_Cliente'] == cidade_selecionada]

    # Gráficos
    total_vendas_mes = px.line(filtered_df, x='Data_Pedido', y='Valor_Total_Venda', labels={'Data_Pedido': 'Mês', 'Valor_Total_Venda': 'Total de Vendas'}, title='Total de Vendas por Mês')
    total_vendas_representante = px.bar(filtered_df, x='Nome_Representante', y='Valor_Total_Venda', labels={'Nome_Representante': 'Representante', 'Valor_Total_Venda': 'Total de Vendas'}, title='Total de Vendas por Representante')
    total_vendas_regional = px.pie(filtered_df, names='Regional', title='Total de Vendas por Regional')
    total_vendas_estado = px.bar(filtered_df, x='Estado_Cliente', y='Valor_Total_Venda', labels={'Estado_Cliente': 'Estado', 'Valor_Total_Venda': 'Total de Vendas'}, title='Total de Vendas por Estado')

    return total_vendas_mes, total_vendas_representante, total_vendas_regional, total_vendas_estado

# Executar o servidor
if __name__ == '__main__':
    app.run_server(debug=True)