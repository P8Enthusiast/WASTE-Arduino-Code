import socket

def is_connected(timeout=3):
    # Connect to Google DNS
    try:
        # Connect to the host -- tells us if the host is actually reachable
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
        return True
    except socket.error as ex:
        # Catches connection errors (e.g., no internet, timeout)
        print(f"Connection check failed: {ex}")
        return False
