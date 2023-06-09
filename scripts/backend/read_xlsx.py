import pandas as pd


# Rearrange data to list of dicts containing paste in ready strings for PDF Form
# Input:    data as dict of pd dataframe
#           deco as decorator for selecting columns of the given dataset
#           grouping_flag as bool to group for column and sort inside group
# Output:   List of Array of entries with paste in ready strings for PDF Form
def sort_data(data, deco, gp_flag):
    final_data = {}
    if deco and gp_flag:
        for entry in data.keys():
            # check if first member of deco
            try:
                final_data[data[entry][deco]].append({
                    'name': f"{data[entry]['firstName']} {data[entry]['lastName']}",
                    'birth': data[entry]['birthDate'],
                    'address': f"{data[entry]['street']} {data[entry]['number']}, " +
                               f"{data[entry]['postalCode']} {data[entry]['city']}",
                    'date_time': ""
                })
            # if first occurrence create entry list of dicts
            except (KeyError, TypeError):
                final_data[data[entry][deco]] = [{
                    'name': f"{data[entry]['firstName']} {data[entry]['lastName']}",
                    'birth': data[entry]['birthDate'],
                    'address': f"{data[entry]['street']} {data[entry]['number']}, " +
                               f"{data[entry]['postalCode']} {data[entry]['city']}",
                    'date_time': ""
                }]
    else:
        final_data[0] = []
        for entry in data:
            final_data[0].append({
                'name': f"{data[entry]['firstName']} {data[entry]['lastName']}",
                'birth': data[entry]['birthDate'],
                'address': f"{data[entry]['street']} {data[entry]['number']}, " +
                           f"{data[entry]['postalCode']} {data[entry]['city']}",
                'date_time': ""
            })
    return final_data


# Read data from xlsx file and return json like object
# Input:    database as path to xlsx file
#           sort_by_list as list of columns for selecting of the given dataset
#           grouping_flag as bool to group for column and sort inside group
# Output:   List of Array of all rows in xlsx with selected columns
def read_and_preprocess(database, sort_by_list, grouping_flag):
    # read xlsx file
    data_init = pd.read_excel(database)

    if sort_by_list:
        for el in sort_by_list:
            if el in data_init.columns:
                df = data_init.sort_values(by=sort_by_list)
                df = df.reset_index(drop=True)
                # create dict from data by columns as key
                data = df.to_dict(orient='index')
                # sort and create Form strings
                data_f = sort_data(data, sort_by_list[0], grouping_flag)
                return data_f
            else:
                print("Sort_Filter_not_appliable - name not found")
                break
    # run without filter ( just row wise)
    return data_init


if __name__ == '__main__':
    print(read_and_preprocess('your_data1.xlsx', 'input_data1'))
    print(read_and_preprocess('your_data2.xlsx', 'input_data2'))
