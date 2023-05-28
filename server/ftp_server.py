import os
os.chdir(‘myfiles’)

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
    intro_message = "Hello! Welcome to our (thicketn - CS, cashau - CS, Lucasrob - ECE) server!\n"

    # TODO: Send this intro message to the client. Don't forget to encode() it!
    #       hint: use the `conn` handle and `sendall`!
    writer.write(intro_message.encode())
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
    
   

async def handle_client(reader, writer):
    """
    Part 1: Introduction
    """
    # TODO: send the introduction message by implementing `send_intro_message` above.
    await send_intro_message(writer)

    """
    Part 2: Long Message Exchange Protocol
    """
    # TODO: Implement function above
    message = await receive_long_message(reader)

    # I'm only printing the last 8 characters of the message here because it's long
    print("done: " +  message[-11:])

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
