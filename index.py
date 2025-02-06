from ast import Not
import logging
import streamlit as st

from dashboard import pandasdal as dal
from dashboard import helpers
from dashboard import header
from pagination import interface

from dbhelpers.mysql import config
from dbhelpers import dbfactory


#   setup logging, dataframe, gui fixes
logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s | %(funcName)s | %(message)s'
)

DB_NAME = 'testing'
config = config.build_config(database=DB_NAME)
SQLITEPATH='testing.db'
DBSOURCE = dbfactory.DbSources.MYSQL
#
# setup db
# TODO: move this to dbfactory
#
if DBSOURCE == dbfactory.DbSources.MYSQL:
    db = dbfactory.get_db(dbfactory.DbSources.MYSQL, **config)
    engine = dbfactory.get_engine(dbfactory.DbSources.MYSQL, **config)
    connection_tester = dbfactory.get_connection_tester(dbfactory.DbSources.MYSQL)
elif DBSOURCE == dbfactory.DbSources.SQLITE:
    db = dbfactory.get_db(dbfactory.DbSources.SQLITE, sqlitepath=SQLITEPATH)
    engine = dbfactory.get_engine(dbfactory.DbSources.SQLITE, sqlitepath=SQLITEPATH)
    connection_tester = dbfactory.get_connection_tester(dbfactory.DbSources.SQLITE)
else:
    raise NotImplementedError(f'{DBSOURCE = }')
#
#
#

# setup data
df  = dal.get_winners(engine).copy()
# logger.info(f'{df.head() = }')
# logger.info(df.head().to_string())
for x in df.head().to_string().split('\n'):
    logger.info(x)
logger.info(f'{len(df) = }')

# https://docs.streamlit.io/develop/concepts/architecture/widget-behavior
helpers.fix_widgets_reload()

#   title
st.title('Analisi lotteria italia')
st.write(f'''
    Dashboard per analisi vincite Lotteria Italia 2024 - 2025
    
    stato della connessione: {dal.get_connection_status(connection_tester)} -- (db: {DBSOURCE})
''')

with st.sidebar:
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
    
#   TABLE
winners = dal.get_winners(engine, **dal.filter_dict_df_keys(df, **st.session_state))
# st.dataframe( winners, hide_index=True )
logger.debug(f'{winners = }')
logger.info(f'{len(winners) = }')
interface.paginated_df(winners)
#   info
if show_count:
    st.write(len(winners))

if show_state:
    st.session_state

helpers.logger_console_space()
