from flask import Flask, render_template, request, redirect, url_for, flash
from captura import criar_pastas, capturar_pagina
from chat_posters import analise_chat_posters
from chat_redes_sociais import analise_chat_redes
from chat_youtube import analise_chat_youtube
import os
from flask import send_from_directory
from weasyprint import HTML
from flask import make_response


app = Flask(__name__)
app.secret_key = 'chave-secreta-super-secreta'

# Configurações
INSTAGRAM_ACCOUNTS = [
    'gabrielmedina',        
    'filipetoledo',        
    'itaglopes',            
    'tatianawestonwebb',   
    'wsl',                 
    'canaloff',            
    'surfertoday',      
    'stab',              
]

YOUTUBE_CHANNELS = [
    'WorldSurfLeague',     
    'CanalOff',          
    'StabMagazine',        
    'TheSurfNetwork',     
    'RedBullSurfing',     
    'SURFER',             
    'Surfline',           
    'JamieONeill',     
]


def limpar_referencias():
    for subpasta in ['posters', 'redes_sociais', 'youtube']:
        pasta = os.path.join(PASTA_REFERENCIAS, subpasta)
        if os.path.exists(pasta):
            for arquivo in os.listdir(pasta):
                caminho_arquivo = os.path.join(pasta, arquivo)
                if os.path.isfile(caminho_arquivo):
                    os.remove(caminho_arquivo)


@app.route('/referencias/<path:filename>')
def referencias(filename):
    base_dir = os.path.join(app.root_path, 'referencias')
    return send_from_directory(base_dir, filename)


PASTA_REFERENCIAS = os.path.join('referencias')

def listar_imagens(categoria):
    caminho = os.path.join(PASTA_REFERENCIAS, categoria)
    if not os.path.exists(caminho):
        return []
    arquivos = sorted(
        [f for f in os.listdir(caminho) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))],
        key=lambda x: os.path.getmtime(os.path.join(caminho, x)),
        reverse=True
    )
    return [os.path.join(categoria, f) for f in arquivos]


@app.route('/', methods=['GET', 'POST'])
def index():
    selecionados_instagram = []
    selecionados_youtube = []
    pinterest = ''

    if request.method == 'POST':
        pinterest = request.form.get('pinterest', '').strip()
        selecionados_instagram = request.form.getlist('instagram[]')
        selecionados_youtube = request.form.getlist('youtube[]')

        if not (pinterest or selecionados_instagram or selecionados_youtube):
            flash('Por favor, informe pelo menos um termo ou seleção para buscar.', 'warning')
            return redirect(url_for('index'))

        limpar_referencias()
        criar_pastas()

        if pinterest:
            url = f'https://br.pinterest.com/search/pins/?q={pinterest.replace(" ", "%20")}'
            capturar_pagina(
                url=url,
                categoria='posters',
                nome_arquivo=pinterest.replace(" ", "_"),
                rolar=True,
                espera=8,
                multiplos=True,
                qtd_prints=4,
                login=False
            )
            analise_chat_posters(os.path.join(PASTA_REFERENCIAS, 'posters'))


        if selecionados_instagram:
            for insta_account in selecionados_instagram:
                url = f'https://www.instagram.com/{insta_account.strip("/")}/'
                capturar_pagina(
                    url=url,
                    categoria='redes_sociais',
                    nome_arquivo=insta_account.replace(" ", "_"),
                    rolar=True,
                    espera=8,
                    multiplos=True,
                    qtd_prints=4,
                    login=True
                )
            analise_chat_redes(os.path.join(PASTA_REFERENCIAS, 'redes_sociais'))

        if selecionados_youtube:
            for yt_channel in selecionados_youtube:
                url = f'https://www.youtube.com/results?search_query={yt_channel.replace(" ", "+")}'
                capturar_pagina(
                    url=url,
                    categoria='youtube',
                    nome_arquivo=yt_channel.replace(" ", "_"),
                    rolar=True,
                    espera=4,
                    multiplos=True,
                    qtd_prints=4,
                    login=False
                )
            analise_chat_youtube(os.path.join(PASTA_REFERENCIAS, 'youtube'))

        flash('Capturas concluídas com sucesso!', 'success')
        return redirect(url_for('analise'))

    return render_template(
        'index.html',
        instagram_accounts=INSTAGRAM_ACCOUNTS,
        youtube_channels=YOUTUBE_CHANNELS,
        pinterest=pinterest,
        selecionados_instagram=selecionados_instagram,
        selecionados_youtube=selecionados_youtube
    )


@app.route('/analise', methods=['GET'])
def analise():
    try:
        with open(os.path.join(PASTA_REFERENCIAS, 'posters', 'info_posters.txt'), 'r', encoding='utf-8') as f:
            referencias_posters = f.read()
    except FileNotFoundError:
        referencias_posters = 'Arquivo info_posters.txt não encontrado.'

    try:
        with open(os.path.join(PASTA_REFERENCIAS, 'redes_sociais', 'info_redes_sociais.txt'), 'r', encoding='utf-8') as f:
            referencias_instagram = f.read()
    except FileNotFoundError:
        referencias_instagram = 'Arquivo info_redes.txt não encontrado.'

    try:
        with open(os.path.join(PASTA_REFERENCIAS, 'youtube', 'info_youtube.txt'), 'r', encoding='utf-8') as f:
            referencias_youtube = f.read()
    except FileNotFoundError:
        referencias_youtube = 'Arquivo info_youtube.txt não encontrado.'

    imagens_posters = listar_imagens('posters')
    imagens_instagram = listar_imagens('redes_sociais')
    imagens_youtube = listar_imagens('youtube')

    return render_template(
        'referencias.html',
        referencias_posters=referencias_posters,
        referencias_instagram=referencias_instagram,
        referencias_youtube=referencias_youtube,
        imagens_posters=imagens_posters,
        imagens_instagram=imagens_instagram,
        imagens_youtube=imagens_youtube
    )


@app.route('/download', methods=['GET'])
def download():
    try:
        with open(os.path.join(PASTA_REFERENCIAS, 'posters', 'info_posters.txt'), 'r', encoding='utf-8') as f:
            referencias_posters = f.read()
    except FileNotFoundError:
        referencias_posters = 'Arquivo info_posters.txt não encontrado.'

    try:
        with open(os.path.join(PASTA_REFERENCIAS, 'redes_sociais', 'info_redes_sociais.txt'), 'r', encoding='utf-8') as f:
            referencias_instagram = f.read()
    except FileNotFoundError:
        referencias_instagram = 'Arquivo info_redes.txt não encontrado.'

    try:
        with open(os.path.join(PASTA_REFERENCIAS, 'youtube', 'info_youtube.txt'), 'r', encoding='utf-8') as f:
            referencias_youtube = f.read()
    except FileNotFoundError:
        referencias_youtube = 'Arquivo info_youtube.txt não encontrado.'

    imagens_posters = listar_imagens('posters')
    imagens_instagram = listar_imagens('redes_sociais')
    imagens_youtube = listar_imagens('youtube')
    
    rendered = render_template(
        'referencias.html',
        referencias_posters=referencias_posters,
        referencias_instagram=referencias_instagram,
        referencias_youtube=referencias_youtube,
        imagens_posters=imagens_posters,
        imagens_instagram=imagens_instagram,
        imagens_youtube=imagens_youtube
    )

    pdf = HTML(string=rendered).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=analise_referencias.pdf'
    return response


if __name__ == '__main__':
    if not os.path.exists(PASTA_REFERENCIAS):
        os.makedirs(PASTA_REFERENCIAS)
        for subfolder in ['posters', 'redes_sociais', 'youtube']:
            os.makedirs(os.path.join(PASTA_REFERENCIAS, subfolder))
    
    app.run(debug=True)