from dh_manager import dh_manager
import time
import csv
from datetime import datetime, timedelta
from plot_manager import PlotManager
from drive_manager import Drive
import logging

# Configuration de base du logging
logging.basicConfig(
    filename='app.log',          # Nom du fichier de log
    filemode='w',
    level=logging.INFO,         # Niveau minimal de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Format des messages
    datefmt='%Y-%m-%d %H:%M:%S',  # Format de la date
)

def main():
    plot = PlotManager()
    plot.create_csv()
    dh = dh_manager()

    end_time = datetime.now() + timedelta(hours=24) # 3h test
    logging.info(f"Program will run until {end_time}")
    try:
        while datetime.now() < end_time:
            try:
                manage(dh)
            except Exception as err:
                logging.error(f"Error in manage function: {err}")
                time.sleep(2) # hardware limitations: 2s after an error

            time.sleep(5) # 5s between 2 readings to let the climate change

    except KeyboardInterrupt:
        logging.warning("Program interrupted by user.")
    except Exception as err:
        logging.error(f'An error occured : {err}')
    finally:
        time.sleep(2) # hardware limitations: 2s after an error
        dh.cleanup()  # Always clean up GPIO

        upload_files()
       

def manage(dh):
    csv_file = 'temperature_humidity_data.csv'
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        temperature, humidity, fan_on, humidifier_on = dh.manage_climate()

        while temperature is None or humidity is None:
            time.sleep(2) # hardware limitation 1s before reading again
            temperature, humidity, fan_on, humidifier_on = dh.manage_climate()
        
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, temperature, humidity, fan_on, humidifier_on])

    except Exception as err:
        raise err

def upload_files():
    try:
        plot = PlotManager()
        
        logging.info('Uploading files...')
        # Files upload
        drive = Drive()
        service = drive.authenticate()

        drive.upload(service, 'app.log', 'text/plain', f'app_{timestamp}.log')
        logging.info('File App.log uploaded')
        timestamp = datetime.now().strftime('%Y-%m-%d')
        drive.upload(service, 'temperature_humidity_data.csv', 'text/csv', f'temperature_humidity_data_{timestamp}.csv')
        logging.info('Data file uploaded')
        plot_file = plot.generate_plot()
        drive.upload(service, plot_file, 'image/png')
        logging.info('Plot file uploaded')
        logging.info("Finished running and cleaned up resources.")
    except Exception as e:
        logging.error(f'An error occured while uploading files : {e}')


if __name__ == "__main__":   
    logging.info('Process starting.')
    main()