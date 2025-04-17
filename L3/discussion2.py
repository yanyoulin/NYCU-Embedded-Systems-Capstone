import struct
import time
import matplotlib.pyplot as plt

# 定義ICM-20948和AK09916的暫存器地址和參數
CHIP_ID = 0xEA
I2C_ADDR = 0x68
I2C_ADDR_ALT = 0x69
ICM20948_BANK_SEL = 0x7f

ICM20948_I2C_MST_ODR_CONFIG = 0x00
ICM20948_I2C_MST_CTRL = 0x01
ICM20948_I2C_MST_DELAY_CTRL = 0x02
ICM20948_I2C_SLV0_ADDR = 0x03
ICM20948_I2C_SLV0_REG = 0x04
ICM20948_I2C_SLV0_CTRL = 0x05
ICM20948_I2C_SLV0_DO = 0x06
ICM20948_EXT_SLV_SENS_DATA_00 = 0x3B

ICM20948_GYRO_SMPLRT_DIV = 0x00
ICM20948_GYRO_CONFIG_1 = 0x01
ICM20948_GYRO_CONFIG_2 = 0x02

# Bank 0
ICM20948_WHO_AM_I = 0x00
ICM20948_USER_CTRL = 0x03
ICM20948_PWR_MGMT_1 = 0x06
ICM20948_PWR_MGMT_2 = 0x07
ICM20948_INT_PIN_CFG = 0x0F

ICM20948_ACCEL_SMPLRT_DIV_1 = 0x10
ICM20948_ACCEL_SMPLRT_DIV_2 = 0x11
ICM20948_ACCEL_INTEL_CTRL = 0x12
ICM20948_ACCEL_WOM_THR = 0x13
ICM20948_ACCEL_CONFIG = 0x14
ICM20948_ACCEL_XOUT_H = 0x2D
ICM20948_GRYO_XOUT_H = 0x33

ICM20948_TEMP_OUT_H = 0x39
ICM20948_TEMP_OUT_L = 0x3A

# IMU溫度計算
ICM20948_TEMPERATURE_DEGREES_OFFSET = 21
ICM20948_TEMPERATURE_SENSITIVITY = 333.87
ICM20948_ROOM_TEMP_OFFSET = 21

# 磁力計參數設定, 可參考12 REGISTER MAP FOR MAGNETOMETER
AK09916_I2C_ADDR = 0x0c
AK09916_CHIP_ID = 0x09
AK09916_WIA = 0x01
AK09916_ST1 = 0x10
AK09916_ST1_DOR = 0b00000010   
AK09916_ST1_DRDY = 0b00000001 
AK09916_HXL = 0x11
AK09916_ST2 = 0x18
AK09916_ST2_HOFL = 0b00001000 
AK09916_CNTL2 = 0x31
AK09916_CNTL2_MODE = 0b00001111
AK09916_CNTL2_MODE_OFF = 0
AK09916_CNTL2_MODE_SINGLE = 1
AK09916_CNTL2_MODE_CONT1 = 2
AK09916_CNTL2_MODE_CONT2 = 4
AK09916_CNTL2_MODE_CONT3 = 6
AK09916_CNTL2_MODE_CONT4 = 8
AK09916_CNTL2_MODE_TEST = 16
AK09916_CNTL3 = 0x32

class ICM20948:
    def write(self, reg, value):
        """向IMU寫入byte data"""
        self._bus.write_byte_data(self._addr, reg, value)
        time.sleep(0.0001)

    def read(self, reg):
        """從IMU讀取byte data"""
        return self._bus.read_byte_data(self._addr, reg)

    def trigger_mag_io(self):
        """觸發磁力計操作"""
        user = self.read(ICM20948_USER_CTRL)
        self.write(ICM20948_USER_CTRL, user | 0x20)
        time.sleep(0.005)
        self.write(ICM20948_USER_CTRL, user)

    def read_bytes(self, reg, length=1):
        """從感測器讀取多個byte data"""
        return self._bus.read_i2c_block_data(self._addr, reg, length)

    def bank(self, value):
        """切換Register Bank, 才能正確存取目標功能與資料範圍"""
        if not self._bank == value:
            self.write(ICM20948_BANK_SEL, value << 4)
            self._bank = value

    def mag_write(self, reg, value):
        """向磁力計寫入byte data"""
        self.bank(3)
        self.write(ICM20948_I2C_SLV0_ADDR, AK09916_I2C_ADDR)  # 寫入一個byte
        self.write(ICM20948_I2C_SLV0_REG, reg)
        self.write(ICM20948_I2C_SLV0_DO, value)
        self.bank(0)
        self.trigger_mag_io()

    def mag_read(self, reg):
        """從磁力計讀取byte data"""
        self.bank(3)
        self.write(ICM20948_I2C_SLV0_ADDR, AK09916_I2C_ADDR | 0x80)
        self.write(ICM20948_I2C_SLV0_REG, reg)
        self.write(ICM20948_I2C_SLV0_DO, 0xff)
        self.write(ICM20948_I2C_SLV0_CTRL, 0x80 | 1)  # 讀取1個byte

        self.bank(0)
        self.trigger_mag_io()

        return self.read(ICM20948_EXT_SLV_SENS_DATA_00)

    def mag_read_bytes(self, reg, length=1):
        """將ICM-20948作為媒介, 從磁力計讀取byte data"""
        self.bank(3)
        self.write(ICM20948_I2C_SLV0_CTRL, 0x80 | 0x08 | length)
        self.write(ICM20948_I2C_SLV0_ADDR, AK09916_I2C_ADDR | 0x80)
        self.write(ICM20948_I2C_SLV0_REG, reg)
        self.write(ICM20948_I2C_SLV0_DO, 0xff)
        self.bank(0)
        self.trigger_mag_io()

        return self.read_bytes(ICM20948_EXT_SLV_SENS_DATA_00, length)


    def magnetometer_ready(self):
        """檢查磁力計是否準備好"""
        return self.mag_read(AK09916_ST1) & 0x01 > 0

    def read_magnetometer_data(self, timeout=1.0):
        """讀取磁力計"""
        self.mag_write(AK09916_CNTL2, 0x01)  # 觸發單次測量
        t_start = time.time()
        while not self.magnetometer_ready():
            if time.time() - t_start > timeout:
                raise RuntimeError("timeout")
            time.sleep(0.00001)

        data = self.mag_read_bytes(AK09916_HXL, 6)

        # 讀取ST2以確認讀取完成，這在連續模式中是必要的
        # self.mag_read(AK09916_ST2)

        x, y, z = struct.unpack("<hhh", bytearray(data))

        # 根據磁通密度uT進行轉換, 是常數
        x *= 0.15
        y *= 0.15
        z *= 0.15

        return x, y, z

    def read_accelerometer_gyro_data(self):
        """讀取加速度計和陀螺儀"""
        self.bank(0)
        data = self.read_bytes(ICM20948_ACCEL_XOUT_H, 12)

        ax, ay, az, gx, gy, gz = struct.unpack(">hhhhhh", bytearray(data))

        self.bank(2)

        # 讀取加速度計的測量範圍, 並使用它來轉換讀數到g
        scale = (self.read(ICM20948_ACCEL_CONFIG) & 0x06) >> 1

        # 根據資料表第3.2節的範圍
        gs = [16384.0, 8192.0, 4096.0, 2048.0][scale]

        ax /= gs
        ay /= gs
        az /= gs

        # 讀取陀螺儀的DPS範圍, 並使用它來轉換讀數到dps
        scale = (self.read(ICM20948_GYRO_CONFIG_1) & 0x06) >> 1

        # 根據資料表第3.1節的範圍
        dps = [131, 65.5, 32.8, 16.4][scale]

        gx /= dps
        gy /= dps
        gz /= dps

        return ax, ay, az, gx, gy, gz

    def set_accelerometer_sample_rate(self, rate=125):
        """加速度計的sample rate"""
        self.bank(2)
        # 125Hz - 1.125 kHz / (1 + rate)
        rate = int((1125.0 / rate) - 1)
        self.write(ICM20948_ACCEL_SMPLRT_DIV_1, (rate >> 8) & 0xff)
        self.write(ICM20948_ACCEL_SMPLRT_DIV_2, rate & 0xff)

    def set_accelerometer_full_scale(self, scale=16):
        """加速度計的測量範圍（+-）"""
        self.bank(2)
        value = self.read(ICM20948_ACCEL_CONFIG) & 0b11111001
        value |= {2: 0b00, 4: 0b01, 8: 0b10, 16: 0b11}[scale] << 1
        self.write(ICM20948_ACCEL_CONFIG, value)

    def set_accelerometer_low_pass(self, enabled=True, mode=5):
        """設定加速度計的低通濾波器"""
        self.bank(2)
        value = self.read(ICM20948_ACCEL_CONFIG) & 0b10001110
        if enabled:
            value |= 0b1
        value |= (mode & 0x07) << 4
        self.write(ICM20948_ACCEL_CONFIG, value)

    def set_gyro_sample_rate(self, rate=125):
        """設定陀螺儀的sample rate"""
        self.bank(2)
        # 125Hz - 1.125 kHz / (1 + rate)
        rate = int((1125.0 / rate) - 1)
        self.write(ICM20948_GYRO_SMPLRT_DIV, rate)

    def set_gyro_full_scale(self, scale=250):
        """設定陀螺儀的測量範圍（+-）"""
        self.bank(2)
        value = self.read(ICM20948_GYRO_CONFIG_1) & 0b11111001
        value |= {250: 0b00, 500: 0b01, 1000: 0b10, 2000: 0b11}[scale] << 1
        self.write(ICM20948_GYRO_CONFIG_1, value)

    def set_gyro_low_pass(self, enabled=True, mode=5):
        """設定陀螺儀的低通濾波器"""
        self.bank(2)
        value = self.read(ICM20948_GYRO_CONFIG_1) & 0b10001110
        if enabled:
            value |= 0b1
        value |= (mode & 0x07) << 4
        self.write(ICM20948_GYRO_CONFIG_1, value)

    def read_temperature(self):
        """讀取當前IMU溫度"""
        self.bank(0)
        temp_raw_bytes = self.read_bytes(ICM20948_TEMP_OUT_H, 2)
        temp_raw = struct.unpack('>h', bytearray(temp_raw_bytes))[0]
        temperature_deg_c = ((temp_raw - ICM20948_ROOM_TEMP_OFFSET) / ICM20948_TEMPERATURE_SENSITIVITY) + ICM20948_TEMPERATURE_DEGREES_OFFSET
        return temperature_deg_c

    def __init__(self, i2c_addr=I2C_ADDR, i2c_bus=None):
        """初始化ICM-20948感測器"""
        self._bank = -1
        self._addr = i2c_addr

        if i2c_bus is None:
            from smbus2 import SMBus
            self._bus = SMBus(1)
        else:
            self._bus = i2c_bus

        self.bank(0)
        if not self.read(ICM20948_WHO_AM_I) == CHIP_ID:
            raise RuntimeError("無法找到ICM20948")

        self.write(ICM20948_PWR_MGMT_1, 0x80)
        time.sleep(0.01)
        self.write(ICM20948_PWR_MGMT_1, 0x01)
        self.write(ICM20948_PWR_MGMT_2, 0x00)

        self.bank(2)

        self.set_gyro_sample_rate(100)
        self.set_gyro_low_pass(enabled=True, mode=5)
        self.set_gyro_full_scale(250)

        self.set_accelerometer_sample_rate(125)
        self.set_accelerometer_low_pass(enabled=True, mode=5)
        self.set_accelerometer_full_scale(16)

        # 設定 Interrupt 行為
        self.bank(0)
        self.write(ICM20948_INT_PIN_CFG, 0x30) 

        # 設定I2C Master, 用於讀取內部整合的磁力計AK09916
        self.bank(3)
        self.write(ICM20948_I2C_MST_CTRL, 0x4D) 
        self.write(ICM20948_I2C_MST_DELAY_CTRL, 0x01)

        if not self.mag_read(AK09916_WIA) == AK09916_CHIP_ID:
            raise RuntimeError("無法找到AK09916")

        # 重置磁力計
        self.mag_write(AK09916_CNTL3, 0x01)
        while self.mag_read(AK09916_CNTL3) == 0x01:
            time.sleep(0.0001)

if __name__ == "__main__":
    imu = ICM20948()

    # 儲存資料的陣列
    raw_mag = []
    corrected_mag = []

    # 初始化 min/max 變數
    min_x = min_y = min_z = float('inf')
    max_x = max_y = max_z = float('-inf')

    plt.ion()  # 開啟Matplotlib 中的 Interactive Mode（互動模式）
    # 讓程式在產生圖表後繼續執行, 可動態更新圖表資料

    try:
        while True:
            print("start")

            # 讀取磁力計數據
            mx, my, mz = imu.read_magnetometer_data()

            for _ in range(100):
                mx, my, mz = imu.read_magnetometer_data()
                raw_mag.append((mx, my, mz))
                min_x, max_x = min(min_x, mx), max(max_x, mx)
                min_y, max_y = min(min_y, my), max(max_y, my)
                min_z, max_z = min(min_z, mz), max(max_z, mz)
                time.sleep(0.01)

            # 計算 offset 並校正
            x_offset = (max_x + min_x) / 2
            y_offset = (max_y + min_y) / 2
            z_offset = (max_z + min_z) / 2

            for mx, my, mz in raw_mag:
                corrected_mag.append((mx - x_offset, my - y_offset, mz - z_offset))

            # 設定固定座標軸範圍
            axis_min, axis_max = -100, 100

            def plot_combined(data, title, filename):
                mx = [d[0] for d in data]
                my = [d[1] for d in data]
                mz = [d[2] for d in data]

                plt.figure(figsize=(8, 8))
                plt.title(title, fontsize=16, fontweight='bold', fontfamily='sans-serif')

                # 符合您圖片風格的顏色與順序
                plt.scatter(mx, my, s=10, label="XY", c='purple', alpha=0.6)
                plt.scatter(my, mz, s=10, label="YZ", c='blue', alpha=0.6)
                plt.scatter(mx, mz, s=10, label="XZ", c='pink', alpha=0.6)

                plt.xlabel("磁場 X / Y", fontsize=12)
                plt.ylabel("磁場 Y / Z", fontsize=12)

                plt.xlim(-100, 100)
                plt.ylim(-100, 100)

                plt.xticks(fontsize=10)
                plt.yticks(fontsize=10)

                plt.grid(True, linestyle='--', alpha=0.5)
                plt.gca().set_aspect('equal', adjustable='box')
                plt.legend(loc='upper right', fontsize=10)
                plt.tight_layout()
                plt.savefig(filename, dpi=300)
                plt.show()
            # 繪製圖形
            plot_combined(raw_mag, "校正前", "before.png")
            plot_combined(corrected_mag, "校正後", "after.png")
            print("end")
            time.sleep(100)

    except KeyboardInterrupt:
        plt.ioff()  # 關閉互動模式
        plt.show()  # 顯示圖表
