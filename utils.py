
def convert_string_to_hex_chars(string):
    hex_chars = []
    for char in list(string):
        hex_char = char.encode("utf-8").hex()
        hex_char = '0'*(4-len(hex_char)) + hex_char
        hex_chars.append(hex_char)
    return ' '.join(hex_chars)

def convert_hex_to_string(hex):
    return bytes.fromhex(hex).decode()