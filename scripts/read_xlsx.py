import pandas as pd

sort_by_dict = {'w': ['Nachname'],
                'u': ['Gruppe', 'Nachname']}


def read_and_preprocess(database, deco):
    data_init = pd.read_excel(database)
    df = data_init.sort_values(by=sort_by_dict[deco])
    df.drop(['e-mail', 'QR-Code', 'Telefonnummer'], inplace=True, axis=1)
    df = df.reset_index(drop=True)

    data = df.to_dict(orient='index')

    if deco == 'u':
        final_data = {}

        for entry in data:
            try:
                final_data[data[entry]['Gruppe']].append({'name': f"{data[entry]['Vorname']} {data[entry]['Nachname']}",
                                                          'birth': data[entry]['Geburtsdatum'],
                                                          'address': f"{data[entry]['Straße']} {data[entry]['Hausnummer']}, {data[entry]['PLZ']} {data[entry]['Stadt']}",
                                                          'date_time': ""
                                                          })
            except (KeyError, TypeError):
                final_data[data[entry]['Gruppe']] = [{'name': f"{data[entry]['Vorname']} {data[entry]['Nachname']}",
                                                      'birth': data[entry]['Geburtsdatum'],
                                                      'address': f"{data[entry]['Straße']} {data[entry]['Hausnummer']}, {data[entry]['PLZ']} {data[entry]['Stadt']}",
                                                      'date_time': ""
                                                      }]
    elif deco == 'w':
        final_data = []
        for entry in data:
            final_data.append({'name': f"{data[entry]['Vorname']} {data[entry]['Nachname']}",
                                'birth': data[entry]['Geburtsdatum'],
                                'address': f"{data[entry]['Straße']} {data[entry]['Hausnummer']}, {data[entry]['PLZ']} {data[entry]['Stadt']}",
                                'date_time': ""
                                })

    return final_data


if __name__ == '__main__':
    # read_and_preprocess('../data/urexweiler.xlsx', 'u')
    print(read_and_preprocess('../data/wnd.xlsx', 'w'))
