# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
    """
    choose the fruits you want in your custom smoothie
    """
)

from snowflake.snowpark.functions import col

# session = get_active_session()

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "What are your favorite fruits",
    my_dataframe,
    #  In case we would like to restrict the max number of selections
    # max_selections = 5
)


ingredients_string  = ''
if ingredients_list:    
    st.write("You selected:", ingredients_list)
    st.text(ingredients_list)
    for i in ingredients_list: 
        ingredients_string += i + ' '
    st.write(ingredients_string)

#  create a table orders to store all the data

name_on_order = st.text_input("Your Name")
st.write("Your name entered is", name_on_order)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """',
            '"""+name_on_order+"""')"""

st.write(my_insert_stmt)

time_to_insert = st.button("Submit Order")
if time_to_insert: 
    if ingredients_string:
        session.sql(my_insert_stmt).collect()
    st.success(f'Your Smoothie is ordered {name_on_order}!', icon="✅")






