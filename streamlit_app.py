# Import python packages
import requests
from snowflake.snowpark.functions import col
import streamlit as st
cnx = st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title(f"Customize Your Smoothie!")
st.write(
  """Choose the fruits you want in your custom Smoothie
  """
)

name = st.text_input('Name on smoothie:')


#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()
#st.dataframe(data=my_dataframe, use_container_width=True)


ingredient_list = st.multiselect('Choose upto 5 elements:',
                                 my_dataframe,
                                max_selections=5)

if ingredient_list:
    
    ingredient_string = ''
    for fruit_chosen in ingredient_list:
        ingredient_string+=fruit_chosen+' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
      
        st.subheader(fruit_chosen + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+search_on)
        sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
    #st.write(ingredient_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredient_string + """','"""+name+ """')"""

    st.write(my_insert_stmt)
    
    time_to_insert=st.button('Submit')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered,{name}!', icon="✅")       
