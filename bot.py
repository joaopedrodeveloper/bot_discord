import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from modules.autenticacao import cadastra, codigo
from modules.le_arquivos import le_arquivos_csv
from modules.log.log import salva_erro_em_log
from modules.ban.ban import verifica_ban_usuario
from constantes import NOME_SERVIDOR_DISCORD

load_dotenv()

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Voce logou como {bot.user}')

    for guild in bot.guilds:
        if str(guild) == NOME_SERVIDOR_DISCORD:
            await verifica_ban_usuario(guild)
        

@bot.event
async def on_member_join(member):
    try:
        sucesso, situacao_cadastro, email = await cadastra.inicia_cadastro_usuario(member, bot)
        if sucesso:
            codigo_gerado = codigo.gera_codigo()
            le_arquivos_csv.cria_cadastro(situacao_cadastro, member, email, codigo_gerado)
            situacao_cadastro = await cadastra.conclui_cadastro_usuario(member, bot, email)
            le_arquivos_csv.atualiza_cadastro(situacao_cadastro, member)
    except Exception as e:
        salva_erro_em_log(e)
        le_arquivos_csv.remove_usuario_do_arquivo_cadastro(member)


@bot.event
async def on_member_remove(member):
    le_arquivos_csv.remove_usuario_do_arquivo_cadastro(member)


API_KEY = os.getenv('DISCORD_API_KEY')
bot.run(API_KEY)