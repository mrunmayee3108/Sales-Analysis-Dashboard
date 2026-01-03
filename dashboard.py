import streamlit as st 
import pandas as pd
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')
import os 

st.set_page_config(page_title='Superstore Dashboard', page_icon='📊', layout='wide')

st.title('📊Superstore Data Insights📊')
st.markdown('<style>div.block-container{padding-top: 2rem;}</style>', unsafe_allow_html=True)

df = pd.read_excel("Sample - Superstore.xlsx")

date_col1, date_col2 = st.columns(2)
df['Order Date'] = pd.to_datetime(df['Order Date'])
startDate = pd.to_datetime(df['Order Date']).min()
endDate = pd.to_datetime(df['Order Date']).max()
with date_col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))
with date_col2: 
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df['Order Date']>=date1) & (df['Order Date']<=date2)].copy()

st.sidebar.write("Choose your filter")

filtered_df = df.copy()

region = st.sidebar.multiselect(
    "Pick your Region",
    filtered_df["Region"].unique()
)
if region:
    filtered_df = filtered_df[filtered_df["Region"].isin(region)]

state = st.sidebar.multiselect(
    "Pick your State",
    filtered_df["State"].unique()
)
if state:
    filtered_df = filtered_df[filtered_df["State"].isin(state)]

city = st.sidebar.multiselect(
    "Pick your City",
    filtered_df["City"].unique()
)
if city:
    filtered_df = filtered_df[filtered_df["City"].isin(city)]

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total Sales", f"${total_sales:,.0f}")
kpi2.metric("Total Profit", f"${total_profit:,.0f}")
kpi3.metric("Orders", total_orders)

chart_col1, chart_col2 = st.columns(2)

category_df = filtered_df.groupby('Category', as_index=False)['Sales'].sum()

with chart_col1:
    st.subheader("Category wise Sales")
    fig = px.bar(
        category_df,
        x='Category',
        y='Sales',
        color='Category',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig, use_container_width=True)

with chart_col2: 
    st.subheader("Region wise Sales")
    fig2 = px.pie(
        filtered_df,
        values='Sales',
        names='Region',
        hole=0.5,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig2, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Profit vs Sales")
    fig3 = px.scatter(
        filtered_df, 
        x = 'Sales', 
        y = 'Profit',
        color = 'Category', 
        color_discrete_sequence = px.colors.qualitative.Set2
    )
    st.plotly_chart(fig3, use_container_width=True)

segment_df = filtered_df.groupby('Segment', as_index=False)['Sales'].sum()
with col2:
    st.subheader("Segment wise Sales")
    fig4 = px.funnel(
        segment_df, 
        x = 'Sales', 
        y = 'Segment', 
        color = 'Segment', 
        color_discrete_sequence = px.colors.qualitative.Set2
    )
    st.plotly_chart(fig4, use_container_width=True)

c1, c2 = st.columns(2)

category_df1 = filtered_df.groupby('Category', as_index=False)['Profit'].sum()
with c1:
    st.subheader("Category wise Profit (Sunburst)")
    fig5 = px.sunburst(
        filtered_df,
        path = ['Category', 'Segment'],
        values = 'Profit',  
        color = 'Category',
        color_discrete_sequence = px.colors.qualitative.Set2,
    )
    fig5.update_traces(
        textinfo="label+value" 
    )
    st.plotly_chart(fig5, use_container_width=True)

shipmode_df = filtered_df.groupby('Ship Mode', as_index=False)['Sales'].sum()
with c2:
    st.subheader("Ship mode vs Sales")
    fig6 = px.bar(
        shipmode_df, 
        x = 'Sales',
        y = 'Ship Mode', 
        color = 'Ship Mode', 
        color_discrete_sequence = px.colors.qualitative.Set2
    )
    st.plotly_chart(fig6, use_container_width = True)

# tree map -- region, category, sub category
st.subheader("Hierarchical view of Sales using treemap")
fig7 = px.treemap(
    filtered_df, 
    path = ['Region', 'Category', 'Sub-Category'], 
    values = 'Sales', 
    hover_data = 'Sales', 
    color = 'Sub-Category' 
)
st.plotly_chart(fig7, use_container_width = True)

