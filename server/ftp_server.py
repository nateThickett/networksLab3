import os
os.chdir("myfiles")

#This code was modified by the following people:
#Austin Cash - cashau
#Nathaniel Thickett - thicketn
#Robert Lucas - Lucasrob


import socket
import asyncio

INTERFACE, SPORT = 'localhost', 8080
CHUNK = 100


##################################
# TODO: Implement me for Part 1! #
##################################
async def send_intro_message(writer):
    # TODO: Replace {ONID} with your ONID (mine is lyakhovs)
    #       and {MAJOR} with your major (i.e. CS, ECE, any others?)
    intro_message = "Please enter the password for the server: \n"

    # TODO: Send this intro message to the client. Don't forget to encode() it!
    #       hint: use the `conn` handle and `sendall`!
    writer.write(intro_message.encode())
    await writer.drain()
    
async def send_pw_confirmation(writer):
    # TODO: Replace {ONID} with your ONID (mine is lyakhovs)
    #       and {MAJOR} with your major (i.e. CS, ECE, any others?)
    intro_message = "ACK Password entered successfully\n"

    # TODO: Send this intro message to the client. Don't forget to encode() it!
    #       hint: use the `conn` handle and `sendall`!
    writer.write(intro_message.encode())
    await writer.drain()
    
async def send_pw_declination(writer):
    # TODO: Replace {ONID} with your ONID (mine is lyakhovs)
    #       and {MAJOR} with your major (i.e. CS, ECE, any others?)
    intro_message = "NAK Password entered incorrect\n"

    # TODO: Send this intro message to the client. Don't forget to encode() it!
    #       hint: use the `conn` handle and `sendall`!
    writer.write(intro_message.encode())
    await writer.drain()
    
async def send_closure(writer):
    # TODO: Replace {ONID} with your ONID (mine is lyakhovs)
    #       and {MAJOR} with your major (i.e. CS, ECE, any others?)
    intro_message = "Close Server\n"

    # TODO: Send this intro message to the client. Don't forget to encode() it!
    #       hint: use the `conn` handle and `sendall`!
    writer.write(intro_message.encode())
    await writer.drain()
    
    
async def send_general(writer, message):
    # TODO: Replace {ONID} with your ONID (mine is lyakhovs)
    #       and {MAJOR} with your major (i.e. CS, ECE, any others?)
    

    # TODO: Send this intro message to the client. Don't forget to encode() it!
    #       hint: use the `conn` handle and `sendall`!
    writer.write(message.encode())
    await writer.drain()


##################################
# TODO: Implement me for Part 2! #
##################################
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

async def handle_commands(reader, writer):
    
    
    
    
    while(True):
        
        await send_general(writer, "Please enter a command: \n")
        command = await receive_command(reader)
        
        command = command.split()
        if command[0] == "list":
            await send_general(writer, "ACK Received LIST command\n")
        elif command[0] == "put":
            await send_general(writer, "ACK Received PUT command\n")
        elif command[0] == "get":
            await send_general(writer, "ACK Received GET command\n")
        elif command[0] == "remove":
            await send_general(writer, "ACK Received REMOVE command\n")
        elif command[0] == "close":
            await send_general(writer, "ACK Received CLOSE command\n")
            return 0
        else:
            await send_general(writer, "NAK Entered Command is not valid\n")
            
    
    return 0
    
    
    
   

async def handle_client(reader, writer):
    """
    Part 1: Introduction
    """
    # TODO: send the introduction message by implementing `send_intro_message` above.
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

# Run the `main()` function
if __name__ == "__main__":
    asyncio.run(main())
