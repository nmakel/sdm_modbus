from sdm_modbus import meter
from pymodbus.constants import Endian


class CARLOGAVAZZI(meter.Meter):
    pass


# Based on https://www.enika.eu/data/files/produkty/energy%20m/CP/em24%20ethernet%20cp.pdf
class EM24(CARLOGAVAZZI):

    def __init__(self, *args, **kwargs):
        self.model = "EM24"
        self.wordorder = Endian.LITTLE

        super().__init__(*args, **kwargs)

        self.registers = {
            "l1_voltage": (0x0000, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "L1 Voltage", "V", 1, 0.1),
            "l2_voltage": (0x0002, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "L2 Voltage", "V", 1, 0.1),
            "l3_voltage": (0x0004, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "L3 Voltage", "V", 1, 0.1),
            "l12_voltage": (0x0006, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "L1-L2 Voltage", "V", 1, 0.1),
            "l23_voltage": (0x0008, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "L2-L3 Voltage", "V", 1, 0.1),
            "l31_voltage": (0x000a, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "L3-L1 Voltage", "V", 1, 0.1),
            "l1_current": (0x000c, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "L1 Current", "A", 1, 0.001),
            "l2_current": (0x000e, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "L2 Current", "A", 1, 0.001),
            "l3_current": (0x0010, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "L3 Current", "A", 1, 0.001),
            "l1_power_active": (0x0012, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "L1 Power (Active)", "W", 1, 0.1),
            "l2_power_active": (0x0014, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "L2 Power (Active)", "W", 1, 0.1),
            "l3_power_active": (0x0016, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "L3 Power (Active)", "W", 1, 0.1),
            "l1_power_apparent": (0x0018, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "L1 Power (Apparent)", "VA", 1, 0.1),
            "l2_power_apparent": (0x001a, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "L2 Power (Apparent)", "VA", 1, 0.1),
            "l3_power_apparent": (0x001c, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "L3 Power (Apparent)", "VA", 1, 0.1),
            "l1_power_reactive": (0x001e, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "L1 Power (Reactive)", "VAr", 1, 0.1),
            "l2_power_reactive": (0x0020, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "L2 Power (Reactive)", "VAr", 1, 0.1),
            "l3_power_reactive": (0x0022, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "L3 Power (Reactive)", "VAr", 1, 0.1),
            "voltage_ln": (0x0024, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "L-N Voltage", "V", 1, 0.1),
            "voltage_ll": (0x0026, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "L-L Voltage", "V", 1, 0.1),
            "power_active": (0x0028, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "Total Power (Active)", "W", 1, 0.1),
            "power_apparent": (0x002a, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "Total Power (Apparent)", "VA", 1, 0.1),
            "power_reactive": (0x002c, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "Total Power (Reactive)", "VAr", 1, 0.1),
            "l1_power_factor": (0x002e, 1, meter.registerType.INPUT, meter.registerDataType.INT16, float, "L1 Power Factor", "", 1, 0.001),
            "l2_power_factor": (0x002f, 1, meter.registerType.INPUT, meter.registerDataType.INT16, float, "L2 Power Factor", "", 1, 0.001),
            "l3_power_factor": (0x0030, 1, meter.registerType.INPUT, meter.registerDataType.INT16, float, "L3 Power Factor", "", 1, 0.001),
            "total_pf": (0x0031, 1, meter.registerType.INPUT, meter.registerDataType.INT16, float, "Total Power Factor", "", 1, 0.001),
            "phase_sequence": (0x0032, 1, meter.registerType.INPUT, meter.registerDataType.INT16, int, "Phase Sequence", "", 1, 1),
            "frequency": (0x0033, 1, meter.registerType.INPUT, meter.registerDataType.UINT16, int, "Frequency", "Hz", 1, 0.1),
            "import_energy_active": (0x0034, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "Imported Energy (Active)", "kWh", 1, 0.1),
            "import_energy_reactive": (0x0036, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "Imported Energy (Reactive)", "Kvarh", 1, 0.1),
            "demand_power_active": (0x0038, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "Demand Power Active", "W", 1, 0.1),
            "maximum_demand_power_active": (0x003a, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "Maximum Demand Power Active", "W", 1, 0.1),
            "l1_import_energy_active": (0x0040, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "L1 Imported Energy (Active)", "kWh", 1, 0.1),
            "l2_import_energy_active": (0x0042, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "L2 Imported Energy (Active)", "kWh", 1, 0.1),
            "l3_import_energy_active": (0x0044, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "L3 Imported Energy (Active)", "kWh", 1, 0.1),
            "export_energy_active": (0x004e, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "Exported Energy (Active)", "kWh", 1, 0.1),
            "export_energy_reactive": (0x0050, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "Exported Energy (Reactive)", "Kvarh", 1, 0.1),
            "demand_power_apparent": (0x0076, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "Demand Power Active", "VA", 1, 0.1),
            "maximum_demand_power_apparent": (0x0078, 2, meter.registerType.INPUT, meter.registerDataType.INT32, float, "Demand Power Active", "VA", 1, 0.1),
        }

