<p align="center">
    <img src="https://github.com/Thassio141/job-public-bot/blob/main/image/imagem%20BOT.png" alt="image">
    <H1> Jobby </H1>
</p>

<h2>Documentação: </h2>

No arquivo main.py se encontra todo o codigo necessario para a execução do bot

Logo no final do arquivo main.py deixa claro o uso do Token do telegram que se for usado em nuvem ou exposto em um repositorio deve se evitar deixar exposto por ser a chave de contato com seu bot.

As anotações ```@bot.message_handler(commands=)``` servem como comandos recebidos durante o chat com o bot

A anotação ```@bot.message_handler(func=lambda msg: True)``` serve para responder qualquer mensagem que não tenha sido identificada anteriormente

Foi usado web scraping para conseguir informações de vagas tanto do linkedin quanto da gupy.

<h2>Versão 1.3:</h2>

-> Melhora a qualidade das respostas (Organizando o que o bot deve responder)
<br>
-> Filtro (Se a vaga é Remota ou Não)
<br>
-> Consegue vagas do linkedin, Gupy e Glassdoor
<br>
-> Deploy em nuvem
<br>
-> Adiciona Log
