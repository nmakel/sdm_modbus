#!/usr/bin/env python3

import argparse
import json
import sdm_modbus


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("host", type=str, help="Modbus TCP/UDP address")
    argparser.add_argument("port", type=int, help="Modbus TCP/UDP port")
    argparser.add_argument("--udp", action="store_true", default=False, help="Use Modbus UDP mode")
    argparser.add_argument("--timeout", type=int, default=1, help="Connection timeout")
    argparser.add_argument("--framer", type=str, default=None, help="Framer (rtu|socket|ascii|binary)")
    argparser.add_argument("--unit", type=int, default=1, help="Modbus device address")
    argparser.add_argument("--json", action="store_true", default=False, help="Output as JSON")
    args = argparser.parse_args()

    meter = sdm_modbus.SDM120(
        host=args.host,
        port=args.port,
        timeout=args.timeout,
        framer=args.framer,
        unit=args.unit,
        udp=args.udp 
    )

    if args.json:
        print(json.dumps(meter.read_all(scaling=True), indent=4))
    else:
        print(f"{meter}:")
        print("\nInput Registers:")

        for k, v in meter.read_all(sdm_modbus.registerType.INPUT).items():
            address, length, rtype, dtype, vtype, label, fmt, batch, sf = meter.registers[k]

            if type(fmt) is list or type(fmt) is dict:
                print(f"\t{label}: {fmt[str(v)]}")
            elif vtype is float:
                print(f"\t{label}: {v:.2f}{fmt}")
            else:
                print(f"\t{label}: {v}{fmt}")

        print("\nHolding Registers:")

        for k, v in meter.read_all(sdm_modbus.registerType.HOLDING).items():
            address, length, rtype, dtype, vtype, label, fmt, batch, sf = meter.registers[k]

            if type(fmt) is list:
                print(f"\t{label}: {fmt[v]}")
            elif type(fmt) is dict:
                print(f"\t{label}: {fmt[str(v)]}")
            elif vtype is float:
                print(f"\t{label}: {v:.2f}{fmt}")
            else:
                print(f"\t{label}: {v}{fmt}")
