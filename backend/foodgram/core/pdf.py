import os

from fpdf import FPDF

from foodgram.settings import BASE_DIR


class Constant:
    DT_CAPTION = 1
    DT_TEXT = 2
    DT_EMPTYLINE = 3
    DT_FOOTER = 4


class PDFMaker(FPDF):
    font_regular_name = 'DejaVuSansCondensed.ttf'
    font_regular_family = 'DejaVu'
    font_bold_family = 'DejaVuBold'
    font_bold_name = 'DejaVuSansCondensed-Bold.ttf'
    font_dir = 'static/fonts/'
    default_font_size = 12
    font_sizes = {
        Constant.DT_CAPTION: 14,
        Constant.DT_TEXT: 12,
        Constant.DT_FOOTER: 10
    }

    data: {}
    footer_text = ''

    line_height = 9  # in mm

    a4_height_mm = 297
    a4_width_mm = 210
    footer_padding = 15

    def __init__(self, orientation='P', unit='mm', format='A4', data=''):
        super().__init__(orientation=orientation, unit=unit, format=format)

        self.data = data

        self.__pdf_init()

    def set_footer_text(self, text):
        self.footer_text = text

    def footer(self):
        if self.footer_text:
            self.set_text_color(70, 70, 70)
            self.set_font(
                self.font_regular_family,
                size=self.__font_size(Constant.DT_FOOTER))
            self.set_y(-self.footer_padding)
            self.line(0, 0, 300, 0)
            self.cell(
                200, self.line_height, txt=self.footer_text, ln=1, align='C')

    def __pdf_init(self):
        font_regular = os.path.join(
            BASE_DIR, self.font_dir, self.font_regular_name)

        font_bold = os.path.join(
            BASE_DIR, self.font_dir, self.font_bold_name)

        self.set_auto_page_break(1)
        self.add_page()
        self.add_font(self.font_regular_family, '', font_regular, uni=True)
        self.add_font(self.font_bold_family, '', font_bold, uni=True)

    def __font_size(self, line_type):
        return self.font_sizes.get(line_type, self.default_font_size)

    def pdf_render(self):
        for line_type, line in self.data:
            self.set_text_color(40, 40, 40)

            if self.a4_height_mm - self.get_y() <= 2 * self.footer_padding:
                self.ln(self.a4_height_mm - self.get_y())

            if line_type == Constant.DT_CAPTION:
                self.set_font(
                    self.font_bold_family, size=self.__font_size(line_type),
                    style='U')
                self.cell(200, self.line_height, txt=line, ln=1, align='C')
            elif line_type == Constant.DT_TEXT:
                self.set_font(
                    self.font_regular_family, size=self.__font_size(line_type))
                self.cell(200, self.line_height, txt=line, ln=1, align='L')
            elif line_type == Constant.DT_EMPTYLINE:
                self.ln(self.line_height)

        self.close()

        return self.__pdf_output()

    def __pdf_output(self):
        return self.output(dest='S').encode('latin1')