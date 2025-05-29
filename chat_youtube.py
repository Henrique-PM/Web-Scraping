import os
import pytesseract
from PIL import Image
from openai import OpenAI

client = OpenAI(api_key="")

def analise_chat_youtube(caminho_pasta):
    textos_extraidos = []

    for nome_arquivo in sorted(os.listdir(caminho_pasta)):
        if nome_arquivo.lower().endswith(('.png', '.jpg', '.jpeg')):
            caminho_completo = os.path.join(caminho_pasta, nome_arquivo)
            print(f"📸 Processando imagem: {nome_arquivo}")

            imagem = Image.open(caminho_completo)
            texto = pytesseract.image_to_string(imagem).strip()
            if texto:
                textos_extraidos.append(f"[{nome_arquivo}]\n{texto}\n")

    if not textos_extraidos:
        print("⚠️ Nenhum texto foi extraído das imagens.")
        return

    texto_completo = "\n\n".join(textos_extraidos)

    prompt = f"""
    Abaixo está o conteúdo extraído de várias imagens de um canal do YouTube voltado para esportes:

    \"\"\"{texto_completo}\"\"\"

    Com base nesses conteúdos, forneça uma análise geral:
    - Quais são os formatos de vídeo mais recorrentes (cortes, resumos, análises, vlogs, bastidores);
    - O estilo visual e de edição (thumbnails, cores, ritmo, cortes rápidos ou lentos, trilha sonora);
    - A linguagem usada e o posicionamento do canal em relação à cultura esportiva atual;
    - Como criadores de conteúdo esportivo podem se inspirar nesse canal para atrair audiência e se destacar.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )

    resposta_gerada = response.choices[0].message.content.strip()

    caminho_saida = os.path.join(caminho_pasta, "info_youtube.txt")
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(resposta_gerada)

    print("info_youtube.txt gerado com análise única consolidada.")
