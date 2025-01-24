import matplotlib.pyplot as plt
from datetime import datetime
import csv
import pandas as pd
import os 
from datetime import datetime
import logging

class Plot:
    csv_file = 'temperature_humidity_data.csv'

    def create_csv(self):
        # Check if the file exists
        if os.path.exists(self.csv_file):
            # Open the CSV file in write mode, erasing its contents except the header
            with open(self.csv_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Temperature (C)', 'Humidity (%)', 'Fan On', 'Humidifier On'])  # Write the header again
        else:
            # Create the CSV file and write the header if it doesn't exist
            with open(self.csv_file, mode='x', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Temperature (C)', 'Humidity (%)', 'Fan On', 'Humidifier On'])

    
    def generate_plot(self):
        data = pd.read_csv(self.csv_file, parse_dates=['Timestamp'])
        data['Time'] = data['Timestamp'].dt.strftime('%H:%M')

        # Create a figure and axis
        fig, ax1 = plt.subplots(figsize=(10, 5))

        # Plot Temperature (on the left y-axis)
        ax1.plot(data['Timestamp'], data['Temperature (C)'], label='Temperature (°C)', color='tab:red', linewidth=0.5)
        ax1.set_title('Temperature and Humidity Over Time')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Temperature (°C)', color='tab:red')
        ax1.set_ylim(10, 40)  # Set the temperature axis range
        ax1.tick_params(axis='y', labelcolor='tab:red')
        ax1.grid(False)

        # Create a second y-axis for Humidity
        ax2 = ax1.twinx()
        ax2.plot(data['Timestamp'], data['Humidity (%)'], label='Humidity (%)', color='tab:blue', linewidth=0.5)
        ax2.set_ylabel('Humidity (%)', color='tab:blue')
        ax2.set_ylim(0, 100)  # Set the humidity axis range
        ax2.tick_params(axis='y', labelcolor='tab:blue')

        # For Fan On True/False use different markers
        # for idx, row in data.iterrows():
        #     if row['Fan On'] == True:
        #         ax1.scatter(row['Timestamp'], row['Temperature (C)'], color='red', marker='o', s=5)
        #     else:
        #         ax1.scatter(row['Timestamp'], row['Temperature (C)'], color='red', marker='x', s=10)

        # For Humidifier On True/False use different markers
        for idx, row in data.iterrows():
            if row['Humidifier On'] == True:
                ax2.scatter(row['Timestamp'], row['Humidity (%)'], color='blue', marker='o', s=5)
            else:
                ax2.scatter(row['Timestamp'], row['Humidity (%)'], color='blue', marker='x', s=10)
        
        # Rotate x-ticks for better visibility
        plt.xticks(rotation=45)

        # Adjust layout and save the plot
        plt.tight_layout()
        timestamp = datetime.now().strftime('%Y-%m-%d')
        plot_filename = f'{timestamp}_plot.png'
        plt.savefig(plot_filename, dpi=200)  # Save the plot as an high resolution image
        return plot_filename
    
    def save_data(self, temperature, humidity):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, temperature, humidity])
        # logging.info(f"Data saved: Temp={temperature}°C, Humidity={humidity}%")
