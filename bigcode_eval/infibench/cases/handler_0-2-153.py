
def handle(response):
    import re
    import string
    response += '     ' # avoid overflow
    top, bottom, left, right = -1, -1, -1, -1
    in_code_block = False
    tot_matched = 0
    matched_list = []
    for i in range(len(response)):
        if in_code_block and response[i:].startswith('border'):
            tot_matched += 1
            matched_list.append(re.match(r'^border[\-a-z0-9]*', response[i:])[0])
            if not response[i:].startswith('border-'):
                # general border
                top, bottom, left, right = 1, 1, 1, 1
            else:
                if response[i:].startswith('border-solid'):
                    top, bottom, left, right = 1, 1, 1, 1
                else:
                    # border-*
                    width = response[i + len('border-')]
                    try:
                        width = int(width)
                        if width == 0:
                            top, bottom, left, right = 0, 0, 0, 0
                        else:
                            top, bottom, left, right = 1, 1, 1, 1
                    except:
                        # not arabic width
                        width = response[i + len('border-') ]
                        if width in ['t', 'b', 'l', 'r']:
                            next = response[i + len('border-') + 1]
                            if next == '-':
                                nextt = response[i + len('border-') + 2]
                                try:
                                    nextt = int(nextt)
                                    if width == 't':
                                        top = 1 if nextt > 0 else 0
                                    elif width == 'b':
                                        bottom = 1 if nextt > 0 else 0
                                    elif width == 'l':
                                        left = 1 if nextt > 0 else 0
                                    elif width == 'r':
                                        right = 1 if nextt > 0 else 0
                                except:
                                    pass
                            elif next not in string.ascii_lowercase:
                                if width == 't':
                                    top = 1 
                                elif width == 'b':
                                    bottom = 1 
                                elif width == 'l':
                                    left = 1 
                                elif width == 'r':
                                    right = 1 
        elif response[i] == '<':
            in_code_block = True
        elif response[i] == '>':
            in_code_block = False
    score = 0.
    details = ''
    if top > 0 and bottom == 0 and left == 0 and right == 0:
        score += 2.
        details = 'goal fulfilled. '
        if tot_matched <= 3:
            score += 1.
            details += f'With only {tot_matched} classes.'
        else:
            details += f'With {tot_matched} classes.'
    return (score, 3.0, {'status': details, 'all_matches': matched_list, 'top': top, 'bottom': bottom, 'left': left, 'right': right})