import urllib.request as req, urllib.error, urllib.parse
import re
import os
from os import system, name
import platform
# define color
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

genre_dict = {
    'action & adventure' : 'https://www.rottentomatoes.com/top/bestofrt/top_100_action__adventure_movies/',
    'animation' :          'https://www.rottentomatoes.com/top/bestofrt/top_100_animation_movies/',
    'drama' :              'https://www.rottentomatoes.com/top/bestofrt/top_100_drama_movies/',
    'comedy' :             'https://www.rottentomatoes.com/top/bestofrt/top_100_comedy_movies/',
    'mystery & suspense' : 'https://www.rottentomatoes.com/top/bestofrt/top_100_mystery__suspense_movies/',
    'horror':              'https://www.rottentomatoes.com/top/bestofrt/top_100_horror_movies/',
    'sci-Fi':              'https://www.rottentomatoes.com/top/bestofrt/top_100_science_fiction__fantasy_movies/',
    'documentary' :        'https://www.rottentomatoes.com/top/bestofrt/top_100_documentary_movies/',
    'romance' :            'https://www.rottentomatoes.com/top/bestofrt/top_100_romance_movies',
    'classics':            'https://www.rottentomatoes.com/top/bestofrt/top_100_classics_movies/'
    }


# show and ask genres from user
def get_genre_list(genre_dict=genre_dict):
    genre_list = list(genre_dict.keys())

    # Show all the genre
    print('\nAvailable genres: ')
    for i in range(len(genre_list)):
        print (bcolors.OKCYAN, '\t{}. {}'.format(i+1, genre_list[i]), bcolors.ENDC)

    # Read user input for genre
    genre_entered = None
    while True:
        genre_entered = input('\nPlease select a Genre name or number: ')

        # check if user enter index of genre or the genre name
        if genre_entered.isnumeric(): # user enter genre index
            # if user enter invalid index
            if int(genre_entered) > len(genre_list):
                print('Invalid input. Please try again...')
            
            #if user enter right index
            else:
                genre_name = genre_list[int(genre_entered) - 1]
                url = genre_dict[genre_name]
                genre_entered = genre_name
                break;

        else: # user enter genre name
            genre_entered = (re.sub(r'[0-9.]','', genre_entered)).strip() # Try to remove un-necessary data
            if genre_entered.lower() in genre_dict:
                genre_name = genre_entered.lower()
                url = genre_dict[genre_name]
                break

            else:
                print('Invalid input. Please try again...')

    return genre_entered, url

# Show and ask movie name
def get_movie_names(url):
    # crawl the entered gener webpage 

    # ***** Read the portion of HTML file which contain all the information *****
    response = req.urlopen(url)
    web_content = response.readlines()

    start_of_table = None
    end_of_table = None

    # Find out where the movie information table starts
    for line_no, line in enumerate(web_content):
        if 'table class="table"' in line.decode("utf-8")  :
            start_of_table = line_no + 1
            break
    # Find out end of that table
    for line_no, line in enumerate(web_content):
        if '/table' in line.decode("utf-8") and line_no > start_of_table:
            end_of_table = line_no + 1
            break

    table_content = web_content[start_of_table - 1: end_of_table]
    table_content = [(i.strip()).decode("utf-8") for i in table_content]
    # ***** - *****

    # Read all the movie name
    movie_link = list()
    movie_name_list = list()
    for content in table_content:
        if '<a' in content :
            link_suffix = content.lstrip('<a href="')
            link_suffix = re.sub('" class="unstyled articleLink">', '', link_suffix)
            movie_link.append('https://www.rottentomatoes.com' + link_suffix)
        if '</a>' in content:
            movie_name_list.append(content.strip('</a>'))

    # Clear the terminal first:
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

    # List all the movie name
    for i in range(len(movie_link)):
        print(bcolors.OKGREEN, str(i+1) +".", (movie_name_list[i]), bcolors.ENDC)

    # Make all movie name lowercase for better matching.
    lower_case_movie_list = [i.lower() for i in movie_name_list]
    name = None
    movie_url = None
    # Ask user for a valid input (movie name)
    while True:
        name = input('\nEnter your favorite movie name or the number / q: ')
        if name == 'q' or name == 'Q':
            break

        # If user provide an index, check if it is valid or not.
        if name.isnumeric():
            if int(name) <= len(movie_name_list):
                movie_index = int(name) - 1
                name = movie_name_list[movie_index]
                movie_url = movie_link[movie_index]
                break
            else:
                print('Please enter a valid name..., your input:', name)

        # if provided input isn't a number
        else:
            # Check if movie name matched exactly (case insensitive)
            if name.lower() in lower_case_movie_list:
                movie_index = lower_case_movie_list.index(name.lower())
                movie_url = movie_link[movie_index]
                # print(movie_url)
                break

            # Check if movie name matches partially.
            else: 
                for _movie_name in lower_case_movie_list:
                    if name.lower() in _movie_name:
                        user_confirmation = input('{} {} {}'.format('Do you mean', _movie_name, '? ([yes]/no)'))
                        if user_confirmation in ('y', 'Y', 'yes', 'Yes', 'YES', ''):
                            name = _movie_name
                            movie_index = lower_case_movie_list.index(name.lower())
                            movie_url = movie_link[movie_index]
                            # print(movie_url)
                            break
                        elif user_confirmation not in ('n', 'N', 'no', 'No', 'NO'):
                            print('Wrong input.')
                            break
                if name.lower() in lower_case_movie_list:
                    # print(name)
                    break
                # If provided input doesn't match with any movie name.
                else:
                    print('Please enter a valid name..., your input:', name)

    return movie_url, name

def main():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
    genre_entered, url = get_genre_list(genre_dict)
    movie_url, name = get_movie_names(url)
    if movie_url != None:
        if platform.system() == 'Windows':
            os.system('python 20CS60R15_A9_P2.py "{}" "{}"'.format(movie_url, name))
        else:
            os.system('python3 20CS60R15_A9_P2.py "{}" "{}"'.format(movie_url, name))

if __name__ == '__main__':
    main()