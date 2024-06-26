
def handle(response):
    import re
    score = 0.0
    detail = 'no button exists'
    for ans in re.finditer(r'<button (.*)>[\s\S]*</button>', response):
        score = 1.0
        inner = ans[1]
        # print(inner)
        detail = 'button exists but inner things are not correct'
        if (inner.count('form=\'my-form\'') > 0 or inner.count('form="my-form"')) and (inner.count('type=\'submit\'') > 0 or inner.count('type="submit"') > 0):
            score = 3.0
            detail = 'perfect'
            return (score, 3.0, detail)
    return (score, 3.0, detail)

