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
            return f"{self.model}({self.device}, {self.mode}: stopbits={self.stopbits}, parity={self.parity}, baud={self.baud}, timeout={self.timeout}, retries={self.retries}, unit={hex(self.unit)})"
        elif self.mode == connectionType.TCP:
            return f"{self.model}({self.host}:{self.port}, {self.mode}: timeout={self.timeout}, retries={self.retries}, unit={hex(self.unit)})"
        else:
            return f"<{self.__class__.__module__}.{self.__class__.__name__} object at {hex(id(self))}>"

    def _read_input_registers(self, address, length):
        for i in range(self.retries):
            result = self.client.read_input_registers(address=address, count=length, unit=self.unit)

            if not isinstance(result, ReadInputRegistersResponse):
                continue
            if len(result.registers) != length:
                continue

            return BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big, wordorder=Endian.Big)

        return None

    def _read_holding_registers(self, address, length):
        for i in range(self.retries):
            result = self.client.read_holding_registers(address=address, count=length, unit=self.unit)

            if not isinstance(result, ReadHoldingRegistersResponse):
                continue
            if len(result.registers) != length:
                continue

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
        address, length, rtype, dtype, vtype, label, fmt, batch = value

        try:
            if rtype == registerType.INPUT:
                return self._decode_value(self._read_input_registers(address, length), length, dtype, vtype)
            elif rtype == registerType.HOLDING:
                return self._decode_value(self._read_holding_registers(address, length), length, dtype, vtype)
            else:
                raise NotImplementedError(rtype)
        except NotImplementedError:
            raise

    def _read_all(self, values, rtype):
        addr_min = False
        addr_max = False

        for k, v in values.items():
            v_addr = v[0]
            v_length = v[1]

            if addr_min is False:
                addr_min = v_addr
            if addr_max is False:
                addr_max = v_addr + v_length

            if v_addr < addr_min:
                addr_min = v_addr
            if (v_addr + v_length) > addr_max:
                addr_max = v_addr + v_length

        results = {}
        offset = addr_min
        length = addr_max - addr_min

        try:
            if rtype == registerType.INPUT:
                data = self._read_input_registers(offset, length)
            elif rtype == registerType.HOLDING:
                data = self._read_holding_registers(offset, length)
            else:
                raise NotImplementedError(rtype)

            if not data:
                return results

            for k, v in values.items():
                address, length, rtype, dtype, vtype, label, fmt, batch = v

                if address > offset:
                    skip_bytes = address - offset
                    offset += skip_bytes
                    data.skip_bytes(skip_bytes * 2)

                results[k] = self._decode_value(data, length, dtype, vtype)
                offset += length
        except NotImplementedError:
            raise

        return results

    def _write(self, value, data):
        address, length, rtype, dtype, vtype, label, fmt, batch = value

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

    def read_all(self, rtype=registerType.INPUT):
        registers = {k: v for k, v in self.registers.items() if (v[2] == rtype)}
        results = {}

        for batch in range(1, len(registers)):
            register_batch = {k: v for k, v in registers.items() if (v[7] == batch)}

            if not register_batch:
                break

            results.update(self._read_all(register_batch, rtype))

        return results


class SDM120(SDM):

    def __init__(self, *args, **kwargs):
        self.model = "SDM120"
        self.baud = 2400

        super().__init__(*args, **kwargs)

        self.registers = {
            "voltage": (0x0000, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Voltage", "V", 1),
            "current": (0x0006, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Current", "A", 1),
            "power_active": (0x000c, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Power (Active)", "W", 1),
            "power_apparent": (0x0012, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Power (Apparent)", "VA", 1),
            "power_reactive": (0x0018, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Power (Reactive)", "VAr", 1),
            "power_factor": (0x001e, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Power Factor", "", 1),
            "phase_angle": (0x0024, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Phase Angle", "°", 1),
            "frequency": (0x0046, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Frequency", "Hz", 1),
            "import_energy_active": (0x0048, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Imported Energy (Active)", "kWh", 1),
            "export_energy_active": (0x004a, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Exported Energy (Active)", "kWh", 1),
            "import_energy_reactive": (0x004c, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Imported Energy (Reactive)", "kVArh", 1),
            "export_energy_reactive": (0x004e, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Exported Energy (Reactive)", "kVArh", 1),
            "total_demand_power_active": (0x0054, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Demand Power (Active)", "W", 2),
            "maximum_total_demand_power_active": (0x0056, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Maximum Total Demand Power (Active)", "W", 2),
            "import_demand_power_active": (0x0058, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Import Demand Power (Active)", "W", 2),
            "maximum_import_demand_power_active": (0x005a, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Maximum Import Demand Power (Active)", "W", 2),
            "export_demand_power_active": (0x005c, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Export Demand Power (Active)", "W", 2),
            "maximum_export_demand_power_active": (0x005e, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Maximum Export Demand Power (Active)", "W", 2),
            "total_demand_current": (0x0102, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Demand Current", "A", 3),
            "maximum_total_demand_current": (0x0108, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Maximum Total Demand Current", "A", 3),
            "total_energy_active": (0x0156, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Energy (Active)", "kWh", 4),
            "total_energy_reactive": (0x0158, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Energy (Reactive)", "kVArh", 4),

            "demand_time": (0x0000, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Demand Time", "s", 1),
            "demand_period": (0x0002, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Demand Period", "s", 1),
            "relay_pulse_width": (0x000c, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Relay Pulse Width", "ms", 1),
            "network_parity_stop": (0x0012, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Network Parity Stop", [
                "N-1", "E-1", "O-1", "N-2"], 1),
            "meter_id": (0x0014, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Meter ID", "", 1),
            "baud": (0x001c, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Baud Rate", [
                2400, 4800, 9600, -1, -1, 1200], 1),
            "p1_output_mode": (0x0056, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "P1 Output Mode", [
                0x0, "Import Energy (Active)", "Import + Export Energy (Active)", 0x3, "Export Energy (Active)",
                "Import Energy (Reactive)", "Import + Export Energy (Reactive)", 0x7, "Export Energy (Reactive)"], 2),
            "display_scroll_timing": (0xf900, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Display Scroll Timing", "s", 3),
            "p1_divisor": (0xf910, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "P1 Divisor", [
                "0.001kWh/imp", "0.01kWh/imp", "0.1kWh/imp", "1kWh/imp"], 3),
            "measurement_mode": (0xf920, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Measurement Mode", [
                0x0, "Total Imported", "Total Imported + Exported", "Total Imported - Exported"], 3),
            "indicator_mode": (0xf930, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Pulse/LED Indicator Mode", [
                "Import + Export Energy (Active)", "Import Energy (Active)", "Export Energy (Active)"], 3)
        }


class SDM230(SDM):

    def __init__(self, *args, **kwargs):
        self.model = "SDM230"
        self.baud = 2400

        super().__init__(*args, **kwargs)

        self.registers = {
            "voltage": (0x0000, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Voltage", "V", 1),
            "current": (0x0006, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Current", "A", 1),
            "power_active": (0x000c, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Power (Active)", "W", 1),
            "power_apparent": (0x0012, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Power (Apparent)", "VA", 1),
            "power_reactive": (0x0018, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Power (Reactive)", "VAr", 1),
            "power_factor": (0x001e, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Power Factor", "", 1),
            "phase_angle": (0x0024, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Phase Angle", "°", 1),
            "frequency": (0x0046, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Frequency", "Hz", 1),
            "import_energy_active": (0x0048, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Imported Energy (Active)", "kWh", 1),
            "export_energy_active": (0x004a, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Exported Energy (Active)", "kWh", 1),
            "import_energy_reactive": (0x004c, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Imported Energy (Reactive)", "kVArh", 1),
            "export_energy_reactive": (0x004e, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Exported Energy (Reactive)", "kVArh", 1),
            "total_demand_power_active": (0x0054, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Demand Power (Active)", "W", 2),
            "maximum_total_demand_power_active": (0x0056, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Maximum Total Demand Power (Active)", "W", 2),
            "import_demand_power_active": (0x0058, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Import Demand Power (Active)", "W", 2),
            "maximum_import_demand_power_active": (0x005a, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Maximum Import Demand Power (Active)", "W", 2),
            "export_demand_power_active": (0x005c, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Export Demand Power (Active)", "W", 2),
            "maximum_export_demand_power_active": (0x005e, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Maximum Export Demand Power (Active)", "W", 2),
            "total_demand_current": (0x0102, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Demand Current", "A", 3),
            "maximum_total_demand_current": (0x0108, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Maximum Total Demand Current", "A", 3),
            "total_energy_active": (0x0156, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Energy (Active)", "kWh", 4),
            "total_energy_reactive": (0x0158, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Energy (Reactive)", "kVArh", 4),

            "relay_pulse_width": (0x000c, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Relay Pulse Width", "ms", 1),
            "network_parity_stop": (0x0012, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Network Parity Stop", [
                "N-1", "E-1", "O-1", "N-2"], 1),
            "meter_id": (0x0014, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Meter ID", "", 1),
            "baud": (0x001c, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Baud Rate", [
                2400, 4800, 9600, -1, -1, 1200], 1),
            "p1_output_mode": (0x0056, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "P1 Output Mode", [
                0x0, "Import Energy (Active)", "Import + Export Energy (Active)", 0x3, "Export Energy (Active)",
                "Import Energy (Reactive)", "Import + Export Energy (Reactive)", 0x7, "Export Energy (Reactive)"], 2),
            "display_scroll_timing": (0xf900, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Display Scroll Timing", "s", 3),
            "p1_divisor": (0xf910, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "P1 Divisor", [
                "0.001kWh/imp", "0.01kWh/imp", "0.1kWh/imp", "1kWh/imp"], 3),
            "measurement_mode": (0xf920, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Measurement Mode", [
                0x0, "Total Imported", "Total Imported + Exported", "Total Imported - Exported"], 3),
            "running_time": (0xf930, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Running Time", "h", 3)
        }


class SDM630(SDM):

    def __init__(self, *args, **kwargs):
        self.model = "SDM630"
        self.baud = 9600

        super().__init__(*args, **kwargs)

        self.registers = {
            "p1_voltage": (0x0000, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P1 Voltage", "V", 1),
            "p2_voltage": (0x0002, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P2 Voltage", "V", 1),
            "p3_voltage": (0x0004, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P3 Voltage", "V", 1),
            "p1_current": (0x0006, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P1 Current", "A", 1),
            "p2_current": (0x0008, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P2 Current", "A", 1),
            "p3_current": (0x000a, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P3 Current", "A", 1),
            "p1_power_active": (0x000c, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P1 Power (Active)", "W", 1),
            "p2_power_active": (0x000e, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P2 Power (Active)", "W", 1),
            "p3_power_active": (0x0010, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P3 Power (Active)", "W", 1),
            "p1_power_apparent": (0x0012, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P1 Power (Apparent)", "VA", 1),
            "p2_power_apparent": (0x0014, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P2 Power (Apparent)", "VA", 1),
            "p3_power_apparent": (0x0016, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P3 Power (Apparent)", "VA", 1),
            "p1_power_reactive": (0x0018, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P1 Power (Reactive)", "VAr", 1),
            "p2_power_reactive": (0x001A, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P2 Power (Reactive)", "VAr", 1),
            "p3_power_reactive": (0x001C, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P3 Power (Reactive)", "VAr", 1),
            "p1_power_factor": (0x001e, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P1 Power Factor", "", 1),
            "p2_power_factor": (0x0020, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P2 Power Factor", "", 1),
            "p3_power_factor": (0x0022, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P3 Power Factor", "", 1),
            "p1_phase_angle": (0x0024, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P1 Phase Angle", "°", 1),
            "p2_phase_angle": (0x0026, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P2 Phase Angle", "°", 1),
            "p3_phase_angle": (0x0028, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P3 Phase Angle", "°", 1),
            "voltage_ln": (0x002a, 2, registerType.INPUT, registerDataType.FLOAT32, float, "L-N Voltage", "V", 1),
            "current_ln": (0x002e, 2, registerType.INPUT, registerDataType.FLOAT32, float, "L-N Current", "A", 1),
            "total_line_current": (0x0030, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Line Current", "A", 1),
            "total_power_active": (0x0034, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Power (Active)", "W", 1),
            "total_power_apparent": (0x0038, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Power (Apparent)", "VA", 1),
            "total_power_reactive": (0x003C, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Power (Reactive)", "VAr", 1),
            "total_power_factor": (0x003E, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Power Factor", "", 1),
            "total_phase_angle": (0x0042, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Phase Angle", "°", 1),
            "frequency": (0x0046, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Frequency", "Hz", 1),
            "import_energy_active": (0x0048, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Imported Energy (Active)", "kWh", 1),
            "export_energy_active": (0x004a, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Exported Energy (Active)", "kWh", 1),
            "import_energy_reactive": (0x004c, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Imported Energy (Reactive)", "kVArh", 1),
            "export_energy_reactive": (0x004e, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Exported Energy (Reactive)", "kVArh", 1),
            "total_energy_apparent": (0x0050, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Energy (Apparent)", "kVAh", 2),
            "total_current": (0x0052, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Current", "A", 2),
            "total_import_demand_power_active": (0x0054, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Import Demand Power (Active)", "W", 2),
            "maximum_import_demand_power_apparent": (0x0056, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Maximum Import Demand Power (Apparent)", "VA", 2),
            "import_demand_power_active": (0x0058, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Import Demand Power (Active)", "W", 2),
            "maximum_import_demand_power_active": (0x005a, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Maximum Import Demand Power (Active)", "W", 2),
            "export_demand_power_active": (0x005c, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Export Demand Power (Active)", "W", 2),
            "maximum_export_demand_power_active": (0x005e, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Maximum Export Demand Power (Active)", "W", 2),
            "total_demand_power_apparent": (0x0064, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Demand Power (Apparent)", "VA", 2),
            "maximum_demand_power_apparent": (0x0066, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Maximum System Power (Apparent)", "VA", 2),
            "neutral_demand_current": (0x0068, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Neutral Demand Current", "A", 2),
            "maximum_neutral_demand_current": (0x006a, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Maximum Neutral Demand Current", "A", 2),
            "p12_voltage": (0x00c8, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P1-P2 Voltage", "V", 3),
            "p23_voltage": (0x00ca, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P2-P3 Voltage", "V", 3),
            "p31_voltage": (0x00cc, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P3-P1 Voltage", "V", 3),
            "voltage_ll": (0x00ce, 2, registerType.INPUT, registerDataType.FLOAT32, float, "L-L Voltage", "V", 3),
            "neutral_current": (0x00e0, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Neutral Current", "A", 3),
            "p1n_voltage_thd": (0x00ea, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P1-N Voltage THD", "%", 3),
            "p2n_voltage_thd": (0x00ec, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P2-N Voltage THD", "%", 3),
            "p3n_voltage_thd": (0x00ee, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P3-N Voltage THD", "%", 3),
            "p1_current_thd": (0x00f0, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P1 Current THD", "%", 3),
            "p2_current_thd": (0x00f2, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P2 Current THD", "%", 3),
            "p3_current_thd": (0x00f4, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P3 Current THD", "%", 3),
            "voltage_ln_thd": (0x00f8, 2, registerType.INPUT, registerDataType.FLOAT32, float, "L-N Voltage THD", "%", 3),
            "current_thd": (0x00fa, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Current THD", "%", 3),
            "p1_demand_current": (0x0102, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P1 Demand Current", "A", 3),
            "p2_demand_current": (0x0104, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P2 Demand Current", "A", 3),
            "p3_demand_current": (0x0106, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P3 Demand Current", "A", 3),
            "maximum_p1_demand_current": (0x0108, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Maximum P1 Demand Current", "A", 3),
            "maximum_p2_demand_current": (0x010a, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Maximum P2 Demand Current", "A", 3),
            "maximum_p3_demand_current": (0x010c, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Maximum P3 Demand Current", "A", 3),
            "p12_voltage_thd": (0x014e, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P1-P2 Voltage THD", "%", 4),
            "p23_voltage_thd": (0x0150, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P2-P3 Voltage THD", "%", 4),
            "p31_voltage_thd": (0x0152, 2, registerType.INPUT, registerDataType.FLOAT32, float, "P3-P1 Voltage THD", "%", 4),
            "voltage_ll_thd": (0x0154, 2, registerType.INPUT, registerDataType.FLOAT32, float, "L-L Voltage THD", "%", 4),
            "total_energy_active": (0x0156, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Energy (Active)", "kWh", 4),
            "total_energy_reactive": (0x0158, 2, registerType.INPUT, registerDataType.FLOAT32, float, "Total Energy (Reactive)", "kVArh", 4),

            "demand_time": (0x0000, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Demand Time", "s", 1),
            "demand_period": (0x0002, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Demand Period", "s", 1),
            "system_voltage": (0x0006, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "System Voltage", "V", 1),
            "system_current": (0x0008, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "System Current", "A", 1),
            "system_type": (0x000a, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "System Type", [
                -1, "1P2W", "3P3W", "3P4W"], 1),
            "relay_pulse_width": (0x000c, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Relay Pulse Width", "ms", 1),
            "network_parity_stop": (0x0012, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Network Parity Stop", [
                "N-1", "E-1", "O-1", "N-2"], 1),
            "meter_id": (0x0014, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Meter ID", "", 1),
            "baud": (0x001c, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "Baud Rate", [
                2400, 4800, 9600, 19200, 38400], 1),
            "system_power": (0x0024, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "System Power", "W", 1),
            "p1_divisor": (0xf910, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "P1 Divisor", [
                "0.001kWh/imp", "0.01kWh/imp", "0.1kWh/imp", "1kWh/imp", "10kWh/imp", "100kWh/imp"], 2)
        }
