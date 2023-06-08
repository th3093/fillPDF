import pandas as pd


# dict to define columns to select per dataset; need to be exactly as written in excel!
sort_by_dict = {'input_data2': ['lastName'],
                'input_data1': ['group', 'lastName']}


# Read data from xlsx file and return json like object
# Input:    database as path to xlsx file
#           deco as decorator for selecting columns of the given dataset
# Output:   List of Array of all rows in xlsx with selected columns
def read_and_preprocess(database, deco):
    # read xlsx file
    data_init = pd.read_excel(database)
    # sort by choosen columns
    df = data_init.sort_values(by=sort_by_dict[deco])
    # drop unneccessary columns
    df.drop(['e-mail', 'phoneNumber'], inplace=True, axis=1)
    # resort data
    df = df.reset_index(drop=True)
    # create dict from data by columns as key
    data = df.to_dict(orient='index')

    # case: sorting all entries inside selector "group"
    if deco == 'input_data1':
        final_data = {}

        for entry in data:
            # check if first member of "group"; can be changed to any other
            # scheme: data[entry]['exactColumnName']
            try:
                final_data[data[entry]['group']].append({
                    'name': f"{data[entry]['firstName']} {data[entry]['lastName']}",
                    'birth': data[entry]['birthDate'],
                    'address': f"{data[entry]['street']} {data[entry]['number']}, {data[entry]['postalCode']} {data[entry]['city']}",
                    'date_time': ""
                })
            # if first occurrence
            except (KeyError, TypeError):
                final_data[data[entry]['Group']] = [{
                    'name': f"{data[entry]['firstName']} {data[entry]['lastName']}",
                    'birth': data[entry]['birthDate'],
                    'address': f"{data[entry]['street']} {data[entry]['number']}, {data[entry]['postalCode']} {data[entry]['city']}",
                    'date_time': ""
                }]
    # case: no sorting inside a special column
    elif deco == 'input_data2':
        final_data = []
        for entry in data:
            final_data.append({
                'name': f"{data[entry]['firstName']} {data[entry]['lastName']}",
                'birth': data[entry]['birthDate'],
                'address': f"{data[entry]['street']} {data[entry]['number']}, {data[entry]['postalCode']} {data[entry]['city']}",
                'date_time': ""
            })

    return final_data


if __name__ == '__main__':
    print(read_and_preprocess('your_data1.xlsx', 'input_data1'))
    print(read_and_preprocess('your_data2.xlsx', 'input_data2'))
