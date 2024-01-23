from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

def fit_text(text, max_width):
    line = ""
    for word in text.split():
        if c.stringWidth(line + word, 'Helvetica', 12) < max_width:
            line += word + " "
        else:
            return line.strip(), text[len(line):].strip()
    return line.strip(), ""


prompt = "German shepherd dog Tyson eat in New York city in front of the Statue of Liberty in the style of a coloring book illustration"
lines = []
max_text_width=512.0
buffer = io.BytesIO()
c = canvas.Canvas(buffer, pagesize=letter)
width, height = letter
while prompt:
    line, prompt = fit_text(prompt, max_text_width)
    lines.append(line)

print(lines)