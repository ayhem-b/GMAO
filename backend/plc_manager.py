# plc_manager.py
import snap7
from snap7.util import get_bool, set_bool
from snap7.type import Areas
import threading
import time
import requests
from queue import Queue

class PLCManager:
    def __init__(self, plc_ip="192.168.10.5", django_url="http://127.0.0.1:8000/update-inputs/"):
        self.client = snap7.client.Client()
        self.plc_ip = plc_ip
        self.django_url = django_url
        self.running = False
        self.write_queue = Queue()
        self.inputs = {}  # Live copy of current input states

    def connect(self):
        self.client.connect(self.plc_ip, 0, 1)

    def disconnect(self):
        self.client.disconnect()

    def start(self):
        self.running = True
        threading.Thread(target=self.run, daemon=True).start()

    def stop(self):
        self.running = False
        self.disconnect()

    def run(self):
        self.connect()
        while self.running:
            try:
                # 1. Read Inputs
                data = self.client.read_area(Areas.PE, 0, 0, 2)
                for byte in range(2):
                    for bit in range(8):
                        key = f"I{byte}.{bit}"
                        self.inputs[key] = get_bool(data, byte, bit)

                # 2. Send to Django
                try:
                    requests.post(self.django_url, json=self.inputs, timeout=0.5)
                except requests.exceptions.RequestException:
                    pass

                # 3. Handle Write Queue
                while not self.write_queue.empty():
                    bit_index, value = self.write_queue.get()
                    mem = self.client.read_area(Areas.MK, 0, 0, 1)
                    set_bool(mem, 0, bit_index, value)
                    self.client.write_area(Areas.MK, 0, 0, mem)
                    print(f"[WRITE] M0.{bit_index} = {value}")

                time.sleep(0.3)

            except Exception as e:
                print(f"[ERROR] PLCManager: {e}")
                time.sleep(1)

    def queue_write(self, bit_index, value):
        self.write_queue.put((bit_index, value))

    def get_inputs(self):
        return self.inputs.copy()
