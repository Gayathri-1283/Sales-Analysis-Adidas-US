#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


df =pd.read_excel("E:\\mp\\new adidas.xlsx")
df.head()


# In[3]:


###Cleaning dataset


# In[4]:


# 1.fill na with mean values for price per unit columns
mean_price = df['Price per Unit'].mean()  # Calculate the mean of the 'Price per Unit' column
df['Price per Unit'].fillna(mean_price, inplace=True)  # Fill missing values with the mean value
df.head()


# In[5]:


# 2.replace 0 values with formula and formatting into int
df['Total Sales'] = (df['Price per Unit'] * df['Units Sold']).astype(int)
df['Operating Profit'] = (df['Operating Margin'] * df['Total Sales']).astype(int)

df.head()


# In[6]:


# 3.split the columns
df['Gender'] = df['Product'].str.split("'s").str[0]
df.head()


# In[7]:


# 4.Data values formatting
df['Invoice Date'] = pd.to_datetime(df['Invoice Date'])  # Convert 'Invoice Date' to datetime format
df['Year'] = df['Invoice Date'].dt.year  # Extract the year

df.head()


# In[8]:


# 5. Trim spaces 
#before trimming
df['length of retailer'] = df['Retailer'].str.len()
df.head()


# In[9]:


#After trimming spaces
df['Retailer1'] = df['Retailer'].str.strip()  
df['length of retailer1'] = df['Retailer1'].str.len()
df.head()


# In[10]:


# Statistical information
df.describe()


# In[11]:


#statistical func 1: col: Price per Unit
from scipy import stats

# Filter dataframe for New York state
ny_df = df[df['State'] == 'New York']

# Group by state and calculate the descriptive statistics for 'Price per Unit'
grouped_stats = ny_df.groupby('State')['Price per Unit'].describe()

# Print the descriptive statistics
print(grouped_stats)

# Calculate mode for 'Price per Unit'
mode = stats.mode(ny_df['Price per Unit'])
print("Mode:", mode.mode[0])

# Calculate median for 'Price per Unit'
median = ny_df['Price per Unit'].median()
print("Median:", median)


# In[12]:


#statistical func 2:

# Filter dataframe for Sales Method = Online
online_df = df[df['Sales Method'] == 'Online']

# Calculate operating margin
operating_margin = online_df['Operating Margin']

# Describe operating margin
operating_margin_stats = operating_margin.describe()
print("Operating Margin Description:")
print(operating_margin_stats)

# Calculate mode for operating margin
operating_margin_mode = stats.mode(operating_margin)
print("Operating Margin Mode:", operating_margin_mode.mode[0])

# Calculate median for operating margin
operating_margin_median = operating_margin.median()
print("Operating Margin Median:", operating_margin_median)


# In[13]:


#statistical func 3:

# Filter dataframe for Year = 2021
df_2021 = df[df['Year'] == 2021]

# Calculate total sales for 2021
total_sales_2021 = df_2021['Total Sales']

# Describe total sales for 2021
total_sales_stats = total_sales_2021.describe()
print("Total Sales Description for 2021:")
print(total_sales_stats)

# Calculate mode for total sales in 2021
total_sales_mode = stats.mode(total_sales_2021)
print("Total Sales Mode for 2021:", total_sales_mode.mode[0])

# Calculate median for total sales in 2021
total_sales_median = total_sales_2021.median()
print("Total Sales Median for 2021:", total_sales_median)


# In[14]:


###Graphs


# In[15]:


#Which region has the highest revenue and operating profit, and which region has the lowest?
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Assuming you have a DataFrame named df with the necessary columns

# Filter the data to exclude any missing values in Total Sales and Operating Profit columns
filtered_df = df.dropna(subset=['Total Sales', 'Operating Profit'])

# Calculate the sum of Total Sales and Operating Profit by Region
revenue_profit_by_region = filtered_df.groupby('Region').agg({'Total Sales': 'sum', 'Operating Profit': 'sum'}).reset_index()

# Sort the data by Total Sales and Operating Profit in descending order
revenue_profit_by_region = revenue_profit_by_region.sort_values(by=['Total Sales', 'Operating Profit'], ascending=False)

# Create bar plots using Seaborn
fig, axes = plt.subplots(2, 1, figsize=(10, 12))

# Total Sales by Region
sns.barplot(data=revenue_profit_by_region, x='Total Sales', y='Region', color='blue', ax=axes[0])
axes[0].set_xlabel('Total Sales')
axes[0].set_ylabel('Region')
axes[0].set_title('Total Sales by Region')

# Operating Profit by Region
sns.barplot(data=revenue_profit_by_region, x='Operating Profit', y='Region', color='green', ax=axes[1])
axes[1].set_xlabel('Operating Profit')
axes[1].set_ylabel('Region')
axes[1].set_title('Operating Profit by Region')

# Region with highest revenue and operating profit
highest_revenue_region = revenue_profit_by_region.iloc[0]['Region']
highest_profit_region = revenue_profit_by_region.iloc[0]['Region']

# Region with lowest revenue and operating profit
lowest_revenue_region = revenue_profit_by_region.iloc[-1]['Region']
lowest_profit_region = revenue_profit_by_region.iloc[-1]['Region']

plt.tight_layout()
plt.show()

print('Region with highest revenue:', highest_revenue_region)
print('Region with highest operating profit:', highest_profit_region)
print('Region with lowest revenue:', lowest_revenue_region)
print('Region with lowest operating profit:', lowest_profit_region)


# In[16]:


#How does the number of units sold vary across different products?

import pandas as pd
import plotly.express as px

# Assuming you have a DataFrame named df with the necessary columns
fig = px.pie(df, values='Units Sold', names='Product', title='Units Sold by Product')
fig.show()


# In[17]:


# How does the relationship between total sales and operating profit differ between men and women?
# Create a figure with two subplots
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Filtered DataFrame for men and women
df_men = df[df['Gender'] == 'Men']
df_women = df[df['Gender'] == 'Women']

# Set the style of the plots
sns.set(style="darkgrid")

# Plot for men (left subplot)
sns.scatterplot(data=df_men, x='Total Sales', y='Operating Profit', ax=axes[0], color='blue')
axes[0].set_title('Men')
axes[0].set_xlabel('Sales')
axes[0].set_ylabel('Margin')

# Plot for women (right subplot)
sns.scatterplot(data=df_women, x='Total Sales', y='Operating Profit', ax=axes[1], color='orange')
axes[1].set_title('Women')
axes[1].set_xlabel('Sales')
axes[1].set_ylabel('Margin')

# Adjust the spacing between subplots
plt.tight_layout()

# Display the plot
plt.show()


# In[18]:


#How does the price per unit affect the number of units sold and total sales?
# Set the style of the plot
sns.set(style="darkgrid")

# Create the bubble chart
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Price per Unit', y='Units Sold', size='Total Sales', sizes=(30, 300),
                alpha=0.7, edgecolor='black')

# Set the title and labels for the plot
plt.title('Price per Unit vs Number of Units Sold (Bubble Size: Total Sales)')
plt.xlabel('Price per Unit')
plt.ylabel('Number of Units Sold')

# Display the plot
plt.show()


# In[19]:


#What is the total revenue generated by the retailer during a specific period?
# Filter the DataFrame for retailer='Amazon' and year='2021'
filtered_df = df[(df['Retailer'] == 'Amazon') & (df['Year'] == 2021)]

df1 = filtered_df[['Retailer', 'Year', 'Region', 'Product', 'Total Sales']]

# Group the filtered data by product and region and calculate the average total sales
average_sales = df1.groupby(['Region', 'Product'])['Total Sales'].mean().reset_index()

# Create the pivot table
pivot_table = average_sales.pivot(index='Region', columns='Product', values='Total Sales')

# Create the heatmap using Seaborn
plt.figure(figsize=(10, 6))
sns.heatmap(data=pivot_table, annot=True, cmap='YlGnBu', fmt='.2f', linewidths=0.5)
plt.title('Average Total Sales by Product and Region')
plt.xlabel('Product')
plt.ylabel('Region')
plt.show()


# In[ ]:



