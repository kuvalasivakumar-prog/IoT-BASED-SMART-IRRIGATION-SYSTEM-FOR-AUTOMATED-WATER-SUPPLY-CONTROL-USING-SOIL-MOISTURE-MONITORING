"""
Generate visualizations for the IoT Smart Irrigation System report.
Creates charts and graphs showing system performance, sensor data, and analysis.
"""

import json
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np
from typing import List, Dict


def load_sensor_data(json_file: str) -> Dict:
    """Load sensor data from JSON file."""
    with open(json_file, 'r') as f:
        return json.load(f)


def load_csv_data(csv_file: str) -> List[Dict]:
    """Load sensor data from CSV file."""
    data = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data


def create_moisture_trend_chart(csv_file: str, output_file: str):
    """Create soil moisture trend chart."""
    data = load_csv_data(csv_file)
    
    # Extract data
    indices = list(range(len(data)))
    moistures = [float(row['soil_moisture']) for row in data]
    pump_status = [row['pump_status'] for row in data]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Plot moisture trend
    ax.plot(indices, moistures, color='#2E86AB', linewidth=2, label='Soil Moisture', alpha=0.8)
    
    # Add threshold lines
    ax.axhline(y=35, color='#A23B72', linestyle='--', linewidth=2, label='Low Threshold (35%)', alpha=0.7)
    ax.axhline(y=65, color='#F18F01', linestyle='--', linewidth=2, label='High Threshold (65%)', alpha=0.7)
    
    # Shade irrigation zones
    ax.fill_between(indices, 0, 35, alpha=0.1, color='red', label='Irrigation Needed Zone')
    ax.fill_between(indices, 65, 100, alpha=0.1, color='green', label='Adequate Moisture Zone')
    
    # Formatting
    ax.set_xlabel('Monitoring Cycle', fontsize=12, fontweight='bold')
    ax.set_ylabel('Soil Moisture (%)', fontsize=12, fontweight='bold')
    ax.set_title('Soil Moisture Trend Over Time', fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3, linestyle=':')
    ax.legend(loc='best', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {output_file}")


def create_temperature_humidity_chart(csv_file: str, output_file: str):
    """Create temperature and humidity dual-axis chart."""
    data = load_csv_data(csv_file)
    
    # Extract data
    indices = list(range(len(data)))
    temperatures = [float(row['temperature']) for row in data]
    humidities = [float(row['humidity']) for row in data]
    
    # Create figure with dual y-axes
    fig, ax1 = plt.subplots(figsize=(14, 6))
    
    # Plot temperature
    color1 = '#D62828'
    ax1.set_xlabel('Monitoring Cycle', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Temperature (°C)', color=color1, fontsize=12, fontweight='bold')
    line1 = ax1.plot(indices, temperatures, color=color1, linewidth=2.5, label='Temperature', alpha=0.8)
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, alpha=0.3, linestyle=':')
    
    # Plot humidity on secondary axis
    ax2 = ax1.twinx()
    color2 = '#1D3557'
    ax2.set_ylabel('Humidity (%)', color=color2, fontsize=12, fontweight='bold')
    line2 = ax2.plot(indices, humidities, color=color2, linewidth=2.5, label='Humidity', alpha=0.8)
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.set_ylim(0, 100)
    
    # Title and legend
    fig.suptitle('Temperature and Humidity Monitoring', fontsize=14, fontweight='bold', y=0.98)
    
    # Combine legends
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {output_file}")


def create_pump_operation_chart(csv_file: str, output_file: str):
    """Create pump operation status chart."""
    data = load_csv_data(csv_file)
    
    # Extract data
    indices = list(range(len(data)))
    pump_status = [1 if row['pump_status'] == 'ON' else 0 for row in data]
    water_dispensed = [float(row['water_dispensed']) for row in data]
    
    # Create figure
    fig, ax1 = plt.subplots(figsize=(14, 6))
    
    # Plot pump status as bar chart
    colors = ['#2D6A4F' if status == 1 else '#E8F5E9' for status in pump_status]
    ax1.bar(indices, pump_status, color=colors, alpha=0.7, label='Pump Status', width=1)
    
    ax1.set_xlabel('Monitoring Cycle', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Pump Status (1=ON, 0=OFF)', fontsize=12, fontweight='bold')
    ax1.set_ylim(0, 1.2)
    ax1.set_title('Water Pump Operation Timeline', fontsize=14, fontweight='bold', pad=20)
    ax1.grid(True, alpha=0.3, linestyle=':', axis='y')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {output_file}")


def create_statistics_summary_chart(json_file: str, output_file: str):
    """Create a comprehensive statistics summary chart."""
    data = load_sensor_data(json_file)
    stats = data['statistics']
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('System Performance Statistics Summary', fontsize=16, fontweight='bold', y=0.995)
    
    # 1. Moisture Statistics
    ax = axes[0, 0]
    moisture_data = [stats['min_moisture'], stats['avg_moisture'], stats['max_moisture']]
    moisture_labels = ['Minimum', 'Average', 'Maximum']
    colors1 = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    bars1 = ax.bar(moisture_labels, moisture_data, color=colors1, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax.set_ylabel('Moisture (%)', fontsize=11, fontweight='bold')
    ax.set_title('Soil Moisture Statistics', fontsize=12, fontweight='bold')
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3, axis='y', linestyle=':')
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # 2. Temperature Statistics
    ax = axes[0, 1]
    temp_data = [stats['min_temperature'], stats['avg_temperature'], stats['max_temperature']]
    temp_labels = ['Minimum', 'Average', 'Maximum']
    colors2 = ['#FFB6C1', '#FF69B4', '#FF1493']
    bars2 = ax.bar(temp_labels, temp_data, color=colors2, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax.set_ylabel('Temperature (°C)', fontsize=11, fontweight='bold')
    ax.set_title('Temperature Statistics', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y', linestyle=':')
    
    # Add value labels on bars
    for bar in bars2:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}°C', ha='center', va='bottom', fontweight='bold')
    
    # 3. Humidity Statistics
    ax = axes[1, 0]
    humidity_data = [stats['min_humidity'], stats['avg_humidity'], stats['max_humidity']]
    humidity_labels = ['Minimum', 'Average', 'Maximum']
    colors3 = ['#87CEEB', '#4682B4', '#00008B']
    bars3 = ax.bar(humidity_labels, humidity_data, color=colors3, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax.set_ylabel('Humidity (%)', fontsize=11, fontweight='bold')
    ax.set_title('Humidity Statistics', fontsize=12, fontweight='bold')
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3, axis='y', linestyle=':')
    
    # Add value labels on bars
    for bar in bars3:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # 4. System Metrics
    ax = axes[1, 1]
    ax.axis('off')
    
    # Create text summary
    metrics_text = f"""
SYSTEM PERFORMANCE METRICS

Total Monitoring Cycles: {stats['total_cycles']}
Irrigation Cycles: {stats['irrigation_cycles']}
Pump Operating Time: {stats['pump_on_percentage']}%

Water Management:
  • Total Water Dispensed: {stats['total_water_dispensed']} L
  • Avg per Cycle: {stats['avg_water_per_cycle']} L

Soil Moisture:
  • Std Dev: {stats['std_moisture']}%
  • Range: {stats['min_moisture']}% - {stats['max_moisture']}%

Environmental:
  • Avg Humidity: {stats['avg_humidity']}%
  • Avg Temp: {stats['avg_temperature']}°C
    """
    
    ax.text(0.05, 0.95, metrics_text, transform=ax.transAxes,
            fontsize=10, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {output_file}")


def create_water_usage_chart(csv_file: str, output_file: str):
    """Create cumulative water usage chart."""
    data = load_csv_data(csv_file)
    
    # Extract data
    indices = list(range(len(data)))
    water_dispensed = [float(row['water_dispensed']) for row in data]
    
    # Calculate cumulative water
    cumulative_water = []
    total = 0
    for w in water_dispensed:
        total += w
        cumulative_water.append(total)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Plot cumulative water usage
    ax.fill_between(indices, cumulative_water, alpha=0.3, color='#1E88E5', label='Cumulative Water Usage')
    ax.plot(indices, cumulative_water, color='#1E88E5', linewidth=2.5, label='Cumulative Water Usage')
    
    # Formatting
    ax.set_xlabel('Monitoring Cycle', fontsize=12, fontweight='bold')
    ax.set_ylabel('Cumulative Water Usage (Liters)', fontsize=12, fontweight='bold')
    ax.set_title('Cumulative Water Dispensed Over Time', fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, linestyle=':')
    ax.legend(loc='best', fontsize=10)
    
    # Add final value annotation
    if cumulative_water:
        final_value = cumulative_water[-1]
        ax.annotate(f'Total: {final_value:.2f} L',
                   xy=(len(indices)-1, final_value),
                   xytext=(len(indices)-100, final_value-5),
                   fontsize=11, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', color='black'))
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {output_file}")


def create_system_efficiency_chart(json_file: str, output_file: str):
    """Create system efficiency metrics pie chart."""
    data = load_sensor_data(json_file)
    stats = data['statistics']
    
    # Calculate efficiency metrics
    pump_on_pct = stats['pump_on_percentage']
    pump_off_pct = 100 - pump_on_pct
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('System Efficiency Analysis', fontsize=14, fontweight='bold')
    
    # 1. Pump Operation Pie Chart
    sizes1 = [pump_on_pct, pump_off_pct]
    labels1 = [f'Pump ON\n{pump_on_pct}%', f'Pump OFF\n{pump_off_pct}%']
    colors1 = ['#2D6A4F', '#E8F5E9']
    explode1 = (0.05, 0)
    
    ax1.pie(sizes1, explode=explode1, labels=labels1, colors=colors1, autopct='%1.1f%%',
            shadow=True, startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax1.set_title('Pump Operating Time Distribution', fontsize=12, fontweight='bold')
    
    # 2. Water Efficiency Metrics
    categories = ['Water\nEfficiency', 'Moisture\nStability', 'System\nOptimization']
    
    # Calculate efficiency scores
    water_eff = 100 - (stats['total_water_dispensed'] / stats['total_cycles']) * 10
    water_eff = max(0, min(100, water_eff))
    
    moisture_std = stats['std_moisture']
    moisture_stability = max(0, 100 - moisture_std * 2)
    
    optimization = 100 - (pump_on_pct * 0.5)
    
    values = [water_eff, moisture_stability, optimization]
    colors2 = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    bars = ax2.bar(categories, values, color=colors2, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax2.set_ylabel('Efficiency Score', fontsize=11, fontweight='bold')
    ax2.set_ylim(0, 100)
    ax2.grid(True, alpha=0.3, axis='y', linestyle=':')
    ax2.set_title('System Performance Scores', fontsize=12, fontweight='bold')
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {output_file}")


def create_distribution_histogram(csv_file: str, output_file: str):
    """Create distribution histograms for sensor data."""
    data = load_csv_data(csv_file)
    
    # Extract data
    moistures = [float(row['soil_moisture']) for row in data]
    temperatures = [float(row['temperature']) for row in data]
    humidities = [float(row['humidity']) for row in data]
    
    # Create figure with subplots
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle('Sensor Data Distribution Analysis', fontsize=14, fontweight='bold')
    
    # 1. Moisture distribution
    axes[0].hist(moistures, bins=30, color='#2E86AB', alpha=0.7, edgecolor='black')
    axes[0].axvline(np.mean(moistures), color='red', linestyle='--', linewidth=2, label=f'Mean: {np.mean(moistures):.1f}%')
    axes[0].set_xlabel('Soil Moisture (%)', fontsize=11, fontweight='bold')
    axes[0].set_ylabel('Frequency', fontsize=11, fontweight='bold')
    axes[0].set_title('Soil Moisture Distribution', fontsize=12, fontweight='bold')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3, axis='y', linestyle=':')
    
    # 2. Temperature distribution
    axes[1].hist(temperatures, bins=30, color='#D62828', alpha=0.7, edgecolor='black')
    axes[1].axvline(np.mean(temperatures), color='blue', linestyle='--', linewidth=2, label=f'Mean: {np.mean(temperatures):.1f}°C')
    axes[1].set_xlabel('Temperature (°C)', fontsize=11, fontweight='bold')
    axes[1].set_ylabel('Frequency', fontsize=11, fontweight='bold')
    axes[1].set_title('Temperature Distribution', fontsize=12, fontweight='bold')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3, axis='y', linestyle=':')
    
    # 3. Humidity distribution
    axes[2].hist(humidities, bins=30, color='#1D3557', alpha=0.7, edgecolor='black')
    axes[2].axvline(np.mean(humidities), color='orange', linestyle='--', linewidth=2, label=f'Mean: {np.mean(humidities):.1f}%')
    axes[2].set_xlabel('Humidity (%)', fontsize=11, fontweight='bold')
    axes[2].set_ylabel('Frequency', fontsize=11, fontweight='bold')
    axes[2].set_title('Humidity Distribution', fontsize=12, fontweight='bold')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3, axis='y', linestyle=':')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {output_file}")


def main():
    """Generate all visualizations."""
    print("\n" + "="*70)
    print("GENERATING VISUALIZATIONS FOR IoT SMART IRRIGATION SYSTEM REPORT")
    print("="*70 + "\n")
    
    base_path = '/home/ubuntu/project'
    csv_file = f'{base_path}/sensor_readings.csv'
    json_file = f'{base_path}/sensor_readings.json'
    
    print("Creating visualizations...\n")
    
    # Generate all charts
    create_moisture_trend_chart(csv_file, f'{base_path}/chart_01_moisture_trend.png')
    create_temperature_humidity_chart(csv_file, f'{base_path}/chart_02_temp_humidity.png')
    create_pump_operation_chart(csv_file, f'{base_path}/chart_03_pump_operation.png')
    create_statistics_summary_chart(json_file, f'{base_path}/chart_04_statistics_summary.png')
    create_water_usage_chart(csv_file, f'{base_path}/chart_05_water_usage.png')
    create_system_efficiency_chart(json_file, f'{base_path}/chart_06_efficiency.png')
    create_distribution_histogram(csv_file, f'{base_path}/chart_07_distributions.png')
    
    print("\n" + "="*70)
    print("All visualizations generated successfully!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
