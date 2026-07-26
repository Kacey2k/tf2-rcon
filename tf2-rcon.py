import socket
import struct


TF2_ADDRESS = "127.0.0.1"
TF2_PORT = 27015
RCON_PASSWORD = "choose_your_own_password"

SERVERDATA_RESPONSE_VALUE = 0
SERVERDATA_EXECCOMMAND = 2
SERVERDATA_AUTH = 3
REQUEST_ID = 1


def receive_exact(sock, length):
    """Receive an exact number of bytes from the connection."""
    data = b""

    while len(data) < length:
        chunk = sock.recv(length - len(data))

        if not chunk:
            raise ConnectionError("TF2 closed the connection.")

        data += chunk

    return data


def create_packet(request_id, packet_type, body):
    """Create a Source RCON packet."""
    payload = struct.pack("<ii", request_id, packet_type)
    payload += body.encode("utf-8")
    payload += b"\x00\x00"

    return struct.pack("<i", len(payload)) + payload


def receive_packet(sock):
    """Receive and decode one Source RCON packet."""
    size_data = receive_exact(sock, 4)
    packet_size = struct.unpack("<i", size_data)[0]

    if packet_size < 10 or packet_size > 4096:
        raise ValueError(f"Invalid RCON packet size: {packet_size}")

    packet = receive_exact(sock, packet_size)
    request_id, packet_type = struct.unpack("<ii", packet[:8])

    if packet[-2:] != b"\x00\x00":
        raise ValueError("Invalid RCON packet ending.")

    body = packet[8:-2].decode("utf-8", errors="replace")
    return request_id, packet_type, body


def authenticate(sock):
    """Authenticate with TF2 using the configured password."""
    packet = create_packet(REQUEST_ID, SERVERDATA_AUTH, RCON_PASSWORD)
    sock.sendall(packet)

    while True:
        request_id, packet_type, _ = receive_packet(sock)

        if request_id == -1:
            raise PermissionError("TF2 rejected the RCON password.")

        if packet_type == SERVERDATA_EXECCOMMAND:
            return


def send_command(sock, command):
    """Send a console command and return TF2's response."""
    packet = create_packet(REQUEST_ID, SERVERDATA_EXECCOMMAND, command)
    sock.sendall(packet)

    request_id, packet_type, response = receive_packet(sock)

    if request_id != REQUEST_ID:
        raise ConnectionError("Received an unexpected RCON response.")

    if packet_type != SERVERDATA_RESPONSE_VALUE:
        raise ConnectionError("Received an unexpected RCON packet type.")

    return response


def main():
    try:
        with socket.create_connection(
            (TF2_ADDRESS, TF2_PORT),
            timeout=5
        ) as sock:
            authenticate(sock)
            print("Connected to Team Fortress 2!")
            print("Type a console command, or type exit to disconnect.\n")

            while True:
                command = input("TF2 > ").strip()

                if not command:
                    continue

                if command.lower() == "exit":
                    print("Disconnected.")
                    break

                response = send_command(sock, command)

                if response:
                    print(response)

    except PermissionError as error:
        print(f"Authentication failed: {error}")

    except (ConnectionError, OSError, ValueError) as error:
        print(f"Connection failed: {error}")


if __name__ == "__main__":
    main()
