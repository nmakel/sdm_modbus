from sdm_modbus import meter
from pymodbus.constants import Endian


class GARO(meter.Meter):
    pass


class GNM3D(GARO):

    def __init__(self, *args, **kwargs):
        self.model = "GNM3D"
        self.wordorder = Endian.Little

        super().__init__(*args, **kwargs)

        self.registers = {
            "l1n_voltage": (0x0000, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L1-N Voltage", "V", 1, 0.1),
            "l2n_voltage": (0x0002, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L2-N Voltage", "V", 1, 0.1),
            "l3n_voltage": (0x0004, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L3-N Voltage", "V", 1, 0.1),
            "l12_voltage": (0x0006, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L1-L2 Voltage", "V", 1, 0.1),
            "l23_voltage": (0x0008, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L2-L3 Voltage", "V", 1, 0.1),
            "l31_voltage": (0x000A, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L3-L1 Voltage", "V", 1, 0.1),
            "l1_current": (0x000C, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L1 Current", "A", 1, 0.001),
            "l2_current": (0x000E, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L2 Current", "A", 1, 0.001),
            "l3_current": (0x0010, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L3 Current", "A", 1, 0.001),
            "l1_power_active": (0x0012, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L1 Power (Active)", "W", 1, 0.1),
            "l2_power_active": (0x0014, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L2 Power (Active)", "W", 1, 0.1),
            "l3_power_active": (0x0016, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L3 Power (Active)", "W", 1, 0.1),
            "l1_energy_apparent": (0x0018, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L1 Energy (Apparent)", "VA", 1, 0.1),
            "l2_energy_apparent": (0x001A, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L2 Energy (Apparent)", "VA", 1, 0.1),
            "l3_energy_apparent": (0x001C, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L3 Energy (Apparent)", "VA", 1, 0.1),
            "l1_energy_reactive": (0x001E, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L1 Energy (Reactive)", "VAr", 1, 0.1),
            "l2_energy_reactive": (0x0020, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L2 Energy (Reactive)", "VAr", 1, 0.1),
            "l3_energy_reactive": (0x0022, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L3 Energy (Reactive)", "VAr", 1, 0.1),
            "voltage_ln": (0x0024, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L-N Voltage", "V", 2, 0.1),
            "voltage_ll": (0x0026, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L-L Voltage", "V", 2, 0.1),
            "power_active": (0x0028, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "Power (Active)", "W", 2, 0.1),
            "power_apparent": (0x002A, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "Power (Apparent)", "VA", 2, 0.1),
            "power_reactive": (0x002C, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "Power (Reactive)", "VAr", 2, 0.1),
            "l1_power_factor": (0x002E, 1, meter.registerType.INPUT, meter.registerDataType.INT16, int, "L1 Power Factor", "", 2, 0.001),
            "l2_power_factor": (0x002F, 1, meter.registerType.INPUT, meter.registerDataType.INT16, int, "L2 Power Factor", "", 2, 0.001),
            "l3_power_factor": (0x0030, 1, meter.registerType.INPUT, meter.registerDataType.INT16, int, "L3 Power Factor", "", 2, 0.001),
            "power_factor": (0x0031, 1, meter.registerType.INPUT, meter.registerDataType.INT16, int, "Power Factor", "", 2, 0.001),
            "frequency": (0x0033, 1, meter.registerType.INPUT, meter.registerDataType.INT16, int, "Frequency", "Hz", 2, 0.1),
            "import_energy_active": (0x0034, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "Imported Energy (Active)", "kWh", 2, 0.1),
            "import_energy_reactive": (0x0036, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "Imported Energy (Reactive)", "kVArh", 2, 0.1),
            "demand_power_active": (0x0038, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "Demand Power (Active)", "W", 2, 0.1),
            "maximum_demand_power_active": (0x003A, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "Maximum Demand Power (Active)", "W", 2, 0.1),
            "l1_import_energy_active": (0x0040, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L1 Imported Energy (Active)", "kWh", 2, 0.1),
            "l2_import_energy_active": (0x0042, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L2 Imported Energy (Active)", "kWh", 2, 0.1),
            "l3_import_energy_active": (0x0044, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L3 Imported Energy (Active)", "kWh", 2, 0.1),
            "export_energy_active": (0x004E, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "Exported Energy (Active)", "kWh", 2, 0.1),
            "export_energy_reactive": (0x0050, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "Exported Energy (Reactive)", "kVArh", 2, 0.1)
        }
