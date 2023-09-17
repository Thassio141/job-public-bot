**BOT VAGAS**

Documentação: 

No arquivo main.py se encontra a chamada das funções presentes no arquivo functions.py

Logo no inicio do arquivo main.py deixa claro o uso do Token do telegram que se for usado em nuvem ou exposto em um repositorio deve se evitar deixar exposto por ser a chave de contato com seu bot.

As anotações *@bot.message_handler(commands=)* servem como comandos recebidos durante o chat com o bot

A anotação *@bot.message_handler(func=lambda msg: True)* serve para responder qualquer mensagem que não tenha sido identificada anteriormente

No arquivo functions.py foi usado web scraping para conseguir informações de vagas tanto do linkedin quanto da gupy.
Versão 1.0:

-> Integrado ao telegram e responde sempre que o usuario pergunta.
-> Pesquisa vagas somente no gupy.io 

Versão 1.1:

-> Melhora a qualidade das respostas (Organizando o que o bot deve responder)
-> Filtro (Se a vaga é Remota ou Não)
-> Consegue vagas do linkedin
