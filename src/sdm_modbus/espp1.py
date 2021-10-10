from sdm_modbus import meter


class ESPP1(meter.Meter):

    def __init__(self, *args, **kwargs):
        self.model = "ESP-P1-MODBUS"

        super().__init__(*args, **kwargs)

        self.registers = {
            "import_energy_active_low": (0x00, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "Imported Energy (Active), Low Tariff", "Wh", 1, 1),
            "import_energy_active_high": (0x02, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "Imported Energy (Active), High Tariff", "Wh", 1, 1),
            "export_energy_active_low": (0x04, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "Exported Energy (Active), Low Tariff", "Wh", 1, 1),
            "export_energy_active_high": (0x06, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "Exported Energy (Active), High Tariff", "Wh", 1, 1),
            "tariff": (0x08, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "Current Tariff", "", 1, 1),
            "import_power_active": (0x0A, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "Import Power (Active)", "W", 1, 1),
            "export_power_active": (0x0C, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "Export Power (Active)", "W", 1, 1),
            "power_failures": (0x0E, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "Number of power failures", "", 1, 1),
            "power_failures_long": (0x10, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "Number of long power failures", "", 1, 1),
            "l1_voltage_sags": (0x12, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "L1 Voltage Sags", "", 1, 1),
            "l2_voltage_sags": (0x14, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "L2 Voltage Sags", "", 1, 1),
            "l3_voltage_sags": (0x16, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "L3 Voltage Sags", "", 1, 1),
            "l1_voltage_swells": (0x18, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "L1 Voltage Swells", "", 1, 1),
            "l2_voltage_swells": (0x1A, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "L2 Voltage Swells", "", 1, 1),
            "l3_voltage_swells": (0x1C, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "L3 Voltage Swells", "", 1, 1),
            "l1_voltage": (0x1E, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "L1 Voltage", "V", 1, .001),
            "l2_voltage": (0x20, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "L2 Voltage", "V", 1, .001),
            "l3_voltage": (0x22, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "L3 Voltage", "V", 1, .001),
            "l1_current": (0x24, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "L1 Current", "A", 1, .001),
            "l2_current": (0x26, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "L2 Current", "A", 1, .001),
            "l3_current": (0x28, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "L3 Current", "A", 1, .001),
            "l1_import_power_active": (0x2A, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "L1 Import Power (Active)", "W", 1, 1),
            "l2_import_power_active": (0x2C, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "L2 Import Power (Active)", "W", 1, 1),
            "l3_import_power_active": (0x2E, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "L3 Import Power (Active)", "W", 1, 1),
            "l1_export_power_active": (0x30, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "L1 Export Power (Active)", "W", 1, 1),
            "l2_export_power_active": (0x32, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "L2 Export Power (Active)", "W", 1, 1),
            "l3_export_power_active": (0x34, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "L3 Export Power (Active)", "W", 1, 1),
            "import_gas_volume": (0x36, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "Imported Gas Volume", "m3", 1, .001),
            "import_thermal_measurement": (0x38, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "Imported Thermal Measurement", "GJ", 1, .001),
            "import_water_volume": (0x3A, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "Imported Water Volume", "m3", 1, .001),
            "import_slave_measurement": (0x3C, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "Imported Slave Measurement", "", 1, 1)
        }