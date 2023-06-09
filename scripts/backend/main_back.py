'''
main routine
'''

from scripts.backend import pdf_handler, read_xlsx
import os


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

dates = []


# function for handling cmd output
# input:    msg as str
def bash_ui(msg):
    os.system('clear')
    print(msg)


# handles process of filling PDFs
# Input:    inp_fn as path of input xlsx
#           out_path as folder path of final PDFs
#           tmp_p as folder path of temporary PDFs
#           template_p as path of template PDF to fill
#           blank_p as path of blank PDF as divider
#           bf_flag as bool blank_filling_flag -> should pages be filled by blank pages,
#           sb as sort_by as list of sorting specifiers, i.e. columns,
#           fq as int filling_quotient -> if bf_flag=true, fq is number of PDFs per page
#           dp_flag as bool div_page_flag for divider pages/PDFs with title description
#           gp_flag as bool grouping_flag for deciding to group after specified columns or not
def filler(
        inp_fn,
        out_path,
        tmp_p,
        template_p,
        blank_p,
        bf_flag,
        sb,
        fq,
        dp_flag,
        gp_flag):
    # start preprocessing
    data = read_xlsx.read_and_preprocess(inp_fn, sb, gp_flag)
    # date loop
    for date in dates:
        tmp_files = []
        output_fn = out_path + f"/final-{date.replace('.', '-')}.pdf"
        pdf = pdf_handler.ProcessPdf(tmp_p, output_fn, template_p, blank_p, bf_flag, sb, fq)

        for act_group_id in data:
            index = 0
            if dp_flag:
                tmp_files.append(pdf.divider_page(f"{sb[0]} :   {group_dict[act_group_id]}", act_group_id, index))
                index += 1

            for row in range(len(data[act_group_id])):
                data[act_group_id][row]['date_time'] = date
                tmp_files.append(pdf.add_data_to_pdf(data[act_group_id][row], index, act_group_id))
                index += 1

            # generating blank filler pages
            if bf_flag:
                while index % fq != 0:
                    tmp_files.append(pdf.blank_page_append(act_group_id, index))
                    index += 1
            bash_ui(f"\nFinished {act_group_id}:  {act_group_id} / {len(data)}" +
                    f"-----  {(act_group_id / len(data) * 100):.2f} %\n\n")

        print('Waiting on merge...')
        pdf_handler.merge_files(tmp_files, output_fn)
        bash_ui(f"\nFinal PDFs finished:   {(int(date[:2])+1)-int(dates[0][:2])} / {len(dates)}" +
                f"-----  {(((int(date[:2])+1) - int(dates[0][:2])) / len(dates) * 100):.2f} %\n\n")


# Tidy up after merge; deleting temporary files
def del_temp_fp():
    # check for deleting of tmp-files
    for f in os.listdir(tmp_path):
        if not f.endswith(".pdf"):
            continue
        os.remove(os.path.join(tmp_path, f))
    print('tmp-files deleted. Bye!')


# get dates to paste into PDF 'date' Form-Field + for creating PDF per day
def get_date(month_, start_, end_):
    for i in range(start_, end_+1):
        if i < 10:
            dates.append(f"0{i}.{month_}.2023")
        else:
            dates.append(f"{i}.{month_}.2023")


# main starting point of scripts
def run(inp_fp,
        out_path,
        month,
        del_tmp_flag,
        blank_filling_flag,
        sort_by_raw,
        div_page_flag,
        grouping_flag,
        filling_quotient=1,
        start_day=1,
        end_day=31):

    get_date(month, int(start_day), int(end_day))
    if sort_by_raw != "":
        sort_by_raw = sort_by_raw.replace(" ", "").split(",")
        bash_ui('\nStarting with sorted data ----\n\n')

    else:
        bash_ui('\nStarting with unsorted data ----\n\n')
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
    dates.clear()
    if del_tmp_flag:
        del_temp_fp()


if __name__ == '__main__':
    pass
