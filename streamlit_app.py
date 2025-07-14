# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col,when_matched

# Write directly to the app
st.title(f"Customize Your Smoothie:cup_with_straw:")
st.write(
"Choose the fruit you want in your Custom Smoothie"
)


name_on_order = st.text_input('Name on Smoothie')
st.write("Name on your smoothie will be", name_on_order)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredient_list=st.multiselect('choose up to 5 ingredient',my_dataframe)

if ingredient_list:
    #st.write(ingredient_list)
    #st.text(ingredient_list)
    ingredient_string=''
    
    for x in ingredient_list:
        ingredient_string+=x+ ' '
    #st.write(ingredient_string)    
    
    my_insert_stmt = """INSERT INTO smoothies.public.orders (ingredients, name_on_order)
                    VALUES ('""" + ingredient_string + """', '""" + name_on_order + """')"""

    
    time_to_insert=st.button('Submit')
    #st.write(my_insert_stmt)
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
    
