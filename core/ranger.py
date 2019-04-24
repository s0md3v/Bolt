def ranger(tokens):
    digits = set()
    alphabets = set()
    for token in tokens:
        for char in token:
            if char in '0123456789':
                digits.add(char)
            elif char in 'abcdefghijklmnopqrstuvwxyz':
                alphabets.add(char)
    return [list(digits), list(alphabets)]
