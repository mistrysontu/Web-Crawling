Name(Author)       : Sontu Mistry
Roll no.           : 20CS60R15
Date(Last Edited)  : 03/04/2021

Language : Python3
OS       : Linux (Ubuntu) | WSL
Compiler(interpreter) : python3 

Run code:
    python3 20CS60R15_A9_P1.py
                or 
    Navigate to this forlder in a linux terminal and write 'make' (without quotation) and everything will be run automatically.

Work flow of 20CS60R15_A9_P1.py:
    (show genre) ==> (take user input for genre) ==> (show all the movie names under the genre) ==> (take user input for movie name) ==> (call 20CS60R15_A8_P2.py with user entered genre name and movie url) ==> tarminate.
    1. All the valid genre names are shown. 
            User can either type genre name (not casesensitive) or index of the genre.
    2. All the movie name under the specific genre are shown. 
            User can either type full movie name or part of it(not casesensitive) or the index of the movie.
    3. Call 20CS60R15_A8_P2.py with user entered genre name and movie url.

Work flow of 20CS60R15_A9_P2.py and 20CS60R15_A9_P3.py
    (crawl the website and read the required data) ==> (show the query the user can ask) ==> (take user input) ==> (show the answer of user query and log the information into log.txt file) ==> tarminate
    1. crawl the website and read the required data.
    2. show the query the user can ask
    3. take user input
            User can enter the query or the index of the query.
    4. Show details 
    5. Loop until user wants to exit.

!! Important:
    1. Run all the code on Ubuntu/Linux.
    2. 20CS60R15_A9_P1.py doen't need any argument. after successful execution of 20CS60R15_A8_P1.py 20CS60R15_A8_P2.py will be automatically called.
    3. 20CS60R15_A9_P2.py needs two argument url and movie name of the movie.
    4. 20CS60R15_A9_P2.py needs two argument url of cast.
    4. If python3 command don't work please manually change 'python3' to 'python' and try again.
    5. All programs are tested using python3.

disclaimer: 
    1. All code are written by the author.
    2. All code are running fine on author's computer. In case any problem please contact the author at mistrysontu@gmail.com
    3. All code are written and tested as per the information provided, with little modification.