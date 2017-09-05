import argparse
import requests

"""
Simple console app to search through SWAPI 
Takes given phrase and prints all SW names containing the phrase
Offers option to save detailed results to txt file
TODO:
-Make detailed search result contain names instead of api links (probably separate function to check each attribute for containing links)
-delete url, created, edited attrs from detailed results
-make use of exeptions xd
"""


def get_search_args():
    parser = argparse.ArgumentParser(description='Search through Star Wars database provided by SWAPI.')
    parser.add_argument('-ch', '--character', dest='people', action='store', help='Look for SW character')
    parser.add_argument('-p', '--planet', dest='planets', action='store', help='Look for SW planet')
    parser.add_argument('-v', '--vehicle', dest='vehicles', action='store', help='Look for SW vehicle')
    parser.add_argument('-sp', '--species', dest='species', action='store', help='Look for SW species')
    parser.add_argument('-ss', '--starship', dest='starships', action='store', help='Look for SW starship')
    parser.add_argument('-f', '--file', dest='save_to_file', action='store_true', help='Save to file')
    return parser.parse_args()


def get_results(resource, phrase):
    return {resource: requests.get(f"https://swapi.co/api/{resource}", params={'search': phrase}).json()['results']}


def get_name_by_link(link):
    data = requests.get(link).json()
    if 'name' in data:
        return data['name']
    if 'title' in data:
        return data['title']


def save_to_file(results_list):
    with open('star_wars_search_results.txt', 'w') as results_file:
        for results in results_list:
            results_file.write(('-- ' + list(results.keys())[0].capitalize() + ' --\n'))

            results = list(results.values())[0]
            for count, single_result in enumerate(results, 1):
                single_result.pop('created')
                single_result.pop('edited')

                results_file.write(f'\n--{count}--\n')

                for key, value in single_result.items():
                    results_file.write(key + ': ')

                    if isinstance(value, list):
                        for i in range(len(value)):
                            value[i] = get_name_by_link(value[i])

                    results_file.write(str(value) + '\n')
            results_file.write('\n\n')


def print_results(results_list):
    for results in results_list:
        print('\n-- ', list(results.keys())[0].capitalize(), ' --')

        results = list(results.values())[0]

        for single_result in results:
            print(single_result['name'])
    print()


def search(search_args):
    resources_dict = {key: value for key, value in vars(search_args).items() if value and key is not "save_to_file"}
    print("Looking for: \n", resources_dict, '\n')

    results_list = [get_results(key, value) for key, value in resources_dict.items()]

    print_results(results_list)

    if search_args.save_to_file:
        save_to_file(results_list)


if __name__ == "__main__":
    search_args = get_search_args()
    search(search_args)
