import streamlit as st
import requests
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")

st.write("Choose the fruit you want in your custom smoothie")

name_on_order = st.text_input('Name on smoothie')
st.write('The name of smoothie will be', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table(
    "smoothies.public.fruit_options"
).select(col('FRUIT_NAME'), col("SEARCH_ON"))

pd_df = my_dataframe.to_pandas()

ingredients_list = st.multiselect(
    'Choose upto 5 ingredients:',
    pd_df['FRUIT_NAME'].tolist(),
    max_selections=5
)

if ingredients_list:

    ingredients_string = ''
    st.write(ingredients_string)

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)

        st.dataframe(
            smoothiefroot_response.json(),
            use_container_width=True
        )
        st.write(",,,,,,,",ingredients_string)
        st.write(",,,,,,,,,,,,,,,,", fruit_chosen)
        

    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    if st.button('Submit Order'):
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")
