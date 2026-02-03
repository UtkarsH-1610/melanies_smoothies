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

st.dataframe(pd_df)

ingredients_list = st.multiselect(
    'Choose upto 5 ingredients:',
    pd_df['FRUIT_NAME'].tolist(),
    max_selections=5
)

if ingredients_list:

    ingredients_string = ", ".join(ingredients_list)

    for fruit_chosen in ingredients_list:

        search_on = pd_df.loc[
            pd_df['FRUIT_NAME'] == fruit_chosen,
            'SEARCH_ON'
        ].iloc[0]

        st.subheader(fruit_chosen + ' Nutrition Information')

        response = requests.get(
            f"https://my.smoothiefroot.com/api/fruit/{search_on}"
        )

        # st.dataframe(response.json(), use_container_width=True)

    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    if st.button('Submit Order'):
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")
