from constantes import ARQUIVO_LOG
import datetime
import pytz

fuso_horario = pytz.timezone('America/Sao_Paulo')

def salva_erro_em_log(error):
    """Salva exceções em arquivo log.txt.
    
    :param error
    """

    dia_do_erro = datetime.datetime.now(fuso_horario).strftime("%d/%m/%Y %H:%M:%S")
    arquivo = open(ARQUIVO_LOG, "a")

    msg = f'[{dia_do_erro}] - {error}\n'
    arquivo.write(msg)

