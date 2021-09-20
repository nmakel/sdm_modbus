from .meter import *
import logging

class GNM3D(Meter):
    byteorder=Endian.Big
    wordorder=Endian.Little

    def __init__(self, *args, **kwargs):
        self.model = "GNM3D"
        super().__init__(*args, **kwargs)

        self.register_description = {
            "p1n_voltage": { "register": (0x0000, 2, registerType.INPUT, registerDataType.INT32, int, "V L1-N", "", 1), "scaling": 1/10 },
            "p2n_voltage": { "register": (0x0002, 2, registerType.INPUT, registerDataType.INT32, int, "V L2-N", "", 1), "scaling": 1/10 },
            "p3n_voltage": { "register": (0x0004, 2, registerType.INPUT, registerDataType.INT32, int, "V L3-N", "", 1), "scaling": 1/10 },
            "p12_voltage": { "register": (0x0006, 2, registerType.INPUT, registerDataType.INT32, int, "V L1-L2", "", 1), "scaling": 1/10 },
            "p23_voltage": { "register": (0x0008, 2, registerType.INPUT, registerDataType.INT32, int, "V L2-L3", "", 1), "scaling": 1/10 },
            "p31_voltage": { "register": (0x000A, 2, registerType.INPUT, registerDataType.INT32, int, "V L3-L1", "", 1), "scaling": 1/10 },
            "p1_current": { "register": (0x000C, 2, registerType.INPUT, registerDataType.INT32, int, "A L1", "", 1), "scaling": 1/1000 },
            "p2_current": { "register": (0x000E, 2, registerType.INPUT, registerDataType.INT32, int, "A L2", "", 1), "scaling": 1/1000 },
            "p3_current": { "register": (0x0010, 2, registerType.INPUT, registerDataType.INT32, int, "A L3", "", 1), "scaling": 1/1000 },
            "p1_power_active": { "register": (0x0012, 2, registerType.INPUT, registerDataType.INT32, int, "W L1", "", 1), "scaling": 1/10 },
            "p2_power_active": { "register": (0x0014, 2, registerType.INPUT, registerDataType.INT32, int, "W L2", "", 1), "scaling": 1/10 },
            "p3_power_active": { "register": (0x0016, 2, registerType.INPUT, registerDataType.INT32, int, "W L3", "", 1), "scaling": 1/10 },
            "p1_energy_apparent": { "register": (0x0018, 2, registerType.INPUT, registerDataType.INT32, int, "VA L1", "VA", 1), "scaling": 1/10 },
            "p2_energy_apparent": { "register": (0x001A, 2, registerType.INPUT, registerDataType.INT32, int, "VA L2", "VA", 1), "scaling": 1/10 },
            "p3_energy_apparent": { "register": (0x001C, 2, registerType.INPUT, registerDataType.INT32, int, "VA L3", "VA", 1), "scaling": 1/10 },
            "p1_energy_reactive": { "register": (0x001E, 2, registerType.INPUT, registerDataType.INT32, int, "VAr L1", "VAr", 1), "scaling": 1/10 },
            "p2_energy_reactive": { "register": (0x0020, 2, registerType.INPUT, registerDataType.INT32, int, "VAr L2", "VAr", 1), "scaling": 1/10 },
            "p3_energy_reactive": { "register": (0x0022, 2, registerType.INPUT, registerDataType.INT32, int, "VAr L3", "VAr", 1), "scaling": 1/10 },
            "voltage_ln": { "register": (0x0024, 2, registerType.INPUT, registerDataType.INT32, int, "V L-N sys", "V", 2), "scaling": 1/10 },
            "voltage_ll": { "register": (0x0026, 2, registerType.INPUT, registerDataType.INT32, int, "V L-L sys", "V", 2), "scaling": 1/10 },
            "power_active": { "register": (0x0028, 2, registerType.INPUT, registerDataType.INT32, int, "W sys", "W", 2), "scaling": 1/10 },
            "power_apparent": { "register": (0x002A, 2, registerType.INPUT, registerDataType.INT32, int, "VA sys", "VA", 2), "scaling": 1/10 },
            "power_reactive": { "register": (0x002C, 2, registerType.INPUT, registerDataType.INT32, int, "VAr sys", "VAr", 2), "scaling": 1/10 },
            "p1_power_factor": { "register": (0x002E, 1, registerType.INPUT, registerDataType.INT16, int, "PF L1", "", 2), "scaling": 1/1000 },
            "p2_power_factor": { "register": (0x002F, 1, registerType.INPUT, registerDataType.INT16, int, "PF L2", "", 2), "scaling": 1/1000 },
            "p3_power_factor": { "register": (0x0030, 1, registerType.INPUT, registerDataType.INT16, int, "PF L3", "", 2), "scaling": 1/1000 },
            "power_factor": { "register": (0x0031, 1, registerType.INPUT, registerDataType.INT16, int, "PF sys", "", 2), "scaling": 1/1000 },
            "frequency": { "register": (0x0033, 1, registerType.INPUT, registerDataType.INT16, int, "Hz", "", 2), "scaling": 1/10 },
            "import_energy_active": { "register": (0x0034, 2, registerType.INPUT, registerDataType.INT32, int, "kWh (+) TOT", "kWh", 2), "scaling": 1/10 },
            "import_energy_reactive": { "register": (0x0036, 2, registerType.INPUT, registerDataType.INT32, int, "kVArh (+) TOT", "kVArh", 2), "scaling": 1/10 },
            "demand_power_active": { "register": (0x0038, 2, registerType.INPUT, registerDataType.INT32, int, "W dmd", "W", 2), "scaling": 1/10 },
            "maximum_demand_power_active": { "register": (0x003A, 2, registerType.INPUT, registerDataType.INT32, int, "W dmd peak", "W", 2), "scaling": 1/10 },
            "p1_import_energy_active": { "register": (0x0040, 2, registerType.INPUT, registerDataType.INT32, int, "kWh (+) L1", "kWh", 2), "scaling": 1/10 },
            "p2_import_energy_active": { "register": (0x0042, 2, registerType.INPUT, registerDataType.INT32, int, "kWh (+) L2", "kWh", 2), "scaling": 1/10 },
            "p3_import_energy_active": { "register": (0x0044, 2, registerType.INPUT, registerDataType.INT32, int, "kWh (+) L3", "kWh", 2), "scaling": 1/10 },
            "export_energy_active": { "register": (0x004E, 2, registerType.INPUT, registerDataType.INT32, int, "kWh (-) TOT", "kWh", 2), "scaling": 1/10 },
            "export_energy_reactive": { "register": (0x0050, 2, registerType.INPUT, registerDataType.INT32, int, "kVArh (-) TOT", "kVArh", 2), "scaling": 1/10 }
        }

        self.registers = {k: v["register"] for k, v in self.register_description.items() }

    def get_scaling(self, key):
        return self.register_description[key].get("scaling", 1)

