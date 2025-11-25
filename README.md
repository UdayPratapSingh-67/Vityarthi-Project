Smart Health Monitoring & Alert System

A Python-based simulation of an IoT health monitoring device. This project simulates sensor data, processes it in real-time using multi-threading, and triggers alerts for critical health events.

Prerequisites

Python 3.7 or higher

Standard libraries used: random, time, json, logging, threading, datetime, queue.

How to Run

We can use the project by running the project.py file.

Run the script.

Enter Patient Name: When prompted, type the name of the patient you wish to monitor and press Enter.

To Stop: Press CTRL+C in the terminal to safely shut down the threads and save the session data.

Project Structure

project.py: The main executable containing the Patient, SensorSimulator, AlertSystem, and HealthMonitorSystem classes.

health_system.log: Automatically generated log file tracking events and errors.

health_data_[timestamp].json: Automatically generated JSON dump of patient vitals when the program stops.

How It Works

User Input: The system begins by accepting dynamic patient details to initialize a unique session.

Simulation: The SensorSimulator class generates vitals using randomization algorithms that account for realistic biological variance and occasional "stress" events.

Concurrency: The system uses threading.Thread to run the monitoring loop in the background, keeping the main process free for UI updates or other tasks.

Logic: The AlertSystem checks every data point against defined VitalThresholds. If a threshold is breached, it prints a stylized ALERT message to the console and logs it as an error.
