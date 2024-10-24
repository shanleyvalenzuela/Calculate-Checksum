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
    return checksum == received_packet[-1], total_sum, wrapped_sum

def sender():
    host = "localhost"
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        # Packet to send
        sent_packet = [7, 11, 12, 0, 6, 0]
        # data = "PKA_NSCOM03" # uncomment for Example 2
        # sent_packet = [ord(char) for char in data] # uncomment for Example 2
        bit_size = 4
        packet_with_checksum = create_sender_table(sent_packet, bit_size)
        
        serialized_packet = pickle.dumps(packet_with_checksum)
        s.sendall(serialized_packet)
        # print(f"Sent String: {data}") # uncomment for Example 2
        print(f"Sent Packet: {packet_with_checksum}")
        print(f"Sent Checksum: {packet_with_checksum[len(packet_with_checksum)-1]}")

def main():
        sender()

if __name__ == "__main__":
    main()
