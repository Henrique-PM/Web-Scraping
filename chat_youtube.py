import os
import pytesseract
from PIL import Image
from openai import OpenAI

client = OpenAI(api_key="")

caminho_pasta = 'referencias/youtube'
resultados = []

def analise_chat_youtube(caminho_pasta):

    for nome_arquivo in sorted(os.listdir(caminho_pasta)):
        if nome_arquivo.lower().endswith(('.png', '.jpg', '.jpeg')):
            caminho_completo = os.path.join(caminho_pasta, nome_arquivo)
            print(f"Processando imagem: {nome_arquivo}")

            imagem = Image.open(caminho_completo)
            texto_extraido = pytesseract.image_to_string(imagem)

            prompt = f"""
                O texto abaixo foi extraído de uma imagem relacionada a um vídeo do YouTube sobre basquete (títulos, comentários, descrições):

                \"\"\"{texto_extraido}\"\"\"

                Analise o conteúdo focando em:
                - Principais temas abordados no vídeo (partidas, análises, curiosidades);
                - Como o vídeo contribui para o conhecimento e interesse sobre basquete;
                - Público-alvo e potencial impacto na comunidade de fãs;
                - Qualquer insight sobre estratégias, técnicas ou histórias do basquete.

                Produza uma análise detalhada e informativa.
                """



            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )

            resposta_texto = response.choices[0].message.content.strip()
            resultados.append(f"Análise GPT:\n{resposta_texto}\n\n")


    with open(os.path.join(caminho_pasta, "info_youtube.txt"), "w", encoding="utf-8") as f:
        f.writelines(resultados)

        print("✅ info_youtube.txt gerado com análises baseadas em texto OCR.")
