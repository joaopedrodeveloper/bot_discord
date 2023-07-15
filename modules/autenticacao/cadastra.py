from modules.cargos import cargo
from modules.autenticacao import codigo, envia_email
from modules.le_arquivos import le_arquivos_csv
from constantes import SITUACAO_CADASTROS_CSV, COLUNA_USUARIO_SITUACAO_CADASTROS_CSV, COLUNA_CODIGO_SITUACAO_CADASTROS_CSV, COLUNA_EMAIL_SITUACAO_CADASTROS_CSV, CARGO_ID_ALUNOS, CARGO_ID_PROFESSORES, CARGO_ID_PRETENDENTE, ALUNOS_CSV, ALUNOS_CSV_COLUNA_NOME, ALUNOS_CSV_COLUNA_EMAIL_ACADEMICO, PROFESSORES_CSV, PROFESSORES_CSV_COLUNA_NOME, PROFESSORES_CSV_COLUNA_EMAIL
from modules.log.log import salva_erro_em_log
from modules.ban.ban import ban_usuario

async def inicia_cadastro_usuario(member, bot):
    """Inicia o cadastro do usuario no servidor do discord. 
    Se o email constar no arquivo alunos.csv ou professores.csv, retorna: True, incompleto e o email. 
    Caso contrário, retorna: False, não encontrado, None.
    
    :param member: discord.class
    :param bot: discord.class
    
    :return bool True ou False
    :return str incompleto ou não encontrado
    :return str email ou None
    """

    await cargo.adiciona_cargo(member, CARGO_ID_PRETENDENTE)
    await member.send('Iniciando seu cadastro')
    await member.send('***ATENÇÃO!!!***  Você tem 15 minutos para digitar o email acadêmico.')

    contador_email = 0

    while contador_email < 3:
        await member.send('Por favor, digite seu email:')
        try:
            email_msg = await bot.wait_for('message', check=lambda m: m.author == member, timeout=900)
            email = email_msg.content
            email = email.lower().strip()
            retorno, dados = le_arquivos_csv.encontra_dado(SITUACAO_CADASTROS_CSV, COLUNA_EMAIL_SITUACAO_CADASTROS_CSV, email)
            if retorno == False:
                retorno_professor, dados_professor = le_arquivos_csv.encontra_dado(PROFESSORES_CSV, PROFESSORES_CSV_COLUNA_EMAIL, email)
                retorno_aluno, dados_aluno = le_arquivos_csv.encontra_dado(ALUNOS_CSV, ALUNOS_CSV_COLUNA_EMAIL_ACADEMICO, email)
                try:
                    if retorno_professor or retorno_aluno:
                        return True, 'incompleto', email
                    else:
                        contador_email += 1
                        await member.send(f'Email inválido. Tentativas: {contador_email}/3')

                        if contador_email == 3:
                            await member.send('Tentativas estouradas. Tente novamente em 24h')
                            await ban_usuario(member=member, duracao_dia=1)
                            return False, 'nao encontrado', None
                except Exception as e:
                    salva_erro_em_log(e)
                    break
            else:
                await member.send('Usuário já está no servidor. Tente novamente em 24h')
                await ban_usuario(member=member, duracao_dia=1)
        except TimeoutError:
            await member.send('Tempo limite estourado. Tente novamente em 24h')
            await ban_usuario(member=member, duracao_dia=1)


async def conclui_cadastro_usuario(member, bot, email):
    """Conclui o cadastro do usuário no servidor do discord. Se tudo certo, retorna: completo.
    
    :param member: discord.class
    :param bot: discord.class
    :param email: str
    
    :return str completo
    """

    membro_tipo_str = str(member)
    retorno, dados = le_arquivos_csv.encontra_dado(SITUACAO_CADASTROS_CSV, COLUNA_USUARIO_SITUACAO_CADASTROS_CSV, membro_tipo_str)
    codigo_gerado = dados[COLUNA_CODIGO_SITUACAO_CADASTROS_CSV].values[0]
    envia_email.envia_codigo_por_email(email, codigo_gerado)

    await member.send('Enviamos um código para seu email. Verifique também na sua caixa de spam.')
    contador_codigo = 0

    while contador_codigo < 3:
        await member.send('Digite o código enviado:')
        code_msg = await bot.wait_for('message', check=lambda m: m.author == member)
        codigo_digitado_usuario = code_msg.content

        if codigo_digitado_usuario == codigo_gerado:
            retorno_professor, dados_professor = le_arquivos_csv.encontra_dado(PROFESSORES_CSV, PROFESSORES_CSV_COLUNA_EMAIL, email)
            retorno_aluno, dados_aluno = le_arquivos_csv.encontra_dado(ALUNOS_CSV, ALUNOS_CSV_COLUNA_EMAIL_ACADEMICO, email)
            if retorno_professor:
                nome = dados_professor[PROFESSORES_CSV_COLUNA_NOME].values[0]
                nome = nome.split()
                nome = f"{nome[0]} {nome[-1]}"
                await cargo.adiciona_cargo(member, CARGO_ID_PROFESSORES)
            elif retorno_aluno:
                nome = dados_aluno[ALUNOS_CSV_COLUNA_NOME].values[0]
                await cargo.adiciona_cargo(member, CARGO_ID_ALUNOS)
                # await verifica_disciplinas_matriculadas(email, member)
        
            await member.edit(nick=nome)
            await cargo.remove_cargo(member, CARGO_ID_PRETENDENTE)
            await member.send(f'Cadastro concluído! Email validado! Acesso ao {member.guild} liberado!')

            return 'completo'
        
        else:
            contador_codigo += 1
            await member.send(f'Código inválido. Tentativas: {contador_codigo}/3')

            if contador_codigo == 3:
                await member.send('Tentativas estouradas. Tente novamente em 24h')
                await ban_usuario(member=member, duracao_dia=1)

                await cargo.remove_cargo(member, CARGO_ID_PRETENDENTE)


# async def verifica_disciplinas_matriculadas(email, member):
#     """Verifica as disciplinas em que os usuários alunos estão matriculados. 
#     Adiciona os cargos das disciplinas ao usuário/membro.
    
#     :param email: str
#     :param member: discord.class
#     """

#     retorno_dados_aluno, dados_aluno = le_arquivos_csv.encontra_dado(ALUNOS_CSV, ALUNOS_CSV_COLUNA_EMAIL_ACADEMICO, email)
#     matricula_aluno = dados_aluno[ALUNOS_CSV_COLUNA_MATRICULA].values[0]
#     for i in range(len(DISCIPLINAS)):
#         retorno_dados_matricula, dados_aluno_matricula = le_arquivos_csv.encontra_dado(f'{PASTA_DISCIPLINAS}/{DISCIPLINAS[i]}', COLUNA_MATRICULADOS_DISCIPLINAS_CSV, matricula_aluno)
#         if retorno_dados_matricula:
#             await cargo.adiciona_cargo(member, CARGOS_DISCIPLINAS[i]['cargo_id_discord'])