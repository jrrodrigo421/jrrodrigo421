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

    fig, ax = plt.subplots(figsize=(10, 6), facecolor='#000')
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, textprops=dict(color="w"))
    
    for wedge in wedges:
        wedge.set_edgecolor('white')

    plt.setp(autotexts, size=10, weight="bold")
    

    # Adicionando fundo gradiente manualmente
    fig.patch.set_facecolor('#000')
    ax.set_facecolor('#4B0082')
    
    fig.patch.set_xy(xy=[50,50])

    fig.savefig(output_path, bbox_inches='tight', transparent=True)
    plt.close()

if __name__ == '__main__':
    repos = get_repositories(USERNAME)
    languages = get_languages(repos)
    plot_languages(languages)