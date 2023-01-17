"""On page 30 there are 13 phones on selling and the rest are not on selling. These 13 phones have an
'offers' parameter and I can use it to sift out the rest, but I don't want to parse the giant json again.
There is no need to create a separate json file for storing a big json from API, I'll delete it at the end
of this project."""

import json
import csv

import requests

from globals import phones, all_count, dict_for_colors, dict_for_urls, dict_for_prices


def writing_json_to_file(html) -> None:
    with open('mobile_json.json', 'w') as file:
        json.dump(html, file, indent=4, ensure_ascii=False)


def filling_dict_for_colors(current_dict: dict):
    """This function was made for creating a dict which would be contained a phone model as a key and
    all colors of this phone as a value"""

    global dict_for_colors
    full_phone_name_without_color = current_dict['full_name'].partition(' (')[0]
    color = current_dict['full_name'].partition(' (')[2][:-1]

    if full_phone_name_without_color in dict_for_colors:
        dict_for_colors[full_phone_name_without_color].append(
            color if ')' not in color else dict_for_colors[full_phone_name_without_color][0]
        )
    else:
        dict_for_colors[full_phone_name_without_color] = [color, ]

    dict_for_colors[full_phone_name_without_color] = list(set(
        dict_for_colors[full_phone_name_without_color]
    ))


def fill_dict_for_url(current_dict: dict):
    global dict_for_urls
    real_name = current_dict['full_name'].partition(' (')[0]
    if real_name in dict_for_urls:
        dict_for_urls[real_name].append(current_dict['html_url'])
    else:
        dict_for_urls[real_name] = []


def get_full_names_of_phones(current_dict: dict) -> None:
    if isinstance(current_dict, dict):
        if 'full_name' in current_dict:
            global all_count
            global phones
            print(current_dict['full_name'])
            print(current_dict['html_url'])
            fill_dict_for_url(current_dict)
            phones += 1
            filling_dict_for_colors(current_dict)
        for key in current_dict.keys():
            get_full_names_of_phones(current_dict[key])
    elif isinstance(current_dict, list):
        for element in current_dict:
            get_full_names_of_phones(element)


def find_selling_phones_on_the_last_page(current_dict: dict, finded_key='full_name'):
    global phones

    if isinstance(current_dict, dict):
        if finded_key in current_dict:
            if finded_key == 'offers':
                phones += 1
                return True
            else:
                filling_dict_for_colors(current_dict)
                for key in current_dict.keys():
                    find_selling_phones_on_the_last_page(current_dict[key])
    elif isinstance(current_dict, list):
        for element in current_dict:
            find_selling_phones_on_the_last_page(element)


if __name__ == '__main__':
    URL = 'https://catalog.onliner.by/sdapi/catalog.api/search/mobile?group=1&page='
    w = 0
    e = 0
    for i in range(1, 31):
        PHONES_JSON = requests.get(URL + str(i)).json()
        if i == 30:
            find_selling_phones_on_the_last_page(PHONES_JSON)
            break
        get_full_names_of_phones(PHONES_JSON)

    print(dict_for_colors)
    with open('phones.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(
            ('phone name\n', 'colors', 'price', 'url')
        )
    lst_for_writing_into_csv = []
    sorted_urls = dict(sorted(dict_for_urls.items())).values()
    for phone_name, colors, url in zip(dict_for_colors.keys(), dict_for_colors.values(), sorted_urls):
        lst_for_writing_into_csv.append([
                phone_name,
                ', '.join(colors),
                '\n'.join(url)]
        )
    print('#' * 50)
    print(*lst_for_writing_into_csv, sep='\n')
    with open('phones.csv', 'a') as file:
        writer = csv.writer(file)
        for data in sorted(lst_for_writing_into_csv, key=lambda item: item[0]):
            writer.writerow(
                data
            )
    print(phones)
    print(dict_for_urls)