import pandas as pd
import os
from procura_arquivo import encontra_caminho_do_arquivo
from constantes import PASTA_DATA, SITUACAO_CADASTROS_CSV, COLUNA_EMAIL_SITUACAO_CADASTROS_CSV, COLUNA_SITUACAO_CADASTROS_CSV, COLUNA_USUARIO_SITUACAO_CADASTROS_CSV, COLUNA_CODIGO_SITUACAO_CADASTROS_CSV
from modules.log.log import salva_erro_em_log

def cria_cadastro(situacao, member, email, codigo):
    """Cria meu membro dentro do arquivo situacao_cadastros.csv. Ele é criado após passar o email.
    
    :param situacao: str
    :param member: str
    :param email: str
    """

    member = str(member)

    caminho_arquivo = encontra_caminho_do_arquivo(pasta=PASTA_DATA, nome_arquivo=SITUACAO_CADASTROS_CSV)
    df = pd.DataFrame({COLUNA_EMAIL_SITUACAO_CADASTROS_CSV: [email], COLUNA_USUARIO_SITUACAO_CADASTROS_CSV: [member], COLUNA_SITUACAO_CADASTROS_CSV: [situacao], COLUNA_CODIGO_SITUACAO_CADASTROS_CSV: [codigo]})

    df.to_csv(caminho_arquivo, mode='a', header=False, index=False)


def atualiza_cadastro(situacao, member):
    """Atualiza a situação cadastral do meu membro dentro do arquivo situacao_cadastros.csv.
    
    :param situacao: str
    :param member: str
    """

    member = str(member)

    df = pd.read_csv(encontra_caminho_do_arquivo(pasta=PASTA_DATA, nome_arquivo=SITUACAO_CADASTROS_CSV), dtype=str)

    retorno, dados = encontra_dado(SITUACAO_CADASTROS_CSV, COLUNA_USUARIO_SITUACAO_CADASTROS_CSV, member)
    if retorno:
        indice_linha = dados.index[0]
        df.loc[indice_linha, COLUNA_SITUACAO_CADASTROS_CSV] = situacao

    df.to_csv(encontra_caminho_do_arquivo(pasta=PASTA_DATA, nome_arquivo=SITUACAO_CADASTROS_CSV), index=False)


def remove_usuario_do_arquivo_cadastro(member):
    """Apaga meu membro do arquivo situacao_cadastros.csv, assim que ele sai do servidor do discord.
    
    :param member: str
    """

    member = str(member)

    df = pd.read_csv(encontra_caminho_do_arquivo(pasta=PASTA_DATA, nome_arquivo=SITUACAO_CADASTROS_CSV), dtype=str)

    retorno, dados = encontra_dado(SITUACAO_CADASTROS_CSV, COLUNA_USUARIO_SITUACAO_CADASTROS_CSV, member)
    if retorno:
        df = df.drop(dados.index[0])
        df.to_csv(encontra_caminho_do_arquivo(pasta=PASTA_DATA, nome_arquivo=SITUACAO_CADASTROS_CSV), index=False)


def encontra_dado(nome_do_arquivo, coluna_a_procurar, dado):
    """Verifica e encontra se o dado existe na minha coluna. Retorna meu dados
    
    :param nome_do_arquivo: str
    :param coluna_a_procurar: str
    :param dado: str

    :return bool True
    :return pandas.core.frame.DataFrame dados
    """

    data_frame = pd.read_csv(encontra_caminho_do_arquivo(pasta=PASTA_DATA, nome_arquivo=nome_do_arquivo), dtype=str)

    try:
        coluna_encontrada = data_frame[coluna_a_procurar]
        if dado in coluna_encontrada.values:
            dados = data_frame.loc[coluna_encontrada == dado]
            return True, dados
        return False, []
    except Exception as e:
        salva_erro_em_log(e)
        return 'Coluna não encontrada'