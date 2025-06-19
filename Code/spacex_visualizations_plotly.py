import sqlite3
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import traceback
from func_timeout import func_timeout, FunctionTimedOut

# Check kaleido availability
try:
    import kaleido
    print(f"Kaleido version: {kaleido.__version__}")
except ImportError:
    print("Kaleido not installed. Install with: pip install kaleido")
    kaleido_available = False
else:
    kaleido_available = True

# Connect to the SQLite database
print("Connecting to database...")
con = sqlite3.connect("my_data1.db")
df = pd.read_sql_query("SELECT * FROM SPACEXTABLE", con)

# Clean and validate data
print("Cleaning and validating data...")
df = df.dropna(subset=['Launch_Site', 'Mission_Outcome', 'Landing_Outcome', 'PAYLOAD_MASS__KG_'])
df['PAYLOAD_MASS__KG_'] = pd.to_numeric(df['PAYLOAD_MASS__KG_'], errors='coerce').fillna(0)
# Remove empty strings or whitespace-only values
df = df[df['Launch_Site'].str.strip() != '']
df = df[df['Mission_Outcome'].str.strip() != '']
# Log unique values for debugging
print(f"Unique Launch_Site values: {df['Launch_Site'].unique()}")
print(f"Unique Mission_Outcome values: {df['Mission_Outcome'].unique()}")

# Helper function to save matplotlib plots (fallback)
def save_matplotlib_plot(fig, filename):
    print(f"Saving {filename} with Matplotlib...")
    fig.savefig(filename, dpi=100, bbox_inches='tight')
    plt.close(fig)

# Slide 39: Pie Chart of Launch Success Count for All Sites
def plot_launch_success_count():
    print("Generating Launch Success Count by Site plot...")
    try:
        # Compute success counts
        success_counts = df.groupby('Launch_Site')['Mission_Outcome'].apply(
            lambda x: x.str.contains('Success', case=False).sum()
        ).reset_index()
        success_counts.columns = ['Launch_Site', 'Success_Count']
        print(f"Success counts:\n{success_counts}")

        if kaleido_available:
            try:
                fig = px.pie(
                    success_counts,
                    values='Success_Count',
                    names='Launch_Site',
                    title='Launch Success Count by Site'
                )
                fig.update_layout(showlegend=True)
                fig.update_traces(textinfo='percent+label')
                print("Saving launch_success_count.png with Plotly...")
                func_timeout(30, fig.write_image, args=('launch_success_count.png',), kwargs={'engine': 'kaleido'})
                print("Saved launch_success_count.png with Plotly")
            except FunctionTimedOut:
                print("Plotly write_image timed out, falling back to Matplotlib...")
                fig = plt.figure(figsize=(8, 8))
                plt.pie(
                    success_counts['Success_Count'],
                    labels=success_counts['Launch_Site'],
                    autopct='%1.1f%%',
                    colors=sns.color_palette('viridis', len(success_counts))
                )
                plt.title('Launch Success Count by Site')
                save_matplotlib_plot(fig, 'launch_success_count.png')
            except Exception as e:
                print(f"Plotly error: {str(e)}")
                traceback.print_exc()
                print("Falling back to Matplotlib...")
                fig = plt.figure(figsize=(8, 8))
                plt.pie(
                    success_counts['Success_Count'],
                    labels=success_counts['Launch_Site'],
                    autopct='%1.1f%%',
                    colors=sns.color_palette('viridis', len(success_counts))
                )
                plt.title('Launch Success Count by Site')
                save_matplotlib_plot(fig, 'launch_success_count.png')
        else:
            print("Kaleido not available, using Matplotlib...")
            fig = plt.figure(figsize=(8, 8))
            plt.pie(
                success_counts['Success_Count'],
                labels=success_counts['Launch_Site'],
                autopct='%1.1f%%',
                colors=sns.color_palette('viridis', len(success_counts))
            )
            plt.title('Launch Success Count by Site')
            save_matplotlib_plot(fig, 'launch_success_count.png')

    except Exception as e:
        print(f"Error in plot_launch_success_count: {str(e)}")
        traceback.print_exc()

# Slide 40: Pie Chart of Launch Site with Highest Success Ratio
def plot_highest_success_ratio():
    print("Generating Highest Success Ratio plot...")
    try:
        success_ratios = df.groupby('Launch_Site')['Mission_Outcome'].apply(
            lambda x: (x.str.contains('Success', case=False).sum() / len(x)) * 100
        ).reset_index()
        success_ratios.columns = ['Launch_Site', 'Success_Ratio']
        top_site = success_ratios.loc[success_ratios['Success_Ratio'].idxmax()]
        print(f"Top site: {top_site['Launch_Site']} with {top_site['Success_Ratio']}% success")

        if kaleido_available:
            try:
                fig = px.pie(
                    values=[top_site['Success_Ratio'], 100 - top_site['Success_Ratio']],
                    names=[top_site['Launch_Site'], 'Other'],
                    title=f'Highest Success Ratio: {top_site["Launch_Site"]}'
                )
                fig.update_traces(textinfo='percent+label')
                print("Saving highest_success_ratio.png with Plotly...")
                func_timeout(30, fig.write_image, args=('highest_success_ratio.png',), kwargs={'engine': 'kaleido'})
                print("Saved highest_success_ratio.png with Plotly")
            except FunctionTimedOut:
                print("Plotly write_image timed out, falling back to Matplotlib...")
                fig = plt.figure(figsize=(8, 8))
                plt.pie(
                    [top_site['Success_Ratio'], 100 - top_site['Success_Ratio']],
                    labels=[top_site['Launch_Site'], 'Other'],
                    autopct='%1.1f%%',
                    colors=sns.color_palette('viridis', 2)
                )
                plt.title(f'Highest Success Ratio: {top_site["Launch_Site"]}')
                save_matplotlib_plot(fig, 'highest_success_ratio.png')
            except Exception as e:
                print(f"Plotly error: {str(e)}")
                traceback.print_exc()
                print("Falling back to Matplotlib...")
                fig = plt.figure(figsize=(8, 8))
                plt.pie(
                    [top_site['Success_Ratio'], 100 - top_site['Success_Ratio']],
                    labels=[top_site['Launch_Site'], 'Other'],
                    autopct='%1.1f%%',
                    colors=sns.color_palette('viridis', 2)
                )
                plt.title(f'Highest Success Ratio: {top_site["Launch_Site"]}')
                save_matplotlib_plot(fig, 'highest_success_ratio.png')
        else:
            print("Kaleido not available, using Matplotlib...")
            fig = plt.figure(figsize=(8, 8))
            plt.pie(
                [top_site['Success_Ratio'], 100 - top_site['Success_Ratio']],
                labels=[top_site['Launch_Site'], 'Other'],
                autopct='%1.1f%%',
                colors=sns.color_palette('viridis', 2)
            )
            plt.title(f'Highest Success Ratio: {top_site["Launch_Site"]}')
            save_matplotlib_plot(fig, 'highest_success_ratio.png')

    except Exception as e:
        print(f"Error in plot_highest_success_ratio: {str(e)}")
        traceback.print_exc()

# Slide 41: Interactive Scatter Plot of Payload vs. Launch Outcome with Range Slider
def plot_payload_vs_launch_outcome():
    print("Generating Payload Mass vs. Landing Outcome plot...")
    try:
        fig = px.scatter(
            df,
            x='PAYLOAD_MASS__KG_',
            y='Landing_Outcome',
            color='Launch_Site',
            title='Payload Mass vs. Landing Outcome',
            labels={'PAYLOAD_MASS__KG_': 'Payload Mass (kg)', 'Landing_Outcome': 'Landing Outcome'}
        )
        fig.update_layout(
            xaxis=dict(rangeslider=dict(visible=True), type='linear')
        )
        if kaleido_available:
            try:
                print("Saving payload_vs_launch_outcome.png with Plotly...")
                func_timeout(30, fig.write_image, args=('payload_vs_launch_outcome.png',), kwargs={'engine': 'kaleido'})
                print("Saved payload_vs_launch_outcome.png with Plotly")
            except (FunctionTimedOut, Exception) as e:
                print(f"Plotly static export failed: {str(e)}")
                print("Saving as HTML instead...")
                fig.write_html('payload_vs_launch_outcome.html')
                print("Saved payload_vs_launch_outcome.html")
        else:
            print("Kaleido not available, saving as HTML...")
            fig.write_html('payload_vs_launch_outcome.html')
            print("Saved payload_vs_launch_outcome.html")

    except Exception as e:
        print(f"Error in plot_payload_vs_launch_outcome: {str(e)}")
        traceback.print_exc()

# Execute Plotly plotting functions
plot_launch_success_count()
plot_highest_success_ratio()
plot_payload_vs_launch_outcome()

# Close the database connection
print("Closing database connection...")
con.close()