from cvzone.SerialModule import SerialObject

# Initialize the Arduino SerialObject with optional parameters
# baudRate = 9600, digits = 1, max_retries = 5
arduino = SerialObject(portNo=None, baudRate=9600, digits=1, max_retries=5)

# Initialize a counter to keep track of iterations
count = 0

# Start an infinite loop
while True:
    # Increment the counter on each iteration
    count += 1

    # Print data received from the Arduino
    # getData method returns the list of data received from the Arduino
    print(arduino.getData())

    # If the count is less than 100
    if count < 100:
        # Send a list containing [1] to the Arduino
        arduino.sendData([1])
    else:
        # If the count is 100 or greater, send a list containing [0] to the Arduino
        arduino.sendData([0])

    # Reset the count back to 0 once it reaches 200
    # This will make the cycle repeat
    if count == 200:
        count = 0