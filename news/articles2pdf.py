from fpdf import FPDF
import os

# articles to pdf 
class PDF(FPDF):
    topic = 'none'
    title = ''
    date = 'none'
    def header(self):
        # add topic_title and logo
        self.image(r'%s/WhatsApp-Bot/news/favic.png'% (os.getcwd()),4,5,25)
        self.set_text_color(0,0,0)
        self.set_font('helvetica','BI',15)
        self.cell(200,10,PDF.topic.encode('latin-1', 'ignore').decode('latin-1'),border=0,align='C')
        self.ln()
        # set font
        self.set_font('helvetica','B',14)
        doc_w = self.w
        length_title = self.get_string_width(self.title)+6
        self.set_x((doc_w-length_title)/2)
        self.set_draw_color(0,80,100)
        self.set_text_color(220,50,50)
        self.set_line_width(1)
        # set the title of the page
        self.cell(length_title,10,PDF.title.encode('latin-1', 'ignore').decode('latin-1'),border = False,ln=1,align='C')
        # break the line
        self.ln()
        self.set_font('times','I',12)
        self.set_text_color(0,128,128)
        self.cell(0,5,PDF.date.encode('latin-1', 'ignore').decode('latin-1'))
        self.ln()
    def footer(self):
        self.set_y(-10)
        self.set_text_color(128,128,0)
        self.set_font('helvetica','B',10)
        self.cell(0,10,f'{self.page_no()}',align='C')
    def chapter_body(self,text):
        for line in text.splitlines():
            line_ =line.strip()
            txt = line_.encode('latin-1', 'ignore').decode('latin-1')
            self.set_font('times','',11)
            self.multi_cell(0,5,txt)
            self.ln(h=0.7)
            self.set_font('times','I',12)
        self.cell(0,5,'End of'+' '+ self.title.encode('latin-1', 'ignore').decode('latin-1'))
    @classmethod
    def title_topic_date(cls,title,topic,date):
        PDF.title = title.encode('latin-1', 'ignore').decode('latin-1')
        PDF.topic = topic.encode('latin-1', 'ignore').decode('latin-1')
        PDF.date = date.encode('latin-1', 'ignore').decode('latin-1')