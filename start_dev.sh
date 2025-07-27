#!/bin/bash
echo "Starting EHB AI Dev Environment..."
echo

echo "Starting Backend Server..."
cd backend
npm run dev &
BACKEND_PID=$!

echo "Starting Frontend Server..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo
echo "EHB AI Dev Environment is starting..."
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:3000"
echo
echo "Press Ctrl+C to stop all servers"
echo

# Wait for user to stop
wait
