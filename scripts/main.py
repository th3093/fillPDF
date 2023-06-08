'''
main routine
'''

from scripts import read_xlsx, pdf_handler
import os

# Datendateien
urex_daten = '../data/urex.xlsx'
wnd_daten = '../data/wnd.xlsx'

group_dict = {1: 'UG',
              2: 'Hesedenz',
              3: 'Brendel',
              4: 'Potempa',
              5: 'Mittermüller',
              6: 'Lenz-Braun',
              7: 'Lorenz, Udo',
              8: 'Ließfeld',
              9: 'Königer',
              10: 'Gessner',
              11: 'Weisgerber',
              12: 'Klein',
              13: 'Lorenz, Dieter',
              14: 'Kirsch',
              15: 'Brill',
              16: 'Magold',
              17: 'Römer',
              18: 'Maurer',
              19: 'Theis',
              20: 'Mörsdorf'}

# PDF - spezifisches
tmp_path = '../files/pdf_tmp/'
template_path = '../data/template.pdf'
blank_path = '../data/blank.pdf'
output_path = '../files/pdf_final/'
# 1 als platzhalter; wird später durch datum ersetzt
output_file_urex = '../files/pdf_final/final_urex-1.pdf'
output_file_wnd = '../files/pdf_final/final_wnd-1.pdf'

datums = []


# function for handling commmand shell output
# input:    msg as str
def bash_ui(msg):
    os.system('cls')
    print(msg)


def generate_blank_pages(index, filelist, group, pdf):
    while index % 4 != 0:
        filelist.append(pdf.blank_page_append(group, index))
        # tmp_files.append(pdf.divider_page('', group, index)) alternative //
        index += 1
    return [index, filelist]


def urex(out_fn, tmp_p, template_p, blank_p):
    # Urex - Data
    data = read_xlsx.read_and_preprocess(urex_daten, 'u')

    for datum in datums[12:29]:

        tmp_files = []
        output_fn = out_fn.split('-')[0] + f"-{datum.replace('.', '-')}.pdf"
        pdf = pdf_handler.ProcessPdf(tmp_p, output_fn, template_p, blank_p)

        for group in data:
            index = 0
            tmp_files.append(pdf.divider_page(f"{group} :   {group_dict[group]}", group, index))
            index += 1

            for row in range(len(data[group])):
                data[group][row]['date_time'] = datum
                tmp_files.append(pdf.add_data_to_pdf(data[group][row], index, group))
                index += 1
                bash_ui(f"\nStep:  {row+1} / {len(data[group])}  -----  {((row+1) / len(data[group]) * 100):.2f} %\n\n")

            '''# generating blank filler pages
            while index % 4 != 0:
                tmp_files.append(pdf.blank_page_append(group, index))
                #tmp_files.append(pdf.divider_page('', group, index)) alternative //
                index += 1'''
            # für blank pages am ende der gruppe ( 4x A6 auf A4)
            #index, tmp_files = generate_blank_pages(index, tmp_files, group, pdf)

            bash_ui(f"\nFinished Groups:  {group} / {len(data)}  -----  {(group / len(data) * 100):.2f} %\n\n")

        print('Waiting on merge...')
        pdf_handler.merge_files(tmp_files, output_fn)
        bash_ui(f"\nFinal PDFs finished:   {int(datum[:2])} / {len(datums)}  -----  {(int(datum[:2]) / len(datums)*100):.2f} %\n\n")


def wen(out_fn, tmp_p, template_p):
    #wen - data
    data = read_xlsx.read_and_preprocess(wnd_daten, 'w')

    for datum in datums[12:29]:
        tmp_files = []
        output_fn = out_fn.split('-')[0] + f"-{datum.replace('.', '-')}.pdf"
        pdf = pdf_handler.ProcessPdf(tmp_p, output_fn, template_p, '')

        index = 0

        for row in range(len(data)):
            data[row]['date_time'] = datum
            tmp_files.append(pdf.add_data_to_pdf(data[row], index, group_no=0))
            index += 1
            bash_ui(f"\nStep:  {row+1} / {len(data)}  -----  {((row+1)/len(data)*100):.2f} %\n\n")

        print('Waiting on merge...')
        pdf_handler.merge_files(tmp_files, output_fn)
        bash_ui(f"\nFinal PDFs finished:   {int(datum[:2])} / {len(datums)}  -----  {(int(datum[:2]) / len(datums)*100):.2f} %\n\n")


def del_temp_fp():
    # check for deleting of tmp-files
    # only for debugging with choice. later on deleting without asking when function is called
    while True:
        choice = input('delete tmp files? [y] , [n]  ')
        if choice == 'y':
            for f in os.listdir(tmp_path):
                if not f.endswith(".pdf"):
                    continue
                os.remove(os.path.join(tmp_path, f))
            print('tmp-files deleted. Bye!')
            break
        elif choice == 'n':
            print('good bye')
            break


def get_datum():
    # Einzusetzendes Datum
    month = input('monat eingeben (01-12):  ')
    for i in range(1, 32):
        if i < 10:
            datums.append(f"0{i}.{month}.2022")
        else:
            datums.append(f"{i}.{month}.2022")


def run():
    get_datum()
    bash_ui('\nStarting set 1 ----\n\n')
    urex(output_file_urex, tmp_path, template_path, blank_path)
    bash_ui('\nStarting set 2 ----\n\n')
    wen(output_file_wnd, tmp_path, template_path)
    # Clean up
    del_temp_fp()


if __name__ == '__main__':
    run()
    #get_datum()
    #wen(output_file_wnd, tmp_path, template_path)
    #urex(output_file_urex, tmp_path, template_path, blank_path)