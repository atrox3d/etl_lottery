import numpy as np

from extract import get_df_from_html



INPUT_PATH = 'data/in/lotteria.html'
OUPUT_PATH = 'data/out/winners.csv'

if __name__ == "__main__":
    
    winners = get_df_from_html(INPUT_PATH)
    
    # export result
    winners.to_csv(OUPUT_PATH, index=False)
