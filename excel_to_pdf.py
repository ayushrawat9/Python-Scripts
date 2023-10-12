from fpdf import FPDF
from textwrap import wrap
import pandas as pd
from pyparsing import col, line

TABLE_COL_NAMES = ['COL1', 'COL2','COL3','COL2', 'COL4']

class Tables(FPDF):
    # def __init__(self):
    #     self.col_width = 0
    #     self.max_lines_per_row = []
    #     self.th = 0

    def nblines(self,width, txt):
        cw = self.current_font['cw']

        if(width == 0):
            width = self.line_width - self.r_margin - self.get_x()
        wmax = (width - 2*self.c_margin) *1000/self.font_size
        s = txt.replace('\r','')
        nb = len(s)
        if(nb > 0 and s[nb-1]=='\n'):
            nb = nb - 1
        sep =-1
        i = 0
        j=0
        l=0
        nl=1
        while(i<nb):
            c = s[i]
            if(c=='\n'):
                i=i+1
                sep =sep-1
                j=il=0
                nl=nl+1
                continue
            if(c==' '):
                sep=i
            l = l +cw[c]
            if(l > wmax):
                if(sep == -1):
                    if(i==j):
                        i=i+1
                else:
                    i = sep+1
                sep = sep-1
                j=i
                l=0 
                nl = nl+1
            else:
                i = i+1
        return nl

    def add_newlines(self,col_width,data):
        max_lines_per_row = []
        for row in data:
            max_lines = 1
            for datum in row:
                lines = self.nblines(col_width,str(datum))
                if max_lines < lines:
                    max_lines = lines
            max_lines_per_row.append(max_lines)
        self.max_lines_per_row = max_lines_per_row
        new_data = []
        for e,row in enumerate(data):
            temp = []
            for datum in row:
                lines = self.nblines(col_width,str(datum))
                temp.append(str(datum)+(max_lines_per_row[e]-lines+1)*'\n')
            new_data.append(temp)
        return new_data

    def render_table_header(self,line_height):
        self.set_font(style="B")  # enabling bold text
        # for col_name in TABLE_COL_NAMES:
        #     self.multi_cell(self.col_width, line_height, col_name, border=1)
        for e,col_name in enumerate(TABLE_COL_NAMES):
            if e==0:
                self.cell(self.col_width//2, 2*self.th, str(col_name), border=1, align='L', fill=1)
            else:
                self.cell(self.col_width, 2*self.th, str(col_name), border=1, align='L', fill=1)
        self.ln(line_height)
        self.set_font(style="")  # disabling bold text

    def table(self):
        self.add_page()
        self.set_font('Times', '', 10.0)
        epw = self.w - self.l_margin
        col_width = epw/5 + 1
        self.col_width = col_width
        data1 = pd.read_excel('tables/listing2.xlsx')
        df = pd.DataFrame(data1)
        s = df[df.columns[0]]
        v = df[df.columns[1]]
        c = df[df.columns[2]]
        d = df[df.columns[3]]
        e = df[df.columns[4]]
        data_retro = [s,v,c,d,e]
        data =[[row[i] for row in data_retro] for i in range(len(data_retro[0]))]
        data = self.add_newlines(col_width,data)
        # data = [[s[0], v[0], c[0], d[0],e[0]], [s[1], v[1], c[1], d[1], e[1]],  [s[2], v[2], c[2], d[2], e[2]],  [s[3], v[3], c[3], d[3], e[3]]]
        th = self.font_size
        self.th = th
        count = 0
        self.set_text_color(0, 0, 0)
        self.set_fill_color(255, 255, 255)
        self.set_margin(10)
        x = y = 0
        intial_x = self.get_x()
        intial_y = self.get_y()
        x = intial_x
        y = intial_y
        # self.set_auto_page_break(True)
        for e,datum in enumerate(df):
            self.set_fill_color(70, 130, 180)
            self.set_font('Times', '', 10)
            if e==0:
                self.cell(col_width//2, 2*th, str(datum), border=1, align='L', fill=1)
            else:
                self.cell(col_width, 2*th, str(datum), border=1, align='L', fill=1)
        x = intial_x
        y = y + 2*th
        to_page_2 = pdf.add_link()
        pdf.set_link(to_page_2, page=2)
        #
        self.set_xy(x,y)
        serial_num_width = col_width//2
        self.set_auto_page_break(False, margin = 0.0)

        with self.unbreakable() as doc:
            for rowno,row in enumerate(data):
                count += 1
                max_y = y
                for e,datum in enumerate(row):
                    doc.set_font('Times', '', 11)
                    if e==0: #serial number column
                        doc.multi_cell(col_width//2, 2*th, str(datum), border=1, align='L', fill=0,link = to_page_2)
                    else:
                        doc.multi_cell(col_width, 2*th, str(datum), border=1, align='L', fill=0,link = to_page_2)
                    if max_y < doc.get_y():
                        max_y = doc.get_y()
                    if e != len(row)-1:
                        if e==0: #serial number column
                            x = x+ col_width//2
                            doc.set_xy(x,y)
                        else:
                            x = x + col_width
                            doc.set_xy(x,y)
                    else:
                        doc.set_xy(intial_x, max_y-2*th)
                        x = intial_x
                        y = max_y-2*th
                print("break\n")
        print('page_break_triggered:', self.page_break_trigger)

pdf = Tables()
pdf.table()
pdf.add_page()
pdf.add_page()
pdf.output('output_pdf.pdf')
