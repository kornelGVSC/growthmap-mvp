import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

@st.cache
def load_data():
    df = pd.read_excel('sample_data.xlsx')
    return df

df = load_data()

def add_fins(x, y):

    # add annotation
    fig.add_annotation(
        x=x
        , y=y
        , text="Deployed Fins"
        , yanchor='bottom'
        , showarrow=True
        , xref="x"
        , yref="y"
        , arrowhead=0
        , arrowcolor="#636363"
        , ax=0
        , ay=-70
        , font=dict(size=15, color="black")
        , align="center")


def add_hcm(x, y):

    # add annotation
    fig.add_annotation(
        x=x
        , y=y
        , text="Deployed HCM"
        , yanchor='bottom'
        , showarrow=True
        , xref="x"
        , yref="y"
        , arrowhead=0
        , arrowcolor="#636363"
        , ax=0
        , ay=-70
        , font=dict(size=15, color="black")
        , align="center")


st.header('GROWTH MAP WIP')

st.write('*the data is fictional for demo purposes only')


# create filters
col1, col2 = st.columns(2)
customer_list = df['Customer Name'].unique().tolist()
with col1:
    selected_cust = st.selectbox(label='Select Customer', options=sorted(customer_list))

with col2:
    selected_skus = st.multiselect(label='Select Product', options=['HCM', 'FINS'])

# create helper variables based on users selection

selected_cust_str = ''.join(selected_cust)
df_filtered = df[df['Customer Name'] == selected_cust_str]

years_list = [2015, 2016, 2017, 2018, 2019, 2020, 2021]

x_axis = years_list
y_axis = df_filtered.iloc[0, 0:7].values.tolist()


# create hcm and fins years and values to pass to the add_hcm and add_fins functions
hcm_year = df_filtered['HCM Deployment'].values
hcm_year = int(hcm_year)

fins_year = df_filtered['Fins Deployment'].values
fins_year = int(fins_year)

hcm_value = df_filtered[hcm_year].values
hcm_value = int(hcm_value)

fins_value = df_filtered[fins_year].values
fins_value = int(fins_value)


# if user selected customer then create a logo variable with logo url
if selected_cust:
    selected_logo = df_filtered['Logo']
    selected_logo = selected_logo.tolist()
    selected_logo = selected_logo[0]
else:
    selected_logo = ''


# if user selected customer then create a title variable
if selected_cust:
    title = '{} Employee Growth with WD'.format(selected_cust)
else:
    title = ''


fig = px.line(x=x_axis, y=y_axis, text=y_axis, title=title, labels={'x':'Years', 'y':'Employees'})
fig.update_traces(textposition='bottom center')


# update layout
fig.update_layout(paper_bgcolor="white", plot_bgcolor='white', autosize=False,
    width=1200,
    height=600, legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1,
    xanchor="left",
    x=0.03
))

# align title
fig.update_layout(
    title={
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        font=dict(size=16))


# Add logo
fig.add_layout_image(
    dict(
        source=selected_logo,
        xref="paper", yref="paper",
        x=0.1, y=1,
        sizex=0.25, sizey=0.25,
        xanchor="right", yanchor="bottom"
    )
)



if 'FINS' in selected_skus:
    add_fins(x=fins_year, y=fins_value)
if 'HCM' in selected_skus:
    add_hcm(x=hcm_year, y=hcm_value)

st.plotly_chart(fig, theme="streamlit", use_container_width=False)


