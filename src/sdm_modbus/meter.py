import enum
import time

from pymodbus.constants import Endian
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.register_read_message import ReadInputRegistersResponse
from pymodbus.register_read_message import ReadHoldingRegistersResponse


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


RETRIES = 3
TIMEOUT = 1
UNIT = 1


class Meter:
    model = "Generic"
    registers = {}

    stopbits = 1
    parity = "N"
    baud = 38400

    wordorder = Endian.Big
    byteorder = Endian.Big

    def __init__(self, **kwargs):
        parent = kwargs.get("parent")

        if parent:
            self.client = parent.client
            self.mode = parent.mode
            self.timeout = parent.timeout
            self.retries = parent.retries

            unit = kwargs.get("unit")

            if unit:
                self.unit = unit
            else:
                self.unit = parent.unit

            if self.mode is connectionType.RTU:
                self.device = parent.device
                self.stopbits = parent.stopbits
                self.parity = parent.parity
                self.baud = parent.baud
            elif self.mode is connectionType.TCP:
                self.host = parent.host
                self.port = parent.port
            else:
                raise NotImplementedError(self.mode)
        else:
            self.timeout = kwargs.get("timeout", TIMEOUT)
            self.retries = kwargs.get("retries", RETRIES)
            self.unit = kwargs.get("unit", UNIT)

            device = kwargs.get("device")

            if device:
                self.device = device

                stopbits = kwargs.get("stopbits")

                if stopbits:
                    self.stopbits = stopbits

                parity = kwargs.get("parity")

                if (parity
                        and parity.upper() in ["N", "E", "O"]):
                    self.parity = parity.upper()
                else:
                    self.parity = False

                baud = kwargs.get("baud")

                if baud:
                    self.baud = baud

                self.mode = connectionType.RTU
                self.client = ModbusSerialClient(
                    method="rtu",
                    port=self.device,
                    stopbits=self.stopbits,
                    parity=self.parity,
                    baudrate=self.baud,
                    timeout=self.timeout
                )
            else:
                self.host = kwargs.get("host")
                self.port = kwargs.get("port", 502)
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
            if not self.connected():
                self.connect()
                time.sleep(0.1)
                continue

            result = self.client.read_input_registers(address=address, count=length, unit=self.unit)

            if not isinstance(result, ReadInputRegistersResponse):
                continue
            if len(result.registers) != length:
                continue

            return BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=self.byteorder, wordorder=self.wordorder)

        return None

    def _read_holding_registers(self, address, length):
        for i in range(self.retries):
            if not self.connected():
                self.connect()
                time.sleep(0.1)
                continue

            result = self.client.read_holding_registers(address=address, count=length, unit=self.unit)

            if not isinstance(result, ReadHoldingRegistersResponse):
                continue
            if len(result.registers) != length:
                continue

            return BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=self.byteorder, wordorder=self.wordorder)

        return None

    def _write_holding_register(self, address, value):
        return self.client.write_registers(address=address, values=value, unit=self.unit)

    def _encode_value(self, data, dtype):
        builder = BinaryPayloadBuilder(byteorder=self.byteorder, wordorder=self.wordorder)

        try:
            if dtype == registerDataType.FLOAT32:
                builder.add_32bit_float(data)
            elif dtype == registerDataType.INT32:
                builder.add_32bit_int(data)
            elif dtype == registerDataType.UINT32:
                builder.add_32bit_uint(data)
            elif dtype == registerDataType.INT16:
                builder.add_16bit_int(data)
            else:
                raise NotImplementedError(dtype)
        except NotImplementedError:
            raise

        return builder.to_registers()

    def _decode_value(self, data, length, dtype, vtype):
        try:
            if dtype == registerDataType.FLOAT32:
                return vtype(data.decode_32bit_float())
            elif dtype == registerDataType.INT32:
                return vtype(data.decode_32bit_int())
            elif dtype == registerDataType.UINT32:
                return vtype(data.decode_32bit_uint())
            elif dtype == registerDataType.INT16:
                return vtype(data.decode_16bit_int())
            else:
                raise NotImplementedError(dtype)
        except NotImplementedError:
            raise

    def _read(self, value):
        address, length, rtype, dtype, vtype, label, fmt, batch, sf = value

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
                address, length, rtype, dtype, vtype, label, fmt, batch, sf = v

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
        address, length, rtype, dtype, vtype, label, fmt, batch, sf = value

        try:
            if rtype == registerType.HOLDING:
                return self._write_holding_register(address, self._encode_value(data, dtype))
            else:
                raise NotImplementedError(rtype)
        except NotImplementedError:
            raise

    def connect(self):
        return self.client.connect()

    def disconnect(self):
        self.client.close()

    def connected(self):
        return self.client.is_socket_open()

    def get_scaling(self, key):
        address, length, rtype, dtype, vtype, label, fmt, batch, sf = self.registers[key]
        return sf

    def read(self, key, scaling=False):
        if key not in self.registers:
            raise KeyError(key)

        if scaling:
            return self._read(self.registers[key]) * self.get_scaling(key)
        else:
            return self._read(self.registers[key])

    def write(self, key, data):
        if key not in self.registers:
            raise KeyError(key)

        return self._write(self.registers[key], data / self.get_scaling(key))

    def read_all(self, rtype=registerType.INPUT, scaling=False):
        registers = {k: v for k, v in self.registers.items() if (v[2] == rtype)}
        results = {}

        for batch in range(1, max(len(registers), 2)):
            register_batch = {k: v for k, v in registers.items() if (v[7] == batch)}

            if not register_batch:
                break

            results.update(self._read_all(register_batch, rtype))

        if scaling:
            return {k: v * self.get_scaling(k) for k, v in results.items()}
        else:
            return {k: v for k, v in results.items()}
