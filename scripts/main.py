'''
main routine
'''

from scripts import read_xlsx, pdf_handler
import os
import sys


group_dict = {
    1: 'Group1',
    2: 'Group2',
    3: 'Group3',
    4: 'Group4',
    5: 'Group5',
    6: 'Group6'
}

# PDF specific paths
tmp_path = '../files/pdf_tmp/'
template_path = '../data/template.pdf'
blank_path = '../data/blank.pdf'
# 1 as placeholder for date
output_file_with_group_selector = '../files/pdf_final/final_group-1.pdf'
output_file_without_group_selector = '../files/pdf_final/final_not_group-1.pdf'

datums = []


# function for handling cmd output
# input:    msg as str
def bash_ui(msg):
    os.system('cls')
    print(msg)


# handles process of filling PDFs with group selector active
# Input:    inp_fn as path of input xlsx
#           out_fn as folder path of final PDFs
#           tmp_p as folder path of temporary PDFs
#           template_p as path of template PDF to fill
#           blank_p as path of blank PDF as divider
def with_group_selector(inp_fn, out_fn, tmp_p, template_p, blank_p):

    data = read_xlsx.read_and_preprocess(inp_fn, 'input_data1')

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

            bash_ui(f"\nFinished Groups:  {group} / {len(data)}  -----  {(group / len(data) * 100):.2f} %\n\n")

        print('Waiting on merge...')
        pdf_handler.merge_files(tmp_files, output_fn)
        bash_ui(f"\nFinal PDFs finished:   {int(datum[:2])} / {len(datums)}  -----  {(int(datum[:2]) / len(datums)*100):.2f} %\n\n")


# handles process of filling PDFs without group selector active
# Input:    inp_fn as path of input xlsx
#           out_fn as folder path of final PDFs
#           tmp_p as folder path of temporary PDFs
#           template_p as path of template PDF to fill
def without_group_selector(inp_fn, out_fn, tmp_p, template_p):

    data = read_xlsx.read_and_preprocess(inp_fn, 'input_data2')

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


# Tidy up after merge, press 'n' to keep the individual PDFs
# or 'y' to delete all temporary files
def del_temp_fp():
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


# get dates to paste into PDF 'date' Form-Field
def get_date():
    month = input('Choose Month (01-12):  ')
    year = input('Choose year:   ')
    for i in range(1, 32):
        if i < 10:
            datums.append(f"0{i}.{month}.{year}")
        else:
            datums.append(f"{i}.{month}.{year}")


# main starting point of scripts
def run(_paths):
    get_date()
    bash_ui('\nStarting set 1 ----\n\n')
    with_group_selector(paths[1], output_file_with_group_selector, tmp_path, template_path, blank_path)
    bash_ui('\nStarting set 2 ----\n\n')
    without_group_selector(paths[2], output_file_without_group_selector, tmp_path, template_path)
    # Clean up
    del_temp_fp()


# run python main.py path_to_first_file path_to_second_file
if __name__ == '__main__':
    paths = sys.argv[:2]
    run(paths)
