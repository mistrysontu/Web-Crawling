import re
import os
import sys
import platform
from ply.lex import lex
from ply.yacc import yacc
from ply import yacc as yc
import urllib.request as req, urllib.error, urllib.parse

# define color theme
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


# ************************************************ Define Token *********************************************

# declear token
tokens = ('LBDAY', 'RBDAY', 'STRING','WSPACE',
         'LCAST_MOVIES', 'MCAST_MOVIES1',
          'MCAST_MOVIES2', 'RCAST_MOVIES', 'SEP')

# ***** Token for DOB *****
def t_LBDAY(t):
    r'<p[\s]class=\"celebrity-bio__item\"[\s]data-qa=\"celebrity-bio-bday\">[\s]*Birthday:[\s]*'
    return t

def t_RBDAY(t):
    r'[\s]*<\/p>'
    return t
# ***** - *****

# ***** Token for All movies *****
def t_LCAST_MOVIES(t):
    r'<tr[\s]data-title=\"'
    return t 

def t_MCAST_MOVIES1(t):
    r'(?s)(?=\"[\s]data-boxoffice=).*?(?=data-tomatometer)data-tomatometer=\"'
    # r'(?s)(?=\"[\s]data-boxoffice=).*?(?=__year)__year\">'
    return t

def t_MCAST_MOVIES2(t):
    r'(?s)(?=\"[\s]*data-audiencescore=).*?(?=__year)__year\">'
    return t

def t_RCAST_MOVIES(t):
    r'<\/td>[\s]*'
    return t
# ***** - *****

# ***** Token for string *****
def t_STRING(t):
    r"[? a-zA-Z0-9\. '  \/ : \- \(\) $ ôôé \& _  # ;]+"
    # "[? a-zA-Z0-9.' \" \/ : \- \(\) $ ôôé \& _ ]+"
    return t
# ***** - *****

# ***** Token for whitespace *****
def t_WSPACE(t):
    r'[\ \t]+'
    return t
# ***** - *****

# ***** Token for separator *****
def t_SEP(t):
    r"[\s, \"-]+"
    return t
# ***** - *****

# Error handling rule
def t_error(t):
    t.lexer.skip(1)
# ***** - *****

# ************************************************* Define Parsing Rules *****************************************
info_retrived = dict()
movie_date_dict = dict()
movie_rating_dict = dict()

# Define Parsing Rules
def p_start(t):
    '''start : cast_movie
             | bday
            '''

# ***** Birth Day *****
def p_bday(t):
    'bday : LBDAY string SEP string RBDAY'
    info_retrived['DOB'] = t[2] + t[3] + t[4]
# ***** - *****

# ***** CAST MOVIE INFORMATION *****
def p_cast_movie(t):
    'cast_movie : LCAST_MOVIES string MCAST_MOVIES1 string MCAST_MOVIES2 string RCAST_MOVIES '''
    t[0] = t[2]

    movie_date_dict[t[2]] = int(t[6])
    movie_rating_dict[t[2]] = t[4]
    if 'ALL MOVIES' in info_retrived.keys():
        info_retrived['ALL MOVIES'] += (', ' + t[0] + ' (' + t[6] + ')')
    else :
        info_retrived['ALL MOVIES'] = (t[0] + ' (' + t[6] + ')')

#   ***** String *****
def p_string_one(t):
    'string : STRING'
    t[1] = re.sub("&#39;", "'", t[1]) # replace '&#39;' with apostrophy
    t[0] = t[1]

def p_string_multi(t):
    'string : STRING wspaces string'
    t[0] = t[1] + t[2] + t[3]

def p_wspaces(t):
    '''wspaces : WSPACE
            | WSPACE wspaces'''
    t[0] = ' '
#   ***** - *****

#   ***** Error *****
def p_error(t):
    pass
# ***** - *****

# ******************************************* MAIN ****************************************************
def main():    
    # check if user provided correct arguments or not
    n = len(sys.argv)
    if n < 1:
        print('Error! This program suppose to get one valid arguments...')
        sys.exit()

    # Try to open the url
    response = None
    try:
        response = req.urlopen(sys.argv[1])
    except:
        print("Url isn't reachable")
        sys.exit()

    # Crawl the website
    b_web_content = response.readlines()

    # ***** Read the portion of HTML file which contain all the information *****
    start_of_table = None
    end_of_table = None

    # Find out where celebrity dob starts
    for line_no, line in enumerate(b_web_content):
        if 'celebrity-bio-bday' in line.decode("utf-8")  :
            start_of_table = line_no + 1
            break

    # Find out end of dob
    for line_no, line in enumerate(b_web_content):
        if '</p>' in line.decode("utf-8") and line_no > start_of_table:
            end_of_table = line_no + 1
            break
    table_content = b_web_content[start_of_table - 1: end_of_table]

    # Find out where the movie information table starts
    for line_no, line in enumerate(b_web_content):
        if 'celebrity-filmography-movies-subheader">Movies' in line.decode("utf-8")  :
            start_of_table = line_no + 1
            break

    # Find out end of that table
    for line_no, line in enumerate(b_web_content):
        if '/table' in line.decode("utf-8") and line_no > start_of_table:
            end_of_table = line_no + 1
            break

    table_content += b_web_content[start_of_table - 1: end_of_table]
    table_content = [(i.strip()).decode("utf-8") for i in table_content]

    web_content = '\n'.join(table_content)
    # ***** - ***** 

    # call lex
    lexer = lex()

    # call yacc
    parser = yacc(errorlog=yc.NullLogger())

    # parse the content
    parser.parse(web_content)

    # ***** Find height and lowest rated movie *****
    movie_rating_dict
    min_ratting = 101
    min_ratted_movie = None
    max_ratted_movie = None
    max_ratting = -1
    for i in movie_rating_dict.keys():
        # find max ratted movie
        if (int(movie_rating_dict[i]) > max_ratting):
            max_ratting = int(movie_rating_dict[i])
            max_ratted_movie = i
            
        # find least ratted movie
        if (int(movie_rating_dict[i]) < min_ratting):
            min_ratting = int(movie_rating_dict[i])
            min_ratted_movie = i
            
    info_retrived['Highest Rated film'] = max_ratted_movie
    info_retrived['Lowest Rated film'] = min_ratted_movie
    # ***** - *****

    # Print all the infomation user can query
    if info_retrived.keys() != None:
        print('\nWhat do you want to know?\n')
        count = 0
        queries = list(info_retrived.keys())
        for key in queries:
            count += 1
            print('\t', str(count) + '. ', key)
    count += 1
    print('\t', str(count) + '. ', 'Query a new movie' )
    count += 1
    print('\t', str(count) + '. ', 'Exit' )

    # Loop until user wants to exit
    while True:
        user_input = input('\nEnter your choice: ')

        # If user enter index of query
        if user_input.isnumeric():
            if int(user_input) <= len(queries) + 2:
                # If user wants to query about a new movie
                if int(user_input) == len(queries)+1:
                    if platform.system() == 'Windows':
                        os.system('cls')
                        os.system('python 20CS60R15_A9_P1.py')
                    else:
                        os.system('clear')
                        os.system('python3 20CS60R15_A9_P1.py')
                    break

                # If user wants to exit
                elif int(user_input) == len(queries)+2:
                    print('Farewell user...')
                    break

                # If user provide valid input
                else: 
                    # Print the information user asked for the movie
                    features =  queries[int(user_input)-1] 
                    value = info_retrived[queries[int(user_input)-1]] 
                    
                    print(bcolors.WARNING + bcolors.UNDERLINE + features + bcolors.ENDC + ': ', end='')
                    print( bcolors.OKCYAN + value + bcolors.ENDC)

                    # If user wants to know about all the movie of the cast
                    query_date = None
                    if features == 'ALL MOVIES':
                        while True:
                            query_date = input('\nEnter the year you want to filter / [skip]: ')
                            if not query_date.isnumeric():
                                if query_date.upper() not in ('SKIP', '', 'N', 'NO', 'QUIT', 'EXIT'):
                                    print('Wrong input(year), please try a vaild year again...')
                                else:
                                    # clear the terminal
                                    if platform.system() == 'Windows':
                                        os.system('cls')
                                    else:
                                        os.system('clear')
                                    
                                    # Print all the valid options again 
                                    if info_retrived.keys() != None:
                                        print('\nWhat do you want to know?\n')
                                        count = 0
                                        queries = list(info_retrived.keys())
                                        for key in queries:
                                            count += 1
                                            print('\t', str(count) + '. ', key)
                                    count += 1
                                    print('\t', str(count) + '. ', 'Query a new movie' )
                                    count += 1
                                    print('\t', str(count) + '. ', 'Exit' )
                                    break
                            elif int(query_date) < min(movie_date_dict.values()):
                                print('Too low, please try a higher year...')
                            elif int(query_date) > max(movie_date_dict.values()):
                                print('Too High, please try a lower year...')
                            else:
                                print(bcolors.WARNING + 'Filtered movie names: ' + bcolors.ENDC, end="")
                                for i in movie_date_dict.keys():
                                    if movie_date_dict[i] >= int(query_date):
                                        print(bcolors.OKBLUE + i + ' (' + str(movie_date_dict[i]) + ') ' +  bcolors.ENDC + ', ', end="")
                                sys.stdout.write('\b\b') # move back the cursor
                                sys.stdout.write(' ')
                                break
                            


            # if user enter wrong input              
            else:
                print('Wrong input. Please entry a valid one.')
        
        # If user enter the qeury name (in word)        
        else:
            if user_input.upper() in queries:

                # Print the information user asked for the movie
                features =  user_input.upper()
                value = info_retrived[user_input.upper()] 
                               
                print(bcolors.WARNING + bcolors.UNDERLINE + features + bcolors.ENDC + ': ', end='')
                print(bcolors.OKCYAN + value + bcolors.ENDC)

                # If user wants to know about all the movie of the cast
                query_date = None
                if features == 'ALL MOVIES':
                    while True:
                        query_date = input('\nEnter the year you want to filter: ')
                        if not query_date.isnumeric():
                            print('Wrong input(year), please try a vaild year again...')
                        elif int(query_date) < min(movie_date_dict.values()):
                            print('Too low, please try a higher year...')
                        elif int(query_date) > max(movie_date_dict.values()):
                            print('Too High, please try a lower year...')
                        else:
                            print(bcolors.WARNING + 'Filtered movie names: ' + bcolors.ENDC, end="")
                            for i in movie_date_dict.keys():
                                if movie_date_dict[i] >= int(query_date):
                                    print(bcolors.OKBLUE + i + ' (' + str(movie_date_dict[i]) + ') ' +  bcolors.ENDC + ', ', end="")
                            sys.stdout.write('\b\b') # move back the cursor
                            sys.stdout.write(' ')
                            break

            # If user wants to exit
            elif user_input.upper() in ('q'.upper(), 'Exit'.upper()):
                print('Farewell user...')
                break

            # If user wants to know about another movie
            elif user_input.upper() == 'Query a new movie'.upper():
                if platform.system() == 'Windows':
                    os.system('cls')
                    os.system('python 20CS60R15_A9_P1.py')
                else:
                    os.system('clear')
                    os.system('python3 20CS60R15_A9_P1.py')
                break

            else:
                print('Wrong input. Please entry a valid one.')


if __name__ == '__main__':
    main()
