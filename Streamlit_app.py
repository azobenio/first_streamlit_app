import streamlit
import pandas 
import requests
import snowflake.connector
from urllib.error import URLEerror

streamlit.title('MY Moms New Healthy Diner')

streamlit.header('🥣Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled free-range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Buid Your Own Fruit Smoothie 🥝🍇')

#import pandas 
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')


#Let's put a pick list here so they can pick the fdruit they want to include
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

#display the table on the page
streamlit.dataframe(my_fruit_list)

# let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display the table on the page
streamlit.dataframe(fruits_to_show)

#New Section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

#import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)


# write your own comment -what does the next line do? 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
streamlit.dataframe(fruityvice_normalized)

# don't run anything past here while we troubleshout
streamlit.stop()


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

def insert_row_snowflake(new_fruit):
  with conn.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list (fruit_name) values ('" + new_fruit + "');")
    return "Thanks for adding " + new_fruit

 # allow the end user to add a fruit to the list
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
  conn = init_connection()
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  conn.commit()
  conn.close()
  streamlit.text(back_from_function)
  
# This will not work correctly, but just go woth it for now
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
