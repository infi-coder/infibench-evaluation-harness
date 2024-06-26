from typing import List

def main_handler(get_score, tot_score, status):
    now_score = 0.
    details = ''
    if status[0].startswith('match'): 
        now_score += 1.0
        details += '+1'
    if status[1].startswith('match'): 
        now_score += 1.0
        details += '+1'
    if status[2].startswith('match') and status[3].startswith('unmatch'): 
        now_score -= 1.0
        details += '-1'
    return max(now_score, 0.0), 2.0, {'status': details}