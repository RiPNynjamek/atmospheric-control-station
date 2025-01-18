from dh_manager import dh_manager
import time
import csv
from datetime import datetime, timedelta
from plot import Plot
# from dh_manager import dh_manager
from drive_manager import Drive
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),     # Logs to file
        logging.StreamHandler()            # Logs to console
    ]
)

def main():
    plot = Plot()
    plot.create_csv()
    dh = dh_manager()
    dh.initialize()
    config = dh.read_config()

    end_time = datetime.now() + timedelta(minutes=60)
    logging.info(f"Program will run until {end_time}")
    try:
        while datetime.now() < end_time:
            manage(dh, config)
            time.sleep(30) # 30s between 2 readings in production
    except KeyboardInterrupt:
        logging.warning("Program interrupted by user.")
    except Exception as err:
        logging.error(f'An error occured : {err}')
    finally:
        dh.cleanup()  # Always clean up GPIO
        plotting(plot)
        logging.info("Finished testing and cleaned up resources.")

def manage(dh, config):
    csv_file = 'temperature_humidity_data.csv'
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        temperature, humidity = dh.manage_climate(config)

        # stepping out if readouts invalid
        if temperature is None or humidity is None:
            return
        
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, temperature, humidity])

    except Exception as err:
        logging.error(f"Error in manage function: {err}")

def plotting(plot):
    print('Generating daily plot....')
    plot_file = plot.generate_plot()
    drive = Drive()
    service = drive.authenticate()
    drive.upload(service, plot_file)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info('Process starting.')
    main()