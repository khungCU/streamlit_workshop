# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie!! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)


name_on_order = st.text_input("Name on Smoothis: ")
st.write('The name on your Smoothie will be: ', name_on_order)

session = get_active_session()
my_dataframe = session\
               .table("smoothies.public.fruit_options")\
               .select(col("FRUIT_NAME"))


ingredients_ist = st.multiselect(
    'Choose up to 5 ingredients: ',
    my_dataframe,
    max_selections = 5
)

if ingredients_ist:
  time_to_insert = st.button('Submit Order!')
  if time_to_insert:
    ingredients_string = ', '.join(i for i in ingredients_ist)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""
    # st.write(my_insert_stmt)
    # st.stop()
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")
