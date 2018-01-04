#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import sys
 
 
#----------------------------------------------------------------------
def camel_case_to_lower_case_underscore(string):
    """
    Split string by upper case letters.
 
    F.e. useful to convert camel case strings to underscore separated ones.
 
    @return words (list)
    """
    words = []
    from_char_position = 0
    for current_char_position, char in enumerate(string):
        if char.isupper() and from_char_position < current_char_position:
            words.append(string[from_char_position:current_char_position].lower())
            from_char_position = current_char_position
    words.append(string[from_char_position:].lower())
    return '_'.join(words)

def camel_case_to_capitalized_spaced(string):
    """
    Split string by upper case letters.
 
    F.e. useful to convert camel case strings to underscore separated ones.
 
    @return words (list)
    """
    words = []
    from_char_position = 0
    for current_char_position, char in enumerate(string):
        if char.isupper() and from_char_position < current_char_position:
            words.append(string[from_char_position:current_char_position].lower())
            from_char_position = current_char_position
    words.append(string[from_char_position:].lower())
    capitalized_words = []
    for word in words:
        capitalized_word = word.upper()[0] + word.lower()[1:]
        capitalized_words.append(capitalized_word)
    return ' '.join(capitalized_words)
 
 
#----------------------------------------------------------------------
def lower_case_underscore_to_camel_case(string):
    """Convert string or unicode from lower-case underscore to camel-case"""
    splitted_string = string.split('_')
    # use string's class to work on the string to keep its type
    class_ = string.__class__
    return splitted_string[0] + class_.join('', map(class_.capitalize, splitted_string[1:]))
 
 
#----------------------------------------------------------------------
def read_data():
    return input()
 
 
#----------------------------------------------------------------------
def detect_conversion_method(data):
    if '_' in data:
        return lower_case_underscore_to_camel_case
    else:
        return camel_case_to_capitalized_spaced
 
 
#----------------------------------------------------------------------
def main():
    data = read_data()
    conversion_method = detect_conversion_method(data)
    result = conversion_method(data)
    sys.stdout.write(result)
 
 
if __name__ == '__main__':
    main()