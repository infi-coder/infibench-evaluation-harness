import pandas as pd

in_path = 'human_study/rater_cases/final_rated.csv'

if __name__ == '__main__':
    in_df = pd.read_csv(in_path)
    in_df = in_df[in_df['human_score'] != -1]
    print(len(in_df))

    matIG = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    matIH = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    matGH = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    matCH = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

    for i in range(len(in_df)):
        ascore, bscore, avote, bvote, H = in_df.iloc[i]['Amodel'], in_df.iloc[i]['Bmodel'], in_df.iloc[i]['gptAvote'], in_df.iloc[i]['gptBvote'], in_df.iloc[i]['human_score']
        # print(ascore, bscore)
        if ascore > bscore + 0.01:
            I = 0
        elif ascore < bscore - 0.01:
            I = 1
        elif ascore >= 0.5:
            I = 2
        else:
            I = 3
        
        if avote > bvote:
            G = 0
        elif avote < bvote:
            G = 1
        elif avote > 0:
            G = 2
        else:
            G = 3
    
        if (I == 0 and G == 1) or (I == 1 and G == 0):
            C = 2
        elif I in [0, 1]:
            C = I
        elif G in [0, 1]:
            C = G
        else:
            C = 3

        matIG[I][G] += 1
        matIH[I][H] += 1
        matGH[G][H] += 1
        matCH[C][H] += 1


        # if I == G:
        #     mat[I][G] += 1
        # else:
        #     mat[I][G] += 1
        #     mat[G][I] += 1
    print(matIG)
    print('------')
    print(matIH)
    print('------')
    print(matGH)
    print('------')
    print(matCH)
    print('------')
        