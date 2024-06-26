
def f(url):
    url='https://drive.google.com/uc?id=' + url.split('/')[-2]
    return url


url1 = 'https://drive.google.com/file/d/0B6GhBwm5vaB2ekdlZW5WZnppb28/view?usp=sharing'
url2 = 'https://drive.google.com/file/d/1234535/view?usp=111'
assert f(url1) == processURL(url1)

assert f(url2) == processURL(url2)

