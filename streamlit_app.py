# Import python packages
import streamlit as st
import requests
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
    
    for fruit_chosen in ingredient_list:
        ingredient_string+=fruit_chosen+ ' '
    #st.write(ingredient_string)  
        st.subheader(fruit_chosen+'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit_chosen)
        sf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    my_insert_stmt = """INSERT INTO smoothies.public.orders (ingredients, name_on_order)
                    VALUES ('""" + ingredient_string + """', '""" + name_on_order + """')"""
    
    
    time_to_insert=st.button('Submit')
    #st.write(my_insert_stmt)
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
    


