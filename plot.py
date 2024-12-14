import matplotlib.pyplot as plt
from datetime import datetime
import csv
import pandas as pd

class Plot:
    csv_file = 'temperature_humidity_data.csv'

    # Create the CSV file with headers if it doesn't exist
    def create_csv(self):
        try:
            with open(self.csv_file, mode='x', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Temperature (C)', 'Humidity (%)'])
        except FileExistsError:
            pass  # CSV file already exists, no need to create it again

    def generate_plot(self):
        data = pd.read_csv(self.csv_file, parse_dates=['Timestamp'])

        plt.figure(figsize=(12, 6))
        # Plot Temperature
        plt.subplot(2, 1, 1)  # (rows, columns, position)
        plt.plot(data['Timestamp'], data['Temperature (C)'], label='Temperature (°C)', color='tab:red')
        plt.title('Temperature Over Time')
        plt.xlabel('Time')
        plt.ylabel('Temperature (°C)')
        plt.xticks(rotation=45)
        plt.grid(True)

        # Plot Humidity
        plt.subplot(2, 1, 2)
        plt.plot(data['Timestamp'], data['Humidity (%)'], label='Humidity (%)', color='tab:blue')
        plt.title('Humidity Over Time')
        plt.xlabel('Time')
        plt.ylabel('Humidity (%)')
        plt.xticks(rotation=45)
        plt.grid(True)

        # Adjust layout and save the plot
        plt.tight_layout()
        plot_filename = 'daily_plot.png'
        plt.savefig(plot_filename)  # Save the plot as an image
        return plot_filename
    
    def save_data(self, temperature, humidity):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, temperature, humidity])
        print(f"Data saved at {timestamp}: Temp={temperature}°C, Humidity={humidity}%")
