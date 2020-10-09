#Convert a string to HEX
def convert_string_to_hex_chars(string):
    hex_chars = []
    for char in list(string):
        hex_char = char.encode('utf-16').hex()
        hex_char = '0' * (8 - len(hex_char)) + hex_char
        hex_chars.append(hex_char)
    return ' '.join(hex_chars)

#Convert HEX to a string
def convert_hex_to_string(hex):
    s = bytes.fromhex(hex).decode('utf-16')
    # Remove trailing new line character if necessary.
    if list(s)[0] == '\x00':
        return str(list(s)[1])
    else:
        return s
