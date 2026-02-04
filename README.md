# Video-streaming-and-HTTP-partial-requests-
A video streaming project using the DASH approach, developed in a Linux environment (WSL) and containerized with Docker.

python3 -m RangeHTTPServer 9999 - Iniciate the server
python3 player.py - Iniciate the player
python3 proxy.py http://localhost:9999/ <videoName> - Iniciate the proxy
