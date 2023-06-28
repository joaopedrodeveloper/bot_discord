import os

def encontra_caminho_do_arquivo(pasta='', nome_arquivo=''):
    """Procura o endereço do meu arquivo desejado. Retorna o diretório.
    ATENÇÃO!! Passe a pasta com o / antes. Exemplo: /data
    
    :param pasta: str
    :param nome_arquivo: str
    
    :return str caminho_arquivo
    """

    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_arquivo = os.path.join(diretorio_atual + pasta, nome_arquivo)

    return caminho_arquivo
