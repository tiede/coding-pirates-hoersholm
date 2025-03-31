# main.py (ESP32 Motor + LED control with joystick UI)

import network
from machine import Pin, PWM, Timer
import socket
import time

# GPIO configuration
LED_PIN = 2
LEFT_FWD = 18
RIGHT_FWD = 19
LEFT_BWD = 22
RIGHT_BWD = 23
LED1_PIN = 15
LED2_PIN = 4

# Access Point configuration
AP_SSID = "ESP32-15"
AP_PASSWORD = "12345678"

HTML = """<!DOCTYPE html>
<html>
<head>
    <title>Motor Control</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { margin: 0; padding: 20px; font-family: Arial; background: #f0f0f0; }
        .container { max-width: 600px; margin: auto; text-align: center; }
        h1 { color: #333; }
        .motor-values { display: flex; justify-content: space-around; margin: 20px 0; }
        .motor-group { background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .motor-value { font-size: 1.2em; margin-bottom: 10px; }
        .direction-indicator { display: flex; gap: 10px; justify-content: center; }
        .led { padding: 5px 10px; border-radius: 5px; background: #ccc; color: white; }
        .led.active { background: #4CAF50; }
        #joystick-zone { width: 200px; height: 200px; margin: 50px auto; background: white; border-radius: 50%; box-shadow: 0 2px 5px rgba(0,0,0,0.1); touch-action: none; position: relative; }
        #joystick-knob { width: 60px; height: 60px; background: #4CAF50; border-radius: 50%; position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); cursor: pointer; }
        .led-buttons { margin-top: 30px; display: flex; justify-content: center; gap: 20px; }
        .led-buttons button { padding: 10px 20px; font-size: 16px; border: none; border-radius: 8px; background-color: #4CAF50; color: white; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Motor Control</h1>
        <div class="motor-values">
            <div class="motor-group">
                <div class="motor-value">Left: <span id="leftValue">0%</span></div>
                <div class="direction-indicator">
                    <div id="leftFwd" class="led">FWD</div>
                    <div id="leftBwd" class="led">BWD</div>
                </div>
            </div>
            <div class="motor-group">
                <div class="motor-value">Right: <span id="rightValue">0%</span></div>
                <div class="direction-indicator">
                    <div id="rightFwd" class="led">FWD</div>
                    <div id="rightBwd" class="led">BWD</div>
                </div>
            </div>
        </div>
        <div id="joystick-zone">
            <div id="joystick-knob"></div>
        </div>
        <div class="led-buttons">
            <button onclick="toggleLED(1)">Toggle LED 1</button>
            <button onclick="toggleLED(2)">Toggle LED 2</button>
        </div>
    </div>
    <script>
        const leftValue = document.getElementById('leftValue');
        const rightValue = document.getElementById('rightValue');
        const leftFwd = document.getElementById('leftFwd');
        const leftBwd = document.getElementById('leftBwd');
        const rightFwd = document.getElementById('rightFwd');
        const rightBwd = document.getElementById('rightBwd');
        const joystickZone = document.getElementById('joystick-zone');
        const joystickKnob = document.getElementById('joystick-knob');

        let isDragging = false;
        let startX, startY;
        let lastLeftSpeed = 0;
        let lastRightSpeed = 0;
        let lastSentTime = 0;
        const MOVEMENT_THRESHOLD = 10;
        const SPEED_CHANGE_THRESHOLD = 5;
        const SEND_INTERVAL = 150;

        function updateIndicators(leftSpeed, rightSpeed) {
            leftFwd.classList.toggle('active', leftSpeed > 0);
            leftBwd.classList.toggle('active', leftSpeed < 0);
            rightFwd.classList.toggle('active', rightSpeed > 0);
            rightBwd.classList.toggle('active', rightSpeed < 0);
            leftValue.textContent = `${Math.abs(Math.round(leftSpeed))}%`;
            rightValue.textContent = `${Math.abs(Math.round(rightSpeed))}%`;
        }

        async function updateMotors(leftSpeed, rightSpeed) {
            const now = Date.now();
            if (now - lastSentTime < SEND_INTERVAL) return;
            if (leftSpeed === lastLeftSpeed && rightSpeed === lastRightSpeed) return;
            lastSentTime = now;
            try {
                await fetch(`/motors?left=${leftSpeed}&right=${rightSpeed}`);
            } catch (error) {
                console.error('Error:', error);
            }
            lastLeftSpeed = leftSpeed;
            lastRightSpeed = rightSpeed;
        }

        function toggleLED(ledNum) {
            fetch(`/led?led=${ledNum}&state=toggle`).catch(err => console.error('LED toggle failed', err));
        }

        function handleStart(e) {
            const touch = e.type === 'mousedown' ? e : e.touches[0];
            isDragging = true;
            const rect = joystickZone.getBoundingClientRect();
            startX = rect.left + rect.width / 2;
            startY = rect.top + rect.height / 2;
        }

        function handleMove(e) {
            if (!isDragging) return;
            e.preventDefault();
            const touch = e.type === 'mousemove' ? e : e.touches[0];
            const rect = joystickZone.getBoundingClientRect();
            const maxDistance = rect.width / 2;
            let deltaX = touch.clientX - startX;
            let deltaY = touch.clientY - startY;
            const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
            if (distance > maxDistance) {
                const angle = Math.atan2(deltaY, deltaX);
                deltaX = Math.cos(angle) * maxDistance;
                deltaY = Math.sin(angle) * maxDistance;
            }
            joystickKnob.style.transform = `translate(${deltaX}px, ${deltaY}px)`;
            const normalizedX = deltaX / maxDistance;
            const normalizedY = -deltaY / maxDistance;
            const baseSpeed = normalizedY * 100;
            const differential = normalizedX * Math.abs(baseSpeed);
            let leftSpeed = Math.round(baseSpeed - differential);
            let rightSpeed = Math.round(baseSpeed + differential);
            leftSpeed = Math.min(100, Math.max(-100, leftSpeed));
            rightSpeed = Math.min(100, Math.max(-100, rightSpeed));
            if ((Math.abs(leftSpeed) > MOVEMENT_THRESHOLD || Math.abs(rightSpeed) > MOVEMENT_THRESHOLD)) {
                updateIndicators(leftSpeed, rightSpeed);
                updateMotors(leftSpeed, rightSpeed);
            } else {
                updateIndicators(0, 0);
                updateMotors(0, 0);
            }
        }

        function handleEnd() {
            if (!isDragging) return;
            isDragging = false;
            joystickKnob.style.transform = 'translate(-50%, -50%)';
            updateMotors(0, 0);
            updateIndicators(0, 0);
        }

        joystickZone.addEventListener('touchstart', handleStart);
        document.addEventListener('touchmove', handleMove, { passive: false });
        document.addEventListener('touchend', handleEnd);
        joystickZone.addEventListener('mousedown', handleStart);
        document.addEventListener('mousemove', handleMove);
        document.addEventListener('mouseup', handleEnd);
        window.addEventListener('beforeunload', () => updateMotors(0, 0));
    </script>
</body>
</html>
"""

class Motor:
    def __init__(self, fwd_pin, bwd_pin):
        self.fwd = PWM(Pin(fwd_pin), freq=2000, duty=0)
        self.bwd = PWM(Pin(bwd_pin), freq=2000, duty=0)
        self.last_speed = 0

    def set_speed(self, speed):
        speed = max(-100, min(100, speed))
        if speed == self.last_speed:
            return
        self.last_speed = speed
        duty = abs(speed) * 1023 // 100
        if speed >= 0:
            self.bwd.duty(0)
            self.fwd.duty(duty)
        else:
            self.fwd.duty(0)
            self.bwd.duty(duty)

def create_ap():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=AP_SSID, password=AP_PASSWORD, authmode=network.AUTH_WPA_WPA2_PSK, channel=8)
    while not ap.active():
        time.sleep(1)
    print('AP Created:', ap.ifconfig()[0])
    return ap.ifconfig()[0]

def parse_query_string(qs):
    params = {}
    if qs:
        for param in qs.split('&'):
            if '=' in param:
                key, value = param.split('=')
                try:
                    params[key] = int(value)
                except:
                    params[key] = value
    return params

def create_response(content_type, content):
    content_bytes = content.encode()
    headers = [
        'HTTP/1.1 200 OK',
        f'Content-Type: {content_type}',
        'Connection: close',
        'Cache-Control: no-cache',
        f'Content-Length: {len(content_bytes)}', '', ''
    ]
    return '\r\n'.join(headers).encode() + content_bytes

def handle_request(client_sock):
    try:
        request = client_sock.recv(1024).decode()
        if not request:
            return
        request_line = request.split('\n')[0]
        method, path, _ = request_line.split()
        query = ''
        if '?' in path:
            path, query = path.split('?')

        if path == '/motors' and query:
            params = parse_query_string(query)
            left_motor.set_speed(params.get('left', 0))
            right_motor.set_speed(params.get('right', 0))
            response = create_response('text/plain', 'OK')
        elif path == '/led' and query:
            params = parse_query_string(query)
            led_num = int(params.get('led', 0))
            state = params.get('state')
            if led_num == 1:
                led1.value(not led1.value() if state == 'toggle' else (1 if state == 'on' else 0))
            elif led_num == 2:
                led2.value(not led2.value() if state == 'toggle' else (1 if state == 'on' else 0))
            response = create_response('text/plain', 'LED OK')
        else:
            response = create_response('text/html', HTML)
        client_sock.send(response)
    except Exception as e:
        print('Request error:', e)
    finally:
        try: client_sock.close()
        except: pass

# Initialize
led = Pin(LED_PIN, Pin.OUT)
led1 = Pin(LED1_PIN, Pin.OUT)
led2 = Pin(LED2_PIN, Pin.OUT)
left_motor = Motor(LEFT_FWD, LEFT_BWD)
right_motor = Motor(RIGHT_FWD, RIGHT_BWD)
left_motor.set_speed(0)
right_motor.set_speed(0)
ip_address = create_ap()
print('Running at:', ip_address)

def blink_led(timer):
    led.value(not led.value())

timer = Timer(0) 
timer.init(period=500, mode=Timer.PERIODIC, callback=blink_led)

server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('0.0.0.0', 80))
server_socket.listen(5)
print('Web server started')

while True:
    try:
        client_sock, addr = server_socket.accept()
        handle_request(client_sock)
    except Exception as e:
        print('Socket error:', e)

