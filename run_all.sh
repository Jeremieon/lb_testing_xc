#!/bin/bash

echo "Starting all F5XC test apps..."
echo "================================"

# Start apps in background
echo "Starting Redirect App on port 8001..."
uvicorn app_redirect:app --host 0.0.0.0 --port 8001 &

echo "Starting CRUD App on port 8002..."
uvicorn app_crud:app --host 0.0.0.0 --port 8002 &

echo "Starting Routing App on port 8003..."
uvicorn app_routes:app --host 0.0.0.0 --port 8003 &

echo "Starting TLS App on port 8443..."
uvicorn app_tls:app --host 0.0.0.0 --port 8443 --ssl-keyfile=./certs/key.pem --ssl-certfile=./certs/cert.pem &

sleep 3

echo ""
echo "================================"
echo "All apps started!"
echo "================================"
echo "Redirect App:  http://localhost:8001"
echo "CRUD App:      http://localhost:8002"
echo "Routing App:   http://localhost:8003"
echo "TLS App:       https://localhost:8443"
echo ""
echo "Press Ctrl+C to stop all apps"
echo ""

# Wait for any process to exit
wait

# Kill all background jobs on exit
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT
