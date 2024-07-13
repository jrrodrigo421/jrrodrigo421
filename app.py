# import requests
# import plotly.graph_objects as go

# # Seu nome de usuário no GitHub
# USERNAME = 'jrrodrigo421'

# def get_repositories(username):
#     """Busca todos os repositórios públicos de um usuário no GitHub."""
#     url = f'https://api.github.com/users/{username}/repos'
#     repos = []
#     while url:
#         response = requests.get(url)
#         response.raise_for_status()
#         repos.extend(response.json())
#         # Paginação: GitHub API retorna 'Link' header com a URL para a próxima página de resultados
#         if 'next' in response.links:
#             url = response.links['next']['url']
#         else:
#             url = None
#     return repos

# def get_languages(repos):
#     """Busca a linguagem principal de cada repositório e conta a frequência de cada linguagem."""
#     languages = {}
#     for repo in repos:
#         lang = repo['language']
#         if lang:
#             if lang in languages:
#                 languages[lang] += 1
#             else:
#                 languages[lang] = 1
#     return languages

# def plot_languages(languages, output_path='languages.html'):
#     """Gera um gráfico de pizza interativo com a distribuição das linguagens."""
#     labels = list(languages.keys())
#     sizes = list(languages.values())

#     fig = go.Figure(data=[go.Pie(labels=labels, values=sizes, hole=.3)])

#     # Melhorias no design
#     fig.update_layout(
#         title_text='Distribuição das Linguagens nos Repositórios GitHub',
#         annotations=[dict(text='Linguagens', x=0.5, y=0.5, font_size=20, showarrow=False)],
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)',
#         font=dict(color='white'),
#         autosize=True,
#         template='plotly_dark',  # Adiciona o template dark
#         margin=dict(l=0, r=0, t=40, b=0),
#         xaxis=dict(
#             showgrid=False,
#             zeroline=False,
#             visible=False
#         ),
#         yaxis=dict(
#             showgrid=False,
#             zeroline=False,
#             visible=False
#         )
#     )

#     fig.update_traces(marker=dict(colors=['#636EFA','#EF553B','#00CC96','#AB63FA','#FFA15A',
#                                           '#19D3F3','#FF6692','#B6E880','#FF97FF','#FECB52']),
#                       pull=[0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0])

#     # Salva o gráfico como um arquivo HTML
#     fig.write_html(output_path, include_plotlyjs='cdn', full_html=False)

#     # Adiciona estilo CSS para centralizar e tornar responsivo com fundo gradiente
#     with open(output_path, 'a') as f:
#         f.write('''<style>
#                     .plotly-graph-div {
#                         margin: auto !important;
#                         background: linear-gradient(90deg, rgba(0,0,0,1) 0%, rgba(75,0,130,1) 100%) !important;
#                     }
#                     @media (max-width: 600px) {
#                         .plotly-graph-div {
#                             width: 100% !important;
#                         }
#                     }
#                    </style>''')

# if __name__ == '__main__':
#     repos = get_repositories(USERNAME)
#     languages = get_languages(repos)
#     plot_languages(languages)



import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

# Seu nome de usuário no GitHub
USERNAME = 'jrrodrigo421'

def get_repositories(username):
    """Busca todos os repositórios públicos de um usuário no GitHub."""
    url = f'https://api.github.com/users/{username}/repos'
    repos = []
    while url:
        response = requests.get(url)
        response.raise_for_status()
        repos.extend(response.json())
        # Paginação: GitHub API retorna 'Link' header com a URL para a próxima página de resultados
        if 'next' in response.links:
            url = response.links['next']['url']
        else:
            url = None
    return repos

def get_languages(repos):
    """Busca a linguagem principal de cada repositório e conta a frequência de cada linguagem."""
    languages = {}
    for repo in repos:
        lang = repo['language']
        if lang:
            if lang in languages:
                languages[lang] += 1
            else:
                languages[lang] = 1
    return languages

def plot_languages(languages, output_path='assets/languages.png'):
    """Gera um gráfico de pizza com a distribuição das linguagens."""
    labels = languages.keys()
    sizes = languages.values()

    fig, ax = plt.subplots(figsize=(10, 7), facecolor='#000')
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, textprops=dict(color="w"))
    
    for wedge in wedges:
        wedge.set_edgecolor('white')

    plt.setp(autotexts, size=10, weight="bold")
    ax.set_title('Distribuição das Linguagens nos Repositórios GitHub', color='white')

    # Adicionando fundo gradiente manualmente
    fig.patch.set_facecolor('#000')
    ax.set_facecolor('#4B0082')

    fig.savefig(output_path, bbox_inches='tight', transparent=True)
    plt.close()

if __name__ == '__main__':
    repos = get_repositories(USERNAME)
    languages = get_languages(repos)
    plot_languages(languages)
