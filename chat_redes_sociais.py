import os
import pytesseract
from PIL import Image
from openai import OpenAI

client = OpenAI(api_key="")

def analise_chat_redes(caminho_pasta):
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
    Abaixo está o conteúdo extraído de várias postagens de um perfil esportivo no Instagram:

    \"\"\"{texto_completo}\"\"\"

    Com base nesses conteúdos, forneça uma análise geral:
    - Quais são os estilos de design mais usados (cores, fontes, layouts, formatos);
    - Quais estratégias de engajamento estão sendo aplicadas (uso de memes, frases de impacto, reels, colaborações);
    - Que tipo de conteúdo parece gerar mais impacto no público;
    - Como criadores de conteúdo esportivo podem se inspirar nesse perfil para fortalecer sua marca.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )

    resposta_gerada = response.choices[0].message.content.strip()

    caminho_saida = os.path.join(caminho_pasta, "info_redes_sociais.txt")
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(resposta_gerada)

    print("info_redes_sociais.txt gerado com análise única consolidada.")
