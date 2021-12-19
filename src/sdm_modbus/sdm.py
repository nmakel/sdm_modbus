from sdm_modbus import meter


class SDM(meter.Meter):
    pass


class SDM72(SDM):

    def __init__(self, *args, **kwargs):
        self.model = "SDM72"
        self.baud = 9600

        super().__init__(*args, **kwargs)

        self.registers = {
            "l1_voltage": (0x0000, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L1 Voltage", "V", 1, 1),
            "l2_voltage": (0x0002, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L2 Voltage", "V", 1, 1),
            "l3_voltage": (0x0004, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L3 Voltage", "V", 1, 1),
            "l1_current": (0x0006, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L1 Current", "A", 1, 1),
            "l2_current": (0x0008, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L2 Current", "A", 1, 1),
            "l3_current": (0x000a, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L3 Current", "A", 1, 1),
            "l1_power_active": (0x000c, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L1 Power (Active)", "W", 1, 1),
            "l2_power_active": (0x000e, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L2 Power (Active)", "W", 1, 1),
            "l3_power_active": (0x0010, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L3 Power (Active)", "W", 1, 1),
            "l1_power_apparent": (0x0012, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L1 Power (Apparent)", "VA", 1, 1),
            "l2_power_apparent": (0x0014, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L2 Power (Apparent)", "VA", 1, 1),
            "l3_power_apparent": (0x0016, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L3 Power (Apparent)", "VA", 1, 1),
            "l1_power_reactive": (0x0018, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L1 Power (Reactive)", "VAr", 1, 1),
            "l2_power_reactive": (0x001A, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L2 Power (Reactive)", "VAr", 1, 1),
            "l3_power_reactive": (0x001C, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L3 Power (Reactive)", "VAr", 1, 1),
            "l1_power_factor": (0x001e, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L1 Power Factor", "", 1, 1),
            "l2_power_factor": (0x0020, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L2 Power Factor", "", 1, 1),
            "l3_power_factor": (0x0022, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L3 Power Factor", "", 1, 1),
            "voltage_ln": (0x002a, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L-N Voltage", "V", 1, 1),
            "current_ln": (0x002e, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L-N Current", "A", 1, 1),
            "total_line_current": (0x0030, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Line Current", "A", 1, 1),
            "total_power": (0x0034, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Power", "W", 1, 1),
            "total_power_apparent": (0x0038, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Power (Apparent)", "VA", 1, 1),
            "total_power_reactive": (0x003C, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Power (Reactive)", "VAr", 1, 1),
            "total_pf": (0x003E, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Power Factor", "", 1, 1),
            "frequency": (0x0046, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Frequency", "Hz", 1, 1),
            "import_energy_active": (0x0048, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Imported Energy (Active)", "kWh", 1, 1),
            "export_energy_active": (0x004a, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Exported Energy (Active)", "kWh", 1, 1),
            "l12_voltage": (0x00c8, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L1-L2 Voltage", "V", 2, 1),
            "l23_voltage": (0x00ca, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L2-L3 Voltage", "V", 2, 1),
            "l31_voltage": (0x00cc, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L3-L1 Voltage", "V", 2, 1),
            "voltage_ll": (0x00ce, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L-L Voltage", "V", 2, 1),
            "neutral_current": (0x00e0, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Neutral Current", "A", 2, 1),
            "total_energy_active": (0x0156, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Energy (Active)", "kWh", 3, 1),
            "total_energy_reactive": (0x0158, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Energy (Reactive)", "kVArh", 3, 1),
            "resettable_total_energy_active": (0x0180, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Resettable Total Energy (Active)", "kWh", 3, 1),
            "resettable_import_enerty_active": (0x0184, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Resettable Import Energy (Active)", "kWh", 3, 1),
            "resettable_export_energy_active": (0x0186, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Resettable Export Energy (Active)", "kWh", 3, 1),
            "net_kwh": (0x018c, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Net kWh (Import - Export)", "kWh", 3, 1),
            "import_total_power_active": (0x0500, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Import Power (Active)", "W", 4, 1),
            "export_total_power_active": (0x0502, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Export Power (Active)", "W", 4, 1),

            "demand_time": (0x0000, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Demand Time", "s", 1, 1),
            "demand_period": (0x0002, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Demand Period", "s", 1, 1),
            "system_voltage": (0x0006, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, float, "System Voltage", "V", 1, 1),
            "system_current": (0x0008, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, float, "System Current", "A", 1, 1),
            "system_type": (0x000a, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "System Type", [
                -1, "1P2W", "3P3W", "3P4W"], 1, 1),
            "relay_pulse_width": (0x000c, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Relay Pulse Width", "ms", 1, 1),
            "network_parity_stop": (0x0012, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Network Parity Stop", [
                "N-1", "E-1", "O-1", "N-2"], 1, 1),
            "meter_id": (0x0014, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Meter ID", "", 1, 1),
            "password": (0x0018, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Password", "", 1, 1),
            "baud": (0x001c, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Baud Rate", [
                2400, 4800, 9600, 19200, 38400], 1, 1),
            "system_power": (0x0024, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, float, "System Power", "W", 1, 1),
            "p1_divisor": (0xf910, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "P1 Divisor", [
                "0.001kWh/imp", "0.01kWh/imp", "0.1kWh/imp", "1kWh/imp", "10kWh/imp", "100kWh/imp"], 2, 1)
        }


class SDM120(SDM):

    def __init__(self, *args, **kwargs):
        self.model = "SDM120"
        self.baud = 2400

        super().__init__(*args, **kwargs)

        self.registers = {
            "voltage": (0x0000, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Voltage", "V", 1, 1),
            "current": (0x0006, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Current", "A", 1, 1),
            "power_active": (0x000c, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Power (Active)", "W", 1, 1),
            "power_apparent": (0x0012, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Power (Apparent)", "VA", 1, 1),
            "power_reactive": (0x0018, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Power (Reactive)", "VAr", 1, 1),
            "power_factor": (0x001e, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Power Factor", "", 1, 1),
            "phase_angle": (0x0024, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Phase Angle", "°", 1, 1),
            "frequency": (0x0046, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Frequency", "Hz", 1, 1),
            "import_energy_active": (0x0048, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Imported Energy (Active)", "kWh", 1, 1),
            "export_energy_active": (0x004a, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Exported Energy (Active)", "kWh", 1, 1),
            "import_energy_reactive": (0x004c, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Imported Energy (Reactive)", "kVArh", 1, 1),
            "export_energy_reactive": (0x004e, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Exported Energy (Reactive)", "kVArh", 1, 1),
            "total_demand_power_active": (0x0054, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Demand Power (Active)", "W", 2, 1),
            "maximum_total_demand_power_active": (0x0056, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Maximum Total Demand Power (Active)", "W", 2, 1),
            "import_demand_power_active": (0x0058, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Import Demand Power (Active)", "W", 2, 1),
            "maximum_import_demand_power_active": (0x005a, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Maximum Import Demand Power (Active)", "W", 2, 1),
            "export_demand_power_active": (0x005c, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Export Demand Power (Active)", "W", 2, 1),
            "maximum_export_demand_power_active": (0x005e, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Maximum Export Demand Power (Active)", "W", 2, 1),
            "total_demand_current": (0x0102, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Demand Current", "A", 3, 1),
            "maximum_total_demand_current": (0x0108, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Maximum Total Demand Current", "A", 3, 1),
            "total_energy_active": (0x0156, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Energy (Active)", "kWh", 4, 1),
            "total_energy_reactive": (0x0158, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Energy (Reactive)", "kVArh", 4, 1),

            "demand_time": (0x0000, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Demand Time", "s", 1, 1),
            "demand_period": (0x0002, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Demand Period", "s", 1, 1),
            "relay_pulse_width": (0x000c, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Relay Pulse Width", "ms", 1, 1),
            "network_parity_stop": (0x0012, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Network Parity Stop", [
                "N-1", "E-1", "O-1", "N-2"], 1, 1),
            "meter_id": (0x0014, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Meter ID", "", 1, 1),
            "baud": (0x001c, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Baud Rate", [
                2400, 4800, 9600, -1, -1, 1200], 1, 1),
            "p1_output_mode": (0x0056, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "P1 Output Mode", [
                0x0, "Import Energy (Active)", "Import + Export Energy (Active)", 0x3, "Export Energy (Active)",
                "Import Energy (Reactive)", "Import + Export Energy (Reactive)", 0x7, "Export Energy (Reactive)"], 2, 1),
            "display_scroll_timing": (0xf900, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Display Scroll Timing", "s", 3, 1),
            "p1_divisor": (0xf910, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "P1 Divisor", [
                "0.001kWh/imp", "0.01kWh/imp", "0.1kWh/imp", "1kWh/imp"], 3, 1),
            "measurement_mode": (0xf920, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Measurement Mode", [
                0x0, "Total Imported", "Total Imported + Exported", "Total Imported - Exported"], 3, 1),
            "indicator_mode": (0xf930, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Pulse/LED Indicator Mode", [
                "Import + Export Energy (Active)", "Import Energy (Active)", "Export Energy (Active)"], 3, 1)
        }


class SDM230(SDM):

    def __init__(self, *args, **kwargs):
        self.model = "SDM230"
        self.baud = 2400

        super().__init__(*args, **kwargs)

        self.registers = {
            "voltage": (0x0000, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Voltage", "V", 1, 1),
            "current": (0x0006, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Current", "A", 1, 1),
            "power_active": (0x000c, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Power (Active)", "W", 1, 1),
            "power_apparent": (0x0012, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Power (Apparent)", "VA", 1, 1),
            "power_reactive": (0x0018, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Power (Reactive)", "VAr", 1, 1),
            "power_factor": (0x001e, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Power Factor", "", 1, 1),
            "phase_angle": (0x0024, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Phase Angle", "°", 1, 1),
            "frequency": (0x0046, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Frequency", "Hz", 1, 1),
            "import_energy_active": (0x0048, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Imported Energy (Active)", "kWh", 1, 1),
            "export_energy_active": (0x004a, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Exported Energy (Active)", "kWh", 1, 1),
            "import_energy_reactive": (0x004c, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Imported Energy (Reactive)", "kVArh", 1, 1),
            "export_energy_reactive": (0x004e, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Exported Energy (Reactive)", "kVArh", 1, 1),
            "total_demand_power_active": (0x0054, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Demand Power (Active)", "W", 2, 1),
            "maximum_total_demand_power_active": (0x0056, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Maximum Total Demand Power (Active)", "W", 2, 1),
            "import_demand_power_active": (0x0058, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Import Demand Power (Active)", "W", 2, 1),
            "maximum_import_demand_power_active": (0x005a, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Maximum Import Demand Power (Active)", "W", 2, 1),
            "export_demand_power_active": (0x005c, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Export Demand Power (Active)", "W", 2, 1),
            "maximum_export_demand_power_active": (0x005e, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Maximum Export Demand Power (Active)", "W", 2, 1),
            "total_demand_current": (0x0102, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Demand Current", "A", 3, 1),
            "maximum_total_demand_current": (0x0108, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Maximum Total Demand Current", "A", 3, 1),
            "total_energy_active": (0x0156, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Energy (Active)", "kWh", 4, 1),
            "total_energy_reactive": (0x0158, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Energy (Reactive)", "kVArh", 4, 1),

            "relay_pulse_width": (0x000c, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Relay Pulse Width", "ms", 1, 1),
            "network_parity_stop": (0x0012, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Network Parity Stop", [
                "N-1", "E-1", "O-1", "N-2"], 1, 1),
            "meter_id": (0x0014, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Meter ID", "", 1, 1),
            "baud": (0x001c, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Baud Rate", [
                2400, 4800, 9600, -1, -1, 1200], 1, 1),
            "p1_output_mode": (0x0056, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "P1 Output Mode", [
                0x0, "Import Energy (Active)", "Import + Export Energy (Active)", 0x3, "Export Energy (Active)",
                "Import Energy (Reactive)", "Import + Export Energy (Reactive)", 0x7, "Export Energy (Reactive)"], 2, 1),
            "display_scroll_timing": (0xf900, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Display Scroll Timing", "s", 3, 1),
            "p1_divisor": (0xf910, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "P1 Divisor", [
                "0.001kWh/imp", "0.01kWh/imp", "0.1kWh/imp", "1kWh/imp"], 3, 1),
            "measurement_mode": (0xf920, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Measurement Mode", [
                0x0, "Total Imported", "Total Imported + Exported", "Total Imported - Exported"], 3, 1),
            "running_time": (0xf930, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Running Time", "h", 3, 1)
        }


class SDM630(SDM):

    def __init__(self, *args, **kwargs):
        self.model = "SDM630"
        self.baud = 9600

        super().__init__(*args, **kwargs)

        self.registers = {
            "l1_voltage": (0x0000, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L1 Voltage", "V", 1, 1),
            "l2_voltage": (0x0002, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L2 Voltage", "V", 1, 1),
            "l3_voltage": (0x0004, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L3 Voltage", "V", 1, 1),
            "l1_current": (0x0006, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L1 Current", "A", 1, 1),
            "l2_current": (0x0008, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L2 Current", "A", 1, 1),
            "l3_current": (0x000a, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L3 Current", "A", 1, 1),
            "l1_power_active": (0x000c, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L1 Power (Active)", "W", 1, 1),
            "l2_power_active": (0x000e, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L2 Power (Active)", "W", 1, 1),
            "l3_power_active": (0x0010, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L3 Power (Active)", "W", 1, 1),
            "l1_power_apparent": (0x0012, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L1 Power (Apparent)", "VA", 1, 1),
            "l2_power_apparent": (0x0014, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L2 Power (Apparent)", "VA", 1, 1),
            "l3_power_apparent": (0x0016, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L3 Power (Apparent)", "VA", 1, 1),
            "l1_power_reactive": (0x0018, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L1 Power (Reactive)", "VAr", 1, 1),
            "l2_power_reactive": (0x001A, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L2 Power (Reactive)", "VAr", 1, 1),
            "l3_power_reactive": (0x001C, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L3 Power (Reactive)", "VAr", 1, 1),
            "l1_power_factor": (0x001e, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L1 Power Factor", "", 1, 1),
            "l2_power_factor": (0x0020, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L2 Power Factor", "", 1, 1),
            "l3_power_factor": (0x0022, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L3 Power Factor", "", 1, 1),
            "l1_phase_angle": (0x0024, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L1 Phase Angle", "°", 1, 1),
            "l2_phase_angle": (0x0026, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L2 Phase Angle", "°", 1, 1),
            "l3_phase_angle": (0x0028, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L3 Phase Angle", "°", 1, 1),
            "voltage_ln": (0x002a, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L-N Voltage", "V", 1, 1),
            "current_ln": (0x002e, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L-N Current", "A", 1, 1),
            "total_line_current": (0x0030, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Line Current", "A", 1, 1),
            "total_power_active": (0x0034, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Power (Active)", "W", 1, 1),
            "total_power_apparent": (0x0038, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Power (Apparent)", "VA", 1, 1),
            "total_power_reactive": (0x003C, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Power (Reactive)", "VAr", 1, 1),
            "total_power_factor": (0x003E, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Power Factor", "", 1, 1),
            "total_phase_angle": (0x0042, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Phase Angle", "°", 1, 1),
            "frequency": (0x0046, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Frequency", "Hz", 1, 1),
            "import_energy_active": (0x0048, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Imported Energy (Active)", "kWh", 1, 1),
            "export_energy_active": (0x004a, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Exported Energy (Active)", "kWh", 1, 1),
            "import_energy_reactive": (0x004c, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Imported Energy (Reactive)", "kVArh", 1, 1),
            "export_energy_reactive": (0x004e, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Exported Energy (Reactive)", "kVArh", 1, 1),
            "total_energy_apparent": (0x0050, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Energy (Apparent)", "kVAh", 2, 1),
            "total_current": (0x0052, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Current", "A", 2, 1),
            "total_import_demand_power_active": (0x0054, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Import Demand Power (Active)", "W", 2, 1),
            "maximum_import_demand_power_apparent": (0x0056, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Maximum Import Demand Power (Apparent)", "VA", 2, 1),
            "import_demand_power_active": (0x0058, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Import Demand Power (Active)", "W", 2, 1),
            "maximum_import_demand_power_active": (0x005a, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Maximum Import Demand Power (Active)", "W", 2, 1),
            "export_demand_power_active": (0x005c, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Export Demand Power (Active)", "W", 2, 1),
            "maximum_export_demand_power_active": (0x005e, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Maximum Export Demand Power (Active)", "W", 2, 1),
            "total_demand_power_apparent": (0x0064, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Demand Power (Apparent)", "VA", 2, 1),
            "maximum_demand_power_apparent": (0x0066, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Maximum System Power (Apparent)", "VA", 2, 1),
            "neutral_demand_current": (0x0068, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Neutral Demand Current", "A", 2, 1),
            "maximum_neutral_demand_current": (0x006a, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Maximum Neutral Demand Current", "A", 2, 1),
            "l12_voltage": (0x00c8, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L1-L2 Voltage", "V", 3, 1),
            "l23_voltage": (0x00ca, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L2-L3 Voltage", "V", 3, 1),
            "l31_voltage": (0x00cc, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L3-L1 Voltage", "V", 3, 1),
            "voltage_ll": (0x00ce, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L-L Voltage", "V", 3, 1),
            "neutral_current": (0x00e0, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Neutral Current", "A", 3, 1),
            "l1n_voltage_thd": (0x00ea, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L1-N Voltage THD", "%", 3, 1),
            "l2n_voltage_thd": (0x00ec, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L2-N Voltage THD", "%", 3, 1),
            "l3n_voltage_thd": (0x00ee, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L3-N Voltage THD", "%", 3, 1),
            "l1_current_thd": (0x00f0, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L1 Current THD", "%", 3, 1),
            "l2_current_thd": (0x00f2, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L2 Current THD", "%", 3, 1),
            "l3_current_thd": (0x00f4, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L3 Current THD", "%", 3, 1),
            "voltage_ln_thd": (0x00f8, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L-N Voltage THD", "%", 3, 1),
            "current_thd": (0x00fa, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Current THD", "%", 3, 1),
            "total_pf": (0x00fe, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Power Factor", "", 3, 1),
            "l1_demand_current": (0x0102, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L1 Demand Current", "A", 3, 1),
            "l2_demand_current": (0x0104, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L2 Demand Current", "A", 3, 1),
            "l3_demand_current": (0x0106, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L3 Demand Current", "A", 3, 1),
            "maximum_l1_demand_current": (0x0108, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Maximum L1 Demand Current", "A", 3, 1),
            "maximum_l2_demand_current": (0x010a, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Maximum L2 Demand Current", "A", 3, 1),
            "maximum_l3_demand_current": (0x010c, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Maximum L3 Demand Current", "A", 3, 1),
            "l12_voltage_thd": (0x014e, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L1-L2 Voltage THD", "%", 4, 1),
            "l23_voltage_thd": (0x0150, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L2-L3 Voltage THD", "%", 4, 1),
            "l31_voltage_thd": (0x0152, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L3-L1 Voltage THD", "%", 4, 1),
            "voltage_ll_thd": (0x0154, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L-L Voltage THD", "%", 4, 1),
            "total_energy_active": (0x0156, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Energy (Active)", "kWh", 4, 1),
            "total_energy_reactive": (0x0158, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Energy (Reactive)", "kVArh", 4, 1),
            "l1_demand_energy_active": (0x015a, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L1 Import Energy (Active)", "kWh", 4, 1),
            "l2_demand_energy_active": (0x015c, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L2 Import Energy (Active)", "kWh", 4, 1),
            "l3_demand_energy_active": (0x015e, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L3 Import Energy (Active)", "kWh", 4, 1),
            "l1_import_energy_active": (0x0160, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L1 Import Energy (Active)", "kWh", 4, 1),
            "l2_import_energy_active": (0x0162, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L2 Import Energy (Active)", "kWh", 4, 1),
            "l3_import_energy_active": (0x0164, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L3 Import Energy (Active)", "kWh", 4, 1),
            "l1_energy_active": (0x0166, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L1 Total Energy (Active)", "kWh", 4, 1),
            "l2_energy_active": (0x0168, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L2 Total Energy (Active)", "kWh", 4, 1),
            "l3_energy_active": (0x016a, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L3 Total Energy (Active)", "kWh", 4, 1),
            "l1_demand_energy_reactive": (0x016c, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L1 Import Energy (Reactive)", "kVArh", 4, 1),
            "l2_demand_energy_reactive": (0x016e, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L2 Import Energy (Reactive)", "kVArh", 4, 1),
            "l3_demand_energy_reactive": (0x0170, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L3 Import Energy (Reactive)", "kVArh", 4, 1),
            "l1_import_energy_reactive": (0x0172, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L1 Import Energy (Reactive)", "kVArh", 4, 1),
            "l2_import_energy_reactive": (0x0174, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L2 Import Energy (Reactive)", "kVArh", 4, 1),
            "l3_import_energy_reactive": (0x0176, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L3 Import Energy (Reactive)", "kVArh", 4, 1),
            "l1_energy_reactive": (0x0178, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L1 Total Energy (Reactive)", "kVArh", 4, 1),
            "l2_energy_reactive": (0x017a, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L2 Total Energy (Reactive)", "kVArh", 4, 1),
            "l3_energy_reactive": (0x017c, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "L3 Total Energy (Reactive)", "kVArh", 4, 1),

            "demand_time": (0x0000, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Demand Time", "s", 1, 1),
            "demand_period": (0x0002, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Demand Period", "s", 1, 1),
            "system_voltage": (0x0006, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, float, "System Voltage", "V", 1, 1),
            "system_current": (0x0008, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, float, "System Current", "A", 1, 1),
            "system_type": (0x000a, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "System Type", [
                -1, "1P2W", "3P3W", "3P4W"], 1, 1),
            "relay_pulse_width": (0x000c, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Relay Pulse Width", "ms", 1, 1),
            "network_parity_stop": (0x0012, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Network Parity Stop", [
                "N-1", "E-1", "O-1", "N-2"], 1, 1),
            "meter_id": (0x0014, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Meter ID", "", 1, 1),
            "baud": (0x001c, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Baud Rate", [
                2400, 4800, 9600, 19200, 38400], 1, 1),
            "system_power": (0x0024, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, float, "System Power", "W", 1, 1),
            "p1_divisor": (0xf910, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "P1 Divisor", [
                "0.001kWh/imp", "0.01kWh/imp", "0.1kWh/imp", "1kWh/imp", "10kWh/imp", "100kWh/imp"], 2, 1)
        }
