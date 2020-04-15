#!/usr/bin/env python3

import argparse
import sys

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client.sync import ModbusTcpClient


def get_register(client, address, length, unit):
    result = client.read_input_registers(address=address, count=length, unit=unit)
    return BinaryPayloadDecoder.fromRegisters(result.registers, Endian.Big).decode_32bit_float()


def get_holding_register(client, address, length, unit):
    result = client.read_holding_registers(address=address, count=length, unit=unit)
    return BinaryPayloadDecoder.fromRegisters(result.registers, Endian.Big).decode_32bit_float()


def write_holding_register(client, address, unit, value):
    return client.write_register(address, value, unit=unit)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("host", type=str, help="ModbusTCP address")
    argparser.add_argument("port", type=int, help="ModbusTCP port")
    argparser.add_argument("unit", type=int, help="target modbus unit")
    argparser.add_argument("baud", type=int, choices=[2400, 4800, 9600, 19200, 38400], help="new baud rate")
    argparser.add_argument("-s", "--simulate", action="store_true", default=False, help="simulate only")
    args = argparser.parse_args()

    baud_map = {
        0: 2400,
        1: 4800,
        2: 9600,
        3: 19200,
        4: 38400,
        2400: 0,
        4800: 1,
        9600: 2,
        19200: 3,
        38400: 4
    }

    try:
        print(f"Connecting to unit {args.unit} on {args.host}:{args.port}")

        mbtcpc = ModbusTcpClient(args.host, args.port)
        mbtcpc.connect()

        print("Retrieving values...")

        meter_id = int(get_holding_register(mbtcpc, 0x0014, 2, args.unit))
        meter_baud = int(get_holding_register(mbtcpc, 0x001C, 2, args.unit))

        print(f"Meter ID: {meter_id}\nBaud Rate: {baud_map[meter_baud]}")

        prompt = False
        prompt = input(f"Update unit {args.unit} to {args.baud} baud, continue? Y/n: ").lower()

        if prompt == "n":
            sys.exit(1)

        prompt = False
        prompt = input("Enable set-up mode on the SDM120 now, continue? Y/n: ").lower()

        if prompt == "n":
            sys.exit(1)

        print("Writing new values...")

        if not args.simulate:
            res = write_holding_register(mbtcpc, 0x001C, args.unit, baud_map[args.baud])

        print("Retrieving values...")

        meter_id = int(get_holding_register(mbtcpc, 0x0014, 2, args.unit))
        meter_baud = int(get_holding_register(mbtcpc, 0x001C, 2, args.unit))

        print(f"Meter ID: {meter_id}\nBaud Rate: {baud_map[meter_baud]}\nDone.")
    except KeyboardInterrupt:
        sys.exit(1)
