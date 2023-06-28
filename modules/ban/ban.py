import discord
import pandas as pd
import pytz
import datetime
import asyncio
from procura_arquivo import encontra_caminho_do_arquivo
from modules.le_arquivos import le_arquivos_csv
from constantes import PASTA_DATA, BANIDOS_CSV, COLUNA_ID_USUARIOS_BANIDOS_CSV, COLUNA_HORA_BAN_BANIDOS_CSV, COLUNA_HORA_DESBAN_BANIDOS_CSV

FUSO_HORARIO = pytz.timezone('America/Sao_Paulo')
MODELO_HORA = "%Y-%m-%d %H:%M:%S.%f%z"

async def ban_usuario(member, duracao_dia):
    """Bane o membro via member.ban(). A duração é passada pelo parâmetro duracao_dia. 
    
    :param member: discord.class
    :param duracao_dia: int
    """

    user_id = member.id
    await member.ban(reason = 'Tempo limite estourado. Tente novamente em 24h')

    hora_do_ban = datetime.datetime.now(FUSO_HORARIO)
    delta = datetime.timedelta(days=duracao_dia)
    hora_desban = hora_do_ban + delta

    caminho_arquivo = encontra_caminho_do_arquivo(pasta=PASTA_DATA, nome_arquivo=BANIDOS_CSV)
    df = pd.DataFrame({COLUNA_ID_USUARIOS_BANIDOS_CSV: [user_id], COLUNA_HORA_BAN_BANIDOS_CSV: [hora_do_ban], COLUNA_HORA_DESBAN_BANIDOS_CSV: [hora_desban]})

    df.to_csv(caminho_arquivo, mode='a', header=False, index=False)


async def verifica_ban_usuario(guild):
    """Verifica a cada 60 segundos se o banimento do usuário já expirou. 
    
    :param guild: discord.class
    """

    while True:
        df = pd.read_csv(encontra_caminho_do_arquivo(pasta=PASTA_DATA, nome_arquivo=BANIDOS_CSV))

        coluna_hora_desban = df[COLUNA_HORA_DESBAN_BANIDOS_CSV]
        for desban in coluna_hora_desban:
            retorno, dados = le_arquivos_csv.encontra_dado(BANIDOS_CSV, COLUNA_HORA_DESBAN_BANIDOS_CSV, desban)

            hora_desban = datetime.datetime.strptime(desban, MODELO_HORA)
            hora_atual = str(datetime.datetime.now(FUSO_HORARIO))
            hora_atual = datetime.datetime.strptime(hora_atual, MODELO_HORA)

            if hora_atual >= hora_desban:
                user_id = dados[COLUNA_ID_USUARIOS_BANIDOS_CSV].values[0]
                apaga_registro_ban_usuario(user_id)
                await guild.unban(discord.Object(id=user_id))
        await asyncio.sleep(60)
        

def apaga_registro_ban_usuario(member):
    """Apaga o registro de banimento do usuário assim que o tempo expira.
    
    :param member: discord.class
    :param cargo_id: int
    """

    df = pd.read_csv(le_arquivos_csv.encontra_caminho_do_arquivo(pasta=PASTA_DATA, nome_arquivo=BANIDOS_CSV))

    retorno, dados = le_arquivos_csv.encontra_dado(BANIDOS_CSV, COLUNA_ID_USUARIOS_BANIDOS_CSV, member)
    if retorno:
        df = df.drop(dados.index[0])
        df.to_csv(le_arquivos_csv.encontra_caminho_do_arquivo(pasta=PASTA_DATA, nome_arquivo=BANIDOS_CSV), index=False)
