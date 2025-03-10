import logging
import streamlit as st

from dashboard import pandasdal as dal
from dashboard import helpers
from dashboard import header
from dbhelpers.dbfactory import setup_db
from pagination import interface

from dbhelpers.mysql import config
from dbhelpers import dbfactory


#################################################################################
# setup logging, db, dataframe, gui fixes #
#################################################################################
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s | %(funcName)s | %(message)s'
)

# mysql variables and options
DB_NAME = 'testing'
mysqlconfig = config.get_default_config(
    database=DB_NAME,
)

# sqlite variables and options
SQLITEPATH='testing.db'
DBSOURCE = dbfactory.DbSources.SQLITE

# call factory to get whatever db is chosen
(
    db, 
    engine, 
    connection_tester, 
    DBDETAILS
) = setup_db(DBSOURCE, mysqlconfig, SQLITEPATH)

# setup data
df  = dal.get_winners(engine).copy()
# just log sample data
for x in df.head().to_string().split('\n'):
    logger.info(x)
logger.info(f'{len(df) = }')

# strange fix
# https://docs.streamlit.io/develop/concepts/architecture/widget-behavior
helpers.fix_widgets_reload()


#################################################################################
# interface #
#################################################################################

#   title
st.title('Analisi lotteria italia')
st.write(f'''
    Dashboard per analisi vincite Lotteria Italia 2024 - 2025
    
    stato della connessione: {dal.get_connection_status(connection_tester)} 
    -- (db: {DBSOURCE})
''')


# sidebar
with st.sidebar:
    st.header('Debug')
    show_count, show_state = header.display_options()

    #   sidebar header filtri
    st.header('Filtri')
    st.write('Usare le opzioni per filtrare i dati')    
    link = header.filter_options()
    
    #   sidebar subheader geo
    st.subheader('Geografia')
    prov, luogo = header.geo_filters(df, link)
    
    #   sidebar subheader biglietto
    st.subheader('Biglietto')
    serie, numero = header.ticket_filters(df, link)
    
    #   sidebar subheader premio
    st.subheader('Premio')
    categoria, premio = header.prize_filters(df, link)


#   paginated table
winners = dal.get_winners(engine, **dal.filter_dict_df_keys(df, **st.session_state))
# st.dataframe( winners, hide_index=True )
logger.debug(f'{winners = }')
logger.info(f'{len(winners) = }')
interface.paginated_df(winners)


#   info
if show_count:
    st.write(f'Totale records: {len(winners)}')

if show_state:
    st.session_state

helpers.logger_console_space()
