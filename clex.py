"""
Simple script for lex analysis of small subset of C 

What is allowed

    Reserved keywords: almost all that I know
    Delimiters: ; , () {} []
    Comments: All
    Identifiers: All
    Operators: +, -, /, *, %, <, =, >, >=, <=, ==, ++, --, +=, -=, *=, /=, &&, &, !, ~
    Headers and Macros
    Numbers and Strings
    

What is not allowed
    Everything for which you get error :)>

"""


from plex import *
from plex.traditional import re
from plex.errors import *

error_text = ""
error_count = 0
prev_token = ""

types = Str("float", "double", "char", "void", "bool", "FILE", "int")
containers = Str("enum", "struct", "union", "typedef")
modifiers = Str("const", "volatile", "extern", "static", "register", "signed", "unsigned")
flow = Str("if", "else",
         "goto",
         "case", "default",
         "continue", "break", )
loops = Str("for", "do", "while" "switch")

reserved = types | containers | modifiers | flow  | loops | Str("return", "sizeof")

operators = Str("=", "+=", "-=", "/=", "*=", "%=","--","++","*","&","~","!", "!=", "%", ">", "<", ">=", "<=", "==", "&&", "+", "-") 

delimiters = Any("{}()[],")

letter = Range("AZaz")
digit = Range("09")
number = Rep1(digit)
space = Any(" \t\n")
variable = (Str("_") | letter) + Rep(letter | digit)

integerNumber = Rep(Any("+-")) + Rep1(digit)
floatNumber = Rep(Any("+-"))  + Rep(digit) + Str(".") + Rep1(digit) 

number = integerNumber | floatNumber 

string = re("\".*\"")

header = Str("#include") + ( re("<.*>")  | re("\".*\"") )
define = Str("#define") + Rep1(space) + variable + Rep1(space) + (string | number) 

token_string = ""

class MyScanner(Scanner):
    
    def __init__(self, file, name):
        Scanner.__init__(self, self.lexicon, file, name)
        self.symbol_table = {
            "comments": {
                "type": "Comment",
                "count": 0
            }
        }


    def begin_comment(self, text):
        if text == "/*":
            self.begin('multiline_comment')
        else:
            self.begin('single_comment')            
        self.symbol_table["comments"]["count"] += 1


    def handle_error(self, text):
        global error_count, error_text
        error_count+=1
        file, line, col = self.position()

        if self.state_name in ["str_double_quotes", "str_single_quote"]:
            error_text = "Missing matching quotes "
        
        print error_text, "at line", line, ",", col+1
        self.begin('')

    def process_reserved(self, text):
        self.update_table(text, "Reserved")
        return "reserved"
    
    def process_operator(self, text):
        self.update_table(text, "Operator")
        return "operators"
        
    def process_delimiter(self, text):
        self.update_table(text, "Delimiter")
        return "Delimiters"
    
    def process_identifier(self, text):
        self.update_table(text, "Identifier")
        return "Identifier"
    
    def process_functions(self, text):
        self.update_table(text, "Functions")
        return "Function"
    
    def process_header(self, text):
        self.update_table(text.replace("#include", "").lstrip(), "Header")
        return "Header"

    def process_number(self, text):
        self.update_table(text, "Number")
        return "Number"
    
    def process_macro(self, text):
        self.update_table(text.replace("#define", "").lstrip(), "Macro")
        return "Macro"
    
   
    def process_semicolon(self, text):
        self.update_table(";", "Delimiters")
        global prev_token, error_count, error_text
        file, line, col = self.position()
        
        if prev_token[1] in ["{", "(", ">", "<", ",", "=", "+=", "-=", "/=", "*=", "%=","*","&","~","!", "!=", "%", ">", "<", ">=", "<=", "==", "&&", "+", "-"]:
            print prev_token,"Unexpected semicolon ';' at ", line, ",", col
            error_count+=1

    def update_table(self, text, type="Unknown"):
        if not self.symbol_table.has_key(text):
            self.symbol_table[text] = {
                "type": type,
                "count": 1
            }
        else:
            self.symbol_table[text]["count"] += 1
    
    def update_string(self, text):
        global token_string
        token_string += text
        return token_string

    def end_string(self, text):
        global token_string
        self.update_table(token_string, "String")
        token_string = ""
        self.begin('')


    # plex matching library
    lexicon = Lexicon([
        (variable + Str("(") + re(".*") + Str(")"), process_functions),        
        (header, process_header),
        (define, process_macro),
        (Str(";") + Eol, process_semicolon),
        (reserved,  process_reserved),
        (operators, process_operator),
        (delimiters, process_delimiter),
        (variable, process_identifier),
        (number, process_number),
        (space  , IGNORE),
        (Str("/*"), begin_comment),
        (Str("//"), begin_comment),
        (Str("\""), Begin('str_double_quotes')),
        (Str("\'"), Begin('str_single_quotes')),


        State('str_double_quotes', [
            (Str("\""),   end_string),
            (Str("\n") | Eol, handle_error),
            (AnyChar,     update_string)
        ]),
        
        State('str_single_quotes', [
            (Str("'"),   end_string),
            (Str("\n") | Eol, handle_error),
            (AnyChar,     update_string)
        ]),
        
        State('single_comment', [
            (Str("\n"),   Begin('')),
            (AnyChar,     IGNORE)
        ]),
        State('multiline_comment', [
            (Str("*/"),   Begin('')),
            (AnyChar,     IGNORE)
        ])
    ])


filename = "text.c"
f = open(filename, "r")
scanner = MyScanner(f, filename)

while 1:
    try:
        token = scanner.read()
        # print token
        if token[0] is None:
            
            file, line, col = scanner.position()
            
            if scanner.state_name == "multiline_comment":
                print "Unexpected end of file, expected end of comment at ",line, ",", col+1
                error_count+=1

            if scanner.state_name == "str_double_quotes":
                print "Unexpected end of file, expected end of string at ",line, ",", (col+1)
                error_count+=1
            
            if scanner.state_name == "str_single_quotes":
                print "Unexpected end of file, expected end of string at ",line, ",", (col+1)
                error_count+=1

            break
        prev_token = token
        
    except Exception as e:
        name, line, col = scanner.position()
        print name, line ,col, e
        

print "\n"
print "\t\t\t\tResult: "
print 

print "{:10} {:20} {:20} {:5} ".format("","Lexicon type", "Lexicon", "No. of occurance")

for key in scanner.symbol_table.keys():
    print "{:10} {:20} {:20} {:5} ".format("",scanner.symbol_table[key]["type"],key, scanner.symbol_table[key]["count"])

print  error_count, " error(s)"
