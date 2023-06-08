import re
import os
import pdfrw

# keys / ids of form fields in PDF-File
form_keys = {
    "name": "string",
    "birth": "string",
    "address": "string",
    "date_time": "string"
}


class ProcessPdf:
    # init file locations
    def __init__(self, temp_directory, output_file, template_path, blank_path):
        self.temp_directory = temp_directory
        self.output_file = output_file
        self.template_path = template_path
        self.blank_path = blank_path
        print('\n##########| Initiating Pdf Creation Process |#########\n')
        print('\nDirectory for storing all temporary files is: ', temp_directory)
        print("Final Pdf name will be: ", output_file)

    # Add data to single tmp PDF
    # Input:    data as dict of single entry (i.e. row of xlsx data)
    #           index as incrementing index of tmp file
    #           group_no as number of "group"
    # Output:   out_string as string filename of temporary PDF-file
    def add_data_to_pdf(self, data, index, group_no):
        # read template pdf
        template = pdfrw.PdfReader(self.template_path)

        for page in template.pages:
            # get form fields
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
                            annotation.update(pdfrw.PdfDict(T=key+str(group_no*1000+index), Ff=1, ))
                        annotation.update(pdfrw.PdfDict(Ff=1))
        # finalize PDF-Object
        template.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
        out_string = f"{self.temp_directory}tmp{int(group_no)*1000+index}.pdf"
        # write PDF-Object to temporary PDF-File
        pdfrw.PdfWriter().write(out_string, template)
        return out_string

    # encodes value to pdfString
    def encode_pdf_string(self, value, value_type):
        if value_type == 'string':
            if value:
                return pdfrw.objects.pdfstring.PdfString.encode(value)
            else:
                return pdfrw.objects.pdfstring.PdfString.encode('')
        return ''

    # places divider page
    # Input:    title as title to print into 'name' form field
    #           index as index of temporary PDF-File
    #           group_no as group number to divide (you can see it as a title page for e.g. a chapter)
    def divider_page(self, title, group_no, index):
        return self.add_data_to_pdf({'name': title}, index, group_no)


# Merge all temporary PDF-Files to a single multipage file for e.g. printing
# Input:    input_fpaths as list of all temporary files
#           output_fn as filename of final PDF
def merge_files(input_fpaths, output_fn):
    # init writer object
    writer = pdfrw.PdfWriter()
    # get first tmp pdf
    r = pdfrw.PdfReader(input_fpaths[0])
    # create file
    writer.addpages(r.pages)
    acro_form = r.Root.AcroForm
    # add other tmp-files as pages
    for file in input_fpaths[1:]:
        writer.addpages(pdfrw.PdfReader(file).pages)
    # safe final PDF
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
