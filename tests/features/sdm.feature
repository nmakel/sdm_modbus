Feature: Reading SDM meter values

  Scenario: Simulate a connection to a fake SDM meter
    Given device byte endianness > and word endianness >
    And simulated memory block at 0x0034
    	| type		| value | comment		|
	| 32bit_float	| 700	| total_system_power	|
	| 18 registers	| 0	| padding		|

    And simulated memory block at 0x0048
    	| type		| value | comment		|
	| 32bit_float	| 10000	| total_import_kwh	|
	| 32bit_float	| 20000	| total_export_kwh	|

    And simulated memory block at 0x0156
    	| type		| value | comment		|
	| 32bit_float	| 0.7	| total_kwh		|

    And simulated memory block at 0x0180
    	| type		| value | comment				|
	| 32bit_float	| 123	| resettable_total_active_energy	|
	| 32bit_float	| 456	| padding? 				|
	| 32bit_float	| 789	| resettable_import_active_energy	|
	| 32bit_float	| 912	| resettable_export_active_energy	|


    And simulated memory block at 0x0500
    	| type		| value | comment			|
	| 32bit_float	| 30000	| total_import_active_power	|
	| 32bit_float	| 40000	| total_export_active_power	|

    And a SDM72 meter client
    When simulating the modbus slave
    And we read all values
    Then the result key "total_system_power" should be equal to 700.0
    And the result key "total_import_kwh" should be equal to 10000.0
    And the result key "total_export_kwh" should be equal to 20000.0
    And the result key "resettable_total_active_energy" should be equal to 123.0
    And the result key "resettable_import_active_energy" should be equal to 789.0
    And the result key "resettable_export_active_energy" should be equal to 912.0
    And the result key "total_import_active_power" should be equal to 30000.0
    And the result key "total_export_active_power" should be equal to 40000.0
    And the result key "total_kwh" should be within 0.0001 of 0.7
