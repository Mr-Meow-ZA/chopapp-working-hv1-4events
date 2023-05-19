def on_microbit_id_io_p14_pin_evt_rise():
    global count_2, total_2
    if pins.digital_read_pin(DigitalPin.P14) == pins.digital_read_pin(DigitalPin.P15):
        count_2 += 1
    elif pins.digital_read_pin(DigitalPin.P14) != pins.digital_read_pin(DigitalPin.P15):
        count_2 += -1
    if state_2 == 1:
        total_2 = count_2
    elif state_2 == 0:
        robotbit.motor_stop(robotbit.Motors.M2A)
    serial.write_value("total_two", total_2)
    serial.write_value("count_two", count_2)
control.on_event(EventBusSource.MICROBIT_ID_IO_P14,
    EventBusValue.MICROBIT_PIN_EVT_RISE,
    on_microbit_id_io_p14_pin_evt_rise)

def on_bluetooth_connected():
    basic.show_icon(IconNames.YES)
bluetooth.on_bluetooth_connected(on_bluetooth_connected)

def on_bluetooth_disconnected():
    basic.show_icon(IconNames.NO)
bluetooth.on_bluetooth_disconnected(on_bluetooth_disconnected)

def clearCounts():
    global count_1, total_1, count_2, total_2
    count_1 = 0
    total_1 = 0
    count_2 = 0
    total_2 = 0
    robotbit.motor_stop_all()
def serialRxTx():
    global temp
    serial.write_string("rx1 is ")
    serial.write_line(rx1)
    serial.write_string("rx2 is ")
    serial.write_line(rx2)
    temp = 0

def on_microbit_id_io_p1_pin_evt_rise():
    global count_1, total_1
    if pins.digital_read_pin(DigitalPin.P1) == pins.digital_read_pin(DigitalPin.P2):
        count_1 += 1
    elif pins.digital_read_pin(DigitalPin.P1) != pins.digital_read_pin(DigitalPin.P2):
        count_1 += -1
    if state_1 == 1:
        total_1 = count_1
    elif state_1 == 0:
        robotbit.motor_stop(robotbit.Motors.M1B)
    serial.write_value("total_one", total_1)
    serial.write_value("count_one", count_1)
control.on_event(EventBusSource.MICROBIT_ID_IO_P1,
    EventBusValue.MICROBIT_PIN_EVT_RISE,
    on_microbit_id_io_p1_pin_evt_rise)

def on_uart_data_received():
    global rx1, rx2, temp, state_1, state_2, target_1, target_2, valX, valz, speed
    rx1 = bluetooth.uart_read_until(serial.delimiters(Delimiters.HASH))
    rx2 = bluetooth.uart_read_until(serial.delimiters(Delimiters.COMMA))
    temp = 1
    if rx1 == "BF":
        clearCounts()
        state_1 = 1
        state_2 = 1
        target_1 = 100
        target_2 = 100
    elif rx1 == "BR":
        clearCounts()
        state_1 = 1
        target_1 = -50
    elif rx1 == "BB":
        clearCounts()
        state_1 = 0
    elif rx1 == "BL":
        clearCounts()
        state_1 = 1
        state_2 = 1
        target_1 = valX
        target_2 = valz
    elif rx1 == "SX":
        valX = Math.round(parse_float(rx2.substr(0, 4)))
    elif rx1 == "SZ":
        valz = Math.round(parse_float(rx2.substr(0, 4)))
    elif rx1 == "SY":
        speed = Math.round(parse_float(rx2.substr(0, 4)))
    else:
        pass
bluetooth.on_uart_data_received(serial.delimiters(Delimiters.COMMA), on_uart_data_received)

rx2 = ""
rx1 = ""
speed = 0
valz = 0
valX = 0
state_2 = 0
total_2 = 0
target_2 = 0
count_2 = 0
state_1 = 0
total_1 = 0
target_1 = 0
count_1 = 0
temp = 0
bluetooth.start_uart_service()
robotbit.motor_stop_all()
basic.show_icon(IconNames.HOUSE)
pins.set_pull(DigitalPin.P1, PinPullMode.PULL_UP)
pins.set_pull(DigitalPin.P2, PinPullMode.PULL_UP)
pins.set_pull(DigitalPin.P14, PinPullMode.PULL_UP)
pins.set_pull(DigitalPin.P15, PinPullMode.PULL_UP)
pins.set_events(DigitalPin.P1, PinEventType.EDGE)
pins.set_events(DigitalPin.P2, PinEventType.EDGE)
pins.set_events(DigitalPin.P14, PinEventType.EDGE)
pins.set_events(DigitalPin.P15, PinEventType.EDGE)
temp = 0
count_1 = 0
target_1 = 0
total_1 = 0
state_1 = 0
count_2 = 0
target_2 = 0
total_2 = 0
state_2 = 0
valX = 0
valz = 0
speed = 0
serial.write_value("total_one", total_1)
serial.write_value("total_two", total_2)
basic.show_icon(IconNames.HAPPY)

def on_forever():
    global state_1, state_2
    if total_1 < target_1:
        robotbit.motor_run(robotbit.Motors.M1B, speed * -1)
    elif total_1 > target_1:
        robotbit.motor_run(robotbit.Motors.M1B, speed)
    elif total_1 == target_1:
        robotbit.motor_stop(robotbit.Motors.M1B)
        state_1 = 0
    if total_2 < target_2:
        robotbit.motor_run(robotbit.Motors.M2A, speed)
    elif total_2 > target_2:
        robotbit.motor_run(robotbit.Motors.M2A, speed * -1)
    elif total_2 == target_2:
        robotbit.motor_stop(robotbit.Motors.M1B)
        state_2 = 0
basic.forever(on_forever)
