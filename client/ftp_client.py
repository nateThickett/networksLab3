import os
os.chdir(‘myfiles’)

#This code was modified by the following people:
#Austin Cash - cashau
#Nathaniel Thickett - thicketn
#Robert Lucas - Lucasrob


import socket
from time import sleep
from threading import Thread
import asyncio

IP, DPORT = 'localhost', 8080

# Helper function that converts an integer into a string of 8 hexadecimal digits
# Assumption: integer fits in 8 hexadecimal digits
def to_hex(number):
    # Verify our assumption: error is printed and program exists if assumption is violated
    assert number <= 0xffffffff, "Number too large"
    return "{:08x}".format(number)

##################################
# TODO: Implement me for Part 1! #
##################################
async def recv_intro_message(reader: asyncio.StreamReader):
    
    full_data = await reader.readline()
    return full_data.decode()
    


##################################
# TODO: Implement me for Part 2! #
##################################
async def send_long_message(writer: asyncio.StreamWriter, data):
    # TODO: Send the length of the message: this should be 8 total hexadecimal digits
    #       This means that ffffffff hex -> 4294967295 dec
    #       is the maximum message length that we can send with this method!
    #       hint: you may use the helper function `to_hex`. Don't forget to encode before sending!

    # Add a delay to simulate network latency
    await asyncio.sleep(1)

    writer.write(to_hex(len(data)).encode())
    writer.write(data.encode())

    await writer.drain()


async def connect(i):
    reader, writer = await asyncio.open_connection(IP, DPORT)

    intro = await recv_intro_message(reader)
    print(intro)

    long_msg = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX" * 100 + f"  CLIENT: " + str(i)

    await send_long_message(writer, long_msg)

    print("Done sending", i)


    return 0


def inputNumber(message):
  while True:
    try:
       userInput = int(input(message))       
    except ValueError:
       print("Not an integer! Try again.")
       continue
    else:
       return userInput 
       break
   

async def main():
    tasks = []
    
    x = inputNumber("Enter number of connections to open: ")
    
    for i in range(x):
        tasks.append(connect(i))

    await asyncio.gather(*tasks)
    print("done")

# Run the `main()` function
if __name__ == "__main__":
    asyncio.run(main())

