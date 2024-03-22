import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import numpy as np


#Read the data 
df=pd.read_csv("EnergyData.csv")

df['billing_date'] = pd.to_datetime(df['billing_date'])

df["year"]=df["billing_date"].dt.year
df["month"]=df["billing_date"].dt.month

num_stores = df["facility"].nunique()

#separate data by utility type
df_electricity =df[ df["utility_type"]=="Electricity"]
df_naturalgas= df[df["utility_type"]=="NaturalGas"]

gpd_df_electricity= df_electricity.groupby(['year', 'month']).mean(numeric_only=True).reset_index()
gpd_df_naturalgas=df_naturalgas.groupby(["year","month" ]).mean(numeric_only=True).reset_index()

def calculate_saving(raw_df, num_stores):
    # Separate the data by year
    df_pre_covid = raw_df[raw_df['year'] <= 2019]
    df_post_covid = raw_df[raw_df['year'].isin([2022, 2023])]

    # Calculate the average usage and cost for the pre-COVID period
    pre_covid_avg_usage = df_pre_covid['usage'].mean()
    pre_covid_avg_cost = df_pre_covid['cost'].mean()

    # Calculate the average usage and cost for the post-COVID period
    post_covid_avg_usage = df_post_covid['usage'].mean()
    post_covid_avg_cost = df_post_covid['cost'].mean()

    # Calculate the difference in average usage and cost
    usage_diff = (post_covid_avg_usage - pre_covid_avg_usage)*num_stores
    cost_diff = (post_covid_avg_cost - pre_covid_avg_cost)*num_stores

    # Calculate the percentage saved
    usage_saved_percentage = (usage_diff / (pre_covid_avg_usage * num_stores)) * 100
    cost_saved_percentage = (cost_diff / (pre_covid_avg_cost * num_stores)) * 100

    st.write(f"usage difference before and after covid years kwh: {usage_diff}")
    st.write(f"cost difference before and after covid years kwh: {cost_diff}")
    st.write(f"usage percentage saved before and after covid years : {usage_saved_percentage}")
    st.write(f"cost percentage saved before and after covid years : {cost_saved_percentage}")
    st.write(f"dollar saved estimated before and after covid based on usage:{(usage_diff*0.192)}")

st.write("electricity:")
calculate_saving(df_electricity, num_stores=num_stores)
st.write("natural gas")
calculate_saving(df_naturalgas, num_stores=num_stores)

################ Store 0309 data ################

df_309=(df[df["facility"]== "SBD0309"])


df_309_electricity = df_309[df_309["utility_type"]=="Electricity"]

st.write(df_309_electricity)

df_309_naturalgas = df_309[df_309["utility_type"]=="NaturalGas"]

gpd_df_309_electricity= df_309_electricity.groupby(['year', 'month']).sum(numeric_only=True).reset_index()
gpd_df_309_naturalgas=df_309_naturalgas.groupby(["year","month" ]).sum(numeric_only=True).reset_index()






###############plot################
# def plot_data(_df, name:str):

#     _df['date'] = pd.to_datetime(_df['year'].astype(str) + '-' + _df['month'].astype(str))

#     # Create a line chart for electricity data
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=_df['date'], y=_df['usage'], mode='lines', name=f'{name} Usage'))
#     fig.add_trace(go.Scatter(x=_df['date'], y=_df['cost'], mode='lines', name=f'{name} Cost', yaxis='y2'))

#     fig.update_layout(
#         title=f'{name} Data',
#         xaxis_title='Date',
#         yaxis_title='Usage',
#         xaxis=dict(
#         tickformat="%Y-%m-%d"
#     ),
#         yaxis2=dict(
#             title='Cost',
#             titlefont=dict(
#                 color='rgb(148, 103, 189)'
#             ),
#             tickfont=dict(
#                 color='rgb(148, 103, 189)'
#             ),
#             overlaying='y',
#             side='right'
#         )
#     )

#     # Display the chart in Streamlit
#     st.plotly_chart(fig)



def plot_data(_df, name:str):

    _df['date'] = pd.to_datetime(_df['year'].astype(str) + '-' + _df['month'].astype(str))

    # Create a line chart for electricity data
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=_df['date'], y=_df['usage'], mode='lines', name=f'{name} Usage'))
    fig.add_trace(go.Scatter(x=_df['date'], y=_df['cost'], mode='lines', name=f'{name} Cost', yaxis='y2'))

    # Fit a line to the 'usage' data and add it to the plot
    z = np.polyfit(_df.index, _df['usage'], 1)
    p = np.poly1d(z)
    fig.add_trace(go.Scatter(x=_df['date'], y=p(_df.index), mode='lines', name=f'{name} Usage Trend'))

    # Fit a line to the 'cost' data and add it to the plot
    z = np.polyfit(_df.index, _df['cost'], 1)
    p = np.poly1d(z)
    fig.add_trace(go.Scatter(x=_df['date'], y=p(_df.index), mode='lines', name=f'{name} Cost Trend', yaxis='y2'))

    fig.update_layout(
        title=f'{name} Data',
        xaxis_title='Date',
        yaxis_title='Usage',
        xaxis=dict(
        tickformat="%Y-%m-%d"
    ),
        yaxis2=dict(
            title='Cost',
            titlefont=dict(
                color='rgb(148, 103, 189)'
            ),
            tickfont=dict(
                color='rgb(148, 103, 189)'
            ),
            overlaying='y',
            side='right'
        )
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig)

plot_data(gpd_df_electricity, "Electricity")
plot_data(gpd_df_naturalgas, "Natural Gas")
plot_data(gpd_df_309_electricity, "Electricity")
plot_data(gpd_df_309_naturalgas, "Natural Gas")


