import socket, subprocess, sys
from pathlib import Path

def free_port(start=8501,end=8599):
    for p in range(start,end+1):
        with socket.socket() as s:
            if s.connect_ex(('127.0.0.1',p)) != 0:
                return p
    raise RuntimeError('No free port available in 8501-8599')

if __name__=='__main__':
    root=Path(__file__).resolve().parent
    port=free_port()
    print(f'Starting WaterTankCare on http://localhost:{port}')
    raise SystemExit(subprocess.call([sys.executable,'-m','streamlit','run',str(root/'app.py'),'--server.port',str(port)],cwd=root))
