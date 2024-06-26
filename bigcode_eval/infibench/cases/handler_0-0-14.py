
def handler(response):
    score = 0.
    if response.count('<Form.Item') > 0 and response.count('<Switch') > 0 and response.count('<span>') > 0:
        score += 1.
        if response.count('</Form.Item>'):
            idx_first_formitem = response.index('<Form.Item')
            idx_first_endformitem = response.index('</Form.Item>')
            substr = response[idx_first_formitem: idx_first_endformitem]
            if substr.count('<Switch') > 0 and substr.count('<span') == 0:
                score += 1.
    return (score, 2.0, str(score))