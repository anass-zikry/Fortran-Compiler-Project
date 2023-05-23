

from automata.fa.dfa import DFA

from visual_automata.fa.dfa import VisualDFA

reserve_DFAs = []

"""## order of the list
 false 
 true 
 program 
 implicit 
 none 
 integer 
 real 
 complex 
 len 
 if 
 then 
 end 
 character 
 parameter 
 else 
 do 
 read 
 print 
 paranthis 

"""
DFA_order_dict = {
    "false": 0,
    "true": 1,
    "program": 2,
    "implicit": 3,
    "none": 4,
    "integer": 5,
    "real": 6,
    "complex": 7,
    "len": 8,
    "if": 9,
    "then": 10,
    "end": 11,
    "character": 12,
    "parameter": 13,
    "else": 14,
    "do": 15,
    "read": 16,
    "print": 17,
    "paranthis": 18,
    
}
dfa_identfier = VisualDFA(
    states={"q0", "q1", "q2"},
    input_symbols={"L", "D", "_", "other"},
    transitions={
        "q0": {"L": "q1", "other": "q2", "D": "q2", "_": "q2"},
        "q1": {"other": "q2", "L": "q1", "L": "q1", "_": "q1", "D": "q1"},
        "q2": {"other": "q2", "L": "q2", "L": "q2", "_": "q2", "D": "q2"},

    },
    initial_state="q0",
    final_states={"q1"},
)
dfa_identfier.show_diagram(font_size=9, arrow_size=0.2)
# list_of_DFAs.append(dfa_identfier)

dfa_false = VisualDFA(
    states={"q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "phi"},
    input_symbols={".", "f", "a", "l", "s", "e"},
    transitions={
        "q0": {".": "q1", **{i: "phi" for i in set(["f", "a", "l", "s", "e"])}},
        "q1": {"f": "q2", **{i: "phi" for i in set([".", "a", "l", "s", "e"])}},
        "q2": {"a": "q3", **{i: "phi" for i in set([".", "f", "l", "s", "e"])}},
        "q3": {"l": "q4", **{i: "phi" for i in set([".", "a", "f", "s", "e"])}},
        "q4": {"s": "q5", **{i: "phi" for i in set([".", "a", "l", "f", "e"])}},
        "q5": {"e": "q6", **{i: "phi" for i in set([".", "a", "l", "s", "f"])}},
        "q6": {".": "q7", **{i: "phi" for i in set(["f", "a", "l", "s", "e"])}},
        "q7": {**{i: "phi" for i in set([".", "f", "a", "l", "s", "e"])}},
        "phi": {**{i: "phi" for i in set([".", "f", "a", "l", "s", "e"])}},

    },
    initial_state="q0",
    final_states={"q7"},
)
# dfa_false.show_diagram(font_size=9,arrow_size=0.2)
reserve_DFAs.append(dfa_false)

dfa_true = VisualDFA(
    states={"q0", "q1", "q2", "q3", "q4", "q5", "q6", "phi"},
    input_symbols={".", "t", "r", "u", "e"},
    transitions={
        "q0": {".": "q1", **{i: "phi" for i in set(["t", "r", "u", "e"])}},
        "q1": {"t": "q2", **{i: "phi" for i in set([".", "r", "u", "e"])}},
        "q2": {"r": "q3", **{i: "phi" for i in set([".", "t", "u", "e",])}},
        "q3": {"u": "q4", **{i: "phi" for i in set([".", "t", "r", "e"])}},
        "q4": {"e": "q5", **{i: "phi" for i in set([".", "t", "r", "u"])}},
        "q5": {".": "q6", **{i: "phi" for i in set(["t", "r", "e", "u"])}},
        "q6": {**{i: "phi" for i in set([".", "t", "r", "e", "u"])}},
        "phi": {**{i: "phi" for i in set([".", "t", "r", "e", "u"])}},

    },
    initial_state="q0",
    final_states={"q6"},
)
# dfa_true.show_diagram(font_size=9,arrow_size=0.2)
reserve_DFAs.append(dfa_true)

dfa_program = VisualDFA(
    states={"q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "phi"},
    input_symbols={"p", "r", "o", "g", "a", "m"},
    transitions={
        "q0": {"p": "q1", **{i: "phi" for i in set(["r", "o", "g", "a", "m"])}},
        "q1": {"r": "q2", **{i: "phi" for i in set(["p", "o", "g", "a", "m"])}},
        "q2": {"o": "q3", **{i: "phi" for i in set(["p", "r", "g", "a", "m"])}},
        "q3": {"g": "q4", **{i: "phi" for i in set(["r", "o", "p", "a", "m"])}},
        "q4": {"r": "q5", **{i: "phi" for i in set(["p", "o", "g", "a", "m"])}},
        "q5": {"a": "q6", **{i: "phi" for i in set(["r", "o", "g", "p", "m"])}},
        "q6": {"m": "q7", **{i: "phi" for i in set(["r", "o", "g", "a", "p"])}},
        "q7": {**{i: "phi" for i in set(["p", "r", "o", "g", "a", "m"])}},
        "phi": {**{i: "phi" for i in set(["p", "r", "o", "g", "a", "m"])}},


    },
    initial_state="q0",
    final_states={"q7"},
)
# dfa_program.show_diagram(font_size=9,arrow_size=0.2)
reserve_DFAs.append(dfa_program)

dfa_implicit = VisualDFA(
    states={"q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "phi"},
    input_symbols={"i", "m", "p", "l", "c", "t"},
    transitions={
        "q0": {"i": "q1", **{i: "phi" for i in set(["m", "p", "l", "c", "t"])}},
        "q1": {"m": "q2", **{i: "phi" for i in set(["i", "p", "l", "c", "t"])}},
        "q2": {"p": "q3", **{i: "phi" for i in set(["i", "m", "l", "c", "t"])}},
        "q3": {"l": "q4", **{i: "phi" for i in set(["i", "m", "p", "c", "t"])}},
        "q4": {"i": "q5", **{i: "phi"for i in set(["m", "p", "l", "c", "t"])}},
        "q5": {"c": "q6", **{i: "phi" for i in set(["i", "m", "p", "l", "t"])}},
        "q6": {"i": "q7", **{i: "phi" for i in set(["m", "p", "l", "c", "t"])}},
        "q7": {"t": "q8", **{i: "phi" for i in set(["i", "m", "p", "l", "c"])}},
        "q8": {**{i: "phi" for i in set(["i", "m", "p", "l", "c", "t"])}},
        "phi": {**{i: "phi" for i in set(["i", "m", "p", "l", "c", "t"])}},
    },
    initial_state="q0",
    final_states={"q8"},
)
# dfa_implicit.show_diagram(font_size=9, arrow_size=0.2)
reserve_DFAs.append(dfa_implicit)

dfa_none = VisualDFA(
    states={"q0", "q1", "q2", "q3", "phi"},
    input_symbols={"n", "o", "n", "e"},
    transitions={
        "q0": {"n": "q1", **{i: "phi" for i in set(["o", "e"])}},
        "q1": {"o": "q2", **{i: "phi" for i in set(["n", "e"])}},
        "q2": {"n": "q3", **{i: "phi" for i in set(["o", "e"])}},
        "q3": {"e": "q3", **{i: "phi" for i in set(["n", "o"])}},
        "phi": {**{i: "phi" for i in set(["n", "o", "e"])}},
    },
    initial_state="q0",
    final_states={"q3"},
)
# dfa_none.show_diagram(font_size=9, arrow_size=0.2)
reserve_DFAs.append(dfa_none)

dfa_integer = VisualDFA(
    states={"q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "phi"},
    input_symbols={"i", "n", "t", "e", "g", "r"},
    transitions={
        "q0": {"i": "q1", **{i: "phi" for i in set(["n", "t", "e", "g", "r"])}},
        "q1": {"n": "q2", **{i: "phi" for i in set(["i", "t", "e", "g", "r"])}},
        "q2": {"t": "q3", **{i: "phi" for i in set(["i", "n", "e", "g", "r"])}},
        "q3": {"e": "q4", **{i: "phi" for i in set(["i", "n", "t", "g", "r"])}},
        "q4": {"g": "q5", **{i: "phi" for i in set(["i", "n", "t", "e", "r"])}},
        "q5": {"e": "q6", **{i: "phi" for i in set(["i", "n", "t", "g", "r"])}},
        "q6": {"r": "q7", **{i: "phi" for i in set(["i", "n", "t", "e", "g"])}},
        "q7": {**{i: "phi" for i in set(["i", "n", "t", "e", "g", "r"])}},
        "phi": {**{i: "phi" for i in set(["i", "n", "t", "e", "g", "r"])}},
    },
    initial_state="q0",
    final_states={"q7"},
)
# dfa_integer.show_diagram(font_size=9, arrow_size=0.2)
reserve_DFAs.append(dfa_integer)

dfa_real = VisualDFA(
    states={"q0", "q1", "q2", "q3", "q4", "phi"},
    input_symbols={"r", "e", "a", "l"},
    transitions={
        "q0": {"r": "q1", **{i: "phi" for i in set(["e", "a", "l"])}},
        "q1": {"e": "q2", **{i: "phi" for i in set(["r", "a", "l"])}},
        "q2": {"a": "q3", **{i: "phi" for i in set(["r", "e", "l"])}},
        "q3": {"l": "q4", **{i: "phi" for i in set(["r", "e", "a"])}},
        "q4": {**{i: "phi" for i in set(["r", "e", "a", "l"])}},
        "phi": {**{i: "phi" for i in set(["r", "e", "a", "l"])}},
    },
    initial_state="q0",
    final_states={"q4"},
)
# dfa_real.show_diagram(font_size=9, arrow_size=0.2)
reserve_DFAs.append(dfa_real)

dfa_complex = VisualDFA(
    states={"q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "phi"},
    input_symbols={"c", "o", "m", "p", "l", "e", "x"},
    transitions={
        "q0": {"c": "q1", **{i: "phi" for i in set(["o", "m", "p", "l", "e", "x"])}},
        "q1": {"o": "q2", **{i: "phi" for i in set(["c", "m", "p", "l", "e", "x"])}},
        "q2": {"m": "q3", **{i: "phi" for i in set(["c", "o", "p", "l", "e", "x"])}},
        "q3": {"p": "q4", **{i: "phi" for i in set(["c", "o", "m", "l", "e", "x"])}},
        "q4": {"l": "q5", **{i: "phi" for i in set(["c", "o", "m", "p", "e", "x"])}},
        "q5": {"e": "q6", **{i: "phi" for i in set(["c", "o", "m", "p", "l", "x"])}},
        "q6": {"x": "q7", **{i: "phi" for i in set(["c", "o", "m", "p", "l", "e"])}},
        "q7": {**{i: "phi" for i in set(["c", "o", "m", "p", "l", "e", "x"])}},
        "phi": {**{i: "phi" for i in set(["c", "o", "m", "p", "l", "e", "x"])}},
    },
    initial_state="q0",
    final_states={"q7"}
)
# dfa_complex.show_diagram(font_size=9, arrow_size=0.2)
reserve_DFAs.append(dfa_complex)

dfa_len = VisualDFA(
    states={"q0", "q1", "q2", "q3", "phi"},
    input_symbols={"l", "e", "n"},
    transitions={
        "q0": {"l": "q1", **{i: "phi" for i in set(["e", "n"])}},
        "q1": {"e": "q2", **{i: "phi" for i in set(["l", "n"])}},
        "q2": {"n": "q3", **{i: "phi" for i in set(["l", "e"])}},
        "q3": {**{i: "phi" for i in set(["l", "e", "n"])}},
        "phi": {**{i: "phi" for i in set(["l", "e", "n"])}},

    },
    initial_state="q0",
    final_states={"q3"},
)
# dfa_len.show_diagram(font_size=9, arrow_size=0.2)
reserve_DFAs.append(dfa_len)

dfa_if = VisualDFA(
    states={"q0", "q1", "q2", "phi"},
    input_symbols={"i", "f"},
    transitions={
        "q0": {"i": "q1", **{i: "phi" for i in set(["f"])}},
        "q1": {"f": "q2", **{i: "phi" for i in set(["i"])}},
        "q2": {**{i: "phi" for i in set(["i", "f"])}},
        "phi": {**{i: "phi" for i in set(["i", "f"])}},
    },
    initial_state="q0",
    final_states={"q2"}
)
# dfa_if.show_diagram(font_size=9, arrow_size=0.2)
reserve_DFAs.append(dfa_if)

dfa_then = VisualDFA(
    states={"q0", "q1", "q2", "q3", "q4", "phi"},
    input_symbols={"t", "h", "e", "n"},
    transitions={
        "q0": {"t": "q1", **{i: "phi" for i in set(["h", "e", "n"])}},
        "q1": {"h": "q2", **{i: "phi" for i in set(["t", "e", "n"])}},
        "q2": {"e": "q3", **{i: "phi" for i in set(["t", "h", "n"])}},
        "q3": {"n": "q4", **{i: "phi" for i in set(["t", "h", "e"])}},
        "q4": {**{i: "phi" for i in set(["t", "h", "e", "n"])}},
        "phi": {**{i: "phi" for i in set(["t", "h", "e", "n"])}},
    },
    initial_state="q0",
    final_states={"q4"}
)
# dfa_then.show_diagram(font_size=9, arrow_size=0.2)
reserve_DFAs.append(dfa_then)

dfa_end = VisualDFA(
    states={"q0", "q1", "q2", "q3", "phi"},
    input_symbols={"e", "n", "d"},
    transitions={
        "q0": {"e": "q1", **{i: "phi" for i in set(["n", "d"])}},
        "q1": {"n": "q2", **{i: "phi" for i in set(["e", "d"])}},
        "q2": {"d": "q3", **{i: "phi" for i in set(["e", "n"])}},
        "q3": {**{i: "phi" for i in set(["e", "n", "d"])}},
        "phi": {**{i: "phi" for i in set(["e", "n", "d"])}},
    },
    initial_state="q0",
    final_states={"q3"}
)
# dfa_end.show_diagram(font_size=9, arrow_size=0.2)
reserve_DFAs.append(dfa_end)

dfa_character = VisualDFA(
    states={"q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "phi"},
    input_symbols={"c", "h", "a", "r", "t", "e", "r"},
    transitions={
        "q0": {"c": "q1", **{i: "phi" for i in set(["h", "a", "r", "t", "e"])}},
        "q1": {"h": "q2", **{i: "phi" for i in set(["c", "a", "r", "t", "e"])}},
        "q2": {"a": "q3", **{i: "phi" for i in set(["c", "h", "r", "t", "e"])}},
        "q3": {"r": "q4", **{i: "phi" for i in set(["c", "h", "a", "t", "e"])}},
        "q4": {"a": "q5", **{i: "phi" for i in set(["c", "h", "r", "t", "e"])}},
        "q5": {"c": "q6", **{i: "phi" for i in set(["h", "a", "r", "t", "e"])}},
        "q6": {"t": "q7", **{i: "phi" for i in set(["c", "h", "a", "r", "e"])}},
        "q7": {"e": "q8", **{i: "phi" for i in set(["c", "h", "a", "r", "t"])}},
        "q8": {"r": "q9", **{i: "phi" for i in set(["c", "h", "a", "t", "e"])}},
        "q9": {**{i: "phi" for i in set(["c", "h", "a", "t", "e", "r"])}},
        "phi": {**{i: "phi" for i in set(["c", "h", "a", "r", "t", "e", "r"])}},
    },
    initial_state="q0",
    final_states={"q9"}
)
# dfa_character.show_diagram(font_size=9, arrow_size=0.2)
reserve_DFAs.append(dfa_character)

dfa_parameter = VisualDFA(
    states={"q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "phi"},
    input_symbols={"p", "a", "r", "m", "t", "e"},
    transitions={
        "q0": {"p": "q1", **{i: "phi" for i in set(["a", "r", "m", "e", "t"])}},
        "q1": {"a": "q2", **{i: "phi" for i in set(["p", "r", "m", "e", "t"])}},
        "q2": {"r": "q3", **{i: "phi" for i in set(["p", "a", "m", "e", "t"])}},
        "q3": {"a": "q4", **{i: "phi" for i in set(["p", "r", "m", "e", "t"])}},
        "q4": {"m": "q5", **{i: "phi" for i in set(["p", "a", "r", "e", "t", "e"])}},
        "q5": {"e": "q6", **{i: "phi" for i in set(["p", "a", "r", "m", "t"])}},
        "q6": {"t": "q7", **{i: "phi" for i in set(["p", "a", "r", "m", "e", "r"])}},
        "q7": {"e": "q8", **{i: "phi" for i in set(["p", "a", "r", "m", "t"])}},
        "q8": {"r": "q9", **{i: "phi" for i in set(["p", "a", "m", "e", "t"])}},
        "q9": {**{i: "phi" for i in set(["p", "a", "r", "m", "t", "e"])}},
        "phi": {**{i: "phi" for i in set(["p", "a", "r", "m", "t", "e"])}},
    },
    initial_state="q0",
    final_states={"q9"}
)
# dfa_parameter.show_diagram(font_size=9, arrow_size=0.2)
reserve_DFAs.append(dfa_parameter)

dfa_else = VisualDFA(
    states={"q0", "q1", "q2", "q3", "q4", "phi"},
    input_symbols={"e", "l", "s"},
    transitions={
        "q0": {"e": "q1", **{i: "phi" for i in set(["l", "s"])}},
        "q1": {"l": "q2", **{i: "phi"for i in set(["e", "s"])}},
        "q2": {"s": "q3", **{i: "phi" for i in set(["e", "l"])}},
        "q3": {"e": "q4", **{i: "phi" for i in set(["l", "s"])}},
        "q4": {**{i: "phi" for i in set(["e", "l", "s"])}},
        "phi": {**{i: "phi" for i in set(["e", "l", "s"])}},
    },
    initial_state="q0",
    final_states={"q4"}
)
# dfa_else.show_diagram(font_size=9, arrow_size=0.2)
reserve_DFAs.append(dfa_else)

dfa_do = VisualDFA(
    states={"q0", "q1", "q2", "phi"},
    input_symbols={"d", "o"},
    transitions={
        "q0": {"d": "q1", **{i: "phi" for i in set(["o"])}},
        "q1": {"o": "q2", **{i: "phi" for i in set(["d"])}},
        "q2": {**{i: "phi" for i in set(["d", "o"])}},
        "phi": {**{i: "phi" for i in set(["d", "o"])}},
    },
    initial_state="q0",
    final_states={"q2"}
)
# dfa_do.show_diagram(font_size=9, arrow_size=0.2)
reserve_DFAs.append(dfa_do)

dfa_read = VisualDFA(
    states={"q0", "q1", "q2", "q3", "q4", "phi"},
    input_symbols={"r", "e", "a", "d"},
    transitions={
        "q0": {"r": "q1", **{i: "phi" for i in set(["e", "a", "d"])}},
        "q1": {"e": "q2", **{i: "phi" for i in set(["r", "a", "d"])}},
        "q2": {"a": "q3", **{i: "phi" for i in set(["r", "e", "d"])}},
        "q3": {"d": "q4", **{i: "phi" for i in set(["r", "e", "a"])}},
        "q4": {**{i: "phi" for i in set(["r", "e", "a", "d"])}},
        "phi": {**{i: "phi" for i in set(["r", "e", "a", "d"])}},
    },
    initial_state="q0",
    final_states={"q4"}
)
# dfa_read.show_diagram(font_size=9, arrow_size=0.2)
reserve_DFAs.append(dfa_read)

dfa_print = VisualDFA(
    states={"q0", "q1", "q2", "q3", "q4", "q5", "phi"},
    input_symbols={"p", "r", "i", "n", "t"},
    transitions={
        "q0": {"p": "q1", **{i: "phi" for i in set(["r", "i", "n", "t"])}},
        "q1": {"r": "q2", **{i: "phi" for i in set(["p", "i", "n", "t"])}},
        "q2": {"i": "q3", **{i: "phi" for i in set(["p", "r", "n", "t"])}},
        "q3": {"n": "q4", **{i: "phi" for i in set(["p", "r", "i", "t"])}},
        "q4": {"t": "q5", **{i: "phi" for i in set(["p", "r", "i", "n"])}},
        "q5": {**{i: "phi" for i in set(["p", "r", "i", "n", "t"])}},
        "phi": {**{i: "phi" for i in set(["p", "r", "i", "n", "t"])}},
    },
    initial_state="q0",
    final_states={"q5"}
)
reserve_DFAs.append(dfa_print)

dfa_string = VisualDFA(
    states={"q0", "q1", "q2", "q3", "phi"},
    input_symbols={"'", "\"", "L", "N", "Y","S"},
    transitions={
        "q0": {"'": "q1", "\"":"q2",**{i: "phi" for i in set(["L", "N", "Y","S"])}},
        "q1": {"'": "q3", **{i: "q1" for i in set(["L", "N", "Y","S","\""])}},
        "q2": {"\"": "q3", **{i: "q2" for i in set(["L", "N", "Y","S","'"])}},
        "q3": {"'": "q1","\"":"q2", **{i: "phi" for i in set(["L", "N", "Y","S"])}},
        "phi":{**{i: "phi" for i in set(["'", "\"", "L", "N", "Y","S"])}},
    },
    initial_state="q0",
    final_states={"q3"}
)
#dfa_string.show_diagram(font_size=9, arrow_size=0.2)

dfa_operators = VisualDFA(
    states={"q0", "q1", "q2", "q3", "q4","q5","q6", "q7", "q8", "q9", "q10","q11","q12","q13","q14","q15","phi"},
    input_symbols={"+", "-", "=","!",">","<","/",":",",","*"},
    transitions={
        "q0": {"+": "q1","-":"q2", "=":"q3",":":"q5","!":"q7",">":"q8","<":"q10","/":"q12",",":"q14","*":"q15"},
        "q1": {**{i: "phi" for i in set(["+", "-", "=","!",">","<","/",":",",","*"])}},
        "q2": {**{i: "phi" for i in set(["+", "-", "=","!",">","<","/",":",",","*"])}},
        "q3": {"=":"q4",**{i: "phi" for i in set(["+", "-","!",">","<","/",":",",","*"])}},
        "q4": {**{i: "phi" for i in set(["+", "-", "=","!",">","<","/",":",",","*"])}},
        "q5": {":":"q6",**{i: "phi" for i in set(["+", "-", "=","!",">","<","/",",","*"])}},
        "q6": {**{i: "phi" for i in set(["+", "-", "=","!",">","<","/",":",",","*"])}},
        "q7": {**{i: "phi" for i in set(["+", "-", "=","!",">","<","/",":",",","*"])}},
        "q8": {"=":"q9",**{i: "phi" for i in set(["+", "-", ":","!",">","<","/",",","*"])}},
        "q9": {**{i: "phi" for i in set(["+", "-", "=","!",">","<","/",":",",","*"])}},
        "q10": {"=":"q11",**{i: "phi" for i in set(["+", "-", ":","!",">","<","/",",","*"])}},
        "q11": {**{i: "phi" for i in set(["+", "-", "=","!",">","<","/",":",",","*"])}},
        "q12": {"=":"q13",**{i: "phi" for i in set(["+", "-", ":","!",">","<","/",",","*"])}},
        "q13": {**{i: "phi" for i in set(["+", "-", "=","!",">","<","/",":",",","*"])}},
        "q14": {**{i: "phi" for i in set(["+", "-", "=","!",">","<","/",":",",","*"])}},
        "q15": {**{i: "phi" for i in set(["+", "-", "=","!",">","<","/",":",",","*"])}},
        "phi":{**{i: "phi" for i in set(["+", "-", "=","!",">","<","/",":",",","*"])}},
    },
    initial_state="q0",
    final_states={"q2","q1","q3","q4","q6", "q7", "q8", "q9", "q10","q11","q12","q13","q14","q15"}
)
#dfa_operators.show_diagram(font_size=9, arrow_size=0.2)


dfa_Parenthesis = VisualDFA(
    states={"q0", "q1", "q2", "phi"},
    input_symbols={"(", ")"},
    transitions={
        "q0": {"(": "q1", ")": "q2"},
        "q1": {"(": "q1", **{i: "phi" for i in set([")"])}},
        "q2": {")": "q2", **{i: "phi" for i in set(["("])}},
        "phi": {**{i: "phi" for i in set(["(", ")"])}},
    },
    initial_state="q0",
    final_states={"q1", "q2"}
)
# dfa_Parenthesis.show_diagram(font_size=9, arrow_size=0.2)
reserve_DFAs.append(dfa_Parenthesis)


def get_reserver_dict():
    return (reserve_DFAs,DFA_order_dict)

def get_operator_dfa():
   return dfa_operators

def get_string_dfa():
    return dfa_string

def get_identfier_dfa():
    return dfa_identfier
# reserve_DFAs[6].show_diagram(font_size=9, arrow_size=0.2,view=True)
