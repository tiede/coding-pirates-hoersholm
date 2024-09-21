import board, busio
from secrets import secrets
from digitalio import DigitalInOut
import adafruit_requests as requests
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi
import adafruit_connection_manager

class Connection:
    def __connect(self, spi, cs, ready, reset, log):
        esp = adafruit_esp32spi.ESP_SPIcontrol(spi, cs, ready, reset)

        # pool = adafruit_connection_manager.get_radio_socketpool(esp)
        # ssl_context = adafruit_connection_manager.get_radio_ssl_context(esp)
        # requests = requests.Session(pool, ssl_context)

        #requests.set_socket(socket, esp)

        if log:
            print("Connecting to AP...")

        while not esp.is_connected:
            try:
                esp.connect_AP(secrets['ssid'], secrets['password'])
            except RuntimeError as e:
                if log:
                    print("could not connect to AP, retrying: ",e)
                continue

        if log:
            print("Connected to", str(esp.ssid, 'utf-8'), "\tRSSI:", esp.rssi)
            print("My IP address is", esp.pretty_ip(esp.ip_address))

    # Connect a PyPortal
    def connect_pyportal(self, spi, log = False):
        esp32_cs = DigitalInOut(board.ESP_CS)
        esp32_ready = DigitalInOut(board.ESP_BUSY)
        esp32_reset = DigitalInOut(board.ESP_RESET)

        self.__connect(spi, esp32_cs, esp32_ready, esp32_reset, log)

    # Connect a PyBadge
    def connect_pybadge(self, spi, log = False):
        esp32_cs = DigitalInOut(board.D13)
        esp32_ready = DigitalInOut(board.D11)
        esp32_reset = DigitalInOut(board.D12)

        esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

        self.pool = adafruit_connection_manager.get_radio_socketpool(esp)
        self.ssl_context = adafruit_connection_manager.get_radio_ssl_context(esp)
        self.session = requests.Session(self.pool, self.ssl_context)

        self.__connect(spi, esp32_cs, esp32_ready, esp32_reset, log)
        print("Ping google.com: %d ms" % esp.ping("google.com"))

    def get(self, url):
        print(self.session)
        return self.session.get(url)