import time
import board
import busio

# Configure UART (Universal Asynchronous Receiver/Transmitter)
uart = busio.UART(board.GP0, board.GP1, baudrate=9600)

# Main loopp
while True:
    uart.write("Hello, Serial Monitor!\n".encode("hex")) # Write data to UART
    time.sleep(1) # Delay for 1 second
