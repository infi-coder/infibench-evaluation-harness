

def handle(response):
    details = ''
    # find candidate patterns
    if response.count('```') < 2:
        return (0.0, 1.0, 'cannot locate generated parts')
    index_s = response.find('```')
    response = response[index_s + 3:]
    index_t = response.find('```')
    response = response[: index_t]

    # sanitize
    params = response.split('/')
    if len(params) > 0:
        for char in ['\'', '"', '\n']:
            while char in params[0]:
                params[0] = params[0][params[0].find(char) + 1: ]
            while char in params[-1]:
                params[-1] = params[-1][: params[-1].find(char)]

    optional_params = [param for param in params if param.startswith(':') and param.endswith('?')]
    if len(optional_params) < 2:
        return (0.0, 1.0, f'Only {len(optional_params)} optional params')
    elif len(optional_params) > 2:
        return (0.0, 1.0, f'{len(optional_params)} optional params, too much')
    else:
        if optional_params[0] == optional_params[1]:
            return (0.0, 1.0, f'Optional params should be different')
        else:
            return (1.0, 1.0, 'Good')