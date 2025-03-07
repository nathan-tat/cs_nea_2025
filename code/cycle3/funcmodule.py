import json
import math as m

def make_component_image(length: int):
    pass


def validateResolution(res) -> bool:
    if str(res) == "":
        return True
    
    if str.isdigit(res):
        if int(res) <= 8:
            return True
        
    return False

def validateIdentifier(identifier):
    if len(identifier) <= 12:
        return True
    
    return False


def dict_to_json(d: dict, f: str) -> None:
    with open(f, "w") as file:
        json.dump(d, file)
        
def json_to_dict(filename: str) -> dict:
    with open(filename, "r") as file:
        return json.load(file)
    
    
def round_sig_fig(num: float, sf: int) -> str:
    # normalise mantissa
    exp = m.floor(m.log10(num))
    mant = num / (10**exp)

    mant = round(mant, sf-1)
    rounded = mant * 10**exp
    
    s = str(rounded)
    # special case with no d.p.
    if sf == 1 and exp == 0:
        return s[0]
    
    # if missing zeroes on the end
    while len(s) < sf + 1:
        s += "0"
    
    return s


def normaliseString(a: str, b: str, maxLen: int = 35, char: str = " ") -> str:
    """ Returns the concatenation of `a` and `b` with `char` in 
    between until they reach `maxLen`"""
    temp = a

    while len(temp) + len(b) < maxLen:
        temp += char

    return temp+b