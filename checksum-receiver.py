import socket
import pickle
import pandas as pd

def ones_complement(decimal_value, bit_size):
    max_value = (2**bit_size) - 1
    return max_value - decimal_value

def handle_wrapping(sum_value, bit_size):
    carry = sum_value >> bit_size
    wrapped_sum = sum_value & ((1 << bit_size) - 1)
    wrapped_sum += carry
    if wrapped_sum >= (1 << bit_size):
        wrapped_sum = handle_wrapping(wrapped_sum, bit_size)
    return wrapped_sum

def calculate_checksum(data, bit_size):
    total_sum = sum(data)
    wrapped_sum = handle_wrapping(total_sum, bit_size)
    checksum = ones_complement(wrapped_sum, bit_size)
    return total_sum, wrapped_sum, checksum

def create_sender_table(sent_packet, bit_size):
    total_sum, wrapped_sum, checksum = calculate_checksum(sent_packet, bit_size)
    received_packet = sent_packet + [checksum]
    return received_packet

def verify_received_packet(received_packet, bit_size):
    total_sum, wrapped_sum, checksum = calculate_checksum(received_packet[:-1], bit_size)
    return checksum == received_packet[-1], total_sum, wrapped_sum, checksum

def receiver():
    host = "localhost"
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        print("Waiting for connection...")

        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            
            data = conn.recv(1024)
            if data:
                received_packet = pickle.loads(data)
                received_data = received_packet[:-1]  # Exclude the last element (checksum)
                received_string = ''.join([chr(i) for i in received_data])
                print(f"Received Packet: {received_packet}")
                # print(f"Received String: {received_string}") #uncomment for Example 2

                # Verify checksum
                bit_size = 4
                total_sum, wrapped_sum, checksum = calculate_checksum(received_packet, bit_size)
                
                print(f"Recalculated checksum: {checksum}")
                if (checksum == 0):
                    print("Checksum verified, data is intact.")
                else:
                    print("Checksum mismatch, data is corrupted.")

def main():
        receiver()

if __name__ == "__main__":
    main()
