# Web-Scraping & Análise de Tendências – Surf

Projeto para **coleta automatizada, análise e geração de insights** sobre conteúdos visuais e textuais relacionados ao **surf**, extraídos de redes sociais como YouTube, Pinterest e Instagram.

## 🌊 Objetivo

Capturar referências visuais, frases, estilos de vida e tendências culturais do universo do **surf**, com foco em:

* Estilo visual e identidade de marcas e atletas
* Conteúdo motivacional e estilo de vida praiano
* Tendências em vestuário, linguagem e estética do surf

## 🧠 Funcionalidades

* 📸 Captura automática de imagens/vídeos de:

  * Pinterest
  * YouTube
  * Instagram (via Selenium)
    * 🧾 Extração de texto de imagens com OCR (Tesseract)
    * 🤖 Análise contextual e criativa com a API da OpenAI:

    * Classificação de conteúdo
    * Geração de insights sobre tendências
    * Sugestões de uso em design, marketing e conteúdo

---

## 🗂 Estrutura do Projeto

```
WEB-SCRAPING/
├── referencias/              # Imagens e textos capturados
├── templates/                # Templates para visualização (Flask)
├── captura.py                # Lógica de scraping
├── app.py                    # Aplicação web (Flask)
├── chat_posters.py           # Análise de pôsteres/visuais
├── chat_redes_sociais.py     # Análise de redes sociais
├── chat_youtube.py           # Análise de vídeos do YouTube
├── requirements.txt          # Dependências do projeto
└── README.md                 # Este arquivo
```

---

## ⚙️ Tecnologias Utilizadas

* **Python 3**
* **Selenium** – Automação do navegador
* **Tesseract OCR** – Reconhecimento de texto em imagens
* **Flask** – Aplicação Web para visualização e análise
* **OpenAI GPT API** – Geração de análises e sugestões criativas
* **Pillow**, **BeautifulSoup**, **Requests**

---

## 🚀 Como Usar

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

2. Instale o [Tesseract OCR](https://github.com/tesseract-ocr/tesseract).

3. Rode o sistema de captura de imagens:

```bash
python captura.py
```

4. Analise os conteúdos:

```bash
python chat_posters.py
python chat_youtube.py
python chat_redes_sociais.py
```

5. Inicie a aplicação web para navegar pelos resultados:

```bash
python app.py
```

## 🏄 Aplicações Práticas

* Branding para marcas de surf e estilo de vida praiano
* Criação de conteúdo visual e textual para redes sociais
* Referências visuais para design gráfico ou direção de arte
* Análise cultural do universo do surf em redes digitais
