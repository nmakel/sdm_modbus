# sdm_modbus

sdm_modbus is a python library that collects data from Eastron SDM single- and three-phase kWh meters over Modbus or ModbusTCP.

This repository is a work in progress.

Supported devices:
* SDM120
* SDM630

## Installation

To install, either clone this project and install using `setuptools`:

```python3 setup.py install```

or install the package from PyPi:

```pip3 install sdm_modbus```

## Usage

The script `example.py` provides a minimal example of connecting to and displaying all input and holding registers on a **SDM120** over **ModbusTCP**.

```
usage: example.py [-h] [--unit UNIT] host port

positional arguments:
  host         ModbusTCP address
  port         ModbusTCP port

optional arguments:
  -h, --help   show this help message and exit
  --unit UNIT  Modbus unit
```

Output:

```
SDM120(10.0.0.123:502, unit=0x1):

Input Registers:
    Voltage: 239.7V
    Current: 7.77A
    Power (Active): -1721.3W
    Power (Apparent): 1845.77VA
    Power (Reactive): -666.3VA
    Power Factor: -0.93
    Frequency: 50.0Hz
    Imported Energy (Active): 1546.99kWh
    Imported Energy (Active): 1320.35kWh
    Imported Energy (Reactive): 0.01kVAh
    Exported Energy (Reactive): 4346.54kVAh
    Total Energy (Active): 2867.35kWh
    Total Energy (Reactive): 0.0kVAh

Holding Registers:
    Demand Time: 1s
    Demand Period: 60s
    Meter ID: 1
    Relay Pulse Width: 60ms
    Network Parity Stop: N-1
    Baud Rate: 9600
    P1 Output Mode: Export Energy (Active)
    Display Scroll Timing: 0s
    P1 Divisor: 0.001kWh/imp
    Measurement Mode: 0
```

## Examples

If you wish to use ModbusTCP the following parameters are relevant:

`host = IP or DNS name of your ModbusTCP gateway, required`  
`port = listening port of the ModbusTCP gateway, required`  
`unit = Modbus device id, default=1, optional`

While if you are using a serial Modbus connection you can specify:

`device = path to serial device, e.g. /dev/ttyUSB0, required`  
`baud = baud rate of your SDM unit, defaults to product default, optional`  
`unit = Modbus unit id, defaults to 1, optional`

Connecting to the meter:

```
    >>> import sdm_modbus

    # SDM120 over ModbusTCP
    >>> device = sdm_modbus.SDM120(host="10.0.0.123", port=502)
    
    # DM630 over Modbus RTU
    >>> device = sdm_modbus.SDM630(device="/dev/ttyUSB0", baud=9600)
```

Test the connection:

```
    >>> device.connected()
    True
```

Printing the class yields basic device parameters:

```
    >>> device
    SDM120(10.0.0.123:502, unit=0x1)
```

Reading a single input register by name:

```
    >>> device.read_input("voltage")
    240.6

    >>> device.read_input("total_energy_active", precision=4)
    2866.6069
```

Read all input registers:

```
    >>> device.read_all_input()
    {
        'voltage': 240.6,
        'current': 8.33,
        'power_active': -1892.4,
        'power_apparent': 1985.36,
        'power_reactive': -600.3,
        'pfactor': -0.95,
        'frequency': 50.0,
        'import_energy_active': 1546.99,
        'export_energy_active': 1319.42,
        'import_energy_reactive': 0.01,
        'export_energy_reactive': 4346.17,
        'total_energy_active': 2866.41,
        'total_energy_reactive': 0.0
    }
```

The same works for holding registers:

```
    >>> device.read_holding("meter_id")
    1

    >>> device.read_all_holding()
    {
        'demand_time': 1,
        'demand_period': 60,
        'meter_id': 1,
        'relay_pulse_width': 60,
        'network_parity_stop': 0,
        'baud': 2,
        'p1_output_mode':
        '0x4',
        'display_scroll_timing': 0,
        'p1_divisor': '0x0',
        'measurement_mode': '0x0'
    }
```

To pretty print all input and holding registers *with* formatting and units:

```
    >>> device.pprint()
    SDM120(10.0.98.239:502, unit=0x1):

    Input Registers:
        Voltage: 239.6V
        Current: 3.4A
        Power (Active): -434.9W
        Power (Apparent): 757.67VA
        Power (Reactive): -620.3VA
        Power Factor: -0.57
        Frequency: 50.0Hz
        Imported Energy (Active): 1546.99kWh
        Imported Energy (Active): 1319.44kWh
        Imported Energy (Reactive): 0.01kVAh
        Exported Energy (Reactive): 4346.18kVAh
        Total Energy (Active): 2866.44kWh
        Total Energy (Reactive): 0.0kVAh

    Holding Registers:
        Demand Time: 1s
        Demand Period: 60s
        Meter ID: 1
        Relay Pulse Width: 60ms
        Network Parity Stop: N-1
        Baud Rate: 9600
        P1 Output Mode: Export Energy (Active)
        Display Scroll Timing: 0s
        P1 Divisor: 0.001kWh/imp
        Measurement Mode: 0
```

Writing to holding registers is also possible. Setting a new baud rate, for example:

```
    >>> device.write_holding("baud", 2)
    WriteMultipleRegisterResponse (28,2)
```

**Remember:** you will need to enable setup mode on your SDM120 by pressing the setup button for 5 seconds. You will receive a `Exception Response(134, 6, GatewayNoResponse)` or similar, otherwise.

## Contributing

Contributions are more than welcome, especially testing on existing and other Eastron SDM units.