import os
import pytesseract
from PIL import Image
from openai import OpenAI

client = OpenAI(api_key="")

caminho_pasta = 'referencias/posters'
resultados = []

def analise_chat_posters(caminho_pasta):

    for nome_arquivo in sorted(os.listdir(caminho_pasta)):
        if nome_arquivo.lower().endswith(('.png', '.jpg', '.jpeg')):
            caminho_completo = os.path.join(caminho_pasta, nome_arquivo)
            print(f"Processando imagem: {nome_arquivo}")

            imagem = Image.open(caminho_completo)
            texto_extraido = pytesseract.image_to_string(imagem)

            prompt = f"""
                Você recebeu o seguinte texto extraído de uma imagem relacionada a basquete, como uma notícia, análise ou estatística:

                \"\"\"{texto_extraido}\"\"\"

                Por favor, faça uma análise detalhada considerando:
                - A performance dos times e jogadores mencionados;
                - Estratégias e táticas evidenciadas;
                - Impacto e reação da torcida e da comunidade do basquete;
                - Tendências e aspectos culturais do esporte destacados.

                Responda com insights claros e relevantes para quem acompanha basquete.
                """


            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )

            resposta_texto = response.choices[0].message.content.strip()
            resultados.append(f"Análise GPT:\n{resposta_texto}\n\n")


    with open(os.path.join(caminho_pasta, "info_posters.txt"), "w", encoding="utf-8") as f:
        f.writelines(resultados)

        print("✅ info_posters.txt gerado com análises baseadas em texto OCR.")
