from pprint import pprint
import csv
import json

'''

number * price -> price
price - (price*discount_percentage) -> total_price
SUM(total_price) -> order_score


json = {
    'order_number': '',
    'order_score' : '',
    'order_date': ''

    'tables': {
        'table_1': [
            {
                'name': '',
                'number':'',
                'units': '',
                'price': '',
                'discount_percentage': '',
                'total_price': ''
            },
            {
                'name': '',
                'number':'',
                'units': '',
                'price': '',
                'discount_percentage': '',
                'total_price': ''
            }
            ...
        ]
    },

    'customer': {
        'address': '',
        'name': '',
        'registration':
    },
    'payer': {
        'address': '',
        'name': '',
        'registration':
    },
    'owner': {
        'address': '',
        'name': '',
        'registration':
    },
    'executor':{
        'address': '',
        'name': '',
        'registration':
    },
    'vehicle': {
        'number': '',
        'name': '',
        'vin': ''
    }
}

'''


def file_to_list(file):
    lines = []
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            lines.append(line.lower().replace(u'\xa0', u' '))
    return lines


def delete_empty_strings(file):
    lines = file_to_list(file)
    with open(file, 'w', encoding='utf-8') as f:
        for line in lines:
            if line.strip():
                f.write(line)


def parse_tables(dataframe_csv, headers):
    temp_table_dict = {}
    in_table = False
    rows = []
    i = 0

    with open(dataframe_csv, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)

    for index, row in enumerate(rows):
        temp_row = {}
        # first table
        if row[0] == 'No' and rows[index+1][0] == '1' and not in_table:
            in_table = True
        # next table
        elif row[0] == 'No' and rows[index+1][0] == '1' and in_table:
            i += 1
        # save data from table
        elif in_table:
            # check trash row between table(s)
            if row[0].isdigit() and len(row) >= len(headers) :
                for key, value in headers.items():
                    temp_row[key] = row[value-1]

                table_name = 'table_{}'.format(i)

                if table_name in temp_table_dict:
                    temp_table_dict[table_name].append(temp_row)
                else:
                    temp_table_dict[table_name] = []
                    temp_table_dict[table_name].append(temp_row)

    return temp_table_dict


def parse_text_marka(text, key_words):
    temp_dict = {}

    delete_empty_strings(text)

    lines = file_to_list(text)

    for word in key_words:
        for index, line in enumerate(lines):
            if word in line:

                if word == 'заказчик':
                    name = lines[index + 1]
                    address = lines[index + 2] + ' ' + lines[index + 3]
                    temp_dict['customer'] = {
                        'address': address,
                        'name': name
                    }
                    break

                elif word == 'исполнитель':
                    temp = line.split(sep=' ')
                    name = ' '.join(temp[1:])
                    address = lines[index + 1]
                    temp_dict['executor'] = {
                        'address': address,
                        'name': name
                    }
                    break

                elif word == 'плательщик':
                    name = lines[index + 1]
                    address = lines[index + 2] + ' ' + lines[index + 3]
                    temp_dict['payer'] = {
                        'address': address,
                        'name': name
                    }
                    break

                elif word == 'дата открытия':
                    temp = line.split(sep=' ')
                    order_date = ' '.join(temp[3:])
                    temp_dict['order_date'] = order_date
                    break

                elif word == 'заказ-наряд':
                    temp = line.split(sep=' ')
                    order_number = ' '.join(temp[2:])
                    temp_dict['order_number'] = order_number
                    break

                elif word == 'vin':
                    vin = lines[index + 1]
                    temp_dict['vehicle'] = {
                        'vin': vin
                    }
                    break

    return temp_dict


def parse_text_mega(text, key_words):
    temp_dict = {}

    delete_empty_strings(text)

    lines = file_to_list(text)

    for word in key_words:
        for index, line in enumerate(lines):
            if word in line:

                if word == 'поставщик':
                    temp = line.split(sep=' ')
                    name = ' '.join(temp[1:])
                    address = lines[index + 1]
                    temp_dict['executor'] = {
                        'name': name,
                        'address': address
                    }
                    break

                elif word == 'заказ-наряд':
                    temp = line.split(sep=' ')
                    order_number = temp[4]
                    order_date = temp[6:]
                    temp_dict['order_number'] = order_number
                    temp_dict['order_date'] = order_date
                    break

                elif word == 'заказчик':
                    temp = line.split(sep=' ')
                    name = ' '.join(temp[1:])
                    address = lines[index + 1] + ' ' + lines[index + 2]
                    temp_dict['customer'] = {
                        'name': name,
                        'address': address
                    }
                    break

                elif word == 'автомобиль':
                    temp = line.split(sep=' ')
                    i = temp.index('vin:')
                    vin = temp[i + 1]
                    temp_dict['vehicle'] = {
                        'vin': vin
                    }
                    break

    return temp_dict


def parse_text_voronezh(text, key_words):
    temp_dict = {}

    delete_empty_strings(text)

    lines = file_to_list(text)

    for word in key_words:
        for index, line in enumerate(lines):
            if word in line:

                if word == 'заказчик':
                    temp = line.split(sep=' ')
                    name = ' '.join(temp[1:])
                    address = lines[index + 1]
                    temp = address.split(sep=' ')
                    if len(temp) > 2:
                        address = ' '.join(temp[2:])
                    temp_dict['customer'] = {
                        'name': name,
                        'address': address
                    }
                    break

                elif word == 'плательщик':
                    temp = line.split(sep=' ')
                    name = ' '.join(temp[1:])
                    temp_dict['payer'] = {
                        'name': name
                    }
                    break

                elif word == 'автомобиль':
                    temp = line.split(sep=' ')
                    i = temp.index('vin:')
                    vin = temp[i + 1]
                    temp_dict['vehicle'] = {
                        'vin': vin
                    }
                    break

                elif word == 'поставщик':
                    temp = line.split(sep=' ')
                    name = ' '.join(temp[1:])
                    address = lines[index + 1]
                    temp = address.split(sep=' ')
                    temp_dict['executor'] = {
                        'name': name,
                        'address': address
                    }
                    break

                elif word == 'заказ-наряд':
                    temp = line.split(sep=' ')
                    order_number = temp[2]
                    order_date = temp[4]
                    temp_dict['order_number'] = order_number
                    temp_dict['order_date'] = order_date
                    break
    return temp_dict


def init(text, dataframe_csv):
    cmp_name = None
    lines = file_to_list(text)


    for company in company_templates.keys():
        for line in lines:
            if company in line:
                cmp_name = company

    if cmp_name is None:
        raise ValueError('Template for this company does not exist. File {}'.format(text))

    temp_dict = {cmp_name: {}}

    temp_dict[cmp_name].update(company_templates[cmp_name]['handler'](text, company_templates[cmp_name]['key_words']))
    temp_dict[cmp_name]['tables'] = parse_tables(dataframe_csv, company_templates[cmp_name]['headers'])

    return temp_dict


company_templates = {
    'воронежтрансбизнес': {
        'handler': parse_text_voronezh,
        'headers': {
            'name': 3,
            'number': 5,
            'units': 6,
            'price': 7,
            'discount': 9,
            'total_price': 10
        },
        'key_words': [
            'заказчик',
            'плательщик',
            'автомобиль',
            'поставщик',
            'заказ-наряд'
        ]
    },
    # 'лидер-авто': {
    #     'headers': {
    #         'name': 3,
    #         'number': 4,
    #         'price': 6,
    #         'total_price': 7
    #     },
    #     'key_words': [
    #         'заказчик',
    #         'исполнитель',
    #         'автомобиль',
    #         'дата открытия',
    #         'vin',
    #         'поставщик',
    #         'плательщик',
    #         'заказ-наряд'
    #     ]
    # },
    'марка': {
        'handler': parse_text_marka,
        'headers': {
            'name': 3,
            'number': 4,
            # 'units': None,
            'price': 5,
            'discount': 7,
            'total_price': 8
        },
        'key_words': [
            'дата открытия',
            'заказчик',
            'плательщик',
            'исполнитель',
            'гос. номер',
            'vin',
            'поставщик',
            'адрес:',
            'заказ-наряд'
        ]
    },
    'мегаальянс': {
        'handler': parse_text_mega,
        'headers': {
            'name': 3,
            'number': 5,
            'units': 6,
            'price': 4,
            'total_price': 7
        },
        'key_words': [
            'заказчик',
            'автомобиль',
            'поставщик',
            'заказ-наряд'
        ]
    },
}


if __name__ == '__main__':
    file_list = [
        5765306,
        5762990,
        5763094,
        5718014,
        5792349,
        5800355,
        5809614,
        5813063,
        5816194,
        5783203,
        5797599,
        5815462
    ]

    for file in file_list:
        txt_path = r'./temp/{}.txt'.format(file)
        csv_path = r'./temp/{}.csv'.format(file)

        data = init(txt_path, csv_path)
        pprint(data)

        with open(r'./out/{}.json'.format(file), 'w', encoding='utf-8') as f:
            json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)

    #pprint(parse_tables(csv_path, company_templates['марка']['headers']))
