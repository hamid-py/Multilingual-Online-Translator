import requests
from bs4 import BeautifulSoup
import sys

from requests.exceptions import ProxyError

headers = {'user-agent': 'my-app/0.0.1'}
lang_dict = {'1': 'arabic', '2': 'german', '3': 'english', '4': 'spanish', '5': 'french', '6': 'hebrew',
             '7': 'japanese', '8': 'dutch', '9': 'polish', '10': 'portuguese', '11': 'romanian', '12': 'russian',
             '13': 'turkish'}


# print("Hello, you're welcome to the translator. Translator supports:")
# for i in range(1, 14):
#     print(f'{i}. {lang_dict[str(i)].capitalize()}')
# lang_type_from = input('Type the number of your language:')
# lang_type_to = input('Type the number of language you want to translate to: ')
# word = input('Type the word you want to translate:')


def translate(lang_type_from, lang_type_to, word):
    first_list = []
    second_list = []
    url = f'https://context.reverso.net/translation/{lang_dict[lang_type_from]}-{lang_dict[lang_type_to]}/{word}'
    try:
        response = requests.get(url, headers=headers)



        soup = BeautifulSoup(response.content, 'html.parser')
        first_translate = soup.find(id='translations-content').find_all('a')
        for i in first_translate:
            first_list.append(i.text.strip())

        second_translate = soup.find(id='examples-content').find_all('div')

        second_translate_from = []
        for i in second_translate:
            second_translate_from.append(i.find_all('div'))
        for i in second_translate_from:
            if len(i) != 0:
                i.pop()
                for j in i:
                    second_translate_to = j.find_all('span', {'class': 'text'})
                    for k in second_translate_to:
                        if len(k) != 0:
                            second_list.append(k.text.strip())
    except ConnectionResetError:
        print("Something wrong with your internet connection")
        return ConnectionResetError
    except ProxyError:
        print("Something wrong with your internet connection")
        return ProxyError
    print()

    print(f'{lang_dict[str(lang_type_to)].capitalize()} Translations:')
    for i in range(1):
        try:
            with open(f'{word}.txt', 'a', encoding='utf-8') as f:
                f.write(f'{lang_dict[str(lang_type_to)].capitalize()} Translations:\n{first_list[i]}'
                        f' \n{first_list[i + 1]} '
                        f' \n{first_list[i + 2]} \n{first_list[i + 3]} \n{first_list[i + 4]} \n')
        except:
            pass
        print(first_list[i])
    print()
    print(f'{lang_dict[str(lang_type_to)].capitalize()} Examples:')
    for i in range(1):
        if i % 2 == 0:
            with open(f'{word}.txt', 'a', encoding='utf-8') as f:
                f.write(f'{lang_dict[str(lang_type_to)].capitalize()} Examples:\n{second_list[i]}'
                        f' \n{second_list[i + 1]} \n')
            print(second_list[i])
            print(second_list[i + 1])
            print()


lang_dict_reverse = {'arabic': '1', 'german': '2', 'english': '3', 'spanish': '4', 'french': '5', 'hebrew': '6',
                     'japanese': '7', 'dutch': '8', 'polish': '9', 'portuguese': '10', 'romanian': '11',
                     'russian': '12',
                     'turkish': '13'}
if __name__ == '__main__':
    translate_from = sys.argv[1]
    translate_to = sys.argv[2]
    word = sys.argv[3]
    lang_type_from = lang_dict_reverse[translate_from]
    try:
        if translate_to == 'all':
            for i in range(1, 14):
                if i == 3:
                    continue
                translate(lang_type_from, str(i), word)
        else:
            lang_type_to = lang_dict_reverse[translate_to]
            translate(lang_type_from, lang_type_to, word)
    except KeyError:
        print(f"Sorry, the program doesn't support {translate_to}")
    except AttributeError:
        print(f"Sorry, unable to find {word}")
