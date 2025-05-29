import os
import pytesseract
from PIL import Image
from openai import OpenAI

client = OpenAI(api_key="")

def analise_chat_posters(caminho_pasta):
    textos_extraidos = []

    for nome_arquivo in sorted(os.listdir(caminho_pasta)):
        if nome_arquivo.lower().endswith(('.png', '.jpg', '.jpeg')):
            caminho_completo = os.path.join(caminho_pasta, nome_arquivo)
            print(f"🖼️ Processando imagem: {nome_arquivo}")

            imagem = Image.open(caminho_completo)
            texto = pytesseract.image_to_string(imagem).strip()
            if texto:
                textos_extraidos.append(f"[{nome_arquivo}]\n{texto}\n")

    if not textos_extraidos:
        print("⚠️ Nenhum texto extraído das imagens.")
        return

    texto_completo = "\n\n".join(textos_extraidos)

    prompt = f"""
    Abaixo está o texto extraído de várias imagens relacionadas ao esporte:

    \"\"\"{texto_completo}\"\"\"

    Com base nesse conteúdo, faça uma análise única e abrangente sobre:
    - As tendências de design gráfico esportivo observadas;
    - Os elementos visuais que se destacam e seu impacto na comunicação (tipografia, cores, composição, emoção);
    - A influência potencial desses estilos em diferentes mídias (TV, redes sociais, ambientes físicos);
    - O que esses materiais sugerem sobre a cultura esportiva contemporânea.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )

    resposta_gerada = response.choices[0].message.content.strip()

    caminho_saida = os.path.join(caminho_pasta, "info_posters.txt")
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(resposta_gerada)

    print("Análise única gerada e salva em info_posters.txt")
