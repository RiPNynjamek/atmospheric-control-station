import matplotlib.pyplot as plt
from datetime import datetime
import csv
import pandas as pd
import os 
from datetime import datetime

class Plot:
    csv_file = 'temperature_humidity_data.csv'

    def create_csv(self):
        # Check if the file exists
        if os.path.exists(self.csv_file):
            # Open the CSV file in write mode, erasing its contents except the header
            with open(self.csv_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Temperature (C)', 'Humidity (%)'])  # Write the header again
        else:
            # Create the CSV file and write the header if it doesn't exist
            with open(self.csv_file, mode='x', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Temperature (C)', 'Humidity (%)'])

    
    def generate_plot(self):
        data = pd.read_csv(self.csv_file, parse_dates=['Timestamp'])

        # Create a figure and axis
        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Plot Temperature (on the left y-axis)
        ax1.plot(data['Timestamp'], data['Temperature (C)'], label='Temperature (°C)', color='tab:red')
        ax1.set_title('Temperature and Humidity Over Time')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Temperature (°C)', color='tab:red')
        ax1.set_ylim(10, 40)  # Set the temperature axis range
        ax1.tick_params(axis='y', labelcolor='tab:red')
        ax1.grid(False)

        # Create a second y-axis for Humidity
        ax2 = ax1.twinx()
        ax2.plot(data['Timestamp'], data['Humidity (%)'], label='Humidity (%)', color='tab:blue')
        ax2.set_ylabel('Humidity (%)', color='tab:blue')
        ax2.set_ylim(0, 100)  # Set the humidity axis range
        ax2.tick_params(axis='y', labelcolor='tab:blue')

        # Rotate x-ticks for better visibility
        plt.xticks(rotation=45)

        # Adjust layout and save the plot
        plt.tight_layout()
        timestamp = datetime.now().strftime('%Y-%m-%d')
        plot_filename = f'{timestamp}_plot.png'
        plt.savefig(plot_filename)  # Save the plot as an image
        return plot_filename
    
    def save_data(self, temperature, humidity):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, temperature, humidity])
        print(f"Data saved at {timestamp}: Temp={temperature}°C, Humidity={humidity}%")
