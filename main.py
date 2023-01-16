"""On page 30 there are 13 phones on selling and the rest are not on selling. These 13 phones have an
'offers' parameter and I can use it to sift out the rest, but I don't want to parse the giant json again.
There is no need to create a separate json file for storing a big json from API, I'll delete it at the end
of this project."""

import json
from sys import getsizeof

import requests


def writing_json_to_file(html) -> None:
    with open('mobile_json.json', 'w') as file:
        json.dump(html, file, indent=4, ensure_ascii=False)


phones = 0
dict_for_colors = dict()    # I use a dict like a global variable because it will be overwritten after
                            # each calling function filling_dict_for_colors()


def get_full_names_of_phones(current_dict: dict) -> None:
    def filling_dict_for_colors():
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

    if isinstance(current_dict, dict):
        if 'full_name' in current_dict:
            global phones
            print(current_dict['full_name'])
            phones += 1
            filling_dict_for_colors()
        for key in current_dict.keys():
            get_full_names_of_phones(current_dict[key])
    elif isinstance(current_dict, list):
        for element in current_dict:
            get_full_names_of_phones(element)


if __name__ == '__main__':
    URL = 'https://catalog.onliner.by/sdapi/catalog.api/search/mobile?group=1&page='
    for i in range(1, 31):
        PHONES_JSON = requests.get(URL + str(i)).json()
        writing_json_to_file(PHONES_JSON)
        get_full_names_of_phones(PHONES_JSON)
    print(dict_for_colors)
    print(len(dict_for_colors))
    print(getsizeof(dict_for_colors))
