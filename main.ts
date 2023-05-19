control.onEvent(EventBusSource.MICROBIT_ID_IO_P2, EventBusValue.MICROBIT_PIN_EVT_RISE, function () {
    edge_state_P2 = 1
    serial.writeValue("state P2", edge_state_P2)
    basic.pause(2)
})
bluetooth.onBluetoothConnected(function () {
    basic.showIcon(IconNames.Yes)
})
bluetooth.onBluetoothDisconnected(function () {
    basic.showIcon(IconNames.No)
})
function clearCounts () {
    count_1 = 0
    total_1 = 0
    target_1 = 0
    robotbit.MotorStopAll()
}
function serialRxTx () {
    serial.writeString("rx1 is ")
    serial.writeLine(rx1)
    serial.writeString("rx2 is ")
    serial.writeLine(rx2)
    temp = 0
}
control.onEvent(EventBusSource.MICROBIT_ID_IO_P1, EventBusValue.MICROBIT_PIN_EVT_RISE, function () {
    edge_state_P1 = 1
    serial.writeValue("state P1", edge_state_P1)
    basic.pause(2)
})
control.onEvent(EventBusSource.MICROBIT_ID_IO_P2, EventBusValue.MICROBIT_PIN_EVT_FALL, function () {
    edge_state_P2 = 0
    serial.writeValue("state P2", edge_state_P2)
    basic.pause(2)
})
control.onEvent(EventBusSource.MICROBIT_ID_IO_P1, EventBusValue.MICROBIT_PIN_EVT_FALL, function () {
    edge_state_P1 = 0
    serial.writeValue("state P1", edge_state_P1)
    basic.pause(2)
})
bluetooth.onUartDataReceived(serial.delimiters(Delimiters.Comma), function () {
    rx1 = bluetooth.uartReadUntil(serial.delimiters(Delimiters.Hash))
    rx2 = bluetooth.uartReadUntil(serial.delimiters(Delimiters.Comma))
    temp = 1
    if (rx2 == "D") {
        if (rx1 == "BF") {
            clearCounts()
            state_1 = 1
            target_1 = 100
        } else if (rx1 == "BR") {
            clearCounts()
            state_1 = 1
            target_1 = -50
        } else if (rx1 == "BB") {
            clearCounts()
            state_1 = 0
            robotbit.MotorStop(robotbit.Motors.M1B)
        } else if (rx1 == "BL") {
            clearCounts()
            state_1 = 1
            target_1 = valX
        }
    }
    if (rx1 == "SX") {
        valX = Math.round(parseFloat(rx2.substr(0, 4)))
    } else if (rx1 == "SY") {
        speed = Math.round(parseFloat(rx2.substr(0, 4)))
    } else if (rx1 == "SZ") {
        valz = Math.round(parseFloat(rx2.substr(0, 4)))
    }
})
let rx2 = ""
let rx1 = ""
let edge_state_P2 = 0
let edge_state_P1 = 0
let speed = 0
let valz = 0
let valX = 0
let state_1 = 0
let total_1 = 0
let target_1 = 0
let count_1 = 0
let temp = 0
bluetooth.startUartService()
robotbit.MotorStopAll()
basic.showIcon(IconNames.House)
pins.setPull(DigitalPin.P1, PinPullMode.PullUp)
pins.setPull(DigitalPin.P2, PinPullMode.PullUp)
pins.setEvents(DigitalPin.P1, PinEventType.Edge)
pins.setEvents(DigitalPin.P2, PinEventType.Edge)
temp = 0
count_1 = 0
target_1 = 0
total_1 = 0
state_1 = 0
valX = 0
valz = 0
speed = 0
edge_state_P1 = 0
edge_state_P2 = 0
basic.showIcon(IconNames.Happy)
basic.forever(function () {
    if (total_1 < target_1) {
        robotbit.MotorRun(robotbit.Motors.M1B, speed * -1)
    } else if (total_1 > target_1) {
        robotbit.MotorRun(robotbit.Motors.M1B, speed)
    } else if (total_1 == target_1) {
        robotbit.MotorStop(robotbit.Motors.M1B)
    }
})
