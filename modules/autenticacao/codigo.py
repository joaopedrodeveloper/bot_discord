def gera_codigo():
    """Gera código aleatório. Retorna o código.
    
    :return str codigo
    """

    from random import randrange

    NUMEROS = '0123456789'
    codigo = ""

    for i in range(6):
        gera_aleatorio = randrange(0, len(NUMEROS))
        codigo += NUMEROS[gera_aleatorio]

    return codigo
