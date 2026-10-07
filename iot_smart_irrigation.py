"""
IoT-Based Smart Irrigation System for Automated Water Supply Control
Using Soil Moisture Monitoring

This module simulates a complete smart irrigation system with sensor monitoring,
data logging, and automated irrigation control based on soil moisture levels.
"""

import random
import datetime
import json
import csv
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple
import statistics


@dataclass
class SensorReading:
    """Represents a sensor reading from the field."""
    timestamp: str
    soil_moisture: float  # Percentage (0-100)
    temperature: float   # Celsius
    humidity: float      # Percentage (0-100)
    pump_status: str     # "ON" or "OFF"
    water_dispensed: float  # Liters


class SoilMoistureSensor:
    """Simulates a soil moisture sensor with realistic readings."""
    
    def __init__(self, calibration_dry: float = 200, calibration_wet: float = 800):
        """
        Initialize the soil moisture sensor.
        
        Args:
            calibration_dry: ADC value for dry soil
            calibration_wet: ADC value for wet soil
        """
        self.calibration_dry = calibration_dry
        self.calibration_wet = calibration_wet
        self.last_reading = None
    
    def read_moisture(self) -> float:
        """
        Read soil moisture with realistic fluctuations.
        
        Returns:
            Soil moisture percentage (0-100)
        """
        # Simulate realistic moisture variations
        if self.last_reading is None:
            base_reading = random.uniform(30, 70)
        else:
            # Add small random fluctuations for realistic behavior
            base_reading = self.last_reading + random.uniform(-2, 2)
            base_reading = max(0, min(100, base_reading))
        
        self.last_reading = base_reading
        return round(base_reading, 2)


class TemperatureSensor:
    """Simulates a temperature sensor."""
    
    def __init__(self):
        self.last_reading = None
    
    def read_temperature(self) -> float:
        """
        Read temperature with daily variation pattern.
        
        Returns:
            Temperature in Celsius
        """
        hour = datetime.datetime.now().hour
        
        # Simulate daily temperature variation (cooler at night, warmer during day)
        base_temp = 20 + 15 * ((hour - 6) / 12) if 6 <= hour <= 18 else 20
        
        # Add random fluctuations
        if self.last_reading is None:
            reading = base_temp + random.uniform(-2, 2)
        else:
            reading = self.last_reading + random.uniform(-0.5, 0.5)
        
        self.last_reading = reading
        return round(reading, 2)


class HumiditySensor:
    """Simulates a humidity sensor."""
    
    def __init__(self):
        self.last_reading = None
    
    def read_humidity(self) -> float:
        """
        Read humidity with realistic variations.
        
        Returns:
            Humidity percentage (0-100)
        """
        if self.last_reading is None:
            reading = random.uniform(40, 80)
        else:
            reading = self.last_reading + random.uniform(-3, 3)
            reading = max(0, min(100, reading))
        
        self.last_reading = reading
        return round(reading, 2)


class WaterPump:
    """Simulates a water pump with flow rate control."""
    
    def __init__(self, max_flow_rate: float = 10.0):
        """
        Initialize the water pump.
        
        Args:
            max_flow_rate: Maximum flow rate in liters per minute
        """
        self.max_flow_rate = max_flow_rate
        self.is_running = False
        self.runtime_seconds = 0
    
    def start(self):
        """Start the water pump."""
        self.is_running = True
        self.runtime_seconds = 0
    
    def stop(self):
        """Stop the water pump."""
        self.is_running = False
    
    def get_water_dispensed(self, duration_seconds: float) -> float:
        """
        Calculate water dispensed during operation.
        
        Args:
            duration_seconds: Duration of operation in seconds
            
        Returns:
            Water dispensed in liters
        """
        if self.is_running:
            duration_minutes = duration_seconds / 60
            return round(self.max_flow_rate * duration_minutes, 2)
        return 0.0


class IrrigationController:
    """Main controller for the smart irrigation system."""
    
    def __init__(self, 
                 moisture_threshold_low: float = 30.0,
                 moisture_threshold_high: float = 70.0,
                 pump_duration_seconds: float = 300):
        """
        Initialize the irrigation controller.
        
        Args:
            moisture_threshold_low: Minimum soil moisture percentage to trigger irrigation
            moisture_threshold_high: Maximum soil moisture percentage to stop irrigation
            pump_duration_seconds: Duration to run pump for each irrigation cycle
        """
        self.moisture_threshold_low = moisture_threshold_low
        self.moisture_threshold_high = moisture_threshold_high
        self.pump_duration_seconds = pump_duration_seconds
        
        # Initialize sensors
        self.moisture_sensor = SoilMoistureSensor()
        self.temperature_sensor = TemperatureSensor()
        self.humidity_sensor = HumiditySensor()
        self.pump = WaterPump()
        
        # Data logging
        self.readings: List[SensorReading] = []
        self.irrigation_cycles = 0
        self.total_water_dispensed = 0.0
    
    def read_sensors(self) -> Tuple[float, float, float]:
        """
        Read all sensors and return current values.
        
        Returns:
            Tuple of (soil_moisture, temperature, humidity)
        """
        moisture = self.moisture_sensor.read_moisture()
        temperature = self.temperature_sensor.read_temperature()
        humidity = self.humidity_sensor.read_humidity()
        return moisture, temperature, humidity
    
    def control_irrigation(self, soil_moisture: float) -> bool:
        """
        Control irrigation based on soil moisture level.
        
        Args:
            soil_moisture: Current soil moisture percentage
            
        Returns:
            True if pump is running, False otherwise
        """
        if soil_moisture < self.moisture_threshold_low and not self.pump.is_running:
            self.pump.start()
            self.irrigation_cycles += 1
            return True
        elif soil_moisture >= self.moisture_threshold_high and self.pump.is_running:
            self.pump.stop()
            return False
        
        return self.pump.is_running
    
    def simulate_cycle(self) -> SensorReading:
        """
        Simulate one complete monitoring and control cycle.
        
        Returns:
            SensorReading object with current readings
        """
        # Read sensors
        moisture, temperature, humidity = self.read_sensors()
        
        # Control irrigation
        pump_running = self.control_irrigation(moisture)
        
        # Calculate water dispensed (assuming 5-second cycle time)
        water_dispensed = self.pump.get_water_dispensed(5)
        self.total_water_dispensed += water_dispensed
        
        # Create reading record
        reading = SensorReading(
            timestamp=datetime.datetime.now().isoformat(),
            soil_moisture=moisture,
            temperature=temperature,
            humidity=humidity,
            pump_status="ON" if pump_running else "OFF",
            water_dispensed=water_dispensed
        )
        
        self.readings.append(reading)
        return reading
    
    def run_simulation(self, num_cycles: int = 1000) -> List[SensorReading]:
        """
        Run the simulation for a specified number of cycles.
        
        Args:
            num_cycles: Number of monitoring cycles to simulate
            
        Returns:
            List of all sensor readings
        """
        for _ in range(num_cycles):
            self.simulate_cycle()
        
        return self.readings
    
    def get_statistics(self) -> Dict:
        """
        Calculate statistics from collected readings.
        
        Returns:
            Dictionary containing various statistics
        """
        if not self.readings:
            return {}
        
        moistures = [r.soil_moisture for r in self.readings]
        temperatures = [r.temperature for r in self.readings]
        humidities = [r.humidity for r in self.readings]
        pump_on_count = sum(1 for r in self.readings if r.pump_status == "ON")
        
        return {
            'avg_moisture': round(statistics.mean(moistures), 2),
            'min_moisture': round(min(moistures), 2),
            'max_moisture': round(max(moistures), 2),
            'std_moisture': round(statistics.stdev(moistures), 2) if len(moistures) > 1 else 0,
            'avg_temperature': round(statistics.mean(temperatures), 2),
            'min_temperature': round(min(temperatures), 2),
            'max_temperature': round(max(temperatures), 2),
            'avg_humidity': round(statistics.mean(humidities), 2),
            'min_humidity': round(min(humidities), 2),
            'max_humidity': round(max(humidities), 2),
            'total_cycles': len(self.readings),
            'irrigation_cycles': self.irrigation_cycles,
            'pump_on_percentage': round((pump_on_count / len(self.readings)) * 100, 2),
            'total_water_dispensed': round(self.total_water_dispensed, 2),
            'avg_water_per_cycle': round(self.total_water_dispensed / self.irrigation_cycles, 2) if self.irrigation_cycles > 0 else 0
        }
    
    def export_to_csv(self, filename: str):
        """
        Export readings to CSV file.
        
        Args:
            filename: Output CSV filename
        """
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'soil_moisture', 'temperature', 'humidity', 'pump_status', 'water_dispensed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for reading in self.readings:
                writer.writerow(asdict(reading))
    
    def export_to_json(self, filename: str):
        """
        Export readings to JSON file.
        
        Args:
            filename: Output JSON filename
        """
        data = {
            'metadata': {
                'total_readings': len(self.readings),
                'irrigation_cycles': self.irrigation_cycles,
                'total_water_dispensed': self.total_water_dispensed,
                'threshold_low': self.moisture_threshold_low,
                'threshold_high': self.moisture_threshold_high
            },
            'statistics': self.get_statistics(),
            'readings': [asdict(r) for r in self.readings]
        }
        
        with open(filename, 'w') as jsonfile:
            json.dump(data, jsonfile, indent=2)


class PerformanceAnalyzer:
    """Analyzes system performance and efficiency."""
    
    @staticmethod
    def calculate_water_efficiency(total_water: float, num_cycles: int) -> float:
        """
        Calculate water efficiency metric.
        
        Args:
            total_water: Total water dispensed in liters
            num_cycles: Number of monitoring cycles
            
        Returns:
            Water efficiency score (0-100)
        """
        # Efficiency based on water usage optimization
        # Lower water usage for same number of cycles = higher efficiency
        efficiency = max(0, 100 - (total_water / num_cycles) * 10)
        return round(efficiency, 2)
    
    @staticmethod
    def calculate_system_uptime(pump_on_count: int, total_cycles: int) -> float:
        """
        Calculate system uptime percentage.
        
        Args:
            pump_on_count: Number of cycles pump was on
            total_cycles: Total number of cycles
            
        Returns:
            Uptime percentage (0-100)
        """
        if total_cycles == 0:
            return 0.0
        return round((pump_on_count / total_cycles) * 100, 2)
    
    @staticmethod
    def calculate_moisture_stability(moisture_readings: List[float]) -> float:
        """
        Calculate soil moisture stability (inverse of standard deviation).
        
        Args:
            moisture_readings: List of soil moisture readings
            
        Returns:
            Stability score (0-100, where 100 is most stable)
        """
        if len(moisture_readings) < 2:
            return 100.0
        
        std_dev = statistics.stdev(moisture_readings)
        # Normalize standard deviation to 0-100 scale
        stability = max(0, 100 - std_dev * 2)
        return round(stability, 2)


def main():
    """Main function to run the simulation."""
    print("=" * 70)
    print("IoT-BASED SMART IRRIGATION SYSTEM SIMULATION")
    print("=" * 70)
    print()
    
    # Initialize controller with realistic thresholds
    controller = IrrigationController(
        moisture_threshold_low=35.0,
        moisture_threshold_high=65.0,
        pump_duration_seconds=300
    )
    
    print("Starting simulation with 1000 monitoring cycles...")
    print("(Each cycle represents 5 seconds of real-time operation)")
    print()
    
    # Run simulation
    readings = controller.run_simulation(num_cycles=1000)
    
    # Get statistics
    stats = controller.get_statistics()
    
    # Export data
    controller.export_to_csv('/home/ubuntu/project/sensor_readings.csv')
    controller.export_to_json('/home/ubuntu/project/sensor_readings.json')
    
    # Display results
    print("SIMULATION RESULTS")
    print("-" * 70)
    print(f"Total Monitoring Cycles: {stats['total_cycles']}")
    print(f"Irrigation Cycles Triggered: {stats['irrigation_cycles']}")
    print(f"Pump Operating Time: {stats['pump_on_percentage']}%")
    print()
    
    print("SOIL MOISTURE STATISTICS")
    print("-" * 70)
    print(f"Average Moisture: {stats['avg_moisture']}%")
    print(f"Minimum Moisture: {stats['min_moisture']}%")
    print(f"Maximum Moisture: {stats['max_moisture']}%")
    print(f"Standard Deviation: {stats['std_moisture']}%")
    print()
    
    print("TEMPERATURE STATISTICS")
    print("-" * 70)
    print(f"Average Temperature: {stats['avg_temperature']}°C")
    print(f"Minimum Temperature: {stats['min_temperature']}°C")
    print(f"Maximum Temperature: {stats['max_temperature']}°C")
    print()
    
    print("HUMIDITY STATISTICS")
    print("-" * 70)
    print(f"Average Humidity: {stats['avg_humidity']}%")
    print(f"Minimum Humidity: {stats['min_humidity']}%")
    print(f"Maximum Humidity: {stats['max_humidity']}%")
    print()
    
    print("WATER MANAGEMENT STATISTICS")
    print("-" * 70)
    print(f"Total Water Dispensed: {stats['total_water_dispensed']} liters")
    print(f"Average Water per Irrigation Cycle: {stats['avg_water_per_cycle']} liters")
    print()
    
    # Performance analysis
    analyzer = PerformanceAnalyzer()
    moistures = [r.soil_moisture for r in readings]
    pump_on_count = sum(1 for r in readings if r.pump_status == "ON")
    
    water_efficiency = analyzer.calculate_water_efficiency(
        stats['total_water_dispensed'],
        stats['total_cycles']
    )
    system_uptime = analyzer.calculate_system_uptime(pump_on_count, stats['total_cycles'])
    moisture_stability = analyzer.calculate_moisture_stability(moistures)
    
    print("SYSTEM PERFORMANCE METRICS")
    print("-" * 70)
    print(f"Water Efficiency Score: {water_efficiency}/100")
    print(f"System Uptime: {system_uptime}%")
    print(f"Soil Moisture Stability: {moisture_stability}/100")
    print()
    
    print("Data exported to:")
    print("  - /home/ubuntu/project/sensor_readings.csv")
    print("  - /home/ubuntu/project/sensor_readings.json")
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
