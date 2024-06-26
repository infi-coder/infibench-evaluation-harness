
def handler(response):
    key1 = "// eslint-disable-next-line react/display-name"
    key2 = "render: "
    if response.count(key1) and response.count(key2) and response.index(key1) < response.index(key2):
        return (1.0, 1.0, 'good')
    else:
        return (0.0, 1.0, 'bad')