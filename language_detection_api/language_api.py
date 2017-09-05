import requests
"""
simple console app that takes text file or a string and prints language of the text

"""


def lang_detection(text):

    params = {'access_key': '12525a4a8f71d1952ad454c2df7061cb', "query": text}
    languages = requests.get('http://apilayer.net/api/detect', params=params).json()

    if languages['success']:
        for result in languages['results']:
            print(result)

    else:
        print("Can't detect")
