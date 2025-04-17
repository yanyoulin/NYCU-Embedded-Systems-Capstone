import RPi.GPIO as GPIO
import time

# pin
TRIGGER_PIN = 16
ECHO_PIN = 18
LED_PIN = 12

# GPIO setting
GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

def get_distance():
    GPIO.output(TRIGGER_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN, GPIO.LOW)
    pulse_start = time.time()
    
    while GPIO.input(ECHO_PIN) == GPIO.LOW:
        pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == GPIO.HIGH:
        pulse_end = time.time()
    
    duration = pulse_end - pulse_start
    distance = (duration * 34300) / 2
    return distance

def led_control():
    try:
        while True:
            distance = get_distance()
            print(f"Distance: {distance:.2f} cm")
            
            if distance < 50:
                GPIO.output(LED_PIN, GPIO.HIGH)
                time.sleep(0.2)
                GPIO.output(LED_PIN, GPIO.LOW)
                time.sleep(0.2)
            elif distance < 100:
                GPIO.output(LED_PIN, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(LED_PIN, GPIO.LOW)
                time.sleep(1)
            else:
                GPIO.output(LED_PIN, GPIO.LOW)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print(f"Exception: KeyboardInterrupt")
    finally:
        GPIO.output(LED_PIN, GPIO.LOW)
        GPIO.cleanup()

if __name__ == "__main__":
    led_control()
