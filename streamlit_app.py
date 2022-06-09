import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents new healthy diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado & Toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')



my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Put a Pick-up list
# streamlit.multiselect("Pick some fruits: " , list (my_fruit_list.index), ['Avocado','Strawberries'])
# Table Display
# streamlit.dataframe(my_fruit_list)

#Fruits Selected
fruit_selected = streamlit.multiselect("Pick some fruits: " , list (my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruit_selected]

# Selected fruit to display
streamlit.dataframe(fruits_to_show)

#create the repeatable code block (called a finction)

def get_fruitvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

#New Section to display fruitvice api response
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('what fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("please select a fruit to get information.")
  else:
      back_from_function = get_frutyvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)
      
except URLError as e:
    streamlit.error()

#for Stopping 

#streamlit.stop()

streamlit.header("Robert's Fruit load list contains : ")
#Snowflake related function
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()
    
# Add a button to load the fruit

if streamlit.button('Get fruit load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

#Secondary text entrybox 

fruit_choice2 = streamlit.text_input('What fruit would you like add ?', 'jackfruit')
streamlit.write('thanks for adding', fruit_choice)

# for Loading from Streamlit
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
