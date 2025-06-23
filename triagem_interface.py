import streamlit as st
from docx import Document
from PyPDF2 import PdfReader

st.set_page_config(page_title="Triagem de Currículos", layout="centered")

def extrair_texto_pdf(arquivo):
    texto = ""
    try:
        reader = PdfReader(arquivo)
        for page in reader.pages:
            texto += page.extract_text() or ""
    except:
        texto = "[Erro na leitura do PDF]"
    return texto

def extrair_texto_docx(arquivo):
    texto = ""
    try:
        doc = Document(arquivo)
        for para in doc.paragraphs:
            texto += para.text + "\n"
    except:
        texto = "[Erro na leitura do DOCX]"
    return texto

st.title("🔍 Triagem de Currículos")

st.markdown("**Envie arquivos .PDF ou .DOCX e defina os critérios para filtrar os currículos automaticamente.**")

criterios = st.text_input("Critérios (separados por vírgula)", "Excel, Administrativo")

arquivos = st.file_uploader("Envie os currículos", accept_multiple_files=True, type=["pdf", "docx"])

if st.button("Analisar") and arquivos:
    criterios_lista = [c.strip().lower() for c in criterios.split(",")]
    resultados = []

    for arq in arquivos:
        texto = ""
        if arq.name.endswith(".pdf"):
            texto = extrair_texto_pdf(arq)
        elif arq.name.endswith(".docx"):
            texto = extrair_texto_docx(arq)
        
        texto = texto.lower()
        encontrados = [c for c in criterios_lista if c in texto]

        if encontrados:
            resultados.append((arq.name, encontrados))

    if resultados:
        st.success(f"{len(resultados)} currículo(s) encontrados com os critérios:")
        for nome, palavras in resultados:
            st.write(f"- **{nome}** → {', '.join(palavras)}")
    else:
        st.warning("Nenhum currículo atendeu aos critérios.")
