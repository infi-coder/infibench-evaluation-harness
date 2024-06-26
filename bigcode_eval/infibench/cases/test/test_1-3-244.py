
def colored_background(r, g, b, text):
    return f'\033[48;2;{r};{g};{b}m{text}'
'''
def colored(background_r, background_g, background_b, text):
    return "\033[48;2;{};{};{}m\033[38;2;0;0;0m{} \033[0m".format(background_r, background_g, background_b, text)
'''
assert colored(100, 200, 150, 'hello').count(colored_background(100, 200, 150, 'hello')) > 0
