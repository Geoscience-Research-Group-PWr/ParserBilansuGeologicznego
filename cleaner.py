from pypdf import PdfReader,PdfWriter

def parse(filename):
    reader =PdfReader(filename)
    writer=PdfWriter()
    name=str(filename)[:-4]
    for page in reader.pages:
        if 'Lp.' in page.extract_text() and ('zag.' in page.extract_text() or "Powiat" in page.extract_text()):# dodac warunek na powiat np zeby odsiac niechciane tabele
            writer.add_page(page)
            with open(f'{name}parsed.pdf', 'wb') as file:
                writer.write(file)


#parse("Bilans_2010.pdf")
# wynik 1 plik z tabelami 