import logging
import pandas as pd
import numpy as np
from pathlib import Path

# from extract import extract
# from extract.main import INPUT_PATH

logger = logging.getLogger(__name__)

pd.options.display.width = 200


def show_dfs(dfs:list[pd.DataFrame]):
    '''display dfs for debugging'''
    for idx, df in enumerate(dfs):
        print(f'------------------- {idx} -----------------------')
        print(df.columns)
        print(df.head(3))


def process_cat1(cat1:pd.DataFrame, col_names:pd.Series) -> pd.DataFrame:
    ''' process first table '''
    
    logger.info('extracting category1')
    cat1.columns = col_names                    # set column names
    cat1 = cat1.drop(index=0)                   # drop first row (header)
    
    if cat1.Premio.dtype == 'O':                # if premio is str
        cat1.Premio = (
            cat1.Premio.str.replace('.', '')    # remove dots
            .astype(int)                        # convert to int
        )
        
    cat1.insert(0, 'Categoria', 1)              # add category column
    
    return cat1


def drop_all_nan_cols(dfs:list[pd.DataFrame]):
    ''' drops all NaN columns from all dataframes '''
    
    logger.info('dropping all NaN columns')
    for ndx, df in enumerate(dfs[1:], 1):       # loop over all dfs skipping 1st
        drop = []                               # reset droppable columns list
        
        for column in df.columns:               # loop over df columns
            if df[column].isna().all():         # check if all values ar NaN
                drop.append(column)             # add to droppable list
                
        if drop:                                # if we have droppable cols
            dfs[ndx] = df.drop(drop, axis=1)    # drop NaN columns and update df


def parse_tables(dfs:list[pd.DataFrame]) -> list[np.ndarray]:
    ''' parse all dfs and return one big list of ndarrays '''
    
    # global col_names
    
    logger.info('parsing other tables')
    category = 1                                                # 1st category is already ok
    rows:list[np.ndarray] = []                                  # output array
                    
    for df in dfs[1:]:                                          # loop over all dfs, skip 1st
        for row in df.values:                                   # loop over each row
                            
            firstcol:str = row[0]                               # save 1st col value
            if len(firstcol) > 2:                               # 1st col should be a 1 or 2 letter code
                #
                #   category or header
                #
                if 'categoria' in firstcol.lower():             # category header
                    category += 1                               # increase category value
                    
                elif 'serie' in firstcol.lower():               # just header
                    pass
                else:
                    raise ValueError(f'unknown pattern {row}')  # unexpected value
            else:
                #
                #   row
                #
                row = np.insert(row, 0, category)               # add category column
                rows.append(row)                                # save row
    return rows


def create_newdf(rows:list[np.ndarray]) -> pd.DataFrame:
    ''' create new global df from the rows '''
    
    logger.info('creating new df from tables')
    newdf = pd.DataFrame(                                       # create dataframe from rows
                    rows, 
                    columns=[
                        'Categoria', 
                        'Serie', 
                        'Numero', 
                        'Località', 
                        'Premio'
                    ]
    )
    
    newdf.insert(                                               # insert prov column
                4, 
                'Prov.', 
                newdf['Località'].str.extract(r'\((.*)\)')      # extract (PROV) from location (regex)
    )
    
    newdf['Località'] = newdf['Località'].apply(                # remove (PROV) from location
                        lambda x: x.split('(')[0]
    )
    
    newdf['Premio'] = newdf['Premio'].astype('str')             # convert premio to str
    
    newdf['Premio'] = newdf.Premio.apply(                       # fix zeroes
                        lambda x: x + '00' 
                        if x.endswith('.0') 
                        else x
    )
    
    newdf.Premio = (                                            # convert premio to int
                newdf.Premio.str.replace('.', '')
                .astype('int')
    )
    
    return newdf


def get_df_from_html(input_path:str) -> pd.DataFrame:
    ''' compound function '''

    logger.info(f'creating df from html {input_path}')
    #
    # get data from html
    #
    if not Path(input_path).exists():
        raise FileNotFoundError(input_path)

    tables = pd.read_html(input_path)
    ############################################
    #
    # extract cat1
    #
    ############################################
    tbl1 = tables[0]
    col_names = tbl1.iloc[0]                        # no Categoria
    cat1 = process_cat1(tbl1, col_names)
    ############################################
    #
    # cleanup other tables
    #
    ############################################
    drop_all_nan_cols(tables)
    ############################################
    #
    # create sum of other tables
    #
    ############################################
    rows = parse_tables(tables)
    newdf = create_newdf(rows)
    ############################################
    #
    # create sum of all tables
    #
    ############################################
    winners = pd.concat([cat1, newdf]).reset_index(drop=True)
    winners = winners.reset_index(drop=True)
    winners = winners.rename(columns={
        'Categoria': 'categoria',
        'Serie': 'serie',
        'Numero': 'numero',
        'Località': 'luogo',
        'Prov.':'prov',
        'Premio': 'premio',
    })
    
    for col in ['serie', 'numero', 'luogo', 'prov']:
        winners[col] = winners[col].astype('str').str.upper().str.rstrip()
    
    return winners


