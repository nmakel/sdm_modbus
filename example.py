#!/usr/bin/env python3

import argparse
import json
import sdm_modbus


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("host", type=str, help="ModbusTCP address")
    argparser.add_argument("port", type=int, help="ModbusTCP port")
    argparser.add_argument("--unit", type=int, default=1, help="Modbus unit")
    argparser.add_argument("--json", action="store_true", default=False, help="Output as JSON")
    args = argparser.parse_args()

    meter = sdm_modbus.SDM120(host=args.host, port=args.port, unit=args.unit)

    if args.json:
        print(json.dumps(meter.read_all(), indent=4))
    else:
        meter.pprint()