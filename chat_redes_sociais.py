import os
import pytesseract
from PIL import Image
from openai import OpenAI

client = OpenAI(api_key="")

caminho_pasta = 'referencias/redes sociais'
resultados = []

def analise_chat_redes(caminho_pasta):
    for nome_arquivo in sorted(os.listdir(caminho_pasta)):
        if nome_arquivo.lower().endswith(('.png', '.jpg', '.jpeg')):
            caminho_completo = os.path.join(caminho_pasta, nome_arquivo)
            print(f"Processando imagem: {nome_arquivo}")

            imagem = Image.open(caminho_completo)
            texto_extraido = pytesseract.image_to_string(imagem)

            prompt = f"""
                Abaixo está o texto extraído de uma imagem de uma publicação em redes sociais sobre basquete:

                \"\"\"{texto_extraido}\"\"\"

                Analise esse conteúdo considerando:
                - O engajamento e sentimento dos fãs de basquete;
                - Informações sobre jogadores, times ou eventos;
                - Aspectos motivacionais ou narrativas presentes;
                - Influência desse conteúdo na cultura do basquete.

                Forneça uma análise que ajude a entender o impacto desse post no universo do basquete.
                """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )

            resposta_texto = response.choices[0].message.content.strip()
            resultados.append(f"Análise GPT:\n{resposta_texto}\n\n")

    with open(os.path.join(caminho_pasta, "info_redes_sociais.txt"), "w", encoding="utf-8") as f:
        f.writelines(resultados)

    print("✅ info_redes.txt gerado com análises baseadas em texto OCR.")
