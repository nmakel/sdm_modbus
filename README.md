# sdm_modbus

sdm_modbus is a python library that collects data from Eastron SDM single- and three-phase kWh meters over Modbus RTU or Modbus TCP.

Supported devices:
* [Eastron SDM72D-M](https://www.eastroneurope.com/products/view/sdm72modbus)
* [Eastron SDM120-Modbus](https://www.eastroneurope.com/products/view/sdm120modbus)
* [Eastron SDM230-Modbus](https://www.eastroneurope.com/products/view/sdm230modbus)
* [Eastron SDM630-Modbus](https://www.eastroneurope.com/products/view/sdm630modbus)
* [Garo GNM3D-RS485](https://www.garo.se/en/professional/products/installation-products/din-rail-components/energy-meters/energymeter-3p-modbus-rs485)
* [ESP2866/32 P1 Modbus](https://github.com/nmakel/esp_p1_modbus)

## Installation

To install, either clone this project and install using `poetry`:

```poetry install```

or install the package from PyPi:

```pip3 install sdm_modbus```

## Usage

The script `example-tcp.py` provides a minimal example of connecting to and displaying all input and holding registers on a **SDM120** over **Modbus TCP**. To display values as a JSON object, add `--json`.

```
usage: example-tcp.py [-h] [--unit UNIT] [--json] host port

positional arguments:
  host         Modbus TCP address
  port         Modbus TCP port

optional arguments:
  -h, --help   show this help message and exit
  --unit UNIT  Modbus device address
  --json       Output as JSON
```

Output:

```
SDM120(10.0.0.123:502, connectionType.TCP: timeout=1, retries=3, unit=0x1):

Input Registers:
    Voltage: 237.00V
    Current: 8.63A
    Power (Active): -1919.70W
    Power (Apparent): 2035.57VA
    Power (Reactive): -676.70VA
    Power Factor: -0.94
    Phase Angle: 0.00°
    Frequency: 50.00Hz
    Imported Energy (Active): 1551.37kWh
    Imported Energy (Active): 1335.69kWh
    Imported Energy (Reactive): 0.01kVAh
    Exported Energy (Reactive): 4362.14kVAh
    Total Demand Power (Active): 1668.02W
    Maximum Total Demand Power (Active): 3347.26W
    Import Demand Power (Active): 0.00W
    Maximum Import Demand Power (Active): 3347.26W
    Export Demand Power (Active): 1668.02W
    Maximum Export Demand Power (Active): 2109.45W
    Total Demand Current: 7.57A
    Maximum Total Demand Current: 14.97A
    Total Energy (Active): 2887.07kWh
    Total Energy (Reactive): 0.00kVAh

Holding Registers:
    Demand Time: 1s
    Demand Period: 60s
    Relay Pulse Width: 60ms
    Network Parity Stop: N-1
    Meter ID: 1
    Baud Rate: 9600
    P1 Output Mode: Export Energy (Active)
    Display Scroll Timing: 0s
    P1 Divisor: 0.001kWh/imp
    Measurement Mode: 0
    Pulse/LED Indicator Mode: Import + Export Energy (Active)
```

### Connecting

If you wish to use Modbus TCP the following parameters are relevant:

`host = IP or DNS name of your Modbus TCP gateway, required`  
`port = TCP port of the Modbus TCP gateway, required`  
`unit = Modbus device address, default=1, optional`

While if you are using a Modbus RTU connection you can specify:

`device = path to serial device, e.g. /dev/ttyUSB0, required`  
`baud = baud rate of your SDM unit, defaults to factory default, optional`  
`unit = Modbus device address, defaults to 1, optional`

Connecting to the meter:

```
    >>> import sdm_modbus

    # SDM120 over Modbus TCP
    >>> device = sdm_modbus.SDM120(host="10.0.0.123", port=502)

    # SDM630 over Modbus RTU
    >>> device = sdm_modbus.SDM630(device="/dev/ttyUSB0", baud=9600)
```

Test the connection:

```
    >>> device.connected()
    True
```

Printing the object yields basic device parameters:

```
    >>> device
    SDM120(10.0.0.123:502, connectionType.TCP: timeout=1, retries=3, unit=0x1):
```

### Connecting to Multiple Devices

Re-using an existing RTU or TCP connection is possible by providing an already connected device as `parent` when creating a new instance. This may be necessary if the Modbus TCP gateway only accepts a limited number of connections, or you wish to address multiple RTU devices on the same bus. For example:

```
    # Connect to a SDM630 over Modbus TCP
    >>> device_1 = sdm_modbus.SDM630(host="10.0.0.123", port=502, unit=1)

    # Connect to a SDM630 using the existing connection
    >>> device_2 = sdm_modbus.SDM630(parent=device_1, unit=2)
```

### Reading Registers

Reading a single input register by name:

```
    >>> device.read("voltage")
    236.89999389648438
```

Read all input registers by passing the `sdm_modbus.registerType.INPUT` enum to `read_all()`. Leave this blank to read both `INPUT` and `HOLDING` registers:

```
    >>> device.read_all(sdm_modbus.registerType.INPUT)
    {
        "voltage": 238.60000610351562,
        "current": 7.59499979019165,
        "power_active": -1673.800048828125,
        "power_apparent": 1797.5904541015625,
        "power_reactive": -655.4000244140625,
        "power_factor": -0.9311425685882568,
        "phase_angle": 0.0,
        "frequency": 50.0,
        "import_energy_active": 1556.35595703125,
        "export_energy_active": 1345.9210205078125,
        "import_energy_reactive": 0.014999999664723873,
        "export_energy_reactive": 4376.02001953125,
        "total_demand_power_active": 1659.360107421875,
        "maximum_total_demand_power_active": 3347.26318359375,
        "import_demand_power_active": 0.0,
        "maximum_import_demand_power_active": 3347.26318359375,
        "export_demand_power_active": 1659.360107421875,
        "maximum_export_demand_power_active": 2109.4541015625,
        "total_demand_current": 7.531858921051025,
        "maximum_total_demand_current": 14.968546867370605,
        "total_energy_active": 2902.277099609375,
        "total_energy_reactive": 4376.03515625
    }

    >>> device.read_all(sdm_modbus.registerType.HOLDING)
    {
        "demand_time": 1,
        "demand_period": 60,
        "relay_pulse_width": 60,
        "network_parity_stop": 0,
        "meter_id": 1,
        "baud": 2,
        "p1_output_mode": 4,
        "display_scroll_timing": 0,
        "p1_divisor": 0,
        "measurement_mode": 0,
        "indicator_mode": 0
    }
```

### Writing Registers

Writing to holding registers is also possible. Setting a new baud rate, for example:

```
    >>> device.write("baud", 2)
    WriteMultipleRegisterResponse (28,2)
```

You will need to **enable setup mode on your device** by pressing the setup button for 5 seconds, otherwise you will receive a `Exception Response(134, 6, GatewayNoResponse)` or similar.

### Register Details

If you need more information about a particular register, to look up the units or enumerations, for example:

```
    >>> device.registers["voltage"]
        # address, length, type, datatype, valuetype, name, unit, batching
        (
            0,
            2,
            <registerType.INPUT: 1>,
            <registerDataType.FLOAT32: 11>,
            <class 'float'>,
            'Voltage',
            'V',
            1
        )

    >>> device.registers["p1_divisor"]
        # address, length, type, datatype, valuetype, name, unit, batching
        (
            63760,
            2,
            <registerType.HOLDING: 2>,
            <registerDataType.FLOAT32: 11>,
            <class 'int'>,
            'P1 Divisor',
            ['0.001kWh/imp', '0.01kWh/imp', '0.1kWh/imp', '1kWh/imp'],
            2
        )
```

## Contributing

Contributions are more than welcome, especially testing on supported units, and adding other Eastron SDM units.