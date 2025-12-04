#!/usr/bin/env python3
import os
import sys
import time
import socket

def wait_for_db(max_retries=30, delay=2):
    db_host = os.environ.get('DB_HOST', 'db')
    db_port = int(os.environ.get('DB_PORT', '5432'))
    db_name = os.environ.get('DB_NAME', 'postgres')
    db_user = os.environ.get('DB_USER', 'postgres')

    print(f"⏳ Attendo che PostgreSQL sia pronto su {db_host}:{db_port}...")
    print(f"   Database: {db_name}, User: {db_user}")

    for attempt in range(1, max_retries + 1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((db_host, db_port))
            sock.close()
            
            if result == 0:
                print(f"✅ PostgreSQL è pronto! (tentativo {attempt}/{max_retries})")
                time.sleep(2)  # sicurezza
                return True
            else:
                raise ConnectionRefusedError("Porta non aperta")
        except (socket.gaierror, socket.error, ConnectionRefusedError):
            print(f"⏳ Tentativo {attempt}/{max_retries}: PostgreSQL non ancora pronto...")
            if attempt < max_retries:
                time.sleep(delay)
            else:
                print(f"❌ Impossibile connettersi a PostgreSQL dopo {max_retries} tentativi")
                sys.exit(1)

if __name__ == "__main__":
    wait_for_db()
    print("✅ Avvio dell’applicazione Django…")
    sys.exit(0)