import smbus2
import time

# Use the detected address for BMP280
BMP280_ADDRESS = 0x77

def read_bmp280_data():
    # Read temperature and pressure raw data from BMP280
    # Temperature
    msb = bus.read_byte_data(BMP280_ADDRESS, 0xFA)
    lsb = bus.read_byte_data(BMP280_ADDRESS, 0xFB)
    xlsb = bus.read_byte_data(BMP280_ADDRESS, 0xFC)
    adc_T = (msb << 16) | (lsb << 8) | xlsb
    adc_T >>= 4

    # Pressure
    msb = bus.read_byte_data(BMP280_ADDRESS, 0xF7)
    lsb = bus.read_byte_data(BMP280_ADDRESS, 0xF8)
    xlsb = bus.read_byte_data(BMP280_ADDRESS, 0xF9)
    adc_P = (msb << 16) | (lsb << 8) | xlsb
    adc_P >>= 4

    return adc_T, adc_P

def compensate_temperature(adc_T):
    # Compensation algorithm from BMP280 datasheet
    var1 = (((adc_T >> 3) - (dig_T1 << 1)) * dig_T2) >> 11
    var2 = (((((adc_T >> 4) - dig_T1) * ((adc_T >> 4) - dig_T1)) >> 12) * dig_T3) >> 14
    t_fine = var1 + var2
    temperature = (t_fine * 5 + 128) >> 8
    return temperature, t_fine

def compensate_pressure(adc_P, t_fine):
    # Compensation algorithm from BMP280 datasheet
    var1 = t_fine - 128000
    var2 = var1 * var1 * dig_P6
    var2 = var2 + ((var1 * dig_P5) << 17)
    var2 = var2 + (dig_P4 << 35)
    var1 = ((var1 * var1 * dig_P3) >> 8) + ((var1 * dig_P2) << 12)
    var1 = (((1 << 47) + var1) * dig_P1) >> 33
    
    if var1 == 0:
        return 0  # Avoid division by zero

    p = 1048576 - adc_P
    p = (((p << 31) - var2) * 3125) // var1
    var1 = (dig_P9 * (p >> 13) * (p >> 13)) >> 25
    var2 = (dig_P8 * p) >> 19
    
    pressure = ((p + var1 + var2) >> 8) + (dig_P7 << 4)
    return pressure

def load_calibration_params():
    # Read calibration data from EEPROM of BMP280
    calib = []
    for i in range(0x88, 0x88+24):
        calib.append(bus.read_byte_data(BMP280_ADDRESS, i))
    calib.append(bus.read_byte_data(BMP280_ADDRESS, 0xA1))
    return calib

# Initialize I2C (SMBus)
bus = smbus2.SMBus(1)

# Load calibration data
calib = load_calibration_params()

# Convert byte data to word values
dig_T1 = (calib[1] << 8) | calib[0]
dig_T2 = (calib[3] << 8) | calib[2]
dig_T3 = (calib[5] << 8) | calib[4]
dig_P1 = (calib[7] << 8) | calib[6]
dig_P2 = (calib[9] << 8) | calib[8]
dig_P3 = (calib[11]<< 8) | calib[10]
dig_P4 = (calib[13]<< 8) | calib[12]
dig_P5 = (calib[15]<< 8) | calib[14]
dig_P6 = (calib[17]<< 8) | calib[16]
dig_P7 = (calib[19]<< 8) | calib[18]
dig_P8 = (calib[21]<< 8) | calib[20]
dig_P9 = (calib[23]<< 8) | calib[22]

try:
    while True:
        # Read raw temperature and pressure data
        adc_T, adc_P = read_bmp280_data()
        
        # Compensate raw temperature and pressure
        temperature, t_fine = compensate_temperature(adc_T)
        pressure = compensate_pressure(adc_P, t_fine)

        print(f"Temperature: {temperature / 100.0:.2f} C")
        print(f"Pressure: {pressure / 25600.0:.2f} hPa")

        time.sleep(1)

except KeyboardInterrupt:
    print("Program stopped")
