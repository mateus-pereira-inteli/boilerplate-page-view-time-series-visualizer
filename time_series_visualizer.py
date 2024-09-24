import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Carregar os dados e realizar a limpeza
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)

# Limpar os dados removendo os outliers
df = df[(df['value'] >= df['value'].quantile(0.025)) &
        (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Desenhar um gráfico de linha
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    
    # Configurar o título e os rótulos em inglês (para passar nos testes)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Salvar a figura
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Preparar dados para o gráfico de barras
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    # Organizar os meses na ordem correta
    months_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=months_order, ordered=True)

    # Agrupar os dados por ano e mês e calcular a média
    df_bar = df_bar.groupby(['year', 'month'], observed=True)['value'].mean().unstack()

    # Desenhar um gráfico de barras
    fig = df_bar.plot(kind='bar', figsize=(12, 6)).figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months')

    # Salvar a figura
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Preparar os dados para o box plot
    df_box = df.copy()
    df_box['year'] = [d.year for d in df_box.index]
    df_box['month'] = [d.strftime('%b') for d in df_box.index]

    # Organizar os meses na ordem correta
    months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_box['month'] = pd.Categorical(df_box['month'], categories=months_order, ordered=True)

    # Desenhar blox plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Gráfico de caixa anual
    sns.boxplot(x='year', y='value', data=df_box, ax=ax1)
    ax1.set_title('Year-wise Box Plot (Trend)') 
    ax1.set_xlabel('Year') 
    ax1.set_ylabel('Page Views')

    # Gráfico de caixa mensal
    sns.boxplot(x='month', y='value', data=df_box, ax=ax2)
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month') 
    ax2.set_ylabel('Page Views')

    # Salvar a figura
    fig.savefig('box_plot.png')
    return fig
