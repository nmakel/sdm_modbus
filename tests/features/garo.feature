Feature: Reading SDM meter values

  Scenario: Simulate a connection to a fake GARO GNM3D meter
    Given device byte endianness > and word endianness <
    And simulated memory block at 0x0000
        | type            | value      | comment                      |
        | 32bit_int       |    2301    | l1n_voltage                  |
        | 32bit_int       |    2302    | l2n_voltage                  |
        | 32bit_int       |    2303    | l3n_voltage                  |
        | 32bit_int       |    4001    | l12_voltage                  |
        | 32bit_int       |    4002    | l23_voltage                  |
        | 32bit_int       |    4003    | l31_voltage                  |
        | 32bit_int       |    10200   | l1_current                   |
        | 32bit_int       |    11400   | l2_current                   |
        | 32bit_int       |    12600   | l3_current                   |
        | 32bit_int       |    1000    | l1_power_active              |
        | 32bit_int       |    2000    | l2_power_active              |
        | 32bit_int       |    3000    | l3_power_active              |
        | 32bit_int       |    1200    | l1_energy_apparent           |
        | 32bit_int       |    2300    | l2_energy_apparent           |
        | 32bit_int       |    3400    | l3_energy_apparent           |
        | 32bit_int       |    100     | l1_energy_reactive           |
        | 32bit_int       |    200     | l2_energy_reactive           |
        | 32bit_int       |    300     | l3_energy_reactive           |

    And simulated memory block at 0x0024
        | type            | value      | comment                      |
        | 32bit_int       |    2305    | voltage_ln                   |
        | 32bit_int       |    4010    | voltage_ll                   |
        | 32bit_int       |    18000   | power_active                 |
        | 32bit_int       |    21000   | power_apparent               |
        | 32bit_int       |    15000   | power_reactive               |
        | 16bit_int       |    1000    | l1_power_factor              |
        | 16bit_int       |    1100    | l2_power_factor              |
        | 16bit_int       |    900     | l3_power_factor              |
        | 16bit_int       |    1010    | power_factor                 |
        | 16bit_int       |    0       | padding (phase sequence) 0x32h |
        | 16bit_int       |    500     | frequency                    |
        | 32bit_int       |    4567    | import_energy_active         |
        | 32bit_int       |    3456    | import_energy_reactive       |
        | 32bit_int       |    10000   | demand_power_active          |
        | 32bit_int       |    20000   | maximum_demand_power_active  |
        | 32bit_int       |    0       | padding (resettable import energy) |
        | 32bit_int       |    0       | padding (resettable import energy reactive) |
        | 32bit_int       |    1230    | l1_import_energy_active      |
        | 32bit_int       |    1340    | l2_import_energy_active      |
        | 32bit_int       |    1450    | l3_import_energy_active      |
        | 8 registers     |    0       | padding                      |
        | 32bit_int       |    9430    | export_energy_active         |
        | 32bit_int       |    2230    | export_energy_reactive       |

    And a GNM3D meter client
    When simulating the modbus slave
    And we read all values
    Then the result key "l1n_voltage" should be close to 230.1
    And the result key "l2n_voltage" should be close to 230.2
    And the result key "l3n_voltage" should be close to 230.3
    And the result key "l12_voltage" should be close to 400.1
    And the result key "l23_voltage" should be close to 400.2
    And the result key "l31_voltage" should be close to 400.3
    And the result key "l1_current" should be close to 10.2
    And the result key "l2_current" should be close to 11.4
    And the result key "l3_current" should be close to 12.6
    And the result key "l1_power_active" should be close to 100.0
    And the result key "l2_power_active" should be close to 200.0
    And the result key "l3_power_active" should be close to 300.0
    And the result key "l1_energy_apparent" should be close to 120.0
    And the result key "l2_energy_apparent" should be close to 230.0
    And the result key "l3_energy_apparent" should be close to 340.0
    And the result key "l1_energy_reactive" should be close to 10.0
    And the result key "l2_energy_reactive" should be close to 20.0
    And the result key "l3_energy_reactive" should be close to 30.0
    And the result key "voltage_ln" should be close to 230.5
    And the result key "voltage_ll" should be close to 401.0
    And the result key "power_active" should be close to 1800.0
    And the result key "power_apparent" should be close to 2100.0
    And the result key "power_reactive" should be close to 1500.0
    And the result key "l1_power_factor" should be close to 1.0
    And the result key "l2_power_factor" should be close to 1.1
    And the result key "l3_power_factor" should be close to 0.9
    And the result key "power_factor" should be close to 1.01
    And the result key "frequency" should be close to 50.0
    And the result key "import_energy_active" should be close to 456.7
    And the result key "import_energy_reactive" should be close to 345.6
    And the result key "demand_power_active" should be close to 1000.0
    And the result key "maximum_demand_power_active" should be close to 2000.0
    And the result key "l1_import_energy_active" should be close to 123.0
    And the result key "l2_import_energy_active" should be close to 134.0
    And the result key "l3_import_energy_active" should be close to 145.0
    And the result key "export_energy_active" should be close to 943.0
    And the result key "export_energy_reactive" should be close to 223.0
