from pypdf import PdfReader,PdfWriter
import camelot
import re
import os

def headers(filename):
    header = ''
    zi=[]
    z = set()
    reader = PdfReader(filename)
    for page in reader.pages:
        t = page.extract_text()
        for i in range(0, 100):
            if t[i] != '\n':
                header = t[0:i]
                header = ''.join(sym for sym in header if not (sym.isdigit() or sym == '.'))
                header=re.sub(r'^\s+|\s+$', '', header)
            else:
                break
        z.add(header)
    for items in z:
        print(items)
        zi.append(items)
    return zi
def getpages(filename,header):
    occurance=[]
    c=[]
    reader=PdfReader(filename)
    for j in range(0,len(reader.pages)):
        page=reader.pages[j]
        if header in page.extract_text():
            occurance.append(j)
    c.append(min(occurance))
    c.append(max(occurance))
    print(c)
    return c

def parseparsed(filename):
    reader = PdfReader(filename)
    z = headers(filename)
    for i in range(0, len(z)):
        writer = PdfWriter()
        header = z[i]
        print(header)
        limits = getpages(filename, header)
        pages = reader.pages[limits[0]:limits[-1] + 1]
        if '/' in header:
            header = header.replace('D/P', 'DO PROD.')
        new_file = open(f'{header}.pdf', 'wb')
        for page in pages:
            writer.add_page(page)
            writer.write(new_file)
        writer.close()
        new_file.close()

def parse(filename):
    reader =PdfReader(filename)
    writer=PdfWriter()
    name=str(filename)[:-4]
    for page in reader.pages:
        if 'Lp.' in page.extract_text():
            writer.add_page(page)
            with open(f'{name}parsed.pdf', 'wb') as file:
                writer.write(file)

def exportdata(filename,year):
    name = str(filename)[:-4]
    print(str(filename))
    table=camelot.read_pdf(filename,pages='all')
    table.export(f'{name}_{year}.csv',f='csv',compress=True)


#parse("Bilans_2010.pdf")
#parseparsed("Bilans_2010parsed.pdf")
#exportdata("Bilans_2017.pdf")
#exportdata('31.   K A L C Y T.pdf')
# eksport do csv automatycznie
'''directory=os.listdir('D:\PyCharm\PyCharm 2023.2.4\parserpdf\year2010')
files=[file for file in directory if file.endswith('.pdf')]
for ffs in files:
    fpath=f'D:\PyCharm\PyCharm 2023.2.4\parserpdf\year2010\{ffs}'
    exportdata(fpath,2010)'''

