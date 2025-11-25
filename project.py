import random
import time
import json
import logging
import threading
from datetime import datetime
from queue import Queue

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("health_system.log"),
        logging.StreamHandler()
    ]
)
class VitalThresholds:
    HEART_RATE = (60, 100)
    SPO2 = (95, 100)
    TEMP = (36.1, 37.2)
    SYSTOLIC = (90, 120)
    DIASTOLIC = (60, 80)
class Patient:
    def __init__(self, patient_id, name, age):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.history = []

class SensorSimulator:
    @staticmethod
    def get_heart_rate(stress_factor=0):
        base = random.randint(65, 95)
        if random.random() < 0.1:
            return base + random.randint(20, 40)
        return base + stress_factor

    @staticmethod
    def get_spo2():
        val = random.choices([98, 97, 99, 96, 95, 90, 85], weights=[30, 20, 20, 15, 10, 4, 1])[0]
        return val

    @staticmethod
    def get_temperature():
        base = round(random.uniform(36.5, 37.0), 1)
        if random.random() < 0.05:
            return round(base + random.uniform(1.0, 2.5), 1)
        return base

    @staticmethod
    def get_bp():
        sys = random.randint(110, 130)
        dia = random.randint(70, 85)
        if random.random() < 0.08:
            sys += 30
            dia += 15
        return sys, dia
class AlertSystem:
    @staticmethod
    def check_vitals(data):
        alerts = []

        if not (VitalThresholds.HEART_RATE[0] <= data['heart_rate'] <= VitalThresholds.HEART_RATE[1]):
            alerts.append(f"CRITICAL: Heart Rate {data['heart_rate']} bpm is abnormal!")

        if data['spo2'] < VitalThresholds.SPO2[0]:
            alerts.append(f"WARNING: Low SpO2 level detected: {data['spo2']}%")

        if data['temperature'] > 37.5:
            alerts.append(f"ALERT: High Fever detected: {data['temperature']}°C")

        return alerts

    @staticmethod
    def send_notification(alerts, patient_name):
        if not alerts:
            return

        print("\n" + "!" * 50)
        print(f" >>> EMERGENCY ALERT DISPATCHED FOR {patient_name.upper()} <<<")
        for alert in alerts:
            print(f" [TYPE]: {alert}")
            logging.error(f"Alert sent to emergency contacts: {alert}")
        print("!" * 50 + "\n")
class HealthMonitorSystem:
    def __init__(self):
        self.active = False
        self.data_log = []
        self.monitor_thread = None

    def start_monitoring(self, patient):
        self.active = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, args=(patient,))
        self.monitor_thread.start()
        print(f"System initialized. Monitoring started for {patient.name}...")

    def stop_monitoring(self):
        self.active = False
        if self.monitor_thread:
            self.monitor_thread.join()
        self.save_session_data()
        print("Monitoring stopped. Data saved.")

    def _monitoring_loop(self, patient):
        while self.active:
            bp_sys, bp_dia = SensorSimulator.get_bp()
            current_data = {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'patient_id': patient.patient_id,
                'heart_rate': SensorSimulator.get_heart_rate(),
                'spo2': SensorSimulator.get_spo2(),
                'temperature': SensorSimulator.get_temperature(),
                'bp_systolic': bp_sys,
                'bp_diastolic': bp_dia
            }

            self.data_log.append(current_data)

            alerts = AlertSystem.check_vitals(current_data)

            self._display_dashboard(patient.name, current_data)

            if alerts:
                AlertSystem.send_notification(alerts, patient.name)

            time.sleep(3)

    def _display_dashboard(self, name, data):
        print(f"--- LIVE MONITOR: {name} | {data['timestamp']} ---")
        print(
            f"HR: {data['heart_rate']} bpm | SpO2: {data['spo2']}% | Temp: {data['temperature']}°C | BP: {data['bp_systolic']}/{data['bp_diastolic']}")
        print("-" * 60)

    def save_session_data(self):
        filename = f"health_data_{int(time.time())}.json"
        with open(filename, 'w') as f:
            json.dump(self.data_log, f, indent=4)
        print(f"Session history exported to {filename}")
if __name__ == "__main__":
    system = HealthMonitorSystem()

    print("--- Smart Health Monitoring System Initialization ---")
    user_name = input("Enter Patient Name: ").strip()

    if not user_name:
        user_name = "Guest Patient"

    p_id = f"P-{random.randint(1000, 9999)}"

    p1 = Patient(patient_id=p_id, name=user_name, age=45)

    try:
        system.start_monitoring(p1)

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nShutting down system...")
        system.stop_monitoring()