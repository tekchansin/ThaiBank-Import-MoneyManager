from PyPDF2 import PdfReader,PdfWriter

def decrypt_file(filename: str, password: str) -> str:
    pdf_writer = PdfWriter()
    pdf_reader = PdfReader(open(filename, 'rb'), strict=False)
    pdf_reader.decrypt(password=password)
    for page_number in range(len(pdf_reader.pages)):
        pdf_writer.add_page(pdf_reader.pages[page_number])
    
    with open("./sample/decypted-2.pdf", "wb") as f:
        pdf_writer.write(f)
    return "PDF file decrypted successfully"

decrypt_file('./sample/e-xxxx.PDF','xxxx')