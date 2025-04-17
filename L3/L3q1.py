import smbus2
import time
import math

# BMP280 I2C address
BMP280_ADDRESS = 0x77

# Initialize I2C bus
bus = smbus2.SMBus(1)

# === Load Calibration Parameters ===
def load_calibration_params():
    calib = []
    for i in range(0x88, 0x88 + 24):
        calib.append(bus.read_byte_data(BMP280_ADDRESS, i))
    calib.append(bus.read_byte_data(BMP280_ADDRESS, 0xA1))
    return calib

calib = load_calibration_params()

# Convert calibration bytes to values
dig_T1 = (calib[1] << 8) | calib[0]
dig_T2 = (calib[3] << 8) | calib[2]
dig_T3 = (calib[5] << 8) | calib[4]
dig_P1 = (calib[7] << 8) | calib[6]
dig_P2 = (calib[9] << 8) | calib[8]
dig_P3 = (calib[11] << 8) | calib[10]
dig_P4 = (calib[13] << 8) | calib[12]
dig_P5 = (calib[15] << 8) | calib[14]
dig_P6 = (calib[17] << 8) | calib[16]
dig_P7 = (calib[19] << 8) | calib[18]
dig_P8 = (calib[21] << 8) | calib[20]
dig_P9 = (calib[23] << 8) | calib[22]

# === Read Raw Data ===
def read_bmp280_data():
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

# === Compensation: Temperature ===
def compensate_temperature(adc_T):
    var1 = (((adc_T >> 3) - (dig_T1 << 1)) * dig_T2) >> 11
    var2 = (((((adc_T >> 4) - dig_T1) * ((adc_T >> 4) - dig_T1)) >> 12) * dig_T3) >> 14
    t_fine = var1 + var2
    temperature = (t_fine * 5 + 128) >> 8  # Return in 0.01 °C
    return temperature, t_fine

# === Compensation: Pressure ===
def compensate_pressure(adc_P, t_fine):
    var1 = t_fine - 128000
    var2 = var1 * var1 * dig_P6
    var2 += (var1 * dig_P5) << 17
    var2 += dig_P4 << 35
    var1 = ((var1 * var1 * dig_P3) >> 8) + ((var1 * dig_P2) << 12)
    var1 = (((1 << 47) + var1) * dig_P1) >> 33

    if var1 == 0:
        return 0  # Avoid division by zero

    p = 1048576 - adc_P
    p = (((p << 31) - var2) * 3125) // var1
    var1 = (dig_P9 * (p >> 13) * (p >> 13)) >> 25
    var2 = (dig_P8 * p) >> 19
    pressure = ((p + var1 + var2) >> 8) + (dig_P7 << 4)
    return pressure  # Pa (Q24.8 format, divide by 256.0 to get real Pa)

# === Altitude Calculation ===
def calculate_altitude(pressure_pa, sea_level_pa=101325.0):
    ratio = pressure_pa / sea_level_pa
    altitude = 44330.0 * (1.0 - pow(ratio, 1.0 / 5.255))
    return altitude

# === Main Loop ===
try:
    while True:
        adc_T, adc_P = read_bmp280_data()
        temperature, t_fine = compensate_temperature(adc_T)
        pressure = compensate_pressure(adc_P, t_fine)

        temp_c = temperature / 100.0
        pressure_pa = pressure / 256.0
        pressure_hpa = pressure_pa / 100.0
        altitude = calculate_altitude(pressure_pa)

        print(f"Temperature: {temp_c:.2f} °C")
        print(f"Pressure:    {pressure_hpa:.2f} hPa")
        print(f"Altitude:    {altitude:.2f} m\n")

        time.sleep(1)

except KeyboardInterrupt:
    print("Program stopped")
