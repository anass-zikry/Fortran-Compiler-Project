from enum import Enum
import re


class Token_type(Enum):  # listing all tokens type
    program = 1
    implicit = 2
    none = 3
    integer = 4
    real = 5
    Complex = 6
    logical = 7
    true = 8
    Semicolon = 9
    EqualOp = 10
    LessThanOp = 11
    GreaterThanOp = 12
    NotEqualOp = 13
    PlusOp = 14
    MinusOp = 15
    MultiplyOp = 16
    DivideOp = 17
    VarDeclOp = 18
    character = 19
    ExclMark = 20
    parameter = 21
    end = 22
    If = 23
    then = 24
    Else = 25
    do = 26
    string = 27
    read = 28
    Print = 29
    LessThanEqualOp = 30
    GreaterThanEqualOp = 31
    EqualEqualOp = 32
    constant = 33
    identifier = 34
    Error = 35
    Comma = 36
    Len = 37
    openParenthesis=38
    closeParenthesis=39
    false=40
    delimiter=41

# Reserved word Dictionary
ReservedWords = {
    "program": Token_type.program,
    "implicit": Token_type.implicit,
    "none": Token_type.none,
    "end": Token_type.end,
    "integer": Token_type.integer,
    "real": Token_type.real,
    "complex": Token_type.Complex,
    "logical": Token_type.logical,
    "character": Token_type.character,
    "parameter": Token_type.parameter,
    "if": Token_type.If,
    "then": Token_type.then,
    "else": Token_type.Else,
    "do": Token_type.do,
    "read": Token_type.read,
    "print": Token_type.Print,
    "len": Token_type.Len,
    ".true.":Token_type.true,
    ".false.":Token_type.false
}


Operators = {
    # ".": Token_type.Dot,
    # ";": Token_type.Semicolon,
    "=": Token_type.EqualOp,
    "+": Token_type.PlusOp,
    "-": Token_type.MinusOp,
    "*": Token_type.MultiplyOp,
    "/": Token_type.DivideOp,
    "::": Token_type.VarDeclOp,
    "!": Token_type.ExclMark,
    ">": Token_type.GreaterThanOp,
    "<": Token_type.LessThanOp,
    "<=": Token_type.LessThanEqualOp,
    ">=": Token_type.GreaterThanEqualOp,
    "/=": Token_type.NotEqualOp,
    "==": Token_type.EqualEqualOp,
    ",": Token_type.Comma,
    "(":Token_type.openParenthesis,
    ")":Token_type.closeParenthesis,
    "\n":Token_type.delimiter
}


# class token to hold string and token type
class token:
    def __init__(self, lex, token_type):
        self.lex = lex
        self.token_type = token_type

    def to_dict(self):
        return {
            'Lex': self.lex,
            'token_type': self.token_type
        }


Tokens=[]
Errors=[]

def find_token(text):
    for line in text :
        lexems = line.split()
        for le in lexems:
            if (le == '!'):
                new_token = token(le, Operators[le])
                Tokens.append(new_token)
                # break  #💀
            elif (le in ReservedWords):
                new_token = token(le, ReservedWords[le])
                Tokens.append(new_token)
            elif (le in Operators):
                new_token = token(le, Operators[le])
                Tokens.append(new_token)
            elif (re.match("^\d+(\.[0-9]*)?$", le)):
                new_token = token(le, Token_type.constant)
                Tokens.append(new_token)
            elif (re.match("^([a-zA-Z][a-zA-Z0-9]*)$", le)):
                new_token = token(le, Token_type.identifier)
                Tokens.append(new_token)
            elif (re.match("^\"[\w. ]+\"$", le) or re.match("^\'[\w. ]+\'$", le)):
                new_token = token(le, Token_type.string)
                Tokens.append(new_token)
            else:
                new_token = token(le, Token_type.Error)
                Errors.append("Lexical error  " + le)
        new_token=token("\n",Token_type.delimiter)
        Tokens.append(new_token)


def get_Dicts() :
    return (Tokens,Errors)

def getToken_type() :
    return Token_type
# #GUI
# root= tk.Tk()
# canvas1 = tk.Canvas(root, width=800, height=600, relief='raised')
# canvas1.pack()
# label1 = tk.Label(root, text='Scan & Parse this file')
# label1.config(font=('helvetica', 14))
# canvas1.create_window(350, 50, window=label1)
# label2 = tk.Label(root, text='Source code file path:')
# label2.config(font=('helvetica', 10))
# canvas1.create_window(300, 100, window=label2)
# entry1 = tk.Entry(root)
# canvas1.create_window(200, 140, window=entry1)

# def Scan():
#     filePath = entry1.get()
#     with open(filePath) as f:
#         lines=f.readlines()
#     print(lines)
#     find_token(lines)
#     df=pandas.DataFrame.from_records([t.to_dict() for t in Tokens])
#     #print(df)
    
#     #to display token stream as table
#     dTDa1 = tk.Toplevel()
#     dTDa1.title('Token Stream')
#     dTDaPT = pt.Table(dTDa1, dataframe=df, showtoolbar=True, showstatusbar=True)
#     dTDaPT.show()
#     # start Parsing
#     # Node=Parse()
#     Node=ProgramStart()
     
    
#     # to display errorlist
#     df1=pandas.DataFrame(Errors)
#     dTDa2 = tk.Toplevel()
#     dTDa2.title('Error List')
#     dTDaPT2 = pt.Table(dTDa2, dataframe=df1, showtoolbar=True, showstatusbar=True)
#     dTDaPT2.show()

#     # leaves=Node.leaves()
#     # print("Length:"+str(len(leaves)))
#     # print(leaves)

#     # print("type:"+ str(type(leaves[4])))
#     # Node.pop(0)
#     # print(Node.leaves())
#     # nn=Node.t
#     # print(nn)
#     # frfl=Tree.fromstring()
#     # for index,leaf in enumerate(leaves)  :
#     #     if leaf == None :
#     #         # print("NoneLeaf:"+str(leaf))
#     #         treeIndex=Node.leaf_treeposition(index)
#     #         print("trI"+str(treeIndex))
#     #         Node.pop([treeIndex])
#     #         # print("x="+str(x))
#     Node.draw()
#     #clear your list
    
#     #label3 = tk.Label(root, text='Lexem ' + x1 + ' is:', font=('helvetica', 10))
#     #canvas1.create_window(200, 210, window=label3)
    
#     #label4 = tk.Label(root, text="Token_type"+x1, font=('helvetica', 10, 'bold'))
#     #canvas1.create_window(200, 230, window=label4)
    
    
# button1 = tk.Button(text='Scan', command=Scan, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
# canvas1.create_window(200, 180, window=button1)
# root.mainloop()