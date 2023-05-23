import re

def get_regex_groups(line):
    m = Type_decl_no_char(line)
    if m:
        return m.groups()
    m = Type_decl_no_char(line)
    if m:
        return m.groups()
    m = Type_decl_no_char(line)
    if m:
        return m.groups()
    
def header(line):
    return re.match("^\s*(program)\s+([a-z]\w*)\s*$",line)


def Type_decl_no_char(line):
    if re.match("^\s*(integer|real|complex|logical)\s*((,)\s*(parameter))?\s*(::)\s*([a-z]\w*)\s*(?:(,)\s*([a-z]\w*))*\s*$",line):
        # le = "integer::x,y,z,o"
        c=line.count(",")
        rep=''
        for i in range(c):
            rep += '(?:(,)\s*([a-z]\w*))'
        return re.match("^\s*(integer|real|complex|logical)\s*((,)\s*(parameter))?\s*(::)\s*([a-z]\w*)\s*"+rep+"\s*$", line)