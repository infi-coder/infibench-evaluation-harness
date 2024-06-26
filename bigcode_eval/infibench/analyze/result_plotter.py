import json
from matplotlib import pyplot as plt
import numpy as np

fname = 'results/main_results.json'

if __name__ == '__main__':
    with open(fname, 'r') as f:
        results = json.load(f)

    z = []
    x = []
    y = []
    yerr_low = []
    yerr_high = []
    placement_delta = {
        'Baichuan2-7B': (0., 0.),
        'phi-1.5': (0., +0.01),
        'WizardCoder-1B': (-0.5, -0.02),
        'WizardCoder-3B': (-3., +0.03),
        'OctoGeeX': (-1., +0.04),
        'deepseek-coder-6.7b': (0., +0.02),
        'Zypher': (0., +0.01),
        'CodeLlama-34B-Instruct': (-6.25, 0.)
    }
    select = ['phi-1', 'phi-1.5', 'OctoGeeX', 'Baichuan2', 'WizardCoder-Python-34B', 'WizardCoder-Python-13B',
              'WizardCoder-1B', 'WizardCoder-3B',
              'deepseek-coder', 'CodeLlama-7B-Instruct', 'CodeLlama-34B',
              'Codellama-13B-Instruct',
              'CodeGeeX2', 'Zypher', 'StarCoderPlus', 'OctoCoder']
    for row in results:
        if row[2]:
            x.append(row[2])
            mean = np.mean(row[4])
            z.append(f'{row[1]}\n{mean * 100.:.2f}%')
            y.append(mean)
            yerr_low.append(mean - np.min(row[4]))
            yerr_high.append(np.max(row[4]) - mean)
    
    plt.style.use('seaborn')
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.errorbar(x, y, np.array([yerr_low, yerr_high]), fmt='o', linewidth=2, capsize=6, markersize=6)

    for i, txt in enumerate(z):
        if any([txt.startswith(s) for s in select]):
        # if True:
            delta_x, delta_y = 0.0, 0.0
            for k in placement_delta:
                if txt.startswith(k):
                    delta_x, delta_y = placement_delta[k]
            ax.annotate(txt, (x[i] + 0.5 + delta_x, y[i] - 0.03 + delta_y), color='tab:blue')

    for i, row in enumerate(results):
        if not row[2]:
            colors = {0: 'green', 1: 'brown', 2: 'pink'}
            xx = [0, 50]
            mean = np.mean(row[4])
            mmin = np.min(row[4])
            mmax = np.max(row[4])
            yy = [mean, mean]
            ax.plot(xx,yy,'-', color=colors[i], label=f'{row[1]}  {mean*100.:.2f}%')
            ax.fill_between(xx, mmin, mmax, alpha=0.2, color=colors[i])
    ax.legend(loc='lower right')

    ax.set(xlim=(0, 40), 
           ylim=(0.0, 0.65), )
    
    vals = ax.get_yticks()
    ax.set_yticklabels(['{:,.0%}'.format(x) for x in vals])

    vals = ax.get_xticks()
    ax.set_xticklabels(['{}B'.format(int(x)) for x in vals])

    plt.xlabel('Model Size (# Parameters)')
    plt.ylabel('Score Achieved')

    plt.subplots_adjust(bottom=0.08, right=0.98, left=0.05, top=0.99)

    # plt.show()
    plt.savefig('raw_all_results.pdf')
