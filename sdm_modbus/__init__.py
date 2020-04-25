#!/usr/bin/env python3

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.register_read_message import ReadInputRegistersResponse
from pymodbus.register_read_message import ReadHoldingRegistersResponse


class SDM:
    model = "SDM"
    baud = 2400
    retries = 3

    input_registers = {}
    holding_registers = {}

    def __init__(
        self, host=False, port=False,
        device=False, baud=False, unit=1
    ):
        self.host = host
        self.port = port
        self.unit = unit
        self.device = device

        if baud:
            self.baud = baud

        if device:
            self.mode = "RTU"
            self.client = ModbusSerialClient(method="rtu", port=self.device, timeout=1)
        else:
            self.mode = "TCP"
            self.client = ModbusTcpClient(self.host, port=self.port)

    def __repr__(self):
        if self.mode == "RTU":
            return f"{self.model}({self.device}, baud={self.baud}, unit={hex(self.unit)})"
        elif self.mode == "TCP":
            return f"{self.model}({self.host}:{self.port}, unit={hex(self.unit)})"
        else:
            return f"<{self.__class__.__module__}.{self.__class__.__name__} object at {hex(id(self))}>"

    def _read_input_register_32f(self, address, length):
        for i in range(self.retries):
            result = self.client.read_input_registers(address=address, count=length, unit=self.unit)

            if isinstance(result, ReadInputRegistersResponse):
                return BinaryPayloadDecoder.fromRegisters(result.registers, Endian.Big).decode_32bit_float()

        return None

    def _read_holding_register_32f(self, address, length):
        for i in range(self.retries):
            result = self.client.read_holding_registers(address=address, count=length, unit=self.unit)

            if isinstance(result, ReadHoldingRegistersResponse):
                return BinaryPayloadDecoder.fromRegisters(result.registers, Endian.Big).decode_32bit_float()

        return None

    def _read(self, value, precision=2):
        address, length, func, rtype, label, fmt = value

        try:
            if func == "_read_input_register_32f":
                raw = self._read_input_register_32f(address, length)
            elif func == "_read_holding_register_32f":
                raw = self._read_holding_register_32f(address, length)

            if rtype is float:
                return float(f"{raw:.{precision}f}")
            elif rtype is hex:
                return hex(int(raw))
            else:
                return rtype(raw)

            raise NotImplementedError(func)
        except NotImplementedError:
            raise

    def _write_holding_register(self, address, value):
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        builder.add_32bit_float(value)
        payload = builder.to_registers()

        return self.client.write_registers(address=address, values=payload, unit=self.unit)

    def connected(self):
        return bool(self.client.connect())

    def read_input(self, key, precision=2):
        if key not in self.input_registers:
            raise KeyError(key)

        return self._read(self.input_registers[key], precision=precision)

    def read_holding(self, key, precision=2):
        if key not in self.holding_registers:
            raise KeyError(key)

        return self._read(self.holding_registers[key], precision=precision)

    def write_holding(self, key, value):
        if key not in self.holding_registers:
            raise KeyError(key)

        address, length, func, rtype, label, fmt = self.holding_registers[key]

        return self._write_holding_register(address, value)

    def read_all_input(self, precision=2):
        return {k: self._read(v, precision=precision) for k, v in self.input_registers.items()}

    def read_all_holding(self, precision=2):
        return {k: self._read(v, precision=precision) for k, v in self.holding_registers.items()}

    def pprint(self):
        print(f"{self}:")

        print("\nInput Registers:")
        for k, v in self.read_all_input().items():
            address, length, func, rtype, label, fmt = self.input_registers[k]

            if type(fmt) is list or type(fmt) is dict:
                print(f"\t{label}: {fmt[v]}")
            else:
                print(f"\t{label}: {v}{fmt}")

        print("\nHolding Registers:")
        for k, v in self.read_all_holding().items():
            address, length, func, rtype, label, fmt = self.holding_registers[k]

            if type(fmt) is list or type(fmt) is dict:
                print(f"\t{label}: {fmt[v]}")
            else:
                print(f"\t{label}: {v}{fmt}")


class SDM120(SDM):

    def __init__(self, *args, **kwargs):
        self.model = "SDM120"

        super().__init__(*args, **kwargs)

        self.input_registers = {
            "voltage": (0x0000, 2, "_read_input_register_32f", float, "Voltage", "V"),
            "current": (0x0006, 2, "_read_input_register_32f", float, "Current", "A"),
            "power_active": (0x000c, 2, "_read_input_register_32f", float, "Power (Active)", "W"),
            "power_apparent": (0x0012, 2, "_read_input_register_32f", float, "Power (Apparent)", "VA"),
            "power_reactive": (0x0018, 2, "_read_input_register_32f", float, "Power (Reactive)", "VA"),
            "pfactor": (0x001e, 2, "_read_input_register_32f", float, "Power Factor", ""),
            "frequency": (0x0046, 2, "_read_input_register_32f", float, "Frequency", "Hz"),
            "import_energy_active": (0x0048, 2, "_read_input_register_32f", float, "Imported Energy (Active)", "kWh"),
            "export_energy_active": (0x004a, 2, "_read_input_register_32f", float, "Imported Energy (Active)", "kWh"),
            "import_energy_reactive": (0x004c, 2, "_read_input_register_32f", float, "Imported Energy (Reactive)", "kVAh"),
            "export_energy_reactive": (0x004e, 2, "_read_input_register_32f", float, "Exported Energy (Reactive)", "kVAh"),
            "total_energy_active": (0x0156, 2, "_read_input_register_32f", float, "Total Energy (Active)", "kWh"),
            "total_energy_reactive": (0x0160, 2, "_read_input_register_32f", float, "Total Energy (Reactive)", "kVAh")
        }

        self.holding_registers = {
            "demand_time": (0x0000, 2, "_read_holding_register_32f", int, "Demand Time", "s"),
            "demand_period": (0x0002, 2, "_read_holding_register_32f", int, "Demand Period", "s"),
            "meter_id": (0x0014, 2, "_read_holding_register_32f", int, "Meter ID", ""),
            "relay_pulse_width": (0x000c, 2, "_read_holding_register_32f", int, "Relay Pulse Width", "ms"),
            "network_parity_stop": (0x0012, 2, "_read_holding_register_32f", int, "Network Parity Stop", ["N-1", "E-1", "O-1", "N-2"]),
            "baud": (0x001c, 2, "_read_holding_register_32f", int, "Baud Rate", [2400, 4800, 9600, -1, -1, 1200]),
            "p1_output_mode": (0x0056, 2, "_read_holding_register_32f", hex, "P1 Output Mode", {
                "0x0": 0x0, "0x1": "Import Energy (Active)", "0x2": "Import + Export Energy (Active)", "0x3": 0x3, "0x4": "Export Energy (Active)",
                "0x5": "Import Energy (Reactive)", "0x6": "Import + Export Energy (Reactive)", "0x7": 0x7, "0x8": "Export Energy (Reactive)"}),
            "display_scroll_timing": (0xf900, 2, "_read_holding_register_32f", int, "Display Scroll Timing", "s"),
            "p1_divisor": (0xf910, 2, "_read_holding_register_32f", hex, "P1 Divisor", {
                "0x0": "0.001kWh/imp", "0x1": "0.01kWh/imp", "0x2": "0.1kWh/imp", "0x3": "1kWh/imp"}),
            "measurement_mode": (0xf920, 2, "_read_holding_register_32f", hex, "Measurement Mode", {
                "0x0": 0x0, "0x1": "Total Imported", "0x2": "Total Imported + Exported", "0x3": "Total Imported - Exported"})
        }


class SDM630(SDM):

    def __init__(self, *args, **kwargs):
        self.model = "SDM630"
        self.baud = 9600

        super().__init__(*args, **kwargs)

        self.input_registers = {
            "p1_voltage": (0x0000, 2, "_read_input_register_32f", float, "P1 Voltage", "V"),
            "p2_voltage": (0x0002, 2, "_read_input_register_32f", float, "P2 Voltage", "V"),
            "p3_voltage": (0x0004, 2, "_read_input_register_32f", float, "P3 Voltage", "V"),
            "p1_current": (0x0006, 2, "_read_input_register_32f", float, "P1 Current", "A"),
            "p2_current": (0x0008, 2, "_read_input_register_32f", float, "P2 Current", "A"),
            "p3_current": (0x000a, 2, "_read_input_register_32f", float, "P3 Current", "A"),
            "p1_power_active": (0x000c, 2, "_read_input_register_32f", float, "P1 Power (Active)", "W"),
            "p2_power_active": (0x000e, 2, "_read_input_register_32f", float, "P2 Power (Active)", "W"),
            "p3_power_active": (0x0010, 2, "_read_input_register_32f", float, "P3 Power (Active)", "W"),
            "p1_power_apparent": (0x0012, 2, "_read_input_register_32f", float, "P1 Power (Apparent)", "VA"),
            "p2_power_apparent": (0x0014, 2, "_read_input_register_32f", float, "P2 Power (Apparent)", "VA"),
            "p3_power_apparent": (0x0016, 2, "_read_input_register_32f", float, "P3 Power (Apparent)", "VA"),
            "p1_power_reactive": (0x0018, 2, "_read_input_register_32f", float, "P1 Power (Reactive)", "VA"),
            "p2_power_reactive": (0x001A, 2, "_read_input_register_32f", float, "P2 Power (Reactive)", "VA"),
            "p3_power_reactive": (0x001C, 2, "_read_input_register_32f", float, "P3 Power (Reactive)", "VA"),
            "p1_pfactor": (0x001e, 2, "_read_input_register_32f", float, "P1 Power Factor", ""),
            "p2_pfactor": (0x0020, 2, "_read_input_register_32f", float, "P2 Power Factor", ""),
            "p3_pfactor": (0x0022, 2, "_read_input_register_32f", float, "P3 Power Factor", ""),
            "p1_phase_angle": (0x0024, 2, "_read_input_register_32f", float, "P1 Phase Angle", "°"),
            "p2_phase_angle": (0x0026, 2, "_read_input_register_32f", float, "P2 Phase Angle", "°"),
            "p3_phase_angle": (0x0028, 2, "_read_input_register_32f", float, "P3 Phase Angle", "°"),
            "average_line_to_neutral_voltage": (0x002a, 2, "_read_input_register_32f", float, "Average Line to Neutral Voltage", "V"),
            "average_line_to_neutral_current": (0x002e, 2, "_read_input_register_32f", float, "Average Line to Neutral Current", "A"),
            "total_line_current": (0x0030, 2, "_read_input_register_32f", float, "Total Line Current", "A"),
            "total_power_active": (0x0034, 2, "_read_input_register_32f", float, "Total Power (Active)", "W"),
            "total_power_apparent": (0x0038, 2, "_read_input_register_32f", float, "Total Power (Apparent)", "VA"),
            "total_power_reactive": (0x003C, 2, "_read_input_register_32f", float, "Total Power (Reactive)", "VA"),
            "total_power_factor": (0x003E, 2, "_read_input_register_32f", float, "Total Power Factor", ""),
            "total_phase_angle": (0x0042, 2, "_read_input_register_32f", float, "Total Phase Angle", ""),
            "frequency": (0x0046, 2, "_read_input_register_32f", float, "Frequency", "Hz"),
            "import_energy_active": (0x0048, 2, "_read_input_register_32f", float, "Imported Energy (Active)", ""),
            "export_energy_active": (0x004a, 2, "_read_input_register_32f", float, "Exported Energy (Active)", ""),
            "import_energy_reactive": (0x004c, 2, "_read_input_register_32f", float, "Imported Energy (Reactive)", ""),
            "export_energy_reactive": (0x004e, 2, "_read_input_register_32f", float, "Exported Energy (Reactive)", ""),
            "total_import_demand_power_active": (0x0054, 2, "_read_input_register_32f", float, "Total Import Demand Power (Active)", "W"),
            "maximum_import_demand_power_apparent": (0x0056, 2, "_read_input_register_32f", float, "Maximum Import Demand Power (Apparent)", "VA"),
            "total_demand_power_apparent": (0x0064, 2, "_read_input_register_32f", float, "Total Demand Power (Apparent)", "VA"),
            "maximum_demand_power_apparent": (0x0066, 2, "_read_input_register_32f", float, "Maximum System Power (Apparent)", "VA"),
            "neutral_demand_current": (0x0068, 2, "_read_input_register_32f", float, "Neutral Demand Current", "A"),
            "maximum_neutral_demand_current": (0x006a, 2, "_read_input_register_32f", float, "Maximum Neutral Demand Current", "A"),
            "l1_to_l2_voltage": (0x00c8, 2, "_read_input_register_32f", float, "L1 to L2 Voltage", "V"),
            "l2_to_l3_voltage": (0x00ca, 2, "_read_input_register_32f", float, "L2 to L3 Voltage", "V"),
            "l3_to_l1_voltage": (0x00cc, 2, "_read_input_register_32f", float, "L3 to L1 Voltage", "V"),
            "average_line_to_line_voltage": (0x00ce, 2, "_read_input_register_32f", float, "Average Line to Line Voltage", "V"),
            "neutral_current": (0x00e0, 2, "_read_input_register_32f", float, "Neutral Current", "A"),
            "p1_line_neutral_voltage_thd": (0x00ea, 2, "_read_input_register_32f", float, "P1 Line to Neutral Voltage THD", "%"),
            "p2_line_neutral_voltage_thd": (0x00ec, 2, "_read_input_register_32f", float, "P2 Line to Neutral Voltage THD", "%"),
            "p3_line_neutral_voltage_thd": (0x00ee, 2, "_read_input_register_32f", float, "P3 Line to Neutral Voltage THD", "%"),
            "p1_current_thd": (0x00f0, 2, "_read_input_register_32f", float, "P1 Current THD", "%"),
            "p2_current_thd": (0x00f2, 2, "_read_input_register_32f", float, "P2 Current THD", "%"),
            "p3_current_thd": (0x00f4, 2, "_read_input_register_32f", float, "P3 Current THD", "%"),
            "average_line_neutral_voltage_thd": (0x00f8, 2, "_read_input_register_32f", float, "Average Line to Neutral Voltage THD", "%"),
            "average_current_thd": (0x00fa, 2, "_read_input_register_32f", float, "Average Current THD", "%"),
            "p1_demand_current": (0x0102, 2, "_read_input_register_32f", float, "P1 Demand Current", "A"),
            "p2_demand_current": (0x0104, 2, "_read_input_register_32f", float, "P2 Demand Current", "A"),
            "p3_demand_current": (0x0106, 2, "_read_input_register_32f", float, "P3 Demand Current", "A"),
            "maximum_p1_demand_current": (0x0108, 2, "_read_input_register_32f", float, "Maximum P1 Demand Current", "A"),
            "maximum_p2_demand_current": (0x010a, 2, "_read_input_register_32f", float, "Maximum P2 Demand Current", "A"),
            "maximum_p3_demand_current": (0x010c, 2, "_read_input_register_32f", float, "Maximum P3 Demand Current", "A"),
            "p1_line_neutral_voltage_thd": (0x00ea, 2, "_read_input_register_32f", float, "P1 Line to Neutral Voltage THD", "%"),
            "p2_line_neutral_voltage_thd": (0x00ec, 2, "_read_input_register_32f", float, "P2 Line to Neutral Voltage THD", "%"),
            "p3_line_neutral_voltage_thd": (0x00ee, 2, "_read_input_register_32f", float, "P3 Line to Neutral Voltage THD", "%"),
            "l1_to_l2_voltage_thd": (0x014e, 2, "_read_input_register_32f", float, "L1 to L2 Voltage THD", "%"),
            "l2_to_l3_voltage_thd": (0x0150, 2, "_read_input_register_32f", float, "L2 to L3 Voltage THD", "%"),
            "l3_to_l1_voltage_thd": (0x0152, 2, "_read_input_register_32f", float, "L3 to L1 Voltage THD", "%"),
            "average_line_to_line_voltage_thd": (0x0154, 2, "_read_input_register_32f", float, "Average Line to Line Voltage THD", "%"),
            "total_energy_active": (0x0156, 2, "_read_input_register_32f", float, "Total Energy (Active)", "kWh"),
            "total_energy_apparent": (0x0050, 2, "_read_input_register_32f", float, "Total Energy (Apparent)", ""),
            "total_energy_reactive": (0x0160, 2, "_read_input_register_32f", float, "Total Energy (Reactive)", "kVAh"),
            "total_current": (0x0052, 2, "_read_input_register_32f", float, "Total Current", "")
        }

        self.holding_registers = {
            "demand_time": (0x0000, 2, "_read_holding_register_32f", int, "Demand Time", "s"),
            "demand_period": (0x0002, 2, "_read_holding_register_32f", int, "Demand Period", "s"),
            "system_voltage": (0x0006, 2, "_read_holding_register_32f", float, "System Voltage", "V"),
            "system_current": (0x0008, 2, "_read_holding_register_32f", float, "System Current", "A"),
            "system_type": (0x000a, 2, "_read_holding_register_32f", int, "System Type", [-1, "1P2W", "3P3W", "3P4W"]),
            "relay_pulse_width": (0x000c, 2, "_read_holding_register_32f", int, "Relay Pulse Width", "ms"),
            "network_parity_stop": (0x0012, 2, "_read_holding_register_32f", int, "Network Parity Stop", ["N-1", "E-1", "O-1", "N-2"]),
            "meter_id": (0x0014, 2, "_read_holding_register_32f", int, "Meter ID", ""),
            "p1_divisor": (0xf910, 2, "_read_holding_register_32f", int, "P1 Divisor", [
                "0.001kWh/imp", "0.01kWh/imp", "0.1kWh/imp", "1kWh/imp", "10kWh/imp", "100kWh/imp"]),
            "baud": (0x001c, 2, "_read_holding_register_32f", int, "Baud Rate", [2400, 4800, 9600, 19200, 38400]),
            "system_power": (0x0024, 2, "_read_holding_register_32f", float, "System Power", "W")
        }
