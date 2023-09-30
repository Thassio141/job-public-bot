import re
import requests
import log_func


def url_shortener(url):
    tinyurl_url = f'https://tinyurl.com/api-create.php?url={url}'

    response = requests.get(tinyurl_url)

    if response.status_code == 200:
        short_url = response.text
        log_func.write_log(f'URL encurtada com sucesso : {short_url}')
        return short_url

    else:
        log_func.write_log(f'Falha ao encurtar url : {url}')


def id_link_linkedin(link):
    match = re.search(r'-\d+\?', link)

    if match:
        number = match.group()
        number_without_special = number.replace('-', '').replace('?', '')
        return f"https://www.linkedin.com/jobs/view/{number_without_special}"

    else:
        print("Não foi possível encontrar o numero no link.")