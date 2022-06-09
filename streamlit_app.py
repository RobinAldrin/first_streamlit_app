import streamlit

streamlit.title('My Parents new healthy diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado & Toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


import pandas
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

#New Section to display fruitvice api response
streamlit.header('Fruityvice Fruit Advice!')
fruit_choice = streamlit.text_input('what fruit would you like information about?', 'kiwi')
streamlit.write('the user entered', fruit_choice)

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)


# taking jason version for normalizing 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#output it the screen as a table
streamlit.dataframe(fruityvice_normalized)

import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.header("Robert's Fruit load list contains : ")
streamlit.dataframe(my_data_row)
