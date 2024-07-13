import requests
import matplotlib.pyplot as plt

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

def plot_languages(languages, output_path='languages.png'):
    """Gera um gráfico de pizza com a distribuição das linguagens."""
    labels = languages.keys()
    sizes = languages.values()
    plt.figure(figsize=(10, 7))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Assegura que o gráfico será desenhado como um círculo.
    plt.title('Distribuição das Linguagens nos Repositórios GitHub')
    plt.savefig(output_path)  # Salva o gráfico em um arquivo
    plt.close()

if __name__ == '__main__':
    repos = get_repositories(USERNAME)
    languages = get_languages(repos)
    plot_languages(languages)
