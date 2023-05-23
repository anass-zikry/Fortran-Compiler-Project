import re

def get_regex_groups(line):
    m = header_regex(line)
    if m:
        return m.groups()
    m = implicit_regex(line)
    if m:
        return m.groups()
    m = constant_Type_decl_no_chart_regex(line)
    if m:
        return m.groups()
    m = char_constant_type_decl1(line)
    if m:
        return m.groups()
    m = char_constant_type_decl2(line)
    if m:
        return m.groups()
    m = do_regex(line)
    if m:
        return m.groups()
    m = Type_decl_no_char_regex(line)
    if m:
        return m.groups()
    m = char_type_decl_regex(line)
    if m:
        return m.groups()
    m = read_regex(line)
    if m:
        return m.groups()
    m = print1_regex(line)
    if m:
        return m.groups()
    m = print2_regex(line)
    if m:
        return m.groups()
    m = assignment_regex(line)
    if m:
        return m.groups()
    m = if_regex(line)
    if m:
        return m.groups()
    
    
    
def header_regex(line):


    return re.match("^\s*(program)?\s+([a-z]\w*)?\s*$",line)

def implicit_regex(line):
    return re.match("^\s*(implicit)?\s+(none)?\s*$",line)

def constant_Type_decl_no_chart_regex(line): #appple
    return re.match("^\s*(integer|real|complex|logical)?\s*(?:(,)?\s*(parameter)?)\s*(::)?\s*([a-z]\w*)?\s*(=)?\s*(?:(-|\+)?(?:[0-9]+|(-|\+)?[0-9]+.?[0-9]*|(?:(\()?\s*(-|\+)?([0-9]+.[0-9]+)?\s*(,)\s*(-|\+)?([0-9]+.[0-9]+)?\s*(\))?)|(.true.|.false.))?)\s*$",line)
    
def char_constant_type_decl1(line):
    return re.match("^\s*(character)?\s*(?:(\()?\s*(len)?\s*(=)?\s*([a-z]\w*|[1-9][0-9]*)?\s*(\))?)?\s*(?:(,)?\s*(parameter)?)\s*(::)?\s*([a-z]w*)?\s*(=)?\s*(\'(?:[\w()*&^%$@!{}[\]~`?/\\|,.#<>+=:;-_\\\s])*\')?\s*$",line)


def char_constant_type_decl2(line):
    return re.match("^\s*(character)?\s*(?:(\()?\s*(len)?\s*(=)?\s*([a-z]\w*|[1-9][0-9]*)?\s*(\))?)?\s*(?:(,)?\s*(parameter)?)\s*(::)?\s*([a-z]w*)?\s*(=)?\s*(\"(?:[\w()*&^%$@!{}[\]~`?/\\|,.#<>+=:;-_\\\s])*\")?\s*$",line)


def do_regex(line) :
  return re.match( "^\s*(do)?\s+([a-z]\w*)?\s*(=)?\s*((-|\+)?(\d+)|(\d+\.\d+))?\s*(,)?\s*([a-z]\w*|(-|\+)?(\d+)|(\d+\.\d+))?\s*(?:(,)?\s*([a-z]\w*|(-|\+)?(\d+)|(\d+\.\d+))?)?\s*$",line)

def Type_decl_no_char_regex(line):
    if re.match("^\s*(integer|real|complex|logical)?\s*\s*(::)?\s*([a-z]\w*)?\s*(?:(,)\s*([a-z]\w*))*\s*$",line):

        # le = "integer::x,y,z,o"
        c=line.count(",")
        rep=''
        for i in range(c):
            rep += '(?:(,)\s*([a-z]\w*))'

        return re.match("^\s*(integer|real|complex|logical)?\s*\s*(::)?\s*([a-z]\w*)?\s*"+rep+"\s*$", line)

    
    
    
def char_type_decl_regex(line):
   # le = "character (len =80) ::x,y,z"

   if re.match("^\s*(character)?\s*(?:(\()?\s*(len)?\s*(=)?\s*([a-z]\w*|[1-9]\d*)?\s*(\)))?\s*(::)?\s*([a-z]\w*)?\s*(?:(,)\s*([a-z]\w*))*\s*$",line):

        c=line.count(",")
        rep=''
        for i in range(c):
            rep += '(?:(,)\s*([a-z]\w*))'

        return re.match("^\s*(character)?\s*(?:(\()?\s*(len)?\s*(=)?\s*([a-z]\w*|[1-9]\d*)?\s*(\)))?\s*(::)?\s*([a-z]\w*)?\s*"+rep+"\s*$", line)

def read_regex(line):
    if re.match("^\s*(read)?\s*(\*)?\s*(,)?\s*([a-z]\w*)?\s*(,)?\s*\s*(?:(,)\s*([a-z]\w*))*\s*$",line):

    # le = "read*,x,y,z"
        c=line.count(",")
        rep=''
        for i in range(c-1):
            rep += '(?:(,)\s*([a-z]\w*))'
    

        return re.match("^\s*(read)?\s*(\*)?\s*(,)?\s*([a-z]\w*)?\s*(,)?\s*\s*"+rep+"\s*$", line)
    
    
def print1_regex(line):
    if re.match("^\s*(print)?\s*(\*)?\s*(?:(,)?\s*((?:[a-z]\w*|(\d+)|(\d+\.\d+)|\'(?:[\w()*&^%$@!{}[\]~`?/\\|,.#<>+=:;-_\s])*\')))*\s*$",line):

        # le = "print*,x,y,'z'"
        c=line.count(",")
        rep=''
        for i in range(c):
            rep += '(?:(,)\s*((?:[a-z]\w*|(\d+)|(\d+\.\d+)|\'(?:[\w()*&^%$@!{}[\]~`?/\\|,.#<>+=:;-_\s])*\')))'
        

        return re.match("^\s*(print)?\s*(\*)?\s*"+rep+"\s*$", line)
    

def print2_regex(line):
    if re.match("^\s*(print)?\s*(\*)?\s*(?:(,)?\s*((?:[a-z]\w*|(\d+)|(\d+\.\d+)|\"(?:[\w()*&^%$@!{}[\]~`?/\\|,.#<>+=:;-_\s])*\")))*\s*$",line):

        # le = 'print*,x,y,"z"'
        c=line.count(",")
        rep=''
        for i in range(c):
            rep += '(?:(,)\s*((?:[a-z]\w*|(\d+)|(\d+\.\d+)|\"(?:[\w()*&^%$@!{}[\]~`?/\\|,.#<>+=:;-_\s])*\")))'

        return re.match("^\s*(print)?\s*(\*)?\s*"+rep+"\s*$", line)
    
    
def assignment_regex(line):
    if re.match("^\s*([a-z]\w*)?\s*(=)?\s*(?:(?:([a-z]\w*)?|(\d+)?|(\d+\.\d+)?)(?:\s*([\*/\-\+])\s*(?:([a-z]\w*)|(\d+)|(\d+\.\d+)))*|(\.true\.|\.false\.)?)\s*$",line):

        #le = "x=5+7-8+9.9"
        c=line.count("+")
        c=c+line.count("-")
        c=c+line.count("*")
        c=c+line.count("/")
        rep=''
        for i in range(c):
            rep += '(?:\s*([\*/\-\+])\s*(?:([a-z]\w*)|(\d+)|(\d+\.\d+)))'
        

        return re.match("^\s*([a-z]\w*)?\s*(=)?\s*(?:(?:([a-z]\w*)?|(\d+)?|(\d+\.\d+)?)"+rep+"|(\.true\.|\.false\.)?)\s*$", line)

    
    
def if_regex(line):
        #le = "if(x==9>0<10>=7<=9/=77) then"

     if re.match("^\s*(if)?\s*(\()\s*(?:([a-z]\w*)?|([0-9]+)?)\s*(?:(<|>|<=|>=|==|/=)\s*(([a-z]\w*)|[0-9]+)|([a-z]\w*)|(\.true|false\.|))*\s*(\))?\s*(then)?\s*",line):

        c=0
        j=0
        for i in range(len(line)):
            
            if(re.match("(<|>|=|/)",line[i])):
                if(line[i+1]=="="):
                    i+=1
                    c+=1
                elif re.match("(<|>)",line[i]):

                    c+=1

        

        rep=''
        for i in range(c):
            rep += '(?:(<|>|<=|>=|==|/=)\s*(([a-z]\w*)|[0-9]+)|([a-z]\w*)|(\.true|false\.|))'
        

        return re.match("^\s*(if)?\s*(\()\s*(?:([a-z]\w*)?|([0-9]+)?)\s*"+rep+"\s*(\))?\s*(then)?\s*", line)

    
    

    
    
    

    