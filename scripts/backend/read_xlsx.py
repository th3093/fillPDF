import pandas as pd


def run_u_w(data, deco, gp_flag):
    final_data = {}
    if deco and gp_flag:
        for entry in data.keys():
            try:
                final_data[data[entry][deco]].append({
                    'name': f"{data[entry]['firstName']} {data[entry]['lastName']}",
                    'birth': data[entry]['birthDate'],
                    'address': f"{data[entry]['street']} {data[entry]['number']}, {data[entry]['postalCode']} {data[entry]['city']}",
                    'date_time': ""
                })
            except (KeyError, TypeError):
                final_data[data[entry][deco]] = [{
                    'name': f"{data[entry]['firstName']} {data[entry]['lastName']}",
                    'birth': data[entry]['birthDate'],
                    'address': f"{data[entry]['street']} {data[entry]['number']}, {data[entry]['postalCode']} {data[entry]['city']}",
                    'date_time': ""
                }]
    else:
        final_data[0] = []
        for entry in data:
            final_data[0].append({
                'name': f"{data[entry]['firstName']} {data[entry]['lastName']}",
                'birth': data[entry]['birthDate'],
                'address': f"{data[entry]['street']} {data[entry]['number']}, {data[entry]['postalCode']} {data[entry]['city']}",
                'date_time': ""
            })
    return final_data


def read_and_preprocess(database, sort_by_list, grouping_flag):
    data_init = pd.read_excel(database)

    if sort_by_list:
        for el in sort_by_list:
            if el in data_init.columns:
                df = data_init.sort_values(by=sort_by_list)
                df = df.reset_index(drop=True)
                data = df.to_dict(orient='index')
                data_f = run_u_w(data, sort_by_list[0], grouping_flag)
                return data_f
            else:
                print("Sort_Filter_not_appliable - name not found")
                break
    # run without filter ( just row wise)
    return data_init


if __name__ == '__main__':
    print(read_and_preprocess('your_data1.xlsx', 'input_data1'))
    print(read_and_preprocess('your_data2.xlsx', 'input_data2'))
