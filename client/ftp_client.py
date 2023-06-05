#This code was modified and created by the following people:
#Austin Cash - cashau  -  932-538-892
#Nathaniel Thickett - thicketn  -  933969798
#Robert Lucas - Lucasrob  -  934293987

import os
import os.path
os.chdir("myfiles")




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


async def recv_intro_message(reader: asyncio.StreamReader):
    
    full_data = await reader.readline()
    return full_data.decode()
    

async def send_long_message(writer: asyncio.StreamWriter, data):
  
    await asyncio.sleep(1)

    writer.write(to_hex(len(data)).encode())
    writer.write(data.encode())

    await writer.drain()
    
    
async def send_command(writer: asyncio.StreamWriter, data):    

    writer.write(to_hex(len(data)).encode())
    writer.write(data.encode())

    await writer.drain()
    
    
async def put(reader, writer, filename):

    try:
        with open(filename, 'r') as file:
            file_data = file.read()
        file_data_length = len(file_data)
        
        writer.write(to_hex(file_data_length).encode())
        await writer.drain()

        await send_general(writer, file_data)

        await send_general(writer, "File {} sent successfully\n".format(filename))

    except FileNotFoundError:
        await send_general(writer, "File not found\n")    
    
def get_command_input():
    
    while(True):
        print("Command options are 1: list, 2: put, 3: get, 4: remove, 5: close\n")
        print("For commands involving file manipulation, please enter the command followed by a space, followed by the filename\n")
        command = input("Please enter a command to send to the server from those 5: ")
        command = command.split()

        if command[0] == "list":
            return "list"
        
        elif command[0] == "put":
            file = command[1]
            if os.path.exists("./" + file):
                print("correct")
                return (command[0] + " " + file)
            else:
                print("File entered is not valid. Please provide a valid filename.\n")

        elif command[0] == "get":
            return "get", command[1]
        
        elif command[0] == "remove":
            return(command[0] + " " + command[1])
        
        elif command[0] == "close":
            return "close"
        
        else:
            print("\nCommand entered is invalid. Please enter a valid command from the 5 listed.\n")
            


async def connect():
    reader, writer = await asyncio.open_connection(IP, DPORT)
    intro = ""
    
    while intro != "ACK Password entered successfully\n" and intro != "Close Server\n":

        intro = await recv_intro_message(reader)
    

        long_msg = input(intro)

        await send_long_message(writer, long_msg)
        
        intro = await recv_intro_message(reader)

        print(intro)
        
        
    while intro != "Close Server\n":
        
        intro = await recv_intro_message(reader)
        
        print(intro)
        
        command = get_command_input()

        if isinstance(command, tuple):
            command, fcontent = command
            await send_command(writer, command)
            await send_long_message(writer, fcontent)
        elif command:
            await send_command(writer, command)
        
        intro = await recv_intro_message(reader)
        print(intro)
        
        if intro == "ACK Received CLOSE command\n" or intro == "Close Server\n":
            print("closing")
            break

        if intro == "ACK Received GET command\n":
            fsize_hx = await reader.readexactly(8)
            file_size = int(fsize_hx, 16)
            await send_long_message(writer, "ACK\n")
            file_data = await reader.readexactly(file_size)
            with open(fcontent, 'wb') as f:
                f.write(file_data)
            response = await reader.readline()
            print(response.decode())
            
        if intro == "ACK Received PUT command\n":
            command = command.split()
            await put(reader, writer, command[1])

        
        
    
    writer.close()
    await writer.wait_closed()

    return

async def send_general(writer, message):
    writer.write(message.encode())
    await writer.drain()

async def put(reader, writer, filename):
    filename = "./" + filename
    
    print(filename)
    try:
        with open(filename, 'r') as file:
            file_data = file.read()
        file_data_length = len(file_data)
        
        writer.write(to_hex(file_data_length).encode())
        await writer.drain()

        await send_general(writer, file_data)


    except FileNotFoundError:
        print("file not found")


def inputNumber(message):
  while True:
    try:
       userInput = int(input(message))       
    except ValueError:
       print("Not an integer! Try again.")
       continue
    else:
       return userInput 

   

async def main():
    tasks = []
    
    tasks.append(connect())
    await asyncio.gather(*tasks)
    print("done")



# Run the `main()` function
if __name__ == "__main__":
    asyncio.run(main())
