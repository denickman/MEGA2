from fpdf import FPDF

pdf = FPDF()

pdf.add_page()
pdf.set_font(family='Times', style='B', size=12)
pdf.cell(0, 10, 'Hello, world!', ln=True)


pdf.add_page()
pdf.set_font(family='Times', style='B', size=12)
pdf.cell(0, 10, 'COOOLLLL!', ln=True)


pdf.output('output.pdf')