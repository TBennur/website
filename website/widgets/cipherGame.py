import os
import random
import platform

if platform.system() == "Windows":
    import widgets.widgetUtilities as widgetUtilities
else:
    import website.widgets.widgetUtilities as widgetUtilities


SPLIT = "-"
NULL = "#"

# Edits original ciphertext with rules
def replace_text(original, rules):
    uppercase_letters = []
    for i in range(len(original)):
        if original[i].isupper():
            uppercase_letters.append(i)
    original = original.upper()
    for rule in rules:
        [l1, l2] = rule.split(SPLIT)
        l1 = l1.upper()
        l2 = l2.lower()
        original = original.replace(l1, l2)
    original_list = list(original.lower())
    for u in uppercase_letters:
        original_list[u] = original_list[u].upper()
    return "".join(original_list)

# Adds an additional hint based on pre-existing rules
def update_hints(hints, user_rules, cipher_rules):
    if len(hints) == len(cipher_rules):
        return
    cipher = random.choice(cipher_rules)
    hint = cipher[::-1].upper()
    while hint in hints:
        cipher = random.choice(cipher_rules)
        hint = cipher[::-1].upper()
    hints.append(hint)
    for i in range(len(user_rules)):
        if user_rules[i][0] == hint[0]:
            user_rules.pop(i)
            return

# Formats hints for display
def format_hints(hints):
    s = ""
    if hints != []:
        s += "Current Hints: \n"
    for hint in hints:
        s += hint + ", "
    return s[:-2]

# Updates existing rules after user input
def update_rules(l1, l2, rules, hints):
    if l1 == NULL or l2 == NULL:
        return
    for hint in hints:
        if l1 == hint[0]:
            return
    formatted = l1 + SPLIT + l2
    p = -1
    for i in range(len(rules)):
        if rules[i][0] == l1:
            p = i
    if p != -1:
        rules.pop(p)
    if formatted[0] != formatted[-1]:
        rules.append(formatted)

# Format rules for display
def format_rules(rules):
    s = ""
    if rules != []:
        s += "Current Substitutions: \n"
    for rule in rules:
        s += rule + ", "
    return s[:-2]

# Generates ciphertext and rules from passage
def generate_message(original):
    uppercase_letters = []
    for i in range(len(original)):
        if original[i].isupper():
            uppercase_letters.append(i)
    original = original.upper()
    l1 = [chr(x) for x in range(97, 123)]
    l2 = l1.copy()
    random.shuffle(l2)
    cipher_rules = [(l1[x] + SPLIT + l2[x]) for x in range(26)]
    for rule in cipher_rules:
        [l1, l2] = rule.split(SPLIT)
        l1 = l1.upper()
        l2 = l2.lower()
        original = original.replace(l1, l2)
    original_list = list(original.lower())
    for u in uppercase_letters:
        original_list[u] = original_list[u].upper()  
    return "".join(original_list), cipher_rules

# Sets up cipher game
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