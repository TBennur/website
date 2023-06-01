import os
import random
import platform

if platform.system() == "Windows":
    import widgets.widgetUtilities as widgetUtilities
else:
    import website.widgets.widgetUtilities as widgetUtilities


SPLIT = "-"
NULL = "#"

def replace_text(o, rs):
    upper = []
    for i in range(len(o)):
        if o[i].isupper():
            upper.append(i)
    o = o.upper()
    for r in rs:
        [l1, l2] = r.split(SPLIT)
        l1 = l1.upper()
        l2 = l2.lower()
        o = o.replace(l1, l2)
    o = o.lower()
    for u in upper:
        o = o[:u] + o[u].upper() + o[u+1:]  
    return o

def update_hints(hs, rs, cs):
    if len(hs) == len(cs):
        return
    cipher = random.choice(cs)
    hint = cipher[::-1].upper()
    while hint in hs:
        cipher = random.choice(cs)
        hint = cipher[::-1].upper()
    hs.append(hint)
    for i in range(len(rs)):
        if rs[i][0] == hint[0]:
            rs.pop(i)
            return

def format_hints(hs):
    s = ""
    if hs != []:
        s += "Current Hints: \n"
    for hint in hs:
        s += hint + ", "
    return s[:-2]

def update_rules(l1, l2, rs, hs):
    if l1 == NULL or l2 == NULL:
        return
    for hint in hs:
        if l1 == hint[0]:
            return
    formatted = l1 + SPLIT + l2
    p = -1
    for i in range(len(rs)):
        if rs[i][0] == l1:
            p = i
    if p != -1:
        rs.pop(p)
    if formatted[0] != formatted[-1]:
        rs.append(formatted)

def format_rules(rs):
    s = ""
    if rs != []:
        s += "Current Substitutions: \n"
    for rule in rs:
        s += rule + ", "
    return s[:-2]

def generate_message(o):
    upper = []
    for i in range(len(o)):
        if o[i].isupper():
            upper.append(i)
    o = o.upper()
    l1 = [chr(x) for x in range(97, 123)]
    l2 = l1.copy()
    random.shuffle(l2)
    rs = [(l1[x] + SPLIT + l2[x]) for x in range(26)]
    for r in rs:
        [l1, l2] = r.split(SPLIT)
        l1 = l1.upper()
        l2 = l2.lower()
        o = o.replace(l1, l2)
    o = o.lower()
    for u in upper:
        o = o[:u] + o[u].upper() + o[u+1:]  
    return o, rs

def setup():
    f = open(widgetUtilities.get_file_path(random.choice(os.listdir(widgetUtilities.get_file_path("cipherTexts")))), "r")
    raw = f.read()
    cipher, rules = generate_message(raw)
    cipher_settings = {
        "raw_text": raw,
        "cipher_rules": rules,
        "cipher_text": cipher,
        "user_rules": [],
        "user_hints": [],
        "user_text": cipher,
        "old_letter": "A",
        "new_letter": "A",
    }
    return cipher_settings
    
