from pypdf import PdfReader
p = PdfReader('Laboratorio4_CICD_FinTech_Nova.pdf')
text = []
for page in p.pages:
    text.append(page.extract_text() or '')
with open('lab4_text.txt', 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(text))
print('Wrote lab4_text.txt')
