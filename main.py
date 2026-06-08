import os
import random
import datetime
import pandas as pd
from fpdf import FPDF

# ==========================================
# 🔐 OFFLINE DEVELOPMENT MODE ZONE
# ==========================================
CSV_DATA_PATH = "data/energy_log.csv"
PDF_REPORT_PATH = "reports/energy_consumption_report.pdf"

class IndustryPDFReporter(FPDF):
    def header(self):
        self.set_fill_color(44, 62, 80)
        self.rect(0, 0, 210, 30, "F")
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(255, 255, 255)
        self.set_y(10)
        self.cell(0, 10, "SMART HOME ENERGY MONITORING REPORT", 0, 1, "C")
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(127, 140, 141)
        self.cell(0, 10, f"Page {self.page_no()} | Automated IoT Telemetry Audit Pipeline", 0, 0, "C")

def execute_simulation_engine(simulation_cycles=12):
    print("=" * 60)
    print("[SYSTEM] Starting Offline Energy Monitoring Simulation Engine...")
    print("=" * 60)
    
    os.makedirs("data", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    cumulative_energy_wh = 0.0
    cost_per_kwh = 6.50  
    sampling_interval_hours = 1.0  # Simulating 1-hour intervals for clear report data
    telemetry_records = []

    appliances = {"Refrigerator": 150, "AirConditioner": 1600, "SmartTV": 120, "LightingGrid": 90}

    for cycle in range(1, simulation_cycles + 1):
        timestamp_now = (datetime.datetime.now() + datetime.timedelta(hours=cycle)).strftime("%Y-%m-%d %H:%M:%S")
        simulated_voltage = round(random.uniform(227.0, 233.0), 1)

        if cycle < 5:
            active_appliances = ["Refrigerator", "LightingGrid"]
        elif 5 <= cycle < 10:
            active_appliances = ["Refrigerator", "AirConditioner", "SmartTV"]
        else:
            active_appliances = ["Refrigerator", "AirConditioner", "SmartTV", "LightingGrid"]

        active_power_watts = sum([appliances[app] for app in active_appliances])
        
        if cycle >= 11:
            active_power_watts += 2200  

        simulated_current = round(active_power_watts / simulated_voltage, 2)
        cumulative_energy_wh += active_power_watts * sampling_interval_hours
        estimated_cost_inr = round((cumulative_energy_wh / 1000.0) * cost_per_kwh, 2)
        
        alert_flag = 1 if simulated_current > 15.0 else 0
        alert_status_string = "CRITICAL" if alert_flag == 1 else "NORMAL"

        cycle_data = {
            "Timestamp": timestamp_now, "Voltage(V)": simulated_voltage,
            "Current(A)": simulated_current, "Power(W)": active_power_watts,
            "Energy(Wh)": round(cumulative_energy_wh, 2), "Cost(INR)": estimated_cost_inr,
            "Status": alert_status_string
        }
        telemetry_records.append(cycle_data)

        print(f"[CYCLE {cycle:02d}/{simulation_cycles:02d}] V={simulated_voltage}V | I={simulated_current}A | P={active_power_watts}W | Status={alert_status_string}")

    # Export to Data Audit Layer (CSV)
    df = pd.DataFrame(telemetry_records)
    df.to_csv(CSV_DATA_PATH, index=False)
    print(f"\n[SUCCESS] Telemetry matrix saved locally to: {CSV_DATA_PATH}")

    # Compile Executive Audit Document (PDF)
    print("[SYSTEM] Compiling executive analytics report PDF...")
    pdf = IndustryPDFReporter()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 10)
    
    # Render stylized table header
    pdf.set_fill_color(52, 152, 219)
    pdf.set_text_color(255, 255, 255)
    headers = ["Timestamp", "Volt(V)", "Amp(A)", "Watt(W)", "Energy(Wh)", "Cost(INR)", "Status"]
    widths = [40, 20, 20, 22, 25, 25, 33]
    
    for header, width in zip(headers, widths):
        pdf.cell(width, 10, header, 1, 0, "C", fill=True)
    pdf.ln()

    # Populate rows
    pdf.set_text_color(0, 0, 0)
    for _, row in df.iterrows():
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(widths[0], 8, str(row["Timestamp"]), 1, 0, "C")
        pdf.cell(widths[1], 8, str(row["Voltage(V)"]), 1, 0, "C")
        pdf.cell(widths[2], 8, str(row["Current(A)"]), 1, 0, "C")
        pdf.cell(widths[3], 8, str(row["Power(W)"]), 1, 0, "C")
        pdf.cell(widths[4], 8, str(row["Energy(Wh)"]), 1, 0, "C")
        pdf.cell(widths[5], 8, f"{row['Cost(INR)']}", 1, 0, "C")
        
        if "CRITICAL" in row["Status"]:
            pdf.set_fill_color(231, 76, 60)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Helvetica", "B", 9)
            pdf.cell(widths[6], 8, str(row["Status"]), 1, 1, "C", fill=True)
            pdf.set_text_color(0, 0, 0)
        else:
            pdf.cell(widths[6], 8, str(row["Status"]), 1, 1, "C")

    pdf.output(PDF_REPORT_PATH)
    print(f"[SUCCESS] Executive verification audit report compiled at: {PDF_REPORT_PATH}")
    print("=" * 60)

if __name__ == "__main__":
    execute_simulation_engine()