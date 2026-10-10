"""Render the already written significance brief; no mathematical inputs are executed."""
from pathlib import Path
import re
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parent
pdfmetrics.registerFont(TTFont('DV', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DV-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFontFamily('DV', normal='DV', bold='DV-Bold')
styles = {
    'title': ParagraphStyle('title', fontName='DV-Bold', fontSize=15, leading=18, spaceAfter=8),
    'meta': ParagraphStyle('meta', fontName='DV', fontSize=8.5, leading=11, textColor=colors.HexColor('#444444'), spaceAfter=9),
    'head': ParagraphStyle('head', fontName='DV-Bold', fontSize=10, leading=12, spaceBefore=7, spaceAfter=3),
    'body': ParagraphStyle('body', fontName='DV', fontSize=9, leading=12.2, spaceAfter=5),
    'formula': ParagraphStyle('formula', fontName='DV', fontSize=9.3, leading=13, spaceAfter=5, leftIndent=9),
    'sources': ParagraphStyle('sources', fontName='DV', fontSize=7.2, leading=9.5, spaceBefore=4),
}

def text_markup(s):
    result=[]
    offset=0
    for m in re.finditer(r'\[([^\]]+)\]\((https://[^)]+)\)', s):
        result.append(escape(s[offset:m.start()]))
        result.append(f'<link href="{escape(m.group(2))}" color="#244c70">{escape(m.group(1))}</link>')
        offset=m.end()
    result.append(escape(s[offset:]))
    return ''.join(result).replace('•', ' | ').replace('c_s', 'c<sub>s</sub>')

story=[]
blocks=ROOT.joinpath('SIGNIFICANCE_BRIEF.md').read_text().strip().split('\n\n')
for i, block in enumerate(blocks):
    block=block.replace('\n',' ')
    if block.startswith('# '):
        style='title'; block=block[2:]
    elif block.startswith('## '):
        style='head'; block=block[3:]
    elif block.startswith('Private significance'):
        style='meta'
    elif block.startswith('Sources:'):
        style='sources'
    elif block.startswith(('J(y;','v_p(')):
        style='formula'
    else:
        style='body'
    markup=text_markup(block)
    if style=='formula':
        markup=markup.replace('He_(A+1)', 'He<sub>A+1</sub>').replace('He_(A−1)', 'He<sub>A−1</sub>')
        markup=markup.replace('v_p(c_(sp))', 'v<sub>p</sub>(c<sub>sp</sub>)')
    story.append(Paragraph(markup,styles[style]))

class FixedCanvas(canvas.Canvas):
    def __init__(self,*args,**kwargs):
        kwargs['invariant']=1
        super().__init__(*args,**kwargs)
        self.setTitle('Local ordinary discriminants of Rogers Szego polynomials')
        self.setSubject('Private significance brief with bounded publication assessment')

doc=SimpleDocTemplate(str(ROOT/'SIGNIFICANCE_BRIEF.pdf'), pagesize=(612,792),
    leftMargin=48,rightMargin=48,topMargin=40,bottomMargin=38,
    title='Local ordinary discriminants of Rogers Szego polynomials')
doc.build(story,canvasmaker=FixedCanvas)
print('Rendered SIGNIFICANCE_BRIEF.pdf')
