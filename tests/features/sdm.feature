Feature: Reading SDM meter values

  Scenario: Simulate a connection to a fake SDM meter
    Given device byte endianness > and word endianness >
    And simulated memory block at 0x0000
    | type        | value  | comment                            |
    | 32bit_float | 230    | voltage                            |
    | 32bit_float | 0      | empty                              |
    | 32bit_float | 0      | empty                              |
    | 32bit_float | 5      | current                            |
    | 32bit_float | 0      | empty                              |
    | 32bit_float | 0      | empty                              |
    | 32bit_float | 1150   | power_active                       |
    | 32bit_float | 0      | empty                              |
    | 32bit_float | 0      | empty                              |
    | 32bit_float | 1150   | power_apparent                     |
    | 32bit_float | 0      | empty                              |
    | 32bit_float | 0      | empty                              |
    | 32bit_float | 1300   | power_reactive                     |
    | 32bit_float | 0      | empty                              |
    | 32bit_float | 0      | empty                              |
    | 32bit_float | 1      | power_factor                       |
    | 32bit_float | 0      | empty                              |
    | 32bit_float | 0      | empty                              |
    | 32bit_float | 0      | phase_angle                        |
    | 32bit_float | 0      | empty                              |
    | 32bit_float | 0      | empty                              |
    | 32bit_float | 0      | empty                              |
    | 32bit_float | 0      | empty                              |
    | 32bit_float | 0      | empty                              |
    | 32bit_float | 0      | empty                              |
    | 32bit_float | 0      | empty                              |
    | 32bit_float | 0      | empty                              |
    | 32bit_float | 0      | empty                              |
    | 32bit_float | 0      | empty                              |
    | 32bit_float | 0      | empty                              |
    | 32bit_float | 0      | empty                              |
    | 32bit_float | 0      | empty                              |
    | 32bit_float | 0      | empty                              |
    | 32bit_float | 0      | empty                              |
    | 32bit_float | 0      | empty                              |
    | 32bit_float | 50     | frequency                          |
    | 32bit_float | 10000  | import_energy_active               |
    | 32bit_float | 5000   | export_energy_active               |
    | 32bit_float | 12000  | import_energy_reactive             |
    | 32bit_float | 6000   | export_energy_reactive             |

    And simulated memory block at 0x0054
    | type        | value  | comment                            |
    | 32bit_float | 1250   | total_demand_power_active          |
    | 32bit_float | 6000   | maximum_total_demand_power_active  |
    | 32bit_float | 5000   | import_demand_power_active         |
    | 32bit_float | 7500   | maximum_import_demand_power_active |
    | 32bit_float | 3000   | export_demand_power_active         |
    | 32bit_float | 5000   | maximum_export_demand_power_active |

    And simulated memory block at 0x0102
    | type        | value  | comment                            |
    | 32bit_float | 18     | total_demand_current               |
    | 32bit_float | 0      | empty                              |
    | 32bit_float | 0      | empty                              |
    | 32bit_float | 32.5   | maximum_total_demand_current       |

    And simulated memory block at 0x0156
    | type        | value  | comment                            |
    | 32bit_float | 10000  | total_energy_active                |
    | 32bit_float | 12000  | total_energy_reactive              |

    And a SDM120 meter client
    When simulating the modbus slave
    And we read all values
    Then the result key "voltage" should be equal to 230.0
    And the result key "current" should be equal to 5
    And the result key "power_active" should be equal to 1150
    And the result key "power_apparent" should be equal to 1150
    And the result key "power_reactive" should be equal to 1300
    And the result key "power_factor" should be equal to 1
    And the result key "phase_angle" should be equal to 0
    And the result key "frequency" should be equal to 50
    And the result key "import_energy_active" should be equal to 10000
    And the result key "export_energy_active" should be equal to 5000
    And the result key "import_energy_reactive" should be equal to 12000
    And the result key "export_energy_reactive" should be equal to 6000
    And the result key "total_demand_power_active" should be equal to 1250
    And the result key "maximum_total_demand_power_active" should be equal to 6000
    And the result key "import_demand_power_active" should be equal to 5000
    And the result key "maximum_import_demand_power_active" should be equal to 7500
    And the result key "export_demand_power_active" should be equal to 3000
    And the result key "maximum_export_demand_power_active" should be equal to 5000
    And the result key "total_demand_current" should be equal to 18
    And the result key "maximum_total_demand_current" should be equal to 32.5
    And the result key "total_energy_active" should be equal to 10000
    And the result key "total_energy_reactive" should be equal to 12000