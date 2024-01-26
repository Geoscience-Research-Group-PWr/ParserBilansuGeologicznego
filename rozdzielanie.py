from pypdf import PdfReader,PdfWriter
import re


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
    year=filename[-14:-10]
    z = headers(filename)
    for i in range(0, len(z)):
        writer = PdfWriter()
        header = z[i]
        print(header)
        limits = getpages(filename, header)
        pages = reader.pages[limits[0]:limits[-1] + 1]
        if '/' in header:
            header = header.replace('D/P', 'DO PROD.')
        new_file = open(f'{header}_{year}.pdf', 'wb')
        for page in pages:
            writer.add_page(page)
            writer.write(new_file)
        writer.close()
        new_file.close()

#parseparsed("Bilans_2010parsed.pdf")
# wynik 1 pdf do kazdej kopaliny