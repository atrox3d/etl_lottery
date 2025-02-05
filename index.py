import logging
import streamlit as st

from dashboard import pandasdal as dal
from dashboard import helpers
from dashboard import header
from pagination import interface


#   setup logging, dataframe, gui fixes
logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s | %(funcName)s | %(message)s'
)

#
#
# TODO: get engine HERE
# TODO: get db HERE
#
#


df  = dal.get_winners().copy()
logger.info(f'{df = }')
logger.info(f'{len(df) = }')


helpers.fix_widgets_reload()

#   title
st.title('Analisi lotteria italia')
st.write(f'''
    Dashboard per analisi vincite Lotteria Italia 2024 - 2025
    
    stato della connessione: {dal.get_connection_status()}
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
winners = dal.get_winners(**dal.filter_dict_df_keys(df, **st.session_state))
# st.dataframe( winners, hide_index=True )
logger.info(f'{winners = }')
logger.info(f'{len(winners) = }')
interface.paginated_df(winners)
#   info
if show_count:
    st.write(len(winners))

if show_state:
    st.session_state

helpers.console_space()
