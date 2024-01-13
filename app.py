import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('data.csv')

# Rename columns for easier access
data.columns = ['Metric', 'Unit'] + [str(year) for year in range(2023, 2036)]

# Streamlit app
def main():
    st.title('Financial Dashboard')

    # Toggle for displaying the data table
    if st.toggle('Show Data Table'):
        st.write(data)

    # Exclude specific metrics from selection
    metrics_to_exclude = ['Dividends (OLNG)', 'Dividends (KOLNG) - RHS']
    selectable_metrics = data[~data['Metric'].isin(metrics_to_exclude)]['Metric'].unique()

    # User interaction: Allow users to select metrics (default to all selected)
    selected_metrics = st.multiselect('Select Metrics:', selectable_metrics, default=selectable_metrics)

    # User interaction: Allow users to select a range of years
    years = list(range(2023, 2036))
    selected_years = st.slider('Select Year Range:', min_value=min(years), max_value=max(years), value=(min(years), max(years)))

    # Filter and prepare the data for plotting
    if selected_metrics:
        plot_data = data[data['Metric'].isin(selected_metrics)]

        # Filter data based on selected years
        year_columns = [str(year) for year in range(selected_years[0], selected_years[1] + 1)]
        plot_data = plot_data[['Metric', 'Unit'] + year_columns]

        # Creating a cumulative sum for each year
        cumulative_data = plot_data.iloc[:, 2:].cumsum()

        # Plotting the bar chart for selected metrics
        fig, ax1 = plt.subplots()
        bars = cumulative_data.T.plot(kind='bar', stacked=True, ax=ax1)

        # Create a second y-axis for the line charts
        ax2 = ax1.twinx()

        # Plotting the line charts for excluded metrics with a separate y-axis
        for metric in metrics_to_exclude:
            line_data = data[data['Metric'] == metric][year_columns].iloc[0]
            ax2.plot(line_data, label=metric)

        # Set the left y-axis range from 0 to 10000
        y_min = -1500
        y_max = 10000
        ax1.set_ylim(y_min, y_max)

        # Calculate the right y-axis range based on the same proportion
        left_range = 10000  # Total range of the left y-axis
        right_max = (2000 / left_range) * y_max
        right_min = (2000 / left_range) * y_min
        ax2.set_ylim(right_min, right_max)

        ax1.set_title('Cumulative Metrics and Specific Dividends Over Years')
        ax1.set_xlabel('Year')
        ax1.set_ylabel('Value in US$ Million')
        ax2.set_ylabel('Dividends Value in US$ Million')

        # Setting the legend with the correct metric names and adjusting style
        ax1_legend_labels = plot_data['Metric']
        ax2_legend_labels = metrics_to_exclude
        ax1.legend(ax1_legend_labels, fontsize='small', loc='upper right')
        ax2.legend(ax2_legend_labels, fontsize='small', loc='upper right')

        # Display the plot
        st.pyplot(fig)
    else:
        st.write("Please select at least one metric to display the chart.")

if __name__ == "__main__":
    main()







