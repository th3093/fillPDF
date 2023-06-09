'''
main routine
'''

from scripts.backend import pdf_handler, read_xlsx
import os
from time import time


# Datendateien
urex_daten = '../data/filler.xlsx'
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
progress = 0.0


# function for handling commmand shell output
# input:    msg as str
def bash_ui(msg):
    os.system('clear')
    print(msg)


# filler(inp_fp,
#                     out_path,
#                     tmp_path,
#                     template_path,
#                     blank_path,
#                     blank_filling_flag,
#                     sort_by,
#                     filling_quotient,
#                     div_page_flag)
def filler(inp_fn, out_path, tmp_p, template_p, blank_p, bf_flag, sb, fq, dp_flag, gp_flag):

    # Urex - Data
    print(f"\nmain_back 66: {datums}\n")
    data = read_xlsx.read_and_preprocess(inp_fn, sb, gp_flag)

    for datum in datums:
        #progress = int(datum[:2]) / len(datums) * 100

        tmp_files = []
        output_fn = out_path + f"/final-{datum.replace('.', '-')}.pdf"
        pdf = pdf_handler.ProcessPdf(tmp_p, output_fn, template_p, blank_p, bf_flag, sb, fq)

        for act_group_id in data:
            index = 0
            if dp_flag:
                tmp_files.append(pdf.divider_page(f"{sb[0]} :   {group_dict[act_group_id]}", act_group_id, index))
                index += 1

            for row in range(len(data[act_group_id])):
                data[act_group_id][row]['date_time'] = datum
                tmp_files.append(pdf.add_data_to_pdf(data[act_group_id][row], index, act_group_id))
                index += 1
                # bash_ui(f"\nStep:  {row + 1} / {len(data[act_group_id])}  -----  {((row + 1) / len(data[act_group_id]) * 100):.2f} %\n\n")

            # generating blank filler pages
            if bf_flag:
                while index % fq != 0:
                    tmp_files.append(pdf.blank_page_append(act_group_id, index))
                    # tmp_files.append(pdf.divider_page('', act_group_id, index)) alternative //
                    index += 1
            bash_ui(f"\nFinished {act_group_id}:  {act_group_id} / {len(data)}  -----  {(act_group_id / len(data) * 100):.2f} %\n\n")

        print('Waiting on merge...')
        pdf_handler.merge_files(tmp_files, output_fn)
        bash_ui(f"\nFinal PDFs finished:   {(int(datum[:2])+1)-int(datums[0][:2])} / {len(datums)}  -----  {(((int(datum[:2])+1)-int(datums[0][:2])) / len(datums)*100):.2f} %\n\n")


def wen(out_fn, tmp_p, template_p):
    #wen - data
    data, tmp = read_xlsx.read_and_preprocess(wnd_daten, 'w')

    for datum in datums:
        progress = int(datum[:2]) / len(datums)*100

        tmp_files = []
        output_fn = out_fn.split('-')[0] + f"-{datum.replace('.', '-')}.pdf"
        pdf = pdf_handler.ProcessPdf(tmp_p, output_fn, template_p, '')

        index = 0

        for row in range(len(data)):
            data[row]['date_time'] = datum
            tmp_files.append(pdf.add_data_to_pdf(data[row], index))
            index += 1
            bash_ui(f"\nStep:  {row+1} / {len(data)}  -----  {((row+1)/len(data)*100):.2f} %\n\n")

        print('Waiting on merge...')
        pdf_handler.merge_files(tmp_files, output_fn)
        bash_ui(f"\nFinal PDFs finished:   {int(datum[:2]+1)-int(datums[0][:2])} / {len(datums)}  -----  {((int(datum[:2]+1)-int(datums[0][:2])) / len(datums)*100):.2f} %\n\n")


def del_temp_fp():
    # check for deleting of tmp-files
    for f in os.listdir(tmp_path):
        if not f.endswith(".pdf"):
            continue
        os.remove(os.path.join(tmp_path, f))
    print('tmp-files deleted. Bye!')


def get_datum(month_, start_, end_):
    for i in range(start_, end_+1):
        if i < 10:
            datums.append(f"0{i}.{month_}.2023")
        else:
            datums.append(f"{i}.{month_}.2023")


def run(inp_fp, out_path, month, del_tmp_flag, blank_filling_flag, sort_by_raw, div_page_flag, grouping_flag, filling_quotient=1, start_day=1, end_day=31):
    #timer start
    timer = time()

    print(f"\nmain_back 144: {start_day} - {end_day}\n")
    get_datum(month, int(start_day), int(end_day))
    if sort_by_raw != "":
        sort_by_raw = sort_by_raw.replace(" ", "").split(",")
        bash_ui('\nStarting with sorted data ----\n\n')

        #wen(output_file_wnd,
            #tmp_path,
            #template_path,
            #)
    else:
        bash_ui('\nStarting with unsorted data ----\n\n')
        #wen(output_file_wnd, tmp_path, template_path)
    print(f"\nmain_back 147: {[inp_fp, out_path, tmp_path, template_path, blank_path, blank_filling_flag, sort_by_raw, filling_quotient, div_page_flag]}\n")
    filler(inp_fp,
           out_path,
           tmp_path,
           template_path,
           blank_path,
           blank_filling_flag,
           sort_by_raw,
           filling_quotient,
           div_page_flag,
           grouping_flag)

    # Clean up
    datums.clear()
    if del_tmp_flag:
        del_temp_fp()

    #timer end
    print(time()-timer)

if __name__ == '__main__':
    run('07', False)
    #get_datum()
    #wen(output_file_wnd, tmp_path, template_path)
    #filler(output_file_urex, tmp_path, template_path, blank_path)