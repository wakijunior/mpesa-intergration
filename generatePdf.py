from fpdf import FPDF
from cloudinaryUpload import upload_pdf



pdf = FPDF()

def generate_pdf(txt, filename):
    print('my filename in generate pdf is', filename)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(200, 10, txt=txt, align='C')
    pdf.output(f"reciepts/{filename}.pdf")
    
    print(f"PDF generated and uploaded successfully as {filename}.pdf")
    
    upload_pdf(filename)
    
    
    


