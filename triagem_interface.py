import os
from tkinter import Tk, filedialog, simpledialog, messagebox, scrolledtext, Button, Label
from docx import Document
from PyPDF2 import PdfReader

def extrair_texto_pdf(caminho):
    texto = ""
    try:
        reader = PdfReader(caminho)
        for page in reader.pages:
            texto += page.extract_text() or ""
    except:
        texto = "[Erro na leitura do PDF]"
    return texto

def extrair_texto_docx(caminho):
    texto = ""
    try:
        doc = Document(caminho)
        for para in doc.paragraphs:
            texto += para.text + "\n"
    except:
        texto = "[Erro na leitura do DOCX]"
    return texto

def selecionar_pasta():
    pasta = filedialog.askdirectory(title="Selecione a pasta com currículos")
    if not pasta:
        return

    criterios_str = simpledialog.askstring("Critérios", "Informe as palavras-chave separadas por vírgula:")
    if not criterios_str:
        return

    criterios = [c.strip().lower() for c in criterios_str.split(",")]

    curriculos_aceitos = []

    for arquivo in os.listdir(pasta):
        caminho_arquivo = os.path.join(pasta, arquivo)
        if arquivo.lower().endswith(".pdf"):
            texto = extrair_texto_pdf(caminho_arquivo)
        elif arquivo.lower().endswith(".docx"):
            texto = extrair_texto_docx(caminho_arquivo)
        else:
            continue

        texto = texto.lower()
        encontrados = [c for c in criterios if c in texto]

        if encontrados:
            curriculos_aceitos.append((arquivo, encontrados))

    # Exibir os resultados
    resultado_text.delete("1.0", "end")
    if curriculos_aceitos:
        for nome, palavras in curriculos_aceitos:
            resultado_text.insert("end", f"- {nome}: {', '.join(palavras)}\n")
    else:
        resultado_text.insert("end", "Nenhum currículo atendeu aos critérios.")

# Interface
root = Tk()
root.title("Triagem de Currículos Automática")
root.geometry("600x400")

Label(root, text="Triagem de Currículos", font=("Arial", 14)).pack(pady=10)

btn = Button(root, text="Selecionar Pasta e Iniciar", command=selecionar_pasta)
btn.pack(pady=5)

resultado_text = scrolledtext.ScrolledText(root, width=80, height=15)
resultado_text.pack(padx=10, pady=10)

root.mainloop()
