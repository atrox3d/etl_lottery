
ENABLED = True
DISABLED = False

FIX_WIDGETS = ENABLED
FIX_INDEX = ENABLED
CLEAR_STATE = ENABLED

# fix_widget_reload | selectbox index| state.clear | state        | select box         | winners table
#-------------------+----------------+-------------+--------------+--------------------+-------------------
#  ENABLED          | ENABLED        | ENABLED     | ok           | ok                 | ok
#  ENABLED          | ENABLED        | *DISABLED   | ok           | ok                 | ok
#-------------------+----------------+-------------+--------------+--------------------+-------------------
#  *DISABLED        | ENABLED        | *DISABLED   | ok           | no value, 2 clicks | no update, 2 clicks
#  *DISABLED        | ENABLED        | *ENABLED    | ok           | no value, 2 clicks | no update, 2 clicks
#-------------------+----------------+-------------+--------------+--------------------+--------------------
#  ENABLED          | *DISABLED      | ENABLED     | cannot reset | cannot reset       | follows state
#  ENABLED          | *DISABLED      | *DISABLED   | cannot reset | cannot reset       | follows state
#-------------------+----------------+-------------+--------------+--------------------+--------------------
#  *DISABLED        | *DISABLED      | *DISABLED   | cannot reset | cannot reset       | follows state
