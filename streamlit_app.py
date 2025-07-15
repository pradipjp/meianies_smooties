# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title(f"Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruit you want in your Custom Smoothie")

name_on_order = st.text_input('Name on Smoothie')
st.write("Name on your smoothie will be", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'), col('SEARCH_ON'))

# Already commented
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

# Convert the Snowpark DataFrame to a Pandas DataFrame so we can use the LOC function
pd_df = my_dataframe.to_pandas()

# Already commented
# st.dataframe(pd_df)
# st.stop()

# Fix: Use fruit names list for multiselect
ingredient_list = st.multiselect('Choose up to 5 ingredient', pd_df['FRUIT_NAME'].tolist())

if ingredient_list:
    # Already commented
    # st.write(ingredient_list)
    # st.text(ingredient_list)

    ingredient_string = ''

    for fruit_chosen in ingredient_list:
        ingredient_string += fruit_chosen + ' '

        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        # Already commented
        # st.write('The search value for ', fruit_chosen, ' is ', search_on, '.')

        st.subheader(f"{fruit_chosen} Nutrition Information")

        try:
            smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on.strip())
            st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        except Exception as e:
            st.error(f"API error for {fruit_chosen}: {e}")

    # FIX: Uncommented and fixed for use
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredient_string.strip()}', '{name_on_order}')
    """

    time_to_insert = st.button('Submit')
    
    # Already commented
    # st.write(my_insert_stmt)

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
