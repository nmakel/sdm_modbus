import threading

from behave import *
from hamcrest import *

from pymodbus.version import version
from pymodbus.server.sync import ModbusTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSparseDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder

import sdm_modbus


@given('device byte endianness {} and word endianness {}')
def step_impl(context, byteendianness, wordendianness):
    context.byteendianness = byteendianness
    context.wordendianness = wordendianness


@given('simulated memory block at {:d}')
def step_impl(context, address):
    if not hasattr(context, 'block'):
        context.block = ModbusSparseDataBlock()

    context.builder_address = address
    context.builder = BinaryPayloadBuilder(
        byteorder=context.byteendianness,
        wordorder=context.wordendianness
    )

    if context.table:
        for row in context.table:
            funcname = 'add_' + row['type']

            if hasattr(context.builder, funcname):
                func = getattr(context.builder, funcname)

                if not callable(func):
                    raise ValueError("{} is not callable".format(funcname))

                func(eval(row['value']))
            else:
                context.execute_steps("Given followed by {} initialized to {}".format(row['type'], row['value']))


    context.block.setValues(context.builder_address, context.builder.to_registers())


@given('followed by {:d} registers initialized to {:d}')
def step_impl(context, wordcount, value):
    assert context.builder

    if not hasattr(context, 'block'):
        context.block = ModbusSparseDataBlock()

    for i in range(0, wordcount):
        context.builder.add_16bit_uint(0)

    context.block.setValues(context.builder_address, context.builder.to_registers())


@when('simulating the modbus slave')
def step_impl(context):
    store = ModbusSlaveContext(
        di=context.block,
        co=context.block,
        hr=context.block,
        ir=context.block,
        zero_mode=True
    )

    servercontext = ModbusServerContext(
        slaves=store,
        single=True
    )

    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName = 'Pymodbus Server'
    identity.MajorMinorRevision = version.short()

    context.modbus_server = ModbusTcpServer(
        servercontext,
        None,
        identity,
        ("localhost", 5020),
        allow_reuse_address=True
    )

    context.modbus_server_thread = threading.Thread(target=context.modbus_server.serve_forever)
    context.modbus_server_thread.start()
    context.add_cleanup(context.modbus_server_thread.join)
    context.add_cleanup(context.modbus_server.shutdown)


@given('a SDM72 meter client')
def step_impl(context):
    context.meter = sdm_modbus.SDM72(host="localhost", port=5020)
    context.add_cleanup(context.meter.disconnect)


@given('a GNM3D meter client')
def step_impl(context):
    context.meter = sdm_modbus.GNM3D(host="localhost", port=5020)
    context.add_cleanup(context.meter.disconnect)


@given('with raw value {}')
def step_impl(context, value):
    assert context.builder_address
    bytevalue = bytearray.fromhex(value)
    context.block.setValues(context.builder_address, list(bytevalue))


@given('block at {:d} with value {}')
def step_impl(context, address, value):
    bytevalue = bytearray.fromhex(value)
    context.block.setValues(address, list(bytevalue))


@when('we read all values')
def step_impl(context):
    context.result = context.meter.read_all()
    print(context.result)


@then('the result key "{}" should be equal to {}')
def step_impl(context, key, value):
    assert_that(context.result, has_entries(key, equal_to(eval(value))))


@then('the result key "{}" should be within {:f} of {:f}')
def step_impl(context, key, delta, value):
    assert_that(context.result, has_entries(key, close_to(value, delta)))


@then('the result key "{}" should be close to {:f}')
def step_impl(context, key, value):
    assert_that(context.result, has_entries(key, close_to(value, 0.00001)))
