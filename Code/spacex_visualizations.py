import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Connect to the SQLite database
con = sqlite3.connect("my_data1.db")
df = pd.read_sql_query("SELECT * FROM SPACEXTABLE", con)

# Helper function to save matplotlib plots
def save_plot(fig, filename):
    fig.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close(fig)

# Slide 18: Scatter Plot of Flight Number vs. Launch Site
def plot_flight_number_vs_launch_site():
    fig = plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x=df.index, y='Launch_Site', hue='Launch_Site', size='PAYLOAD_MASS__KG_', sizes=(50, 200))
    plt.title('Flight Number vs. Launch Site')
    plt.xlabel('Flight Number')
    plt.ylabel('Launch Site')
    plt.legend(title='Launch Site')
    save_plot(fig, 'flight_number_vs_launch_site.png')

# Slide 19: Scatter Plot of Payload vs. Launch Site
def plot_payload_vs_launch_site():
    fig = plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='PAYLOAD_MASS__KG_', y='Launch_Site', hue='Launch_Site', size='PAYLOAD_MASS__KG_', sizes=(50, 200))
    plt.title('Payload Mass vs. Launch Site')
    plt.xlabel('Payload Mass (kg)')
    plt.ylabel('Launch Site')
    plt.legend(title='Launch Site')
    save_plot(fig, 'payload_vs_launch_site.png')

# Slide 20: Bar Chart of Success Rate vs. Orbit Type
def plot_success_rate_vs_orbit():
    success_df = df.groupby('Orbit')['Mission_Outcome'].apply(lambda x: (x.str.contains('Success').sum() / len(x)) * 100).reset_index()
    success_df.columns = ['Orbit', 'Success_Rate']
    fig = plt.figure(figsize=(10, 6))
    sns.barplot(data=success_df, x='Orbit', y='Success_Rate', hue='Orbit', palette='viridis', legend=False)
    plt.title('Success Rate vs. Orbit Type')
    plt.xlabel('Orbit Type')
    plt.ylabel('Success Rate (%)')
    plt.xticks(rotation=45)
    save_plot(fig, 'success_rate_vs_orbit.png')

# Slide 21: Scatter Plot of Flight Number vs. Orbit Type
def plot_flight_number_vs_orbit():
    fig = plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x=df.index, y='Orbit', hue='Orbit', size='PAYLOAD_MASS__KG_', sizes=(50, 200))
    plt.title('Flight Number vs. Orbit Type')
    plt.xlabel('Flight Number')
    plt.ylabel('Orbit Type')
    plt.legend(title='Orbit Type')
    save_plot(fig, 'flight_number_vs_orbit.png')

# Slide 22: Scatter Plot of Payload vs. Orbit Type
def plot_payload_vs_orbit():
    fig = plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='PAYLOAD_MASS__KG_', y='Orbit', hue='Orbit', size='PAYLOAD_MASS__KG_', sizes=(50, 200))
    plt.title('Payload Mass vs. Orbit Type')
    plt.xlabel('Payload Mass (kg)')
    plt.ylabel('Orbit Type')
    plt.legend(title='Orbit Type')
    save_plot(fig, 'payload_vs_orbit.png')

# Slide 23: Line Chart of Launch Success Yearly Trend
def plot_yearly_success_trend():
    df['Year'] = pd.to_datetime(df['Date']).dt.year
    yearly_success = df.groupby('Year')['Mission_Outcome'].apply(lambda x: (x.str.contains('Success').sum() / len(x)) * 100).reset_index()
    yearly_success.columns = ['Year', 'Success_Rate']
    fig = plt.figure(figsize=(10, 6))
    sns.lineplot(data=yearly_success, x='Year', y='Success_Rate', marker='o')
    plt.title('Yearly Launch Success Trend')
    plt.xlabel('Year')
    plt.ylabel('Success Rate (%)')
    save_plot(fig, 'yearly_success_trend.png')

# Slide 39: Pie Chart of Launch Success Count for All Sites
def plot_launch_success_count():
    success_counts = df.groupby('Launch_Site')['Mission_Outcome'].apply(lambda x: x.str.contains('Success').sum()).reset_index()
    success_counts.columns = ['Launch_Site', 'Success_Count']
    fig = px.pie(success_counts, values='Success_Count', names='Launch_Site', title='Launch Success Count by Site')
    fig.update_layout(showlegend=True)
    fig.update_traces(textinfo='percent+label')
    fig.write_image('launch_success_count.png')

# Slide 40: Pie Chart of Launch Site with Highest Success Ratio
def plot_highest_success_ratio():
    success_ratios = df.groupby('Launch_Site')['Mission_Outcome'].apply(lambda x: (x.str.contains('Success').sum() / len(x)) * 100).reset_index()
    success_ratios.columns = ['Launch_Site', 'Success_Ratio']
    top_site = success_ratios.loc[success_ratios['Success_Ratio'].idxmax()]
    fig = px.pie(values=[top_site['Success_Ratio'], 100 - top_site['Success_Ratio']], 
                 names=[top_site['Launch_Site'], 'Other'], 
                 title=f'Highest Success Ratio: {top_site["Launch_Site"]}')
    fig.update_traces(textinfo='percent+label')
    fig.write_image('highest_success_ratio.png')

# Slide 41: Interactive Scatter Plot of Payload vs. Launch Outcome with Range Slider
def plot_payload_vs_launch_outcome():
    # Fix typo in original: 'Launch_S520' to 'Launch_Site'
    fig = px.scatter(df, x='PAYLOAD_MASS__KG_', y='Landing_Outcome', color='Launch_Site', size='PAYLOAD_MASS__KG_',
                     title='Payload Mass vs. Landing Outcome',
                     labels={'PAYLOAD_MASS__KG_': 'Payload Mass (kg)', 'Landing_Outcome': 'Landing Outcome'})
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(visible=True),
            type='linear'
        )
    )
    fig.write_html('payload_vs_launch_outcome.html')  # Save as HTML for interactivity

# Execute all plotting functions
plot_flight_number_vs_launch_site()
plot_payload_vs_launch_site()
plot_success_rate_vs_orbit()
plot_flight_number_vs_orbit()
plot_payload_vs_orbit()
plot_yearly_success_trend()
plot_launch_success_count()
plot_highest_success_ratio()
plot_payload_vs_launch_outcome()

# Close the database connection
con.close()