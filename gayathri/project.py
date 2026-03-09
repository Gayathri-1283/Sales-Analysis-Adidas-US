import streamlit as st
import plotly.express as px
import pandas as pd 
import numpy as np
import os
from streamlit_option_menu import option_menu
from prophet import Prophet
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Python-Streamlit Dashoard",page_icon=":earth_asia:",layout="wide")

st.title(":earth_asia: Analysing Adidas Sales ")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>',unsafe_allow_html=True)



    
def Home():
    # Load data from Excel file
    df =pd.read_excel("new adidas.xlsx")

    # Split the app layout into two columns
    col1, col2 = st.columns((2))
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], format="%d-%m-%Y" )

    # Getting the min and max date 
    startDate = pd.to_datetime(df["InvoiceDate"]).min()
    endDate = pd.to_datetime(df["InvoiceDate"]).max()

    # Allow user to select a date range
    with col1:
        date1 = pd.to_datetime(st.date_input("Start Date", startDate))

    with col2:
        date2 = pd.to_datetime(st.date_input("End Date", endDate))

    # Filter the data based on the selected date range
    df = df[(df["InvoiceDate"] >= date1) & (df["InvoiceDate"] <= date2)].copy()

# Sidebar
    st.sidebar.header("Choose your filter: ")

    # Filter By Region
    region = st.sidebar.multiselect("Pick your Region", df["Region"].unique())
    if not region:
        df2 = df.copy()
    else:
        df2 = df[df["Region"].isin(region)]

    # Filter By State
    state = st.sidebar.multiselect("Pick the State", df2["State"].unique())
    if not state:
        df3 = df2.copy()
    else:
        df3 = df2[df2["State"].isin(state)]

    # Filter By City
    city = st.sidebar.multiselect("Pick the City",df3["City"].unique())

    # Filter the data based on Region, State and City
    if not region and not state and not city:
        filtered_df = df
    elif not state and not city:
        filtered_df = df[df["Region"].isin(region)]
    elif not region and not city:
        filtered_df = df[df["State"].isin(state)]
    elif state and city:
        filtered_df = df3[df["State"].isin(state) & df3["City"].isin(city)]
    elif region and city:
        filtered_df = df3[df["Region"].isin(region) & df3["City"].isin(city)]
    elif region and state:
        filtered_df = df3[df["Region"].isin(region) & df3["State"].isin(state)]
    elif city:
        filtered_df = df3[df3["City"].isin(city)]
    else:
        filtered_df = df3[df3["Region"].isin(region) & df3["State"].isin(state) & df3["City"].isin(city)]
# visualizations
    
    # Category wise Sales
    category_df = filtered_df.groupby(by = ["Product"], as_index = False)["TotalSales"].sum()

    with col1:
        st.subheader("Category wise Sales")
    # Create bar chart 
        fig = px.bar(category_df, x = "Product", y = "TotalSales", text = ['${:,.2f}'.format(x) for x in category_df["TotalSales"]],
                    template = "seaborn")
        st.plotly_chart(fig,use_container_width=True, height = 200)

        # Display summary tables
        with st.expander("Category wise Sales Data"):
            st.dataframe(category_df.style.background_gradient(cmap="Blues"), height=600)

        # Download button
            csv = category_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="Category.csv", mime="text/csv",
                        help='Click here to download the data as a CSV file')
     # Create pie chart
        st.subheader("Sales Methods")
        fig = px.pie(filtered_df, values = "TotalSales", names = "SalesMethod", hole = 0.5)
        fig.update_traces(text = filtered_df["SalesMethod"], textposition = "outside")
        st.plotly_chart(fig,use_container_width=True)

        # Display summary tables
        with st.expander("Sales Methods"):
            st.write(category_df.style.background_gradient(cmap="Blues"))
            csv = category_df.to_csv(index = False).encode('utf-8')
        # Download button
        st.download_button("Download Data", data = csv, file_name = "Sales Methods.csv", mime = "text/csv",
                                help = 'Click here to download the data as a CSV file')
        

    
    
    

    with col2:
    # Region wise Sales
        st.subheader("Region wise Sales")
        fig = px.pie(filtered_df, values = "TotalSales", names = "Region", hole = 0.5)
        fig.update_traces(text = filtered_df["Region"], textposition = "outside")
        st.plotly_chart(fig,use_container_width=True)

        # Display summary tables
        with st.expander("Region Wise Sales"):
            region = filtered_df.groupby(by = "Region", as_index = False)["TotalSales"].sum()
            st.write(region.style.background_gradient(cmap="Oranges"))
            csv = region.to_csv(index = False).encode('utf-8')
        # Download button
        st.download_button("Download Data", data = csv, file_name = "Region.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')

    # Retailer wise Sales   
        st.subheader("Retailer wise Sales")
        fig = px.pie(filtered_df, values = "TotalSales", names = "Retailer", hole = 0.5)
        fig.update_traces(text = filtered_df["Retailer"], textposition = "outside")
        st.plotly_chart(fig,use_container_width=True)

        # Display summary tables
        with st.expander("Retailer wise Sales"):
            region = filtered_df.groupby(by = "Retailer", as_index = False)["TotalSales"].sum()
            st.write(region.style.background_gradient(cmap="Oranges"))
        # Download button
        csv = region.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Retailer wise Sales.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')

    
        
# Time series analysis
        
    # Assuming filtered_df is defined elsewhere in your code

    filtered_df["month_year"] = filtered_df["InvoiceDate"].dt.to_period("M").astype(str)

    st.subheader('Time Series Analysis')
    # Group by month_year and sum TotalSales
    linechart = pd.DataFrame(filtered_df.groupby("month_year")["TotalSales"].sum()).reset_index()

    # Sort linechart by month_year in ascending order
    linechart = linechart.sort_values("month_year")

    fig2 = px.line(linechart, x="month_year", y="TotalSales", labels={"Sales": "Amount"}, height=500, width=1000, template="gridon",
                hover_data={"month_year": False, "TotalSales": True})  # Customize hover data

    fig2.update_traces(hovertemplate='%{x}: %{y}')  # Customize hover template

    st.plotly_chart(fig2, use_container_width=True)

    with st.expander("View Data of TimeSeries:"):
        st.write(linechart.T.style.background_gradient(cmap="Blues"))
        csv = linechart.to_csv(index=False).encode("utf-8")
        st.download_button('Download Data', data=csv, file_name="TimeSeries.csv", mime='text/csv')


    

def Geomap():
    options = ['Total sales', 'Retailer wise', 'Product wise', 'Sales Method']
    selected_option = st.selectbox('Select an option to visualize sales data', options)
    
    if selected_option == 'Total sales':
        df = pd.read_csv("C:\\gayathri\\total_sales_by_state.csv")
        year_list = list(df.Year.unique())[::-1]
        selected_year = st.selectbox('Select a year', year_list)
        df_selected_year = df[df.Year == selected_year]
        color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
        selected_color_theme = st.selectbox('Select a color theme', color_theme_list)

        def make_choropleth(input_df, input_id, input_column, input_color_theme):
            choropleth = px.choropleth(input_df, 
                                        locations=input_id, 
                                        color=input_column, 
                                        locationmode="USA-states",
                                        color_continuous_scale=input_color_theme,
                                        range_color=(0, max(df_selected_year.TotalSales)),  
                                        scope="usa",
                                        hover_name='State',
                                        labels={'totalSales':'TotalSales'},
                                        title='Total Sales by State',
                                        hover_data={input_id: False}  
                                    )
            choropleth.update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                margin=dict(l=0, r=0, t=0, b=0),
                height=350
            )
            return choropleth
    
        choropleth = make_choropleth(df_selected_year, 'state_code', 'TotalSales', selected_color_theme)
        st.plotly_chart(choropleth, use_container_width=True)
    elif selected_option == 'Retailer wise':
        
        df = pd.read_csv("C:\\gayathri\\total_sales_of_Retailers_by_state.csv")
        # Find the dominant retailer in each state
        dominant_retailer_by_state = df.loc[df.groupby('State')['TotalSales'].idxmax()]
        
        color_mapping = {
            'Foot Locker': 'blue',
            'West Gear': 'green',
            'Sports Direct': 'pink',
            "Kohl's": 'orange',
            'Amazon': 'yellow',
            'Walmart': 'red'
        }

        dominant_retailer_by_state['Color'] = dominant_retailer_by_state['Retailer'].map(color_mapping)

        # Inside the 'Retailer wise' branch of the Geomap function

     
        fig = px.choropleth(dominant_retailer_by_state, 
                                locations='state_code', 
                                locationmode='USA-states', 
                                color='Retailer',  
                                scope="usa",
                                hover_name='State',
                                hover_data={'TotalSales': True},
                                color_discrete_map=color_mapping,
                                title='Dominant Retailer by State')
        dominant_retailer_by_state['TotalSales_Million'] = round(dominant_retailer_by_state['TotalSales'] / 1_000_000, 2)
        fig.update_traces(hovertemplate='%{customdata[0]:,.2f} Million USD<br>%{hovertext}<extra></extra>',
                  customdata=dominant_retailer_by_state[['TotalSales_Million']].values)

        fig.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='rgba(0,0,0,0)'))

        st.plotly_chart(fig)
        
    elif selected_option == 'Product wise':
        df = pd.read_csv("C:\\gayathri\\Sales_by_Product.csv")
        # Find the dominant Product in each state
        dominant_product_by_state = df.loc[df.groupby('State')['UnitsSold'].idxmax()]
        
        color_mapping = {
            "Men's Apparel": 'blue',
            "Men's Athletic Footwear":'green',
            "Men's Street Footwear": 'pink',
            "Women's Apparel": 'orange',
            "Women's Athletic Footwear": 'yellow',
            "Women's Street Footwear": 'red'
        }

        dominant_product_by_state['Color'] = dominant_product_by_state['Product'].map(color_mapping)

       

     
        fig = px.choropleth(dominant_product_by_state, 
                                locations='state_code', 
                                locationmode='USA-states', 
                                color='Product',  
                                scope="usa",
                                hover_name='State',
                                hover_data={'UnitsSold': True},
                                color_discrete_map=color_mapping,
                                title='Dominant Product In Each State')
        
        
        fig.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='rgba(0,0,0,0)'))

        st.plotly_chart(fig)
    elif selected_option == 'Sales Method':
        # Load data
        df = pd.read_csv("C:\\gayathri\\Salesmethod_by_state.csv")

        # Find the dominant sales method in each state
        idx = df.groupby('State')['TotalSales'].idxmax()
        dominant_sales_method = df.loc[idx]

        # Create the choropleth map
        fig = px.choropleth(dominant_sales_method,
                            locations='state_code',
                            locationmode='USA-states',
                            color='SalesMethod',
                            scope='usa',
                            color_discrete_map={'Online': 'blue', 'Outlet': 'green', 'Instore': 'red'},  # Assign colors to sales methods
                            hover_name='State',
                            hover_data={'SalesMethod': False},  # Remove the SalesMethod label
                            title='Dominant Sales Method by State')

        fig.update_traces(hovertemplate='<b>%{hovertext}</b><br>Sales Method: %{customdata}<extra></extra>',
                  customdata=dominant_sales_method['SalesMethod'].values)
        # Update layout
        fig.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='rgba(0,0,0,0)'))

        # Display the plot
        st.plotly_chart(fig)
    


def Predict():
    monthly_sales= pd.read_csv("monthly_sales.csv")
    model = Prophet()
    monthly_sales = monthly_sales.rename(columns={'Month': 'ds', 'TotalSales': 'y'})
    model.fit(monthly_sales)
    future_dates = model.make_future_dataframe(periods=3, freq='M')
    forecast = model.predict(future_dates)
    fig = model.plot(forecast)
    plt.xlabel('Month')
    plt.ylabel('Sales Qty')
    plt.title('Monthly Sales Forecast')
    ymin, ymax = plt.gca().get_ylim()

    # Set the y-axis limits to display actual sales values
    plt.yticks(plt.yticks()[0], ['{:,.0f}'.format(x) for x in plt.yticks()[0]])

    # Show the plot
    st.pyplot(fig)




#sidebar 
def sideBar():
    with st.sidebar:
        selected=option_menu(
            menu_title="Main Menu",
            options=["Home","Geomap","Prediction"],
            icons=["house","eye"],
            menu_icon="cast",
            default_index=0
        )
    if selected=="Home":
        Home()
    elif selected=="Geomap":
        Geomap()
    elif selected=="Prediction":
        Predict()
    


sideBar()





