from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_pdf():
    pdf_path = "backend/data/sample_doc.pdf"
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(72, height - 72, "ShieldBot 9000 User Manual")
    
    # Subtitle
    c.setFont("Helvetica", 14)
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.drawString(72, height - 100, "Version 9.4.0 Confidential Documentation")
    
    c.setStrokeColorRGB(0.7, 0.7, 0.7)
    c.line(72, height - 110, width - 72, height - 110)
    
    c.setFillColorRGB(0, 0, 0)
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height - 150, "1. System Activation code")
    
    c.setFont("Helvetica", 11)
    text = (
        "To activate the ShieldBot 9000 defense mechanism, the administrator must enter "
        "the secret system activation key: 'SHIELD-GOLD-777-SECURE'. "
        "Once entered, the mechanical robot initializes in active protection mode and patrols "
        "the perimeter. The default security clearance password is 'admin_pass_9000'."
    )
    y = height - 170
    words = text.split()
    line = ""
    for word in words:
        if c.stringWidth(line + " " + word, "Helvetica", 11) < (width - 144):
            line += " " + word
        else:
            c.drawString(72, y, line.strip())
            line = word
            y -= 15
    if line:
        c.drawString(72, y, line.strip())
        
    c.showPage()
    c.save()
    print("Generated PDF successfully at:", pdf_path)

if __name__ == "__main__":
    generate_pdf()
