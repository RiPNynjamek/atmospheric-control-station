from dh_manager import dh_manager
import time
import csv
from datetime import datetime, timedelta
from plot import Plot
from drive_manager import Drive
import logging

# Configuration de base du logging
logging.basicConfig(
    filename='app.log',          # Nom du fichier de log
    filemode='w'
    level=logging.DEBUG,         # Niveau minimal de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Format des messages
    datefmt='%Y-%m-%d %H:%M:%S',  # Format de la date
)

def main():
    plot = Plot()

    plot.create_csv()
    dh = dh_manager()
    dh.initialize()
    config = dh.read_config()

    end_time = datetime.now() + timedelta(minutes=90) # 1h30 test
    logging.info(f"Program will run until {end_time}")
    try:
        while datetime.now() < end_time:
            try:
                manage(dh, config)
            except Exception as err:
                logging.error(f"Error in manage function: {err}")
                time.sleep(2) # hardware limitations: 2s after an error

            time.sleep(5) # 5s between 2 readings to let the climate change

    except KeyboardInterrupt:
        logging.warning("Program interrupted by user.")
    except Exception as err:
        logging.error(f'An error occured : {err}')
    finally:
        timestamp = datetime.now().strftime('%Y-%m-%d')
        dh.cleanup()  # Always clean up GPIO
        plot_file = plot.generate_plot()
        uploadFile('app.log', 'text/plain')
        uploadFile('temperature_humidity_data.csv', 'text/csv', f'temperature_humidity_data_{timestamp}.csv')
        uploadFile(plot_file, 'image/png')
        logging.info("Finished running and cleaned up resources.")

def manage(dh, config):
    csv_file = 'temperature_humidity_data.csv'
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        temperature, humidity, fan_on, humidifier_on = dh.manage_climate(config)

        while temperature is None or humidity is None:
            time.sleep(2) # hardware limitation 1s before reading again
            temperature, humidity, fan_on, humidifier_on = dh.manage_climate(config)
        
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, temperature, humidity, fan_on, humidifier_on])

    except Exception as err:
        raise err

def uploadFile(file, mimetype, remoteFile=None):

    drive = Drive()
    service = drive.authenticate()
    drive.upload(service, file, mimetype, remoteFile)


if __name__ == "__main__":
    # logging.basicConfig(
    #     level=logging.DEBUG,
    #     format='%(asctime)s - %(levelname)s - %(message)s'
    # )
    logging.info('Process starting.')
    main()