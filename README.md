# clex
Basic lexical analyzer for subset of C 
##What is allowed

    Reserved keywords: almost all that I know
    Delimiters: ; , () {} []
    Comments: All
    Identifiers: All
    Operators: +, -, /, *, %, <, =, >, >=, <=, ==, ++, --, +=, -=, *=, /=, &&, &, !, ~
    Headers and Macros
    Numbers and Strings
    

##What is not allowed
    Everything for which you get error :)>
    
## Run
    sudo pip install plex
    python clex.py

## Result
    For sample test.c
    

				Result: 

           Lexicon type         Lexicon              No. of occurance 
           Header               <stdio.h>                1 
           Identifier           asds                     1 
           Functions            main()                   1 
           Identifier           total                    4 
           Functions            sub(a,b)                 1 
           Functions            mult( a,b )              1 
           Reserved             const                    1 
           Number               0                        1 
           Delimiter            )                        1 
           Delimiter            (                        1 
           Operator             +                        3 
           Operator             *                        1 
           Comment              comments                 2 
           Number               1                        2 
           Reserved             int                      2 
           Number               3                        1 
           Number               2                        1 
           Number               4                        1 
           Delimiters           ;                       12 
           Operator             =                        5 
           Functions            add(a,10)                1 
           Reserved             return                   1 
           Macro                PI      3.14             1 
           Functions            div(a*10,b)              1 
           String               asd                      1 
           Identifier           a                        3 
           Reserved             char                     1 
           Identifier           b                        9 
           Operator             ++                       3 
           Header               "custom.h"               1 
           Number               50                       1 
           Operator             --                       3 
           Operator             -=                       1 
           Identifier           x                        1 
           Delimiter            {                        1 
           Delimiter            }                        1 
           Operator             +=                       3 
    0  error(s)


## Sample error
    Missing matching quotes  at line 39 , 9
    Unexpected end of file, expected end of comment at  42 , 1



