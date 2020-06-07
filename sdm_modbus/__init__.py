import enum

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.register_read_message import ReadInputRegistersResponse
from pymodbus.register_read_message import ReadHoldingRegistersResponse


RETRIES = 3
TIMEOUT = 1
UNIT = 1


class connectionType(enum.Enum):
    RTU = 1
    TCP = 2


class registerType(enum.Enum):
    INPUT = 1
    HOLDING = 2


class registerDataType(enum.Enum):
    BITS = 1
    UINT8 = 2
    UINT16 = 3
    UINT32 = 4
    UINT64 = 5
    INT8 = 6
    INT16 = 7
    INT32 = 8
    INT64 = 9
    FLOAT16 = 10
    FLOAT32 = 11
    STRING = 12


class SDM:

    model = "SDM"
    stopbits = 1
    parity = "N"
    baud = 38400
    registers = {}

    def __init__(
        self, host=False, port=False,
        device=False, stopbits=False, parity=False, baud=False,
        timeout=TIMEOUT, retries=RETRIES, unit=UNIT
    ):
        self.host = host
        self.port = port
        self.device = device

        if stopbits:
            self.stopbits = stopbits

        if parity:
            self.parity = parity

        if baud:
            self.baud = baud

        self.timeout = timeout
        self.retries = retries
        self.unit = unit

        if device:
            self.mode = connectionType.RTU
            self.client = ModbusSerialClient(
                method="rtu",
                port=self.device,
                stopbits=self.stopbits,
                parity=self.parity,
                baudrate=self.baud,
                timeout=self.timeout)
        else:
            self.mode = connectionType.TCP
            self.client = ModbusTcpClient(
                host=self.host,
                port=self.port,
                timeout=self.timeout
            )

    def __repr__(self):
        if self.mode == connectionType.RTU:
            return f"{self.model}({self.device}, {self.mode}: stopbits={self.stopbits}, parity={self.parity}, baud={self.baud}, timeout={self.timeout}, unit={hex(self.unit)})"
        elif self.mode == connectionType.TCP:
            return f"{self.model}({self.host}:{self.port}, {self.mode}: timeout={self.timeout}, unit={hex(self.unit)})"
        else:
            return f"<{self.__class__.__module__}.{self.__class__.__name__} object at {hex(id(self))}>"

    def _read_input_registers(self, address, length):
        for i in range(self.retries):
            result = self.client.read_input_registers(address=address, count=length, unit=self.unit)

            if isinstance(result, ReadInputRegistersResponse):
                return BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big, wordorder=Endian.Big)

        return None

    def _read_holding_registers(self, address, length):
        for i in range(self.retries):
            result = self.client.read_holding_registers(address=address, count=length, unit=self.unit)

            if isinstance(result, ReadHoldingRegistersResponse):
                return BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big, wordorder=Endian.Big)

        return None

    def _write_holding_register(self, address, value):
        return self.client.write_registers(address=address, values=value, unit=self.unit)

    def _encode_value(self, data, dtype):
        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)

        try:
            if dtype == registerDataType.FLOAT32:
                builder.add_32bit_float(data)
            else:
                raise NotImplementedError(dtype)
        except NotImplementedError:
            raise

        return builder.to_registers()

    def _decode_value(self, data, length, dtype, vtype):
        try:
            if dtype == registerDataType.FLOAT32:
                return vtype(data.decode_32bit_float())
            else:
                raise NotImplementedError(dtype)
        except NotImplementedError:
            raise

    def _read(self, value):
        address, length, rtype, dtype, vtype, label, fmt = value

        try:
            if rtype == registerType.INPUT:
                return self._decode_value(self._read_input_registers(address, length), length, dtype, vtype)
            elif rtype == registerType.HOLDING:
                return self._decode_value(self._read_holding_registers(address, length), length, dtype, vtype)
            else:
                raise NotImplementedError(rtype)
        except NotImplementedError:
            raise

    def _write(self, value, data):
        address, length, rtype, dtype, vtype, label, fmt = value

        try:
            if rtype == registerType.HOLDING:
                return self._write_holding_register(address, self._encode_value(data, dtype))
            else:
                raise NotImplementedError(rtype)
        except NotImplementedError:
            raise

    def connected(self):
        return bool(self.client.connect())

    def read(self, key):
        if key not in self.registers:
            raise KeyError(key)

        return self._read(self.registers[key])

    def write(self, key, data):
        if key not in self.registers:
            raise KeyError(key)

        return self._write(self.registers[key], data)

    def read_all(self, rtype=False):
        if rtype:
            return {k: self.read(k) for k, v in self.registers.items() if (v[2] == rtype)}
        else:
            return {k: self.read(k) for k, v in self.registers.items()}


class SDM120(SDM):

    def __init__(self, *args, **kwargs):
        self.model = "SDM120"
        self.baud = 2400

        super().__init__(*args, **kwargs)

        self.registers = {
            "voltage": (0x0000, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Voltage", "V"),
            "current": (0x0006, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Current", "A"),
            "power_active": (0x000c, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Power (Active)", "W"),
            "power_apparent": (0x0012, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Power (Apparent)", "VA"),
            "power_reactive": (0x0018, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Power (Reactive)", "VAr"),
            "power_factor": (0x001e, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Power Factor", ""),
            "phase_angle": (0x0024, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Phase Angle", "°"),
            "frequency": (0x0046, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Frequency", "Hz"),
            "import_energy_active": (0x0048, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Imported Energy (Active)", "kWh"),
            "export_energy_active": (0x004a, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Imported Energy (Active)", "kWh"),
            "import_energy_reactive": (0x004c, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Imported Energy (Reactive)", "kVArh"),
            "export_energy_reactive": (0x004e, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Exported Energy (Reactive)", "kVArh"),
            "total_demand_power_active": (0x0054, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Demand Power (Active)", "W"),
            "maximum_total_demand_power_active": (0x0056, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Maximum Total Demand Power (Active)", "W"),
            "import_demand_power_active": (0x0058, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Import Demand Power (Active)", "W"),
            "maximum_import_demand_power_active": (0x005a, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Maximum Import Demand Power (Active)", "W"),
            "export_demand_power_active": (0x005c, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Export Demand Power (Active)", "W"),
            "maximum_export_demand_power_active": (0x005e, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Maximum Export Demand Power (Active)", "W"),
            "total_demand_current": (0x0102, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Demand Current", "A"),
            "maximum_total_demand_current": (0x0108, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Maximum Total Demand Current", "A"),
            "total_energy_active": (0x0156, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Energy (Active)", "kWh"),
            "total_energy_reactive": (0x0158, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Energy (Reactive)", "kVArh"),

            "demand_time": (0x0000, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Demand Time", "s"),
            "demand_period": (0x0002, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Demand Period", "s"),
            "relay_pulse_width": (0x000c, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Relay Pulse Width", "ms"),
            "network_parity_stop": (0x0012, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Network Parity Stop", [
                "N-1", "E-1", "O-1", "N-2"]),
            "meter_id": (0x0014, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Meter ID", ""),
            "baud": (0x001c, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Baud Rate", [
                2400, 4800, 9600, -1, -1, 1200]),
            "p1_output_mode": (0x0056, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "P1 Output Mode", [
                0x0, "Import Energy (Active)", "Import + Export Energy (Active)", 0x3, "Export Energy (Active)",
                "Import Energy (Reactive)", "Import + Export Energy (Reactive)", 0x7, "Export Energy (Reactive)"]),
            "display_scroll_timing": (0xf900, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Display Scroll Timing", "s"),
            "p1_divisor": (0xf910, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "P1 Divisor", [
                "0.001kWh/imp", "0.01kWh/imp", "0.1kWh/imp", "1kWh/imp"]),
            "measurement_mode": (0xf920, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Measurement Mode", [
                0x0, "Total Imported", "Total Imported + Exported", "Total Imported - Exported"]),
            "indicator_mode": (0xf930, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Pulse/LED Indicator Mode", [
                "Import + Export Energy (Active)", "Import Energy (Active)", "Export Energy (Active)"])

        }


class SDM630(SDM):

    def __init__(self, *args, **kwargs):
        self.model = "SDM630"
        self.baud = 9600

        super().__init__(*args, **kwargs)

        self.registers = {
            "p1_voltage": (0x0000, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P1 Voltage", "V"),
            "p2_voltage": (0x0002, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P2 Voltage", "V"),
            "p3_voltage": (0x0004, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P3 Voltage", "V"),
            "p1_current": (0x0006, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P1 Current", "A"),
            "p2_current": (0x0008, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P2 Current", "A"),
            "p3_current": (0x000a, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P3 Current", "A"),
            "p1_power_active": (0x000c, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P1 Power (Active)", "W"),
            "p2_power_active": (0x000e, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P2 Power (Active)", "W"),
            "p3_power_active": (0x0010, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P3 Power (Active)", "W"),
            "p1_power_apparent": (0x0012, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P1 Power (Apparent)", "VA"),
            "p2_power_apparent": (0x0014, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P2 Power (Apparent)", "VA"),
            "p3_power_apparent": (0x0016, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P3 Power (Apparent)", "VA"),
            "p1_power_reactive": (0x0018, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P1 Power (Reactive)", "VA"),
            "p2_power_reactive": (0x001A, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P2 Power (Reactive)", "VA"),
            "p3_power_reactive": (0x001C, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P3 Power (Reactive)", "VA"),
            "p1_power_factor": (0x001e, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P1 Power Factor", ""),
            "p2_power_factor": (0x0020, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P2 Power Factor", ""),
            "p3_power_factor": (0x0022, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P3 Power Factor", ""),
            "p1_phase_angle": (0x0024, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P1 Phase Angle", "°"),
            "p2_phase_angle": (0x0026, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P2 Phase Angle", "°"),
            "p3_phase_angle": (0x0028, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P3 Phase Angle", "°"),
            "average_line_to_neutral_voltage": (0x002a, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Average Line to Neutral Voltage", "V"),
            "average_line_to_neutral_current": (0x002e, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Average Line to Neutral Current", "A"),
            "total_line_current": (0x0030, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Line Current", "A"),
            "total_power_active": (0x0034, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Power (Active)", "W"),
            "total_power_apparent": (0x0038, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Power (Apparent)", "VA"),
            "total_power_reactive": (0x003C, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Power (Reactive)", "VA"),
            "total_power_factor": (0x003E, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Power Factor", ""),
            "total_phase_angle": (0x0042, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Phase Angle", "°"),
            "frequency": (0x0046, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Frequency", "Hz"),
            "import_energy_active": (0x0048, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Imported Energy (Active)", ""),
            "export_energy_active": (0x004a, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Exported Energy (Active)", ""),
            "import_energy_reactive": (0x004c, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Imported Energy (Reactive)", ""),
            "export_energy_reactive": (0x004e, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Exported Energy (Reactive)", ""),
            "total_import_demand_power_active": (0x0054, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Import Demand Power (Active)", "W"),
            "maximum_import_demand_power_apparent": (0x0056, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Maximum Import Demand Power (Apparent)", "VA"),
            "total_demand_power_apparent": (0x0064, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Demand Power (Apparent)", "VA"),
            "maximum_demand_power_apparent": (0x0066, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Maximum System Power (Apparent)", "VA"),
            "neutral_demand_current": (0x0068, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Neutral Demand Current", "A"),
            "maximum_neutral_demand_current": (0x006a, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Maximum Neutral Demand Current", "A"),
            "l1_to_l2_voltage": (0x00c8, 2, registerType.INPUT, registerDataType.FLOAT32, float, "L1 to L2 Voltage", "V"),
            "l2_to_l3_voltage": (0x00ca, 2, registerType.INPUT, registerDataType.FLOAT32, float, "L2 to L3 Voltage", "V"),
            "l3_to_l1_voltage": (0x00cc, 2, registerType.INPUT, registerDataType.FLOAT32, float, "L3 to L1 Voltage", "V"),
            "average_line_to_line_voltage": (0x00ce, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Average Line to Line Voltage", "V"),
            "neutral_current": (0x00e0, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Neutral Current", "A"),
            "p1_line_neutral_voltage_thd": (0x00ea, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P1 Line to Neutral Voltage THD", "%"),
            "p2_line_neutral_voltage_thd": (0x00ec, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P2 Line to Neutral Voltage THD", "%"),
            "p3_line_neutral_voltage_thd": (0x00ee, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P3 Line to Neutral Voltage THD", "%"),
            "p1_current_thd": (0x00f0, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P1 Current THD", "%"),
            "p2_current_thd": (0x00f2, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P2 Current THD", "%"),
            "p3_current_thd": (0x00f4, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P3 Current THD", "%"),
            "average_line_neutral_voltage_thd": (0x00f8, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Average Line to Neutral Voltage THD", "%"),
            "average_current_thd": (0x00fa, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Average Current THD", "%"),
            "p1_demand_current": (0x0102, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P1 Demand Current", "A"),
            "p2_demand_current": (0x0104, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P2 Demand Current", "A"),
            "p3_demand_current": (0x0106, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P3 Demand Current", "A"),
            "maximum_p1_demand_current": (0x0108, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Maximum P1 Demand Current", "A"),
            "maximum_p2_demand_current": (0x010a, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Maximum P2 Demand Current", "A"),
            "maximum_p3_demand_current": (0x010c, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Maximum P3 Demand Current", "A"),
            "l1_to_l2_voltage_thd": (0x014e, 2, registerType.INPUT, registerDataType.FLOAT32, float, "L1 to L2 Voltage THD", "%"),
            "l2_to_l3_voltage_thd": (0x0150, 2, registerType.INPUT, registerDataType.FLOAT32, float, "L2 to L3 Voltage THD", "%"),
            "l3_to_l1_voltage_thd": (0x0152, 2, registerType.INPUT, registerDataType.FLOAT32, float, "L3 to L1 Voltage THD", "%"),
            "average_line_to_line_voltage_thd": (0x0154, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Average Line to Line Voltage THD", "%"),
            "total_energy_active": (0x0156, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Energy (Active)", "kWh"),
            "total_energy_apparent": (0x0050, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Energy (Apparent)", ""),
            "total_energy_reactive": (0x0160, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Energy (Reactive)", "kVAh"),
            "total_current": (0x0052, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Current", ""),

            "demand_time": (0x0000, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Demand Time", "s"),
            "demand_period": (0x0002, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Demand Period", "s"),
            "system_voltage": (0x0006, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "System Voltage", "V"),
            "system_current": (0x0008, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "System Current", "A"),
            "system_type": (0x000a, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "System Type", [
                -1, "1P2W", "3P3W", "3P4W"]),
            "relay_pulse_width": (0x000c, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Relay Pulse Width", "ms"),
            "network_parity_stop": (0x0012, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Network Parity Stop", [
                "N-1", "E-1", "O-1", "N-2"]),
            "meter_id": (0x0014, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Meter ID", ""),
            "p1_divisor": (0xf910, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "P1 Divisor", [
                "0.001kWh/imp", "0.01kWh/imp", "0.1kWh/imp", "1kWh/imp", "10kWh/imp", "100kWh/imp"]),
            "baud": (0x001c, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Baud Rate", [
                2400, 4800, 9600, 19200, 38400]),
            "system_power": (0x0024, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "System Power", "W")
        }
