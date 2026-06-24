from pypdf import PdfReader
p = PdfReader('Laboratorio 3 – Automatización, Monitoreo y Contenerización de FinTech Nova (1).pdf')
text = []
for page in p.pages:
    text.append(page.extract_text() or '')
full = '\n\n'.join(text)
with open('lab3_text.txt','w',encoding='utf-8') as f:
    f.write(full)
print('Wrote lab3_text.txt')
