#This code was modified and created by the following people:
#Austin Cash - cashau  -  932-538-892
#Nathaniel Thickett - thicketn  -  933969798
#Robert Lucas - Lucasrob  -  934293987

import os
os.chdir("myfiles")


import socket
import asyncio

INTERFACE, SPORT = 'localhost', 8080
CHUNK = 100


async def send_long_message(writer: asyncio.StreamWriter, data):
    writer.write(to_hex(len(data)).encode())
    writer.write(data.encode())

    await writer.drain()



def to_hex(number):
    assert number <= 0xffffffff, "Number too large"
    return "{:08x}".format(number)



async def send_intro_message(writer):
    intro_message = "Welcome to the ftp server! Please enter the password for the server: \n"

    writer.write(intro_message.encode())
    await writer.drain()
    
async def send_pw_confirmation(writer):
    intro_message = "ACK Password entered successfully\n"

    writer.write(intro_message.encode())
    await writer.drain()
    
async def send_pw_declination(writer):
    intro_message = "NAK Password entered incorrect\n"

    writer.write(intro_message.encode())
    await writer.drain()
    
async def send_closure(writer):
    intro_message = "Close Server\n"

    writer.write(intro_message.encode())
    await writer.drain()
    
    
async def send_general(writer, message):
    writer.write(message.encode())
    await writer.drain()


async def receive_long_message(reader: asyncio.StreamReader):
    # First we receive the length of the message: this should be 8 total hexadecimal digits!
    # Note: `socket.MSG_WAITALL` is just to make sure the data is received in this case.
    data_length_hex = await reader.readexactly(8)

    # Then we convert it from hex to integer format that we can work with
    data_length = int(data_length_hex, 16)

   
    full_data = await reader.readexactly(data_length)
    return full_data.decode()


async def receive_command(reader: asyncio.StreamReader):
    # First we receive the length of the message: this should be 8 total hexadecimal digits!
    # Note: `socket.MSG_WAITALL` is just to make sure the data is received in this case.
    data_length_hex = await reader.readexactly(8)

    # Then we convert it from hex to integer format that we can work with
    data_length = int(data_length_hex, 16)

   
    full_data = await reader.readexactly(data_length)
    return full_data.decode()



async def get(reader, writer, filename):

    await send_general(writer, "ACK Received GET command\n")

    try:
        with open(filename, 'r') as file:
            file_data = file.read()
        file_data_length = len(file_data)
        
        writer.write(to_hex(file_data_length).encode())
        await writer.drain()

        await receive_long_message(reader)

        await send_general(writer, file_data)

        await send_general(writer, "File {} sent successfully\n".format(filename))

    except FileNotFoundError:
        await send_general(writer, "File not found\n")




async def handle_commands(reader, writer):
    
    while(True):
        
        await send_general(writer, "Please enter a command: \n")
        command = await receive_command(reader)
        command = command.split()


        if command[0] == "list":
            await list_files(writer)

        elif command[0] == "put":
            await send_general(writer, "ACK Received PUT command\n")
            fname = command[1]
            fcontent = await receive_long_message(reader)
            with open(fname, 'w') as file:
                file.write(fcontent)

        elif command[0] == "get":
            fname = await receive_command(reader)
            await get(reader, writer, fname)

                

        elif command[0] == "remove":
            if len(command) > 1:
                await remove_file(writer, command[1])
            else:
                await send_general(writer, "NAK No file specified\n")
  
        elif command[0] == "close":
            await send_general(writer, "ACK Received CLOSE command\n")
            return
    
        else:
            await send_general(writer, "NAK Entered Command is not valid\n")

    
    return   

    
   

async def handle_client(reader, writer):
    """
    Part 1: Introduction
    """
    for i in range(3):
        flag = False
        
        
        await send_intro_message(writer)

        message = await receive_long_message(reader)
            
        if message == "password12":
            await send_pw_confirmation(writer)
            flag = True
        elif i == 2:
            await send_closure(writer)
            break
        else:
            await send_pw_declination(writer)
            

        # I'm only printing the last 8 characters of the message here because it's long
        if flag == True:
            print("done: password entered successfully")
            
            await handle_commands(reader, writer)
            break


    writer.close()
    await writer.wait_closed()
    


async def main():

    server = await asyncio.start_server(
            handle_client,
            INTERFACE, SPORT
    )

    async with server:
        await server.serve_forever()



async def list_files(writer):
    files = os.listdir('.')
    files_list = ', '.join(files)
    await send_general(writer, f"ACK Files: {files_list}\n")

async def remove_file(writer, filename):
    if os.path.exists(filename):
        os.remove(filename)
        await send_general(writer, f"ACK File {filename} removed successfully\n")
    else:
        await send_general(writer, "NAK File doesn't exist\n")




# Run the `main()` function
if __name__ == "__main__":
    asyncio.run(main())
