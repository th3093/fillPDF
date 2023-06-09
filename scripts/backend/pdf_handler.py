import re
import os
import pdfrw


form_keys = {
    "name": "string",
    "birth": "string",
    "address": "string",
    "date_time": "string"
}


class ProcessPdf:

    def __init__(self, temp_directory, output_file, template_path,
                 blank_path, blank_filling_flag, sort_by, filling_quotient):

        self.temp_directory = temp_directory
        self.output_file = output_file
        self.template_path = template_path
        self.blank_path = blank_path
        self.blank_filling_flag = blank_filling_flag
        self.sort_by = sort_by
        self.filling_quotient = filling_quotient

        print('\n##########| Initiating Pdf Creation Process |#########\n')
        print('\nDirectory for storing all temporary files is: ', temp_directory)
        print("Final Pdf name will be: ", output_file)

    def add_data_to_pdf(self, data, index, group_no=0):

        template = pdfrw.PdfReader(self.template_path)

        for page in template.pages:
            annotations = page['/Annots']
            if annotations is None:
                continue

            for annotation in annotations:
                if annotation['/Subtype'] == '/Widget':
                    if annotation['/T']:
                        key = annotation['/T'][1:-1]
                        if re.search(r'.-[0-9]+', key):
                            key = key[:-2]

                        if key in data:
                            annotation.update(
                                pdfrw.PdfDict(V=self.encode_pdf_string(data[key], form_keys[key]), Ff=1)
                            )
                            annotation.update(pdfrw.PdfDict(T=key+str(group_no*1000+index), Ff=1))
                        annotation.update(pdfrw.PdfDict(Ff=1))

        template.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
        out_string = f"{self.temp_directory}tmp{int(group_no)*1000+index}.pdf"
        pdfrw.PdfWriter().write(out_string, template)

        return out_string

    def encode_pdf_string(self, value, value_type):
        if value_type == 'string':
            if value:
                return pdfrw.objects.pdfstring.PdfString.encode(value)
            else:
                return pdfrw.objects.pdfstring.PdfString.encode('')
        return ''

    def divider_page(self, title, group_no, index):
        return self.add_data_to_pdf({'name': title}, index, group_no)

    def blank_page_append(self, group_no, index):
        out_str = f"{self.temp_directory}tmp{int(group_no)*1000+index}.pdf"
        pdfrw.PdfWriter().write(out_str, pdfrw.PdfReader(self.blank_path))
        return out_str


def merge_files(input_fpaths, output_fn):
    writer = pdfrw.PdfWriter()
    r = pdfrw.PdfReader(input_fpaths[0])
    writer.addpages(r.pages)
    acro_form = r.Root.AcroForm

    for file in input_fpaths[1:]:
        writer.addpages(pdfrw.PdfReader(file).pages)

    writer.trailer.Root.AcroForm = acro_form
    writer.write(output_fn)


if __name__ == '__main__':
    '''
    data = [{'name': "Anonymous Participant", 'birth': "01.01.1999", 'address': "Langenamestraße 1, 12345 Musterstadt", 'date_time': "01.01.2022, 11:00"},
            {'name': "c d", 'birth': "11.01.1999", 'address': "straße 1, 12345 musterstadt", 'date_time': "01.01.2022, 11:00"},
            {'name': "e f", 'birth': "21.01.1999", 'address': "straße 1, 12345 musterstadt", 'date_time': "01.01.2022, 11:00"}]

    temp_files = []

    for row in range(len(data)):
        output_file = f'pdf_final/final_pdf{row}.pdf'
        pdf_template_path = '../data/template.pdf'
        pdf = ProcessPdf('pdf_tmp/', output_file, pdf_template_path)
        data_pdf = pdf.add_data_to_pdf(data[row])
        temp_files.append(data_pdf)

    '''
    x = pdfrw.PdfReader('../data/template.pdf')
    print(x)
    print(x.pages[0]['/Annots'])
