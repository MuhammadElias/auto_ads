import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('vehicles_us.csv')
df.info()
# fill 'n/a' for object columns and 0 for numerical columns:

fill_values = {'model': 'unknown', 'condition': 'unknown', 'fuel': 'unknown', 
               'transmission': 'unknown', 'type': 'unknown', 'paint_color': 'unknown',
               'model_year': 0, 'cylinders': 0, 'odometer': 0, 
               'is_4wd': 0, 'date_posted': 0, 'days_listed': 0}

df.fillna(value=fill_values, inplace=True)

df.info()

#creating header with an option to filter the data and the checkbox:
#dataset includes mainly used cars, but there are several new options as well
#let users decide whether they want to see new cars from dealers or not) 

st.header('Used cars market')
st.write("""
##### Filter the data below to see the ads by brand
""")
show_new_cars = st.checkbox('Include new cars from dealers')

show_new_cars
if not show_new_cars:
    df = df[df.condition!='like new']
#creating options for filter  from all manufacturers and different years
Model_selection = df['model'].unique()
Select_car_model = st.selectbox('Select manufacturer:', Model_selection)
Select_car_model
#next let's create a slider for years, so that users can filter cars by years of produciton
#creating min and max years as limits for sliders
min_year, max_year=int(df['model_year'].min()), int(df['model_year'].max())

#creating slider 
year_range = st.slider(
     "Choose years",
     value=(min_year,max_year),min_value=min_year,max_value=max_year )
year_range
#filtering dataset on chosen manufacturer and chosen year range
filtered_type=df[(df.model == df['model'].unique) & (df.model_year >= year_range[0]) &
                 (df.model_year <= year_range[1])]

#showing the final table in streamlit
st.table(filtered_type)
df
st.header('Price analysis')
st.write("""
###### here is an analysis of what influences price the most. How will price fluctuate depending on 
transmission, number of cylinders or body type and vehicle conditions.
""")

import plotly.express as px

# Will create histograms with the split by parameter of choice: color, transmission, engine_type, body_type, state

#creating list of options to choose from
list_for_hist=['transmission','cylinders','type','condition']

#creating selectbox
choice_for_hist = st.selectbox('price fluctuation distribution', list_for_hist)

#plotly histogram, where price_usd is split by the choice made in the selectbox
fig1 = px.histogram(df, x="price", color=choice_for_hist)

#adding tittle
fig1.update_layout(title="<b> Split of price by {}</b>".format(choice_for_hist))

#embedding into streamlit
st.plotly_chart(fig1)
fig1.show()
# creating age category of cars, cause we want to take it into account when analyze the price
df['age']=2022-df['model_year']

def age_category(x):
    if x<5: return '<5'
    elif x>=5 and x<10: return '5-10'
    elif x>=10 and x<20: return '10-20'
    else: return '>20'

df['age_category']=  df['age'].apply(age_category)    
df['age_category']
st.write("""
###### Now let's check how price is affected by odometer, engine capacity or number of photos in the adds
""")

#Distribution of price depending on odometer, number of cylinders, and the number of days the cr has been listed.
#with the split by age category
list_for_scatter=['odometer','cylinder','days_listed']
choice_for_scatter = st.selectbox('Price dependency on ', list_for_scatter)
fig2 = px.scatter(df, x="price", y=choice_for_scatter,hover_data=['model_year'])

fig2.update_layout(
title="<b> Price vs {}</b>".format(choice_for_scatter))
st.plotly_chart(fig2)
fig2
#EDA.py