from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.add_font('DejaVu', '', 'DefaVu/DejaVuSansCondensed.ttf', uni=True)
pdf.set_font('DejaVu', '', 16)
pdf.cell(200, 10, txt="dddd", align="B")
pdf.cell(200, 10, txt='dsa', align='')
pdf.output("simple_demo.pdf")