import tkinter as tk
import pandas
import pandastable as pt
from Scanner import find_token,get_Dicts,getToken_type,Operators
from nltk.tree import *
from dfa_test import get_reserver_dict ,get_identfier_dfa,get_operator_dfa,get_string_dfa,get_constant_dfa
import re 

reserve_DFAs,DFA_order_dict=get_reserver_dict()
identfier_dfa=get_identfier_dfa()
string_dfa=get_string_dfa()
operators_dfa=get_operator_dfa()
constant_dfa=get_constant_dfa()
Token_type=[]
Tokens=[] 
Errors=[]
#Integer Regex : /^integer\s*::\s*([a-zA-Z][a-zA-Z0-9]*)\s*(,\s*([a-zA-Z][a-zA-Z0-9]*))*\s*$/gm
# /^(integer|real|complex|logical)\s*::\s*([a-zA-Z][a-zA-Z0-9]*)\s*(,\s*([a-zA-Z][a-zA-Z0-9]*))*\s*$/gm
#💀💀💀💀💀💀💀💀💀💀💀

comment_indeces=[]
comment_token=0
def skip_comments():
    global Tokens
    for i in range(len(Tokens)):
        if Tokens[i].to_dict()['token_type'] == Token_type.ExclMark :
            global comment_indeces
            comment_indeces.append(i)
    for commentIndex in comment_indeces:
        global comment_token
        comment_token=Tokens.pop(commentIndex)

def add_comments():
    for commentIndex in comment_indeces:
        Tokens.insert(commentIndex,comment_token)
def Match(TT,i) :
    out = dict()
    if(i<len(Tokens)) :
        TokDict=Tokens[i].to_dict()
        if(TokDict['token_type'] == TT) :
            i+=1
            out['node'] = [TokDict['Lex']]
            out['index']=i
            return out
        else:
            out['node']=['error']
            if Tokens[i]!=Token_type.delimiter:
                while i < len(Tokens):
                    if Tokens[i].to_dict()['token_type']==Token_type.delimiter :
                        i+=1
                        break
                    i+=1
            out['index']=i
            Errors.append("Syntax Error: "+TokDict['Lex']+"==>Expected:"+str(TT))
            return out
    else :
        out['node']=['error']
        out['index']=i
        return out



#💀💀💀💀💀💀💀💀💀💀💀

# def Parse():
#     i = 0
#     ProgramStartDict = ProgramStart(i)
#     Parse_Node=Tree("")
#     return ProgramStartDict


def ProgramStart():
    i=0
    # ProgramStart_Dict = dict()
    ProgramStart_Children = []
    Dict1 = ProgramUnit(i)
    ProgramStart_Children.append(Dict1['node'])
    Dict2 = ProgramStart2(Dict1['index'])
    ProgramStart_Children.append(Dict2['node'])
    if None in ProgramStart_Children:
        ProgramStart_Children.remove(None)
    ProgramStart_Node = Tree("ProgramStart", ProgramStart_Children)
    return ProgramStart_Node


def ProgramStart2(i):
    ProgramStart2_Dict = dict()
    ProgramStart2_Children = []
    if i < len(Tokens):
        Temp = Tokens[i].to_dict()
        if Temp['token_type'] == Token_type.program:
            Dict1 = ProgramUnit(i)
            ProgramStart2_Children.append(Dict1['node'])
            Dict2 = ProgramStart2(Dict1['index'])
            ProgramStart2_Children.append(Dict2['node'])
            ProgramStart2_Node = Tree("ProgramStart2", ProgramStart2_Children)
            ProgramStart2_Dict['node'] = ProgramStart2_Node
            ProgramStart2_Dict['index'] = Dict2['index']
            return ProgramStart2_Dict
        else:
            match1 = Match(Token_type.Error, i)
            ProgramStart2_Children.append(match1['node'])
            ProgramStart2_Node = Tree("ProgramStart2", ProgramStart2_Children)
            ProgramStart2_Dict['node'] = ProgramStart2_Node
            ProgramStart2_Dict['index'] = match1['index']
            return ProgramStart2_Dict
    else:
        ProgramStart2_Dict['node'] = None
        ProgramStart2_Dict['index'] = i
        return ProgramStart2_Dict


def ProgramUnit(i):
    ProgramUnit_dict = dict()
    ProgramUnit_children = []
    dict1 = Header(i)
    ProgramUnit_children.append(dict1['node'])
    dict2 = Block(dict1['index'])
    ProgramUnit_children.append(dict2['node'])
    dict3 = Footer(dict2['index'])
    ProgramUnit_children.append(dict3['node'])
    ProgramUnit_node = Tree("ProgramUnit", ProgramUnit_children)
    ProgramUnit_dict['node'] = ProgramUnit_node
    ProgramUnit_dict['index'] = dict3['index']
    return ProgramUnit_dict


def Header(i):
    Header_dict = dict()
    Header_children = []
    match1 = Match(Token_type.program, i)
    Header_children.append(match1['node'])
    match2 = Match(Token_type.identifier, match1['index'])
    Header_children.append(match2['node'])
    match3 = Match(Token_type.delimiter, match2['index'])
    Header_children.append(match3['node'])
    Header_node = Tree("Header", Header_children)
    Header_dict['node'] = Header_node
    Header_dict['index'] = match3['index']
    return Header_dict


def Block(i):
    Block_dict = dict()
    Block_children = []
    match1 = Match(Token_type.implicit, i)
    Block_children.append(match1['node'])
    match2 = Match(Token_type.none, match1['index'])
    Block_children.append(match2['node'])
    match3 = Match(Token_type.delimiter, match2['index'])
    Block_children.append(match3['node'])
    dict4 = TypeDecls(match3['index'])
    Block_children.append(dict4['node'])
    dict5 = Statements(dict4['index'])
    Block_children.append(dict5['node'])
    Block_node = Tree("Block", Block_children)
    Block_dict['node'] = Block_node
    Block_dict['index'] = dict5['index']
    return Block_dict


def Footer(i):
    Footer_dict = dict()
    Footer_children = []
    match1 = Match(Token_type.end, i)
    Footer_children.append(match1['node'])
    match2 = Match(Token_type.program, match1['index'])
    Footer_children.append(match2['node'])
    match3 = Match(Token_type.identifier, match2['index'])
    Footer_children.append(match3['node'])
    match4 = Match(Token_type.delimiter, match3['index'])
    Footer_children.append(match4['node'])
    Footer_node = Tree("Footer", Footer_children)
    Footer_dict['node'] = Footer_node
    Footer_dict['index'] = match4['index']
    return Footer_dict


def TypeDecls(i):
    TypeDecls_dict = dict()
    TypeDecls_children = []
    last_index = i
    if i < len(Tokens):
        Temp = Tokens[i].to_dict()
        ############################################
        if Temp['token_type'] in [Token_type.integer, Token_type.real, Token_type.Complex, Token_type.logical, Token_type.character]:
            dict1 = TypeDecl(i)
            TypeDecls_children.append(dict1['node'])
            dict2 = TypeDecls2(dict1['index'])
            TypeDecls_children.append(dict2['node'])
            if None in TypeDecls_children:
                TypeDecls_children.remove(None)
            last_index = dict2['index']
        else:
            TypeDecls_dict['node'] = None
            TypeDecls_dict['index'] = i
            return TypeDecls_dict
    else:
        match1 = Match(Token_type.Error, i)
        TypeDecls_children.append(match1['node'])
        last_index = match1['index']

    TypeDecls_node = Tree("TypeDecls", TypeDecls_children)
    TypeDecls_dict['node'] = TypeDecls_node
    TypeDecls_dict['index'] = last_index
    return TypeDecls_dict


def TypeDecls2(i):
    TypeDecls2_dict = dict()
    TypeDecls2_children = []
    last_index = i
    if i < len(Tokens):
        Temp = Tokens[i].to_dict()
        ############################################
        if Temp['token_type'] in [Token_type.integer, Token_type.real, Token_type.Complex, Token_type.logical, Token_type.character]:
            dict1 = TypeDecl(i)
            TypeDecls2_children.append(dict1['node'])
            dict2 = TypeDecls2(dict1['index'])
            TypeDecls2_children.append(dict2['node'])
            if None in TypeDecls2_children:
                TypeDecls2_children.remove(None)
            last_index = dict2['index']
        else:
            TypeDecls2_dict['node'] = None
            TypeDecls2_dict['index'] = i
            return TypeDecls2_dict
    else:
        match1 = Match(Token_type.Error, i)
        TypeDecls2_children.append(match1['node'])
        last_index = match1['index']

    TypeDecls2_node = Tree("TypeDecls2", TypeDecls2_children)
    TypeDecls2_dict['node'] = TypeDecls2_node
    TypeDecls2_dict['index'] = last_index
    return TypeDecls2_dict


def TypeDecl(i):
    TypeDecl_dict = dict()
    TypeDecl_children = []
    dict1 = DataType(i)
    TypeDecl_children.append(dict1['node'])
    dict2 = TypeDecl2(dict1['index'])
    TypeDecl_children.append(dict2['node'])
    TypeDecl_node = Tree("TypeDecl", TypeDecl_children)
    TypeDecl_dict['node'] = TypeDecl_node
    TypeDecl_dict['index'] = dict2['index']
    return TypeDecl_dict


def TypeDecl2(i):
    TypeDecl2_dict = dict()
    TypeDecl2_children = []
    last_index = i
    if i < len(Tokens):
        temp = Tokens[i].to_dict()
        if temp['token_type'] == Token_type.VarDeclOp:
            match1 = Match(Token_type.VarDeclOp, i)
            TypeDecl2_children.append(match1['node'])
            dict2 = IdentifierList(match1['index'])
            TypeDecl2_children.append(dict2['node'])
            match3 = Match(Token_type.delimiter, dict2['index'])
            TypeDecl2_children.append(match3['node'])
            last_index = match3['index']
        elif temp['token_type'] == Token_type.Comma:
            match1 = Match(Token_type.Comma, i)
            TypeDecl2_children.append(match1['node'])
            match2 = Match(Token_type.parameter, match1['index'])
            TypeDecl2_children.append(match2['node'])
            match3 = Match(Token_type.VarDeclOp, match2['index'])
            TypeDecl2_children.append(match3['node'])
            dict4 = NamedConstant(match3['index'])
            TypeDecl2_children.append(dict4['node'])
            match5 = Match(Token_type.delimiter, dict4['index'])
            TypeDecl2_children.append(match5['node'])
            last_index = match5['index']
        else:
            match1 = Match(Token_type.Error, i)
            TypeDecl2_children.append(match1['node'])
            last_index = match1['index']
    else:
        match1 = Match(Token_type.Error, i)
        TypeDecl2_children.append(match1['node'])
        last_index = match1['index']
    TypeDecl2_node = Tree("TypeDecl2", TypeDecl2_children)
    TypeDecl2_dict['node'] = TypeDecl2_node
    TypeDecl2_dict['index'] = last_index
    return TypeDecl2_dict


def DataType(i):
    DataType_dict = dict()
    DataType_children = []
    last_index = i
    if i < len(Tokens):
        temp = Tokens[i].to_dict()
        if temp['token_type'] == Token_type.integer:
            match1 = Match(Token_type.integer, i)
            DataType_children.append(match1['node'])
            last_index = match1['index']
        elif temp['token_type'] == Token_type.real:
            match1 = Match(Token_type.real, i)
            DataType_children.append(match1['node'])
            last_index = match1['index']
        elif temp['token_type'] == Token_type.Complex:
            match1 = Match(Token_type.Complex, i)
            DataType_children.append(match1['node'])
            last_index = match1['index']
        elif temp['token_type'] == Token_type.logical:
            match1 = Match(Token_type.logical, i)
            DataType_children.append(match1['node'])
            last_index = match1['index']
        elif temp['token_type'] == Token_type.character:
            dict1 = CharacterDType(i)
            DataType_children.append(dict1['node'])
            last_index = dict1['index']
        else:
            match1 = Match(Token_type.Error, i)
            DataType_children.append(match1['node'])
            last_index = match1['index']

    else:
        match1 = Match(Token_type.Error, i)
        DataType_children.append(match1['node'])
        last_index = match1['index']
    DataType_node = Tree("DataType", DataType_children)
    DataType_dict['node'] = DataType_node
    DataType_dict['index'] = last_index
    return DataType_dict


def NamedConstant(i):
    NamedConstant_dict = dict()
    NamedConstant_children = []
    match1 = Match(Token_type.identifier, i)
    NamedConstant_children.append(match1['node'])
    match2 = Match(Token_type.EqualOp, match1['index'])
    NamedConstant_children.append(match2['node'])
    dict3 = NamedConstant2(match2['index'])
    NamedConstant_children.append(dict3['node'])
    NamedConstant_node = Tree("NamedConstant", NamedConstant_children)
    NamedConstant_dict['node'] = NamedConstant_node
    NamedConstant_dict['index'] = dict3['index']
    return NamedConstant_dict
def NamedConstant2(i):
    NamedConstant2_dict=dict()
    NamedConstant2_children=[]
    last_index=i
    if i<len(Tokens):
        temp=Tokens[i].to_dict()
        if temp['token_type'] in [Token_type.true,Token_type.false,Token_type.constant]:
            dict1=LogicalOrConst(i)
            NamedConstant2_children.append(dict1['node'])
            last_index=dict1['index']
        elif temp['token_type'] == Token_type.openParenthesis :
            dict1=ComplexNotation(i)
            NamedConstant2_children.append(dict1['node'])
            last_index=dict1['index']
    else :
        match1=Match(Token_type.Error,i)
        NamedConstant2_children.append(match1['node'])
        last_index=match1['index']
    NamedConstant2_node=Tree("NamedConstant2",NamedConstant2_children)
    NamedConstant2_dict['node']=NamedConstant2_node
    NamedConstant2_dict['index']=last_index
    return NamedConstant2_dict
        
    
def CharacterDType(i):
    CharacterDType_dict = dict()
    CharacterDType_children = []
    match1 = Match(Token_type.character, i)
    CharacterDType_children.append(match1['node'])
    dict2 = CharacterDType2(match1['index'])
    CharacterDType_children.append(dict2['node'])
    if None in CharacterDType_children:
        CharacterDType_children.remove(None)
    CharacterDType_node = Tree("CharacterDType", CharacterDType_children)
    CharacterDType_dict['node'] = CharacterDType_node
    CharacterDType_dict['index'] = dict2['index']
    return CharacterDType_dict


def CharacterDType2(i):
    CharacterDType2_dict = dict()
    CharacterDType2_children = []
    last_index = i
    if i < len(Tokens):
        temp = Tokens[i].to_dict()
        if temp['token_type'] == Token_type.openParenthesis:
            match1 = Match(Token_type.openParenthesis, i)
            CharacterDType2_children.append(match1['node'])
            match2 = Match(Token_type.Len, match1['index'])
            CharacterDType2_children.append(match2['node'])
            match3 = Match(Token_type.EqualOp, match2['index'])
            CharacterDType2_children.append(match3['node'])
            dict4 = IdorConst(match3['index'])
            CharacterDType2_children.append(dict4['node'])
            match5 = Match(Token_type.closeParenthesis, dict4['index'])
            CharacterDType2_children.append(match5['node'])
            last_index = match5['index']
        else:
            CharacterDType2_dict['node'] = None
            CharacterDType2_dict['index'] = i
            return CharacterDType2_dict
    else:
        match1 = Match(Token_type.Error, i)
        CharacterDType2_children.append(match1['node'])
        last_index = match1['index']
    CharacterDType2_node = Tree("CharacterDType2", CharacterDType2_children)
    CharacterDType2_dict['node'] = CharacterDType2_node
    CharacterDType2_dict['index'] = last_index
    return CharacterDType2_dict


def Statements(i):
    Statements_dict = dict()
    Statements_children = []
    dict1 = Statement(i)
    Statements_children.append(dict1['node'])
    dict2 = Statements2(dict1['index'])
    Statements_children.append(dict2['node'])
    if None in Statements_children:
        Statements_children.remove(None)
    Statements_node = Tree("Statements", Statements_children)
    Statements_dict['node'] = Statements_node
    Statements_dict['index'] = dict2['index']
    return Statements_dict


def Statements2(i):
    Statements2_dict = dict()
    Statements2_children = []
    last_index = i
    if i < len(Tokens):
        temp = Tokens[i].to_dict()
        #################################################
        if temp['token_type'] in [Token_type.identifier, Token_type.Print, Token_type.read, Token_type.If, Token_type.do]:
            dict1 = Statement(i)
            Statements2_children.append(dict1['node'])
            dict2 = Statements2(dict1['index'])
            Statements2_children.append(dict2['node'])
            if None in Statements2_children:
                Statements2_children.remove(None)
            last_index = dict2['index']

        else:
            Statements2_dict['node'] = None
            Statements2_dict['index'] = i
            return Statements2_dict
    else:
        match1 = Match(Token_type.Error, i)
        Statements2_children.append(match1['node'])
        last_index = match1['index']
    Statements2_node = Tree("Statements2", Statements2_children)
    Statements2_dict['node'] = Statements2_node
    Statements2_dict['index'] = last_index
    return Statements2_dict


def Statement(i):
    Statement_dict = dict()
    Statement_children = []
    last_index = i
    if i < len(Tokens):
        temp = Tokens[i].to_dict()
        if temp['token_type'] == Token_type.identifier:
            dict1 = Assignment(i)
            Statement_children.append(dict1['node'])
            last_index = dict1['index']
        elif temp['token_type'] == Token_type.Print:
            dict1 = Print(i)
            Statement_children.append(dict1['node'])
            last_index = dict1['index']
        elif temp['token_type'] == Token_type.read:
            dict1 = Read(i)
            Statement_children.append(dict1['node'])
            last_index = dict1['index']
        elif temp['token_type'] == Token_type.If:
            dict1 = If(i)
            Statement_children.append(dict1['node'])
            last_index = dict1['index']
        elif temp['token_type'] == Token_type.do:
            dict1 = DoLoop(i)
            Statement_children.append(dict1['node'])
            last_index = dict1['index']
        else:
            Statement_dict['node'] = None
            Statement_dict['index'] = i
            return Statement_dict
    else:
        match1 = Match(Token_type.Error, i)
        Statement_children.append(match1['node'])
        last_index = match1['index']
    Statement_node = Tree("Statement", Statement_children)
    Statement_dict['node'] = Statement_node
    Statement_dict['index'] = last_index
    return Statement_dict


def Assignment(i):
    Assignment_dict = dict()
    Assignment_children = []
    match1 = Match(Token_type.identifier, i)
    Assignment_children.append(match1['node'])
    match2 = Match(Token_type.EqualOp, match1['index'])
    Assignment_children.append(match2['node'])
    dict3 = Relations(match2['index'])
    Assignment_children.append(dict3['node'])
    match4 = Match(Token_type.delimiter, dict3['index'])
    Assignment_children.append(match4['node'])
    Assignment_node = Tree("Assignment", Assignment_children)
    Assignment_dict['node'] = Assignment_node
    Assignment_dict['index'] = match4['index']
    return Assignment_dict


def Relations(i):
    Relations_dict = dict()
    Relations_children = []
    last_index = i
    if i < len(Tokens):
        temp = Tokens[i].to_dict()
        #################################################
        if temp['token_type'] in [Token_type.identifier, Token_type.constant]:
            dict1 = Expression(i)
            Relations_children.append(dict1['node'])
            # dict2 = Relation(dict1['index'])
            # Relations_children.append(dict2['node'])
            if None in Relations_children:
                Relations_children.remove(None)
            last_index = dict1['index']
        elif temp['token_type'] in [Token_type.true, Token_type.false]:
            dict1 = LogicalVal(i)
            Relations_children.append(dict1['node'])
            last_index = dict1['index']
        elif temp['token_type'] == Token_type.openParenthesis:
            dict1=ComplexNotation(i)
            Relations_children.append(dict1['node'])
            last_index=dict1['index']
        else:
            match1 = Match(Token_type.Error, i)
            Relations_children.append(match1['node'])
            last_index = match1['index']
    else:
        match1 = Match(Token_type.Error, i)
        Relations_children.append(match1['node'])
        last_index = match1['index']
    Relations_node = Tree("Relations", Relations_children)
    Relations_dict['node'] = Relations_node
    Relations_dict['index'] = last_index
    return Relations_dict

def Expression(i):
    Expression_dict=dict()
    Expression_children=[]
    dict1=MultTerm(i)
    Expression_children.append(dict1['node'])
    dict2=Expression2(dict1['index'])
    Expression_children.append(dict2['node'])
    if None in Expression_children:
        Expression_children.remove(None)
    Expression_node=Tree("Expression",Expression_children)
    Expression_dict['node']=Expression_node
    Expression_dict['index']=dict2['index']
    return Expression_dict

def Expression2(i):
    Expression2_dict=dict()
    Expression2_children=[]
    last_index=i
    if i<len(Tokens):
        temp=Tokens[i].to_dict()
        if temp['token_type'] in [Token_type.MinusOp,Token_type.PlusOp]:
            dict1=AddOp(i)
            Expression2_children.append(dict1['node'])
            dict2=MultTerm(dict1['index'])
            Expression2_children.append(dict2['node'])
            dict3=Expression2(dict2['index'])
            Expression2_children.append(dict3['node'])
            if None in Expression2_children :
                Expression2_children.remove(None)
            last_index=dict3['index']
        else:
            Expression2_dict['node']=None
            Expression2_dict['index']=i
            return Expression2_dict
    else:
        match1=Match(Token_type.Error,i)
        Expression2_children.append(match1['node'])
        last_index=match1['index']
    Expression2_node=Tree("Expression2",Expression2_children)
    Expression2_dict['node']=Expression2_node
    Expression2_dict['index']=last_index
    return Expression2_dict

def MultTerm(i):
    MultTerm_dict=dict()
    MultTerm_children=[]
    dict1=IdorConst(i)
    MultTerm_children.append(dict1['node'])
    dict2=MultTerm2(dict1['index'])
    MultTerm_children.append(dict2['node'])
    if None in MultTerm_children:
        MultTerm_children.remove(None)
    MultTerm_node=Tree("MultTerm",MultTerm_children)
    MultTerm_dict['node']=MultTerm_node
    MultTerm_dict['index']=dict2['index']
    return MultTerm_dict

def MultTerm2(i):
    MultTerm2_dict=dict()
    MultTerm2_children=[]
    last_index=i
    if i<len(Tokens):
        temp=Tokens[i].to_dict()
        if temp['token_type'] in [Token_type.MultiplyOp,Token_type.DivideOp] :
            dict1=MultOp(i)
            MultTerm2_children.append(dict1['node'])
            dict2=IdorConst(dict1['index'])
            MultTerm2_children.append(dict2['node'])
            dict3=MultTerm2(dict2['index'])
            MultTerm2_children.append(dict3['node'])
            if None in MultTerm2_children:
                MultTerm2_children.remove(None)
            last_index=dict3['index']
        else:
            MultTerm2_dict['node']=None
            MultTerm2_dict['index']=i
            return MultTerm2_dict
    else:
        match1=Match(Token_type.Error,i)
        MultTerm2_children.append(match1['node'])
        last_index=match1['index']
    MultTerm2_node=Tree("MultTerm2",MultTerm2_children)
    MultTerm2_dict['node']=MultTerm2_node
    MultTerm2_dict['index']=last_index
    return MultTerm2_dict

# def Relation(i):
#     Relation_dict = dict()
#     Relation_children = []
#     last_index = i
#     if i < len(Tokens):
#         temp = Tokens[i].to_dict()
#         #################################################
#         if temp['token_type'] in [Token_type.PlusOp, Token_type.MultiplyOp, Token_type.MinusOp, Token_type.DivideOp]:
#             dict1 = ArithmeticOp(i)
#             Relation_children.append(dict1['node'])
#             dict2 = IdorConst(dict1['index'])
#             Relation_children.append(dict2['node'])
#             dict3 = Relation2(dict2['index'])
#             Relation_children.append(dict3['node'])
#             if None in Relation_children:
#                 Relation_children.remove(None)
#             last_index = dict3['index']

#         else:
#             Relation_dict['node'] = None
#             Relation_dict['index'] = i
#             return Relation_dict
#     else:
#         match1 = Match(Token_type.Error, i)
#         Relation_children.append(match1['node'])
#         last_index = match1['index']
#     Relation_node = Tree("Relation", Relation_children)
#     Relation_dict['node'] = Relation_node
#     Relation_dict['index'] = last_index
#     return Relation_dict


# def Relation2(i):
#     Relation2_dict = dict()
#     Relation2_children = []
#     last_index = i
#     if i < len(Tokens):
#         temp = Tokens[i].to_dict()
#         #################################################
#         if temp['token_type'] in [Token_type.PlusOp, Token_type.MultiplyOp, Token_type.MinusOp, Token_type.DivideOp]:
#             dict1 = ArithmeticOp(i)
#             Relation2_children.append(dict1['node'])
#             dict2 = IdorConst(dict1['index'])
#             Relation2_children.append(dict2['node'])
#             dict3 = Relation2(dict2['index'])
#             Relation2_children.append(dict3['node'])
#             if None in Relation2_children:
#                 Relation2_children.remove(None)
#             last_index = dict3['index']

#         else:
#             Relation2_dict['node'] = None
#             Relation2_dict['index'] = i
#             return Relation2_dict
#     else:
#         match1 = Match(Token_type.Error, i)
#         Relation2_children.append(match1['node'])
#         last_index = match1['index']
#     Relation_node = Tree("Relation", Relation2_children)
#     Relation2_dict['node'] = Relation_node
#     Relation2_dict['index'] = last_index
#     return Relation2_dict


def Print(i):
    Print_dict = dict()
    Print_children = []
    match1 = Match(Token_type.Print, i)
    Print_children.append(match1['node'])
    match2 = Match(Token_type.MultiplyOp, match1['index'])
    Print_children.append(match2['node'])
    dict3 = PrintCall(match2['index'])
    Print_children.append(dict3['node'])
    match4 = Match(Token_type.delimiter, dict3['index'])
    Print_children.append(match4['node'])
    if None in Print_children:
        Print_children.remove(None)
    Print_node = Tree("Print", Print_children)
    Print_dict['node'] = Print_node
    Print_dict['index'] = match4['index']
    return Print_dict


def PrintCall(i):
    PrintCall_dict = dict()
    PrintCall_children = []
    last_index = i
    if i < len(Tokens):
        temp = Tokens[i].to_dict()
        #################################################
        if temp['token_type'] == Token_type.Comma:
            match1 = Match(Token_type.Comma, i)
            PrintCall_children.append(match1['node'])
            dict2 = PrintList(match1['index'])
            PrintCall_children.append(dict2['node'])
            last_index = dict2['index']

        else:
            PrintCall_dict['node'] = None
            PrintCall_dict['index'] = i
            return PrintCall_dict
    else:
        match1 = Match(Token_type.Error, i)
        PrintCall_children.append(match1['node'])
        last_index = match1['index']
    PrintCall_node = Tree("PrintCall", PrintCall_children)
    PrintCall_dict['node'] = PrintCall_node
    PrintCall_dict['index'] = last_index
    return PrintCall_dict


def PrintList(i):
    PrintList_dict = dict()
    PrintList_children = []
    dict1 = PrintHolder(i)
    PrintList_children.append(dict1['node'])
    dict2 = PrintList2(dict1['index'])
    PrintList_children.append(dict2['node'])
    if None in PrintList_children:
        PrintList_children.remove(None)
    PrintList_node = Tree("PrintList", PrintList_children)
    PrintList_dict['node'] = PrintList_node
    PrintList_dict['index'] = dict2['index']
    return PrintList_dict


def PrintList2(i):
    PrintList2_dict = dict()
    PrintList2_children = []
    last_index = i
    if i < len(Tokens):
        temp = Tokens[i].to_dict()
        #################################################
        if temp['token_type'] == Token_type.Comma:
            match1 = Match(Token_type.Comma, i)
            PrintList2_children.append(match1['node'])
            dict2 = PrintHolder(match1['index'])
            PrintList2_children.append(dict2['node'])
            dict3 = PrintList2(dict2['index'])
            PrintList2_children.append(dict3['node'])
            if None in PrintList2_children:
                PrintList2_children.remove(None)
            last_index = dict3['index']

        else:
            PrintList2_dict['node'] = None
            PrintList2_dict['index'] = i
            return PrintList2_dict
    else:
        match1 = Match(Token_type.Error, i)
        PrintList2_children.append(match1['node'])
        last_index = match1['index']
    PrintList2_node = Tree("PrintList2", PrintList2_children)
    PrintList2_dict['node'] = PrintList2_node
    PrintList2_dict['index'] = last_index
    return PrintList2_dict


def PrintHolder(i):
    PrintHolder_dict = dict()
    PrintHolder_children = []
    last_index = i
    if i < len(Tokens):
        temp = Tokens[i].to_dict()
        #################################################
        if temp['token_type'] == Token_type.identifier:
            match1 = Match(Token_type.identifier, i)
            PrintHolder_children.append(match1['node'])
            last_index = match1['index']
        elif temp['token_type'] == Token_type.constant:
            match1 = Match(Token_type.constant, i)
            PrintHolder_children.append(match1['node'])
            last_index = match1['index']
        elif temp['token_type'] == Token_type.string:
            match1 = Match(Token_type.string, i)
            PrintHolder_children.append(match1['node'])
            last_index = match1['index']
        else:
            PrintHolder_dict['node'] = None
            PrintHolder_dict['index'] = i
            return PrintHolder_dict
    else:
        match1 = Match(Token_type.Error, i)
        PrintHolder_children.append(match1['node'])
        last_index = match1['index']
    PrintHolder_node = Tree("PrintHolder", PrintHolder_children)
    PrintHolder_dict['node'] = PrintHolder_node
    PrintHolder_dict['index'] = last_index
    return PrintHolder_dict


def Read(i):
    Read_dict = dict()
    Read_children = []
    match1 = Match(Token_type.read, i)
    Read_children.append(match1['node'])
    match2 = Match(Token_type.MultiplyOp, match1['index'])
    Read_children.append(match2['node'])
    match3 = Match(Token_type.Comma, match2['index'])
    Read_children.append(match3['node'])
    dict4 = IdentifierList(match3['index'])
    Read_children.append(dict4['node'])
    match5 = Match(Token_type.delimiter, dict4['index'])
    Read_children.append(match5['node'])
    Read_node = Tree("Read", Read_children)
    Read_dict['node'] = Read_node
    Read_dict['index'] = match5['index']
    return Read_dict


def If(i):
    If_dict = dict()
    If_children = []
    dict1 = IfStart(i)
    If_children.append(dict1['node'])
    dict2 = If2(dict1['index'])
    If_children.append(dict2['node'])
    If_node = Tree("If", If_children)
    If_dict['node'] = If_node
    If_dict['index'] = dict2['index']
    return If_dict


def If2(i):
    If2_dict = dict()
    If2_children = []
    last_index = i
    if i < len(Tokens):
        temp = Tokens[i].to_dict()
        #################################################
        if temp['token_type'] == Token_type.end:
            match1 = Match(Token_type.end, i)
            If2_children.append(match1['node'])
            match2 = Match(Token_type.If, match1['index'])
            If2_children.append(match2['node'])
            match3 = Match(Token_type.delimiter, match2['index'])
            If2_children.append(match3['node'])
            last_index = match3['index']
        elif temp['token_type'] == Token_type.Else:
            match1 = Match(Token_type.Else, i)
            If2_children.append(match1['node'])
            match2 = Match(Token_type.delimiter, match1['index'])
            If2_children.append(match2['node'])
            dict3 = Statements(match2['index'])
            If2_children.append(dict3['node'])
            match4 = Match(Token_type.end, dict3['index'])
            If2_children.append(match4['node'])
            match5 = Match(Token_type.If, match4['index'])
            If2_children.append(match5['node'])
            match6 = Match(Token_type.delimiter, match5['index'])
            If2_children.append(match6['node'])
            last_index = match6['index']
        else:
            match1 = Match(Token_type.Error, i)
            If2_children.append(match1['node'])
            last_index = match1['index']
    else:
        match1 = Match(Token_type.Error, i)
        If2_children.append(match1['node'])
        last_index = match1['index']
    If2_node = Tree("If2", If2_children)
    If2_dict['node'] = If2_node
    If2_dict['index'] = last_index
    return If2_dict


def IfStart(i):
    IfStart_dict = dict()
    IfStart_children = []
    match1 = Match(Token_type.If, i)
    IfStart_children.append(match1['node'])
    match2 = Match(Token_type.openParenthesis, match1['index'])
    IfStart_children.append(match2['node'])
    dict3 = Conditional(match2['index'])
    IfStart_children.append(dict3['node'])
    match4 = Match(Token_type.closeParenthesis, dict3['index'])
    IfStart_children.append(match4['node'])
    match5 = Match(Token_type.then, match4['index'])
    IfStart_children.append(match5['node'])
    match6 = Match(Token_type.delimiter, match5['index'])
    IfStart_children.append(match6['node'])
    dict7 = Statements(match6['index'])
    IfStart_children.append(dict7['node'])
    IfStart_node = Tree("IfStart", IfStart_children)
    IfStart_dict['node'] = IfStart_node
    IfStart_dict['index'] = dict7['index']
    return IfStart_dict


def DoLoop(i):
    DoLoop_dict = dict()
    DoLoop_children = []
    dict1 = DoStart(i)
    DoLoop_children.append(dict1['node'])
    dict2 = Statements(dict1['index'])
    DoLoop_children.append(dict2['node'])
    match3 = Match(Token_type.end, dict2['index'])
    DoLoop_children.append(match3['node'])
    match4 = Match(Token_type.do, match3['index'])
    DoLoop_children.append(match4['node'])
    match5 = Match(Token_type.delimiter, match4['index'])
    DoLoop_children.append(match5['node'])
    DoLoop_node = Tree("DoLoop", DoLoop_children)
    DoLoop_dict['node'] = DoLoop_node
    DoLoop_dict['index'] = match5['index']
    return DoLoop_dict


def DoStart(i):
    DoStart_dict = dict()
    DoStart_children = []
    match1 = Match(Token_type.do, i)
    DoStart_children.append(match1['node'])
    match2 = Match(Token_type.identifier, match1['index'])
    DoStart_children.append(match2['node'])
    match3 = Match(Token_type.EqualOp, match2['index'])
    DoStart_children.append(match3['node'])
    dict4 = IdorConst(match3['index'])
    DoStart_children.append(dict4['node'])
    match5 = Match(Token_type.Comma, dict4['index'])
    DoStart_children.append(match5['node'])
    dict6 = IdorConst(match5['index'])
    DoStart_children.append(dict6['node'])
    dict7 = Step(dict6['index'])
    DoStart_children.append(dict7['node'])
    match8 = Match(Token_type.delimiter, dict7['index'])
    DoStart_children.append(match8['node'])
    if None in DoStart_children:
        DoStart_children.remove(None)
    DoStart_node = Tree("DoStart", DoStart_children)
    DoStart_dict['node'] = DoStart_node
    DoStart_dict['index'] = match8['index']
    return DoStart_dict


def Step(i):
    Step_dict = dict()
    Step_children = []
    last_index = i
    if i < len(Tokens):
        temp = Tokens[i].to_dict()
        if temp['token_type'] == Token_type.Comma:
            match1 = Match(Token_type.Comma, i)
            Step_children.append(match1['node'])
            dict2 = IdorConst(match1['index'])
            Step_children.append(dict2['node'])
            last_index = dict2['index']
        else:
            Step_dict['node'] = None
            Step_dict['index'] = i
            return Step_dict

    else:
        match1 = Match(Token_type.Error, i)
        Step_children.append(match1['node'])
        last_index = match1['index']
    Step_node = Tree("Step", Step_children)
    Step_dict['node'] = Step_node
    Step_dict['index'] = last_index
    return Step_dict


# def ArithmeticOp(i):
#     ArithmeticOp_dict = dict()
#     ArithmeticOp_children = []
#     last_index = i
#     if i < len(Tokens):
#         temp = Tokens[i].to_dict()
#         if temp['token_type'] == Token_type.MultiplyOp:
#             match1 = Match(Token_type.MultiplyOp, i)
#             ArithmeticOp_children.append(match1['node'])
#             last_index = match1['index']
#         elif temp['token_type'] == Token_type.DivideOp:
#             match1 = Match(Token_type.DivideOp, i)
#             ArithmeticOp_children.append(match1['node'])
#             last_index = match1['index']
#         elif temp['token_type'] == Token_type.PlusOp:
#             match1 = Match(Token_type.PlusOp, i)
#             ArithmeticOp_children.append(match1['node'])
#             last_index = match1['index']
#         elif temp['token_type'] == Token_type.MinusOp:
#             match1 = Match(Token_type.MinusOp, i)
#             ArithmeticOp_children.append(match1['node'])
#             last_index = match1['index']
#         else:
#             match1 = Match(Token_type.Error, i)
#             ArithmeticOp_children.append(match1['node'])
#             last_index = match1['index']

#     else:
#         match1 = Match(Token_type.Error, i)
#         ArithmeticOp_children.append(match1['node'])
#         last_index = match1['index']
#     ArithmeticOp_node = Tree("ArithmeticOp")
#     ArithmeticOp_dict['node'] = ArithmeticOp_node
#     ArithmeticOp_dict['index']
#     return ArithmeticOp_dict

def MultOp(i):
    MultOp_dict=dict()
    MultOp_children=[]
    last_index=i
    if i<len(Tokens):
        temp=Tokens[i].to_dict()
        if temp['token_type'] == Token_type.MultiplyOp:
            match1=Match(Token_type.MultiplyOp,i)
            MultOp_children.append(match1['node'])
            last_index=match1['index']
        elif temp['token_type'] == Token_type.DivideOp:
            match1=Match(Token_type.DivideOp,i)
            MultOp_children.append(match1['node'])
            last_index=match1['index']
        else:
            match1 = Match(Token_type.Error, i)
            MultOp_children.append(match1['node'])
            last_index = match1['index']
    else:
        match1 = Match(Token_type.Error, i)
        MultOp_children.append(match1['node'])
        last_index = match1['index']
    MultOp_node=Tree("MultOp",MultOp_children)
    MultOp_dict['node']=MultOp_node
    MultOp_dict['index']=last_index
    return MultOp_dict

def AddOp(i):
    AddOp_dict=dict()
    AddOp_children=[]
    last_index=i
    if i<len(Tokens):
        temp=Tokens[i].to_dict()
        if temp['token_type'] == Token_type.PlusOp:
            match1=Match(Token_type.PlusOp,i)
            AddOp_children.append(match1['node'])
            last_index=match1['index']
        elif temp['token_type'] == Token_type.MinusOp:
            match1=Match(Token_type.MinusOp,i)
            AddOp_children.append(match1['node'])
            last_index=match1['index']
        else:
            match1 = Match(Token_type.Error, i)
            AddOp_children.append(match1['node'])
            last_index = match1['index']
    else:
        match1 = Match(Token_type.Error, i)
        AddOp_children.append(match1['node'])
        last_index = match1['index']
    MultOp_node=Tree("AddOp",AddOp_children)
    AddOp_dict['node']=MultOp_node
    AddOp_dict['index']=last_index
    return AddOp_dict

def IdentifierList(i):
    IdentifierList_dict = dict()
    IdentifierList_children = []
    match1 = Match(Token_type.identifier, i)
    IdentifierList_children.append(match1['node'])
    dict2 = IdentifierList2(match1['index'])
    IdentifierList_children.append(dict2['node'])
    if None in IdentifierList_children:
        IdentifierList_children.remove(None)
    IdentifierList_node = Tree("IdentifierList", IdentifierList_children)
    IdentifierList_dict['node'] = IdentifierList_node
    IdentifierList_dict['index'] = dict2['index']
    return IdentifierList_dict


def IdentifierList2(i):
    IdentifierList2_dict = dict()
    IdentifierList2_children = []
    last_index = i
    if i < len(Tokens):
        temp = Tokens[i].to_dict()
        if temp['token_type'] == Token_type.Comma:
            match1 = Match(Token_type.Comma, i)
            IdentifierList2_children.append(match1['node'])
            match2 = Match(Token_type.identifier, match1['index'])
            IdentifierList2_children.append(match2['node'])
            dict3 = IdentifierList2(match2['index'])
            IdentifierList2_children.append(dict3['node'])
            if None in IdentifierList2_children:
                IdentifierList2_children.remove(None)
            last_index = dict3['index']

        else:
            IdentifierList2_dict['node'] = None
            IdentifierList2_dict['index'] = i
            return IdentifierList2_dict

    else:
        match1 = Match(Token_type.Error, i)
        IdentifierList2_children.append(match1['node'])
        last_index = match1['index']
    IdentifierList2_node = Tree("IdentifierList2", IdentifierList2_children)
    IdentifierList2_dict['node'] = IdentifierList2_node
    IdentifierList2_dict['index'] = last_index
    return IdentifierList2_dict


def Conditional(i):
    Conditional_dict = dict()
    Conditional_children = []
    last_index = i
    if i < len(Tokens):
        temp = Tokens[i].to_dict()
        if temp['token_type'] in [Token_type.identifier, Token_type.constant]:
            dict1 = BooleanExp(i)
            Conditional_children.append(dict1['node'])
            last_index = dict1['index']
        elif temp['token_type'] == Token_type.identifier:
            match1 = Match(Token_type.identifier, i)
            Conditional_children.append(match1['node'])
            last_index = match1['index']
        elif temp['token_type'] in [Token_type.true, Token_type.false]:
            dict1 = LogicalVal(i)
            Conditional_children.append(dict1['node'])
            last_index = dict1['index']
        else:
            match1 = Match(Token_type.Error, i)
            Conditional_children.append(match1['node'])
            last_index = match1['index']
    else:
        match1 = Match(Token_type.Error, i)
        Conditional_children.append(match1['node'])
        last_index = match1['index']
    Conditional_node = Tree("Conditional", Conditional_children)
    Conditional_dict['node'] = Conditional_node
    Conditional_dict['index'] = last_index
    return Conditional_dict

def BooleanExp(i):
    BooleanExp_dict = dict()
    BooleanExp_children = []
    dict1=RelationalTerm(i)
    BooleanExp_children.append(dict1['node'])
    dict2=BooleanExp2(dict1['index'])
    BooleanExp_children.append(dict2['node'])
    if None in BooleanExp_children:
        BooleanExp_children.remove(None)
    BooleanExp_node=Tree("BooleanExp",BooleanExp_children)
    BooleanExp_dict['node']=BooleanExp_node
    BooleanExp_dict['index']=dict2['index']
    return BooleanExp_dict

def BooleanExp2(i):
    BooleanExp2_dict = dict()
    BooleanExp2_children = []
    last_index = i
    if i < len(Tokens):
        temp = Tokens[i].to_dict()
        if temp['token_type'] in [Token_type.EqualEqualOp, Token_type.NotEqualOp]:
            dict1 = EqualityOp(i)
            BooleanExp2_children.append(dict1['node'])
            dict2=RelationalTerm(dict1['index'])
            BooleanExp2_children.append(dict2['node'])
            dict3=BooleanExp2(dict2['index'])
            BooleanExp2_children.append(dict3['node'])
            last_index = dict3['index']
        else:
            BooleanExp2_dict['node'] = None
            BooleanExp2_dict['index'] = i
            return BooleanExp2_dict
    else:
        match1 = Match(Token_type.Error, i)
        BooleanExp2_children.append(match1['node'])
        last_index = match1['index']
    if None in BooleanExp2_children:
        BooleanExp2_children.remove(None)
    BooleanExp2_node = Tree("BooleanExp2", BooleanExp2_children)
    BooleanExp2_dict['node'] = BooleanExp2_node
    BooleanExp2_dict['index'] = last_index
    return BooleanExp2_dict

def RelationalTerm(i):
    RelationalTerm_dict = dict()
    RelationalTerm_children = []
    dict1=Expression(i)
    RelationalTerm_children.append(dict1['node'])
    dict2=RelationalTerm2(dict1['index'])
    RelationalTerm_children.append(dict2['node'])
    if None in RelationalTerm_children:
        RelationalTerm_children.remove(None)
    RelationalTerm_node=Tree("RelationalTerm",RelationalTerm_children)
    RelationalTerm_dict['node']=RelationalTerm_node
    RelationalTerm_dict['index']=dict2['index']
    return RelationalTerm_dict

def RelationalTerm2(i):
    RelationalTerm2_dict = dict()
    RelationalTerm2_children = []
    last_index = i
    if i < len(Tokens):
        temp = Tokens[i].to_dict()
        if temp['token_type'] in [Token_type.GreaterThanOp, Token_type.LessThanOp,Token_type.LessThanEqualOp,Token_type.GreaterThanEqualOp]:
            dict1 = RelationalOp(i)
            RelationalTerm2_children.append(dict1['node'])
            dict2=Expression(dict1['index'])
            RelationalTerm2_children.append(dict2['node'])
            dict3=RelationalTerm2(dict2['index'])
            RelationalTerm2_children.append(dict3['node'])
            last_index = dict3['index']
        else:
            RelationalTerm2_dict['node'] = None
            RelationalTerm2_dict['index'] = i
            return RelationalTerm2_dict
    else:
        match1 = Match(Token_type.Error, i)
        RelationalTerm2_children.append(match1['node'])
        last_index = match1['index']
    if None in RelationalTerm2_children:
        RelationalTerm2_children.remove(None)
    RelationalTerm2_node = Tree("RelationalTerm2", RelationalTerm2_children)
    RelationalTerm2_dict['node'] = RelationalTerm2_node
    RelationalTerm2_dict['index'] = last_index
    return RelationalTerm2_dict

def EqualityOp(i):
    EqualityOp_dict = dict()
    EqualityOp_children = []
    last_index = i
    if i < len(Tokens):
        temp = Tokens[i].to_dict()
        if temp['token_type'] == Token_type.EqualEqualOp:
            match1 = Match(Token_type.EqualEqualOp, i)
            EqualityOp_children.append(match1['node'])
            last_index = match1['index']
        elif temp['token_type'] == Token_type.NotEqualOp:
            match1 = Match(Token_type.NotEqualOp, i)
            EqualityOp_children.append(match1['node'])
            last_index = match1['index']
        else:
            match1 = Match(Token_type.Error, i)
            EqualityOp_children.append(match1['node'])
            last_index = match1['index']
    else:
        match1 = Match(Token_type.Error, i)
        EqualityOp_children.append(match1['node'])
        last_index = match1['index']
    EqualityOp_node = Tree("EqualityOp", EqualityOp_children)
    EqualityOp_dict['node'] = EqualityOp_node
    EqualityOp_dict['index'] = last_index
    return EqualityOp_dict

def ComplexNotation(i):
    ComplexNotation_dict=dict()
    ComplexNotation_children=[]
    match1=Match(Token_type.openParenthesis,i)
    ComplexNotation_children.append(match1['node'])
    dict2=NegorPos(match1['index'])
    ComplexNotation_children.append(dict2['node'])
    match3=Match(Token_type.constant,dict2['index'])
    ComplexNotation_children.append(match3['node'])
    match4=Match(Token_type.Comma,match3['index'])
    ComplexNotation_children.append(match4['node'])
    dict5=NegorPos(match4['index'])
    ComplexNotation_children.append(dict5['node'])
    match6=Match(Token_type.constant,dict5['index'])
    ComplexNotation_children.append(match6['node'])
    match7=Match(Token_type.closeParenthesis,match6['index'])
    ComplexNotation_children.append(match7['node'])
    if None in ComplexNotation_children:
        ComplexNotation_children.remove(None)
    ComplexNotation_node=Tree("ComplexNotation",ComplexNotation_children)
    ComplexNotation_dict['node']=ComplexNotation_node
    ComplexNotation_dict['index']=match7['index']
    return ComplexNotation_dict

def IdorConst(i):
    IdorConst_dict = dict()
    IdorConst_children = []
    dict1=NegorPos(i)
    IdorConst_children.append(dict1['node'])
    dict2=IdorConst2(dict1['index'])
    IdorConst_children.append(dict2['node'])
    if None in IdorConst_children:
        IdorConst_children.remove(None)
    IdorConst_node=Tree("IdorConst",IdorConst_children)
    IdorConst_dict['node']=IdorConst_node
    IdorConst_dict['index']=dict2['index']
    return IdorConst_dict

def IdorConst2(i):
    IdorConst2_dict = dict()
    IdorConst2_children = []
    last_index = i
    if i < len(Tokens):
        temp = Tokens[i].to_dict()
        if temp['token_type'] == Token_type.identifier:
            match1 = Match(Token_type.identifier, i)
            IdorConst2_children.append(match1['node'])
            last_index = match1['index']
        elif temp['token_type'] == Token_type.constant:
            match1 = Match(Token_type.constant, i)
            IdorConst2_children.append(match1['node'])
            last_index = match1['index']

        else:
            match1 = Match(Token_type.Error, i)
            IdorConst2_children.append(match1['node'])
            last_index = match1['index']
    else:
        match1 = Match(Token_type.Error, i)
        IdorConst2_children.append(match1['node'])
        last_index = match1['index']
    IdorConst2_node = Tree("IdorConst2", IdorConst2_children)
    IdorConst2_dict['node'] = IdorConst2_node
    IdorConst2_dict['index'] = last_index
    return IdorConst2_dict


def RelationalOp(i):
    RelationalOp_dict = dict()
    RelationalOp_children = []
    last_index = i
    if i < len(Tokens):
        temp = Tokens[i].to_dict()
        if temp['token_type'] == Token_type.GreaterThanOp:
            match1 = Match(Token_type.GreaterThanOp, i)
            RelationalOp_children.append(match1['node'])
            last_index = match1['index']
        elif temp['token_type'] == Token_type.LessThanOp:
            match1 = Match(Token_type.LessThanOp, i)
            RelationalOp_children.append(match1['node'])
            last_index = match1['index']
        elif temp['token_type'] == Token_type.LessThanEqualOp:
            match1 = Match(Token_type.LessThanEqualOp, i)
            RelationalOp_children.append(match1['node'])
            last_index = match1['index']
        elif temp['token_type'] == Token_type.GreaterThanEqualOp:
            match1 = Match(Token_type.GreaterThanEqualOp, i)
            RelationalOp_children.append(match1['node'])
            last_index = match1['index']
        elif temp['token_type'] == Token_type.EqualEqualOp:
            match1 = Match(Token_type.EqualEqualOp, i)
            RelationalOp_children.append(match1['node'])
            last_index = match1['index']
        elif temp['token_type'] == Token_type.NotEqualOp:
            match1 = Match(Token_type.NotEqualOp, i)
            RelationalOp_children.append(match1['node'])
            last_index = match1['index']
        else:
            match1 = Match(Token_type.Error, i)
            RelationalOp_children.append(match1['node'])
            last_index = match1['index']
    else:
        match1 = Match(Token_type.Error, i)
        RelationalOp_children.append(match1['node'])
        last_index = match1['index']
    RelationalOp_node = Tree("RelationalOp", RelationalOp_children)
    RelationalOp_dict['node'] = RelationalOp_node
    RelationalOp_dict['index'] = last_index
    return RelationalOp_dict


# def LogicalOrIdentifier(i):
#     LogicalOrIdentifier_dict = dict()
#     LogicalOrIdentifier_children = []
#     last_index = i
#     if i < len(Tokens):
#         temp = Tokens[i].to_dict()
#         if temp['token_type'] in [Token_type.true, Token_type.false]:
#             dict1 = LogicalVal(i)
#             LogicalOrIdentifier_children.append(dict1['node'])
#             last_index = dict1['index']
#         elif temp['token_type'] == Token_type.identifier:
#             dict1 = IdentifierList(i)
#             LogicalOrIdentifier_children.append(dict1['node'])
#             last_index = dict1['index']
#         else:
#             match1 = Match(Token_type.Error, i)
#             LogicalOrIdentifier_children.append(match1['node'])
#             last_index = match1['index']
#     else:
#         match1 = Match(Token_type.Error, i)
#         LogicalOrIdentifier_children.append(match1['node'])
#         last_index = match1['index']
#     LogicalOrIdentifier_node = Tree(
#         "LogicalOrIdentifier", LogicalOrIdentifier_children)
#     LogicalOrIdentifier_dict['node'] = LogicalOrIdentifier_node
#     LogicalOrIdentifier_dict['index'] = last_index
#     return LogicalOrIdentifier_dict


def LogicalOrConst(i):
    LogicalOrConst_dict = dict()
    LogicalOrConst_children = []
    last_index = i
    if i < len(Tokens):
        temp = Tokens[i].to_dict()
        if temp['token_type'] in [Token_type.true, Token_type.false]:
            dict1 = LogicalVal(i)
            LogicalOrConst_children.append(dict1['node'])
            last_index = dict1['index']
        elif temp['token_type'] == Token_type.constant:
            match1 = Match(Token_type.constant, i)
            LogicalOrConst_children.append(match1['node'])
            last_index = match1['index']
        else:
            match1 = Match(Token_type.Error, i)
            LogicalOrConst_children.append(match1['node'])
            last_index = match1['index']
    else:
        match1 = Match(Token_type.Error, i)
        LogicalOrConst_children.append(match1['node'])
        last_index = match1['index']
    LogicalOrConst_node = Tree("LogicalOrConst", LogicalOrConst_children)
    LogicalOrConst_dict['node'] = LogicalOrConst_node
    LogicalOrConst_dict['index'] = last_index
    return LogicalOrConst_dict


def LogicalVal(i):
    LogicalVal_dict = dict()
    LogicalVal_children = []
    last_index = i
    if i < len(Tokens):
        temp = Tokens[i].to_dict()
        if temp['token_type'] == Token_type.true:
            match1 = Match(Token_type.true, i)
            LogicalVal_children.append(match1['node'])
            last_index = match1['index']
        elif temp['token_type'] == Token_type.false:
            match1 = Match(Token_type.false, i)
            LogicalVal_children.append(match1['node'])
            last_index = match1['index']
        else:
            match1 = Match(Token_type.Error, i)
            LogicalVal_children.append(match1['node'])
            last_index = match1['index']
    else:
        match1 = Match(Token_type.Error, i)
        LogicalVal_children.append(match1['node'])
        last_index = match1['index']
    LogicalVal_node = Tree("LogicalVal", LogicalVal_children)
    LogicalVal_dict['node'] = LogicalVal_node
    LogicalVal_dict['index'] = last_index
    return LogicalVal_dict

def NegorPos(i):
    NegorPos_dict=dict()
    NegorPos_children=[]
    last_index=i
    if i<len(Tokens):
        temp=Tokens[i].to_dict()
        if temp['token_type']==Token_type.MinusOp:
            match1=Match(Token_type.MinusOp,i)
            NegorPos_children.append(match1['node'])
            last_index=match1['index']
        elif temp['token_type']==Token_type.PlusOp:
            match1=Match(Token_type.PlusOp,i)
            NegorPos_children.append(match1['node'])
            last_index=match1['index']
        else:
            NegorPos_dict['node']=None
            NegorPos_dict['index']=i
            return NegorPos_dict
    else:
        match1=Match(Token_type.Error,i)
        NegorPos_children.append(match1['node'])
        last_index=match1['index']
    NegorPos_node=Tree("NegorPos",NegorPos_children)
    NegorPos_dict['node']=NegorPos_node
    NegorPos_dict['index']=last_index
    return NegorPos_dict

#GUI
root= tk.Tk()
canvas1 = tk.Canvas(root, width=800, height=600, relief='raised',background='lightblue')
canvas1.pack()
label1 = tk.Label(root, text='Scan & Parse this file')
label1.config(font=('helvetica', 14),background='lightblue')
canvas1.create_window(400, 50, window=label1)
label2 = tk.Label(root, text='Source code file path:')
label2.config(font=('helvetica', 10),background='lightblue')
canvas1.create_window(400, 100, window=label2,anchor='center')
entry1 = tk.Entry(root,width=100)
canvas1.create_window(400, 140, window=entry1)
 
def Scan():
    filePath = entry1.get()
    with open(filePath) as f:
        lines=f.readlines()
    find_token(lines)
    global Token_type ,Tokens ,Errors
    ScannerData=get_Dicts()
    Token_type=getToken_type()
    Tokens=ScannerData[0]
    Errors=ScannerData[1]
    skip_comments()
    Node=ProgramStart()
    add_comments()
    showable_tokens=[]
    
    for t in Tokens : 
        t=t.to_dict() 
        if(t["token_type"]==Token_type.delimiter):
            continue
        else:
         showable_tokens.append(t)
         
    df=pandas.DataFrame.from_records([t for t in showable_tokens])
    # def update_buttons():
    #     for i, row in df.iterrows():
    #         button = tk.Button(root, text='DFA', command=lambda key= i: DFA_click(key))
    #         df.at[i, 'Button'] = button
    
    # update_buttons()
    #print(df)
    # def loop_dfa(tok,dfa_index):
    #     for i in range(len(tok["Lex"])):
    #         reserve_DFAs[dfa_index].show_diagram(input_str=tok['Lex'][:i],font_size=9, arrow_size=0.2,format_type='jpg',path="Diagrams/",filename=tok["Lex"])
    def DFA_click(Token_index):
        temp=showable_tokens[Token_index]
        if temp['token_type'] == Token_type.identifier :
            idntString=""
            for i in temp["Lex"]:
                if(re.match("[0-9]",i)):
                    idntString=idntString+"D"
                elif (re.match("[a-z]",i)):
                    idntString=idntString+"L"
                elif(i=="_"):
                    idntString=idntString+"_"
                    
            identfier_dfa.show_diagram(input_str=idntString,font_size=9, arrow_size=0.2,format_type='pdf',path="Diagrams/",filename=temp["Lex"],view=True)
        elif temp['token_type'] == Token_type.string :
        
            tok_string_string=""
            for i in temp["Lex"]:
                if(re.match("['\"]",i)):
                    tok_string_string=tok_string_string+i
                elif (re.match("[a-z]",i)):
                    tok_string_string=tok_string_string+"L"
                elif (re.match("[0-9]",i)):
                    tok_string_string=tok_string_string+"N"
                elif(re.match("[\$%#@!]",i)):
                    tok_string_string=tok_string_string+"Y"
                elif(re.match("\s",i)):
                    tok_string_string=tok_string_string+"S"
                  
            # print(tok_string_string)      
            string_dfa.show_diagram(input_str=tok_string_string,font_size=9, arrow_size=0.2,format_type='pdf',path="Diagrams/",filename=temp['Lex'],view=True)        
        elif temp['Lex'] in Operators:
            # print(temp['Lex'])
            operators_dfa.show_diagram(input_str=temp['Lex'],font_size=9, arrow_size=0.2,format_type='pdf',path="Diagrams/",filename="op",view=True)  
        elif temp['token_type'] == Token_type.constant :
            const_str=""
            for i in temp["Lex"]:
                if(re.match("[0-9]",i)):
                    const_str=const_str+"N"
                elif (re.match("[-\+\.]",i)):
                    const_str=const_str+i
                    
            constant_dfa.show_diagram(input_str=const_str,font_size=9, arrow_size=0.2,format_type='pdf',path="Diagrams/",filename="constant",view=True)
        else:
            dfa_index=DFA_order_dict[temp['Lex']]
            reserve_DFAs[dfa_index].show_diagram(input_str=temp['Lex'],font_size=9, arrow_size=0.2,format_type='pdf',path="Diagrams/",filename=temp["Lex"],view=True)
        
        # # loop_dfa(temp,dfa_index)
        # dfa_di=tk.Toplevel()
        # dfa_di.title(temp["Lex"])
        # img_label=tk.Label(dfa_di)
        # if temp['Lex'] in Operators:
        #     path="Diagrams/"+"op"+".jpg"
        # else:
        #  path="Diagrams/"+temp['Lex']+".jpg"
        # img = Image.open(fp=path, mode='r')
        # photo = ImageTk.PhotoImage(image=img)
        # img_label.config(image=photo)
        # img_label.image = photo
        # img_label.pack()
        # v1 = pdf.ShowPdf()
        # v2 = v1.pdf_view(dfa_di,pdf_location = r"Diagrams/"+temp['Lex']+".pdf", width = 800, height = 600)
        # v2.pack()

        # print("button clicked"+str(Token_index))
    
    #to display token stream as table
    dTDa1 = tk.Toplevel()
    dTDa1.title('Token Stream')
    dTDaPT = pt.Table(dTDa1, dataframe=df, showtoolbar=True, showstatusbar=True)
    # dTDaPT.addColumn(newname="DFA")
    dTDaPT.show()
    # start Parsing
    # Node=Parse()
    DFA_wind=tk.Toplevel()
    DFA_wind.title('DFA Diagrams')
    DFA_canvas=tk.Canvas(DFA_wind,scrollregion=(0,0,1000,1000))
    # vbar=tk.Scrollbar(DFA_canvas,orient=tk.VERTICAL)
    # vbar.pack(side=tk.RIGHT,fill=tk.Y)
    # vbar.config(command=tk.Canvas.yview)
    # DFA_canvas.config(width=300,height=300)
    # DFA_canvas.config( yscrollcommand=vbar.set)
    DFA_canvas.pack(side=tk.TOP,expand=True,fill=tk.BOTH)
    for i in range(len(showable_tokens)):
        if i %30 ==0 : 
            DFA_wind=tk.Toplevel()
            DFA_wind.title('DFA Diagrams')
            DFA_canvas.pack(side=tk.TOP,expand=True,fill=tk.BOTH)
        dfa_button=tk.Button(DFA_wind, text='DFA'+str(i+1), command=lambda key= i: DFA_click(key),padx=100)
        dfa_button.pack()
    # DFA_canvas.pack()
        
     
    # to display errorlist
    df1=pandas.DataFrame(Errors)
    dTDa2 = tk.Toplevel()
    dTDa2.title('Error List')
    dTDaPT2 = pt.Table(dTDa2, dataframe=df1, showtoolbar=True, showstatusbar=True)
    dTDaPT2.show()

    # leaves=Node.leaves()
    # print("Length:"+str(len(leaves)))
    # print(leaves)

    # print("type:"+ str(type(leaves[4])))
    # Node.pop(0)
    # print(Node.leaves())
    # nn=Node.t
    # print(nn)
    # frfl=Tree.fromstring()
    # for index,leaf in enumerate(leaves)  :
    #     if leaf == None :
    #         # print("NoneLeaf:"+str(leaf))
    #         treeIndex=Node.leaf_treeposition(index)
    #         print("trI"+str(treeIndex))
    #         Node.pop([treeIndex])
    #         # print("x="+str(x))
    Node.draw()
    #clear your list
    
    #label3 = tk.Label(root, text='Lexem ' + x1 + ' is:', font=('helvetica', 10))
    #canvas1.create_window(200, 210, window=label3)
    
    #label4 = tk.Label(root, text="Token_type"+x1, font=('helvetica', 10, 'bold'))
    #canvas1.create_window(200, 230, window=label4)
    
    
button1 = tk.Button(text='Scan', command=Scan, bg='green', fg='white', font=('helvetica', 10, 'bold'),padx=25,pady=10)
canvas1.create_window(600, 200, window=button1)
root.mainloop()