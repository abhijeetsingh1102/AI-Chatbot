from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_pdf():
    pdf_path = "backend/data/simple.pdf"
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(72, height - 72, "Secure Chat Guardian User Guide")
    
    # Subtitle
    c.setFont("Helvetica", 14)
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.drawString(72, height - 100, "Documentation for version 1.0.0 (Local deployment)")
    
    c.setStrokeColorRGB(0.7, 0.7, 0.7)
    c.line(72, height - 110, width - 72, height - 110)
    
    # Reset Fill color
    c.setFillColorRGB(0, 0, 0)
    
    # Section 1: Overview
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height - 150, "1. Project Overview")
    
    c.setFont("Helvetica", 11)
    text = (
        "Secure Chat Guardian is an advanced client-server AI assistant designed to provide "
        "intelligent responses using both general LLM capabilities and Retrieval-Augmented Generation (RAG). "
        "The system is divided into a robust FastAPI backend and an interactive Streamlit frontend. "
        "By utilizing local sentence embedding models, it can read and index PDF documents securely "
        "without leaking context to external embedding providers."
    )
    # Simple word wrap logic
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
        
    # Section 2: Key Features
    y -= 30
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, y, "2. Key Features")
    
    features = [
        "Feature A: Extremely fast text generation powered by Groq and the LLaMA 3.1 8B model.",
        "Feature B: Pure NumPy L2 vector distance search running entirely on local CPU.",
        "Feature C: High accuracy text splitters with overlapping chunk sizes of 800 characters.",
        "Feature D: Dual interaction modes including General Chat and PDF Document context retrieval."
    ]
    
    y -= 20
    c.setFont("Helvetica", 11)
    for feat in features:
        c.drawString(90, y, f"- {feat}")
        y -= 20
        
    # Section 3: Technical Specifications
    y -= 20
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, y, "3. Technical Specifications")
    
    y -= 20
    c.setFont("Helvetica", 11)
    tech_info = [
        "Backend Server Frame: FastAPI (runs on port 8000)",
        "Frontend Client Frame: Streamlit (runs on port 8501)",
        "Local Embeddings Model: sentence-transformers/all-MiniLM-L6-v2 (384 dimensions)",
        "Main Language Model: llama-3.1-8b-instant (via Groq Cloud API)"
    ]
    for tech in tech_info:
        c.drawString(90, y, f"* {tech}")
        y -= 20
        
    # Save the PDF
    c.showPage()
    c.save()
    print("Generated PDF successfully at:", pdf_path)

if __name__ == "__main__":
    generate_pdf()
