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
tokens = ('LNAME', 'STRING', 'RNAME',  'ANCHOR',
          'LWRITERS', 'LPRODUCERS', 'LDIRECTORS',
          'LLANGUAGE', 'LCAST', 'MCAST','RCAST', 'SCAST',
          'LSTORY',  'LCOLLECTION', 'SEP', 'RA', 'BR',
          'LRUNTIME', 'RRUNTIME', 'RTAG', 'WSPACE',
          'SLIKE', 'LLIKE', 'MLIKE', 'RLIKE', 'ELIKE',
          'SWATCH', 'LWATCH', 'RWATCH', 'EWATCH')

# Define the tokens

# ***** Token for where to watch *****
def t_SWATCH(t):
    r'[\s]*<ul[\s]class=\"affiliates__list[\s]js-affiliates-list\">[\s]*'
    return t

def t_LWATCH(t):
    r'[\s]*<li[\s]class=\"affiliate__item\"([^>]*>){2}[\s]*<affiliate-icon[\s]name=\"[\s]*'
    return t

def t_RWATCH(t):
    r'[\s]*\"[\s]alignicon=\"left[\s]center\"([^>]*>){8}[\s]*'
    return t

def t_EWATCH(t):
    r'[\s]*<\/ul>[\s]*<\/div>[\s]*'
    return t
# ***** - *****

# ***** Token for you make like *****
def t_SLIKE(t):
    r'<div[\s]class=\"posters-container\"[\s]slot=\"posters-container\">[\s]*'
    return t

def t_LLIKE(t):
    r'<a[\s]href=\"/m/'
    return t

def t_MLIKE(t):
    r"\"[\s]class=\"recommendations-panel__poster-link[^>]*>([\s]*[^>]*>){10}"
    return t

def t_RLIKE(t):
    r'<\/span>[\s]*<\/tile-poster-meta>[\s]*<\/tile-poster>[\s]*</a>'
    return t

def t_ELIKE(t):
    r'[\s]*<\/div>[\s]*<rt-icon([^>]*>){5}'
    return t
# ***** - *****

# ***** Token for string *****
def t_STRING(t):
    r"[? a-zA-Z0-9\. '  \/ : \- \(\) $ ôôé \& _  # ;]+"
    # "[? a-zA-Z0-9.' \" \/ : \- \(\) $ ôôé \& _ ]+"
    return t
# ***** - *****

# ***** Token for page break *****
def t_BR(t):
    r'[\s]*<br>[\s]*'
    return t
# ***** - *****

# ***** Token for movie name *****
def t_LNAME(t):
    r'<h1[\s]slot=\"title\"[\s]class=\"scoreboard__title\"[\s]data-qa=\"score-panel-movie-title\">'
    return t

def t_RNAME(t):
    r'</h1>[ \t\r\n\f]*<p[\s]slot=\"info\"[\s]class=\"scoreboard__info\">[\s]*'
    return t
# ***** - *****

# ***** Token for Director, writer and producer *****
def t_LDIRECTORS(t):
    r'<div[\s]class=\"meta-label[\s]subtle\"[\s]data-qa=\"movie-info-item-label\">Director:</div>[ \t\r\n\f]*<div[\s]class=\"meta-value\"[\s]data-qa=\"movie-info-item-value\">[\s]*'
    return t

def t_LWRITERS(t):
    r'<div[\s]class=\"meta-label[\s]subtle\"[\s]data-qa=\"movie-info-item-label\">Writer:</div>[ \t\r\n\f]*<div[\s]class=\"meta-value\"[\s]data-qa=\"movie-info-item-value\">[\s]*'
    return t

def t_LPRODUCERS(t):
    r'<div[\s]class=\"meta-label[\s]subtle\"[\s]data-qa=\"movie-info-item-label\">Producer:</div>[ \t\r\n\f]*<div[\s]class=\"meta-value\"[\s]data-qa=\"movie-info-item-value\">[\s]*'
    return t

def t_RTAG(t):
    r'[ \t\r\n\f]*</div>'
    return t
# ***** - *****

# ***** Token for anchor tag *****
def t_ANCHOR(t):
    r'<a\shref=".*">'
    return t

def t_RA(t): # Right anchor
    r'[\s]*</a>[\s]*'
    return t
# ***** - *****
      
# ***** Token for cast information *****
def t_SCAST(t):
    r'<div[\s]class=[^>]*>[\s]*<div[\s][^>]*>[\s]*<a[\s]href=\"/celebrity/'
    return t
def t_LCAST(t):
    r'\"[\s]data-qa=\"cast-crew-item-img-link\">[\s]*([^>]*>){6}[\s]*'
    return t

def t_MCAST(t):
    r'[\s]*<\/span>[\s]*<\/a>[\s]*<span[^>]*>[\s]*(<br\/>|<br>)[\s]*'
    return t

def t_RCAST(t):
    r'[\s]*(<br/>|<br>)*[\s]*<\/span>[\s]*<\/div>[\s]*<\/div>'
    return t         
# ***** - *****

# ***** Token for stroyline *****
def t_LSTORY(t):
    r'<div[\s]id=\"movieSynopsis\"[\s]class=\"movie_synopsis[\s]clamp[\s]clamp-6[\s]js-clamp\"[\s]style=\"clear:both\"[\s]data-qa=\"movie-info-synopsis\">[\s]*'
    return t
# ***** - *****

# ***** Token for box office collection *****
def t_LCOLLECTION(t):
    r'<div[\s]class=\"meta-label[\s]subtle\"[\s]data-qa=\"movie-info-item-label\">Box[\s]Office[\s]\(Gross[\s]USA\):</div>[ \t\r\n\f]*<div[\s]class=\"meta-value\"[\s]data-qa=\"movie-info-item-value\">[\s]*'
    return t
# ***** - *****

# ***** Token for runtime *****
def t_LRUNTIME(t):
    r'[\s]*<time[\s]datetime=".*">[\s]*'
    return t

def t_RRUNTIME(t):
    r'[\s]*</time>'
    return t
# ***** - *****

# ***** Token for white space *****
def t_WSPACE(t):
    r'[\ \t]+'
    return t
# ***** - *****

# ***** Token for language *****
def t_LLANGUAGE(t):
    r'[\s\t\r\n\f]*<div[\s]class=\"meta-label[\s]subtle\"[\s]data-qa=\"movie-info-item-label\">Original[\s]Language:<\/div>[ \t\r\n\f]*<div[\s]class="meta-value"[\s]data-qa="movie-info-item-value">'
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

# ************************************************* Define Parsing Rules *****************************************
info_retrived = dict()
u_may_like_list = dict()
cast_information = dict()
movie_date_dict = dict()
movie_rating_dict = dict()
online_platform_list = list()
similar_movie_list = list()

# Define Parsing Rules
def p_start(t):
    '''start : mname
            | directors
            | writer
            | producers
            | language
            | cast
            | story
            | collection
            | runtime
            | similar_movie
            | watch
            '''

#   ***** Where to watch *****
def p_watch(t):
    'watch : SWATCH platforms EWATCH'
    info_retrived['WHERE TO WATCH'] = t[2]

def p_platform(t):
    'platform : LWATCH string RWATCH'
    t[0] = t[2]

def p_platform_multi(t):
    '''platforms : platform
                 | platform platforms'''
    t[1] = re.sub("-", " ", t[1]) # replace '-' with space
    t[1] = re.sub(" us", "", t[1]) # remove ' us'
    t[1] = t[1].replace(t[1][0], t[1][0].upper(), 1) # make first character uppercase
    online_platform_list.append(t[1])
    t[0] = ', '.join(online_platform_list)
#   ***** - *****

#   ***** you may like *****
def p_similar_movie(t):
    'similar_movie : SLIKE u_may_like ELIKE'
    info_retrived['SIMILAR MOVIE'] = t[2]

def p_single_like(t):
    'single_like : LLIKE string MLIKE string RLIKE'
    t[0] = t[4]
    u_may_like_list[(t[4]).upper()] = t[2]

def p_like_multi(t):
    '''u_may_like : single_like SEP u_may_like
                  | single_like
                  '''
    similar_movie_list.append(t[1])
    t[0] = ', '.join(similar_movie_list)
#   ***** - *****

#   ***** Movie name *****
def p_mname(t):
    'mname : LNAME movie_name RNAME'
    info_retrived['NAME'] = t[2]

def p_movie_name(t):
    '''movie_name : string SEP string
                  | string
                  | string STRING
     '''
    if len(t) == 4:
        t[0] = t[1] + t[2] + t[3]
    else:
        t[0] = t[1]
#   *****  *****

#   ***** Directors' name *****
def p_directors(t):
    'directors : LDIRECTORS celebrity RTAG'
    info_retrived['DIRECTORS'] = t[2]

#   ***** Writers' name *****
def p_writer(t):
    'writer : LWRITERS celebrity RTAG'
    info_retrived['WRITERS'] = t[2]

#   ***** Producers' name *****
def p_producers(t):
    'producers : LPRODUCERS celebrity RTAG'
    info_retrived['PRODUCERS'] = t[2]

def p_celebrity(t):
    'celebrity : ANCHOR string RA'
    t[0] = t[2]

def p_multi_celebrity(t):
    'celebrity : ANCHOR string RA SEP celebrity '
    t[0] = t[2] + ', ' + t[5]
#   ***** - *****

#   ***** Movie Language *****
def p_language(t):
    'language : LLANGUAGE string RTAG'
    info_retrived['LANGUAGE'] = t[2]
#   ***** - *****

#   ***** Cast information *****
def p_cast(t):
    'cast :  SCAST string LCAST string MCAST role RCAST '
    if 'CAST' in info_retrived.keys():
        info_retrived['CAST'] += ( '; ' + t[4] + " : " + t[6])
    else :
        info_retrived['CAST'] =  t[4] + " : " + t[6]
    cast_information[(t[4]).upper()] = 'https://www.rottentomatoes.com//celebrity/' + t[2]
    
def p_cast_role(t):
    'role : string'
    t[0] = t[1]

def p_cast_roles(t):
    'role : role SEP string'
    t[0] = t[1] + ', ' + t[3]

def p_cast_roles_multi(t):
    'role : role BR string'
    t[0] = t[1] + ', ' + t[3]
#   ***** - *****

#   ***** Story line *****
def p_story(t):
    'story : LSTORY temp_story RTAG'
    info_retrived['STORY'] = t[2]

def p_temp_story(t):
    '''temp_story : string
                  | STRING stories
                  | temp_story stories
    '''
    if len(t) == 3:
        t[0] = t[1] + t[2]
    else:
        t[0] = t[1]

def p_temp_stories(t):

    '''stories : STRING string
              | SEP string
    '''
    t[0] = t[1] + t[2] 
#   ***** - *****

#   ***** Box office collection *****
def p_collection(t):
    'collection : LCOLLECTION string RTAG'
    info_retrived['COLLECTION'] = (t[2] + " dollars")
#   ***** - *****

#   ***** Runtime *****
def p_runtime(t):
    'runtime : LRUNTIME time RRUNTIME'
    info_retrived['RUNTIME'] = t[2] 

def p_time(t):
    '''time : STRING string 
            | STRING'''
    if len(t) == 3:
        t[0] = t[1] + t[2]
    else:
        t[0] = t[1]
#   ***** - *****

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


# *********************************************** U May LIKE ******************************************

def get_similar_movie_info(u_may_like_list):
    # keep asking for a valid input from the user
    while True:
        new_movie = input('Enter the movie name you want to see / [skip] : ')
        if(new_movie.upper() in u_may_like_list.keys()):
            new_movie_url = 'https://www.rottentomatoes.com/m/' + u_may_like_list[new_movie.upper()]
            
            # clear the terminal
            if platform.system() == 'Windows':
                os.system('cls')
            else:
                os.system('clear')

            # Redirect to the new movie
            print(bcolors.OKGREEN,bcolors.BOLD,'Loading information of', bcolors.OKCYAN, bcolors.UNDERLINE, '{}'.format(new_movie), bcolors.ENDC)
            if platform.system() == 'Windows':
                os.system('python 20CS60R15_A9_P2.py "{}" "{}"'.format(new_movie_url, new_movie))
            else:
                os.system('python3 20CS60R15_A9_P2.py "{}" "{}"'.format(new_movie_url, new_movie))
            return True
        elif new_movie.upper() not in ('SKIP', '', 'N', 'NO', 'QUIT', 'EXIT'):
            print("Wrong input. please enter a valid input.")
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

    return False

# ***************************************** Cast Information ************************************************

def get_cast_info(cast_information):
    # keep asking for a valid input from the user
    while True:
        cast_name = input('Enter the cast name (underlined ones) you want to see / [skip] : ')
        if(cast_name.upper() in cast_information.keys()):
            cast_url = cast_information[cast_name.upper()]
            
            # clear the terminal
            if platform.system() == 'Windows':
                os.system('cls')
            else:
                os.system('clear')

            # Redirect to the cast information program (20CS60R15_A9_P3.py)
            print(bcolors.OKGREEN,bcolors.BOLD,'Loading information of', bcolors.OKCYAN, bcolors.UNDERLINE, '{}'.format(cast_name), bcolors.ENDC)
            if platform.system() == 'Windows':
                os.system('python 20CS60R15_A9_P3.py "{}"'.format(cast_url))
            else:
                os.system('python3 20CS60R15_A9_P3.py "{}"'.format(cast_url))
            return True
        elif cast_name.upper() not in ('SKIP', '', 'N', 'NO', 'QUIT', 'EXIT'):
            print("Wrong input. please enter a valid input.")
        else: # if user doesn't want to know more about the cast
            # clear the terminal
            if platform.system() == 'Windows':
                os.system('cls')
            else:
                os.system('clear')

            # Print all the infomation (again) user can query
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
    return False

# ******************************************* MAIN ****************************************************
def main():    
    # check if user provided correct arguments or not
    n = len(sys.argv)
    if n < 2:
        print('Error! This program suppose to get two valid arguments...')
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
    web_content = ""
    for i in b_web_content:
        web_content += i.decode("utf-8")

    # call lex
    lexer = lex()

    # call yacc
    parser = yacc(errorlog=yc.NullLogger())

    # parse the content
    parser.parse(web_content)

    if "NAME" not in info_retrived.keys():
        try:
            info_retrived['NAME'] = sys.argv[2]
        except :
            info_retrived['NAME'] = "NO NAME"

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
                    msg = features + " : " + value + '\n' 
                    movie_name = info_retrived['NAME']

                    # If user asked cast information
                    if features.upper() == 'CAST':
                        casts_info = ""
                        value_list = value.split('; ')
                        for cast_info in value_list:
                            cast_info_list = cast_info.split(" : ")
                            cast_info_list[0] = bcolors.UNDERLINE + bcolors.HEADER +cast_info_list[0] + bcolors.ENDC
                            if casts_info == "":
                                casts_info += " : ".join(cast_info_list)
                            else:
                                casts_info += ("; " + " : ".join(cast_info_list))
                        value = casts_info
                    
                    print(bcolors.WARNING + bcolors.UNDERLINE + features + bcolors.ENDC + ': ', end='')
                    print( bcolors.OKCYAN + value + bcolors.ENDC)

                    # If user wants to see similar movie then show him/her the available options
                    if features == "SIMILAR MOVIE":
                        yes_please = get_similar_movie_info(u_may_like_list)
                        if yes_please:
                            break 

                    # If user wants to see cast information then show him/her the available options
                    if features == "CAST":
                        yes_please = get_cast_info(cast_information)
                        if yes_please:
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
                msg = features + " : " + value + '\n' 
                movie_name = info_retrived['NAME']
                
                # If user asked cast information
                if features.upper() == 'CAST':
                    casts_info = ""
                    value_list = value.split('; ')
                    for cast_info in value_list:
                        cast_info_list = cast_info.split(" : ")
                        cast_info_list[0] = bcolors.UNDERLINE + bcolors.HEADER +cast_info_list[0] + bcolors.ENDC
                        if casts_info == "":
                            casts_info += " : ".join(cast_info_list)
                        else:
                            casts_info += ("; " + " : ".join(cast_info_list))
                    value = casts_info
                
                print(bcolors.WARNING + bcolors.UNDERLINE + features + bcolors.ENDC + ': ', end='')
                print(bcolors.OKCYAN + value + bcolors.ENDC)

                # If user wants to see similar movie then show him/her the available options
                if features == "SIMILAR MOVIE":
                    yes_please = get_similar_movie_info(u_may_like_list)
                    if yes_please:
                        break 
                
                # If user wants to see cast information then show him/her the available options
                if features == "CAST":
                    yes_please = get_cast_info(cast_information)
                    if yes_please:
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