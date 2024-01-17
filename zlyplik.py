from pypdf import PdfReader,PdfWriter
import camelot
def headers(filename):
    header = ''
    zi=[]
    z = set()
    reader = PdfReader(filename)
    for page in reader.pages:
        t = page.extract_text()
        for i in range(0, 40):
            if t[i] != '\n':
                header = t[0:i]
            else:
                break
        z.add(header)
    for items in z:
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
    return c
def parseparsed(filename):
    reader = PdfReader(filename)
    z=headers(filename)
    for i in range(0,len(z)):
        writer = PdfWriter()
        header=z[i]
        limits = getpages(filename, header)
        pages = reader.pages[limits[0]:limits[-1] + 1]
        if '/' in header:
            header=header.replace('D/P','DO PROD.')
        new_file = open(f'{header}.pdf', 'wb')
        for page in pages:
            writer.add_page(page)
            writer.write(new_file)
        writer.close()
        new_file.close()
def exportdata(file):
    file_name=str(file)
    table=camelot.read_pdf(file,pages='all')
    table.export(f'{file_name}.csv',f='csv',compress=True)

exportdata('G A Z  Z I E M N Y  1.pdf')
