#!/usr/bin/env python3

import argparse
import json
import sdm_modbus


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("host", type=str, help="Modbus TCP address")
    argparser.add_argument("port", type=int, help="Modbus TCP port")
    argparser.add_argument("--timeout", type=int, default=1, help="Connection timeout")
    argparser.add_argument("--unit", type=int, default=1, help="Modbus device address")
    argparser.add_argument("--json", action="store_true", default=False, help="Output as JSON")    
    argparser.add_argument("--zeromq", action="store_true", default=False, help="Publish with zeromq")
    argparser.add_argument("--zport", type=int, default=5556, help="Port for zeromq")
    argparser.add_argument("--ztopic", type=int, default=1, help="Topic for zeromq")
    argparser.add_argument("--zsleep", type=int, default=1, help="Sleep time between messages for zeromq")
    args = argparser.parse_args()

    meter = sdm_modbus.SDM120(
        host=args.host,
        port=args.port,
        timeout=args.timeout,
        unit=args.unit
    )

    if args.json:
        print(json.dumps(meter.read_all(scaling=True), indent=4))
    elif args.zeromq:
        import zmq
        port = args.zport
        topic = args.ztopic
        sleep = args.zsleep
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind("tcp://*:%s" % port) 
        print(f"Publishing with zeromq on port:{port}")
        while True:
            messagedata = json.dumps(meter.read_all(scaling=True), indent=None, separators=(',', ':'))
            print(f"{topic} {messagedata}")
            socket.send_string(f"{topic} {messagedata}")
            time.sleep(sleep) 
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
