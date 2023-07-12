def fazer_pesquisa_stackoverflow(pergunta):
    import requests
    from modules.log import log

    URL = "https://api.stackexchange.com/2.3/search"
    PARAMETROS = {
        "site": "stackoverflow",
        "intitle": pergunta,
        "order": "desc",
        "sort": "relevance"
    }

    try:
        resposta = requests.get(URL, params=PARAMETROS)
        dados = resposta.json()
        
        if dados['items'] != []:
            for i in range(len(dados['items'])):
                if i == 0:
                    # titulo_pesquisa = (f"Título da pergunta: {dados['items'][0]['title']}")
                    link_pergunta = (f"Link: {dados['items'][0]['link']}")
                    return (link_pergunta, )
        return (False,)

    except requests.exceptions.RequestException as e:
        log.salva_erro_em_log(e)