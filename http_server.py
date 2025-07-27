import http.server
import json
import socketserver

PORT = 8000

class EHBHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                "message": "🏥 EHB Healthcare API is running!",
                "status": "operational",
                "service": "EHB Healthcare System"
            }
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                "status": "healthy",
                "service": "EHB Healthcare API"
            }
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/api/patients':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            patients = [
                {"id": "P001", "name": "Ahmed Khan", "status": "active"},
                {"id": "P002", "name": "Fatima Ali", "status": "active"},
                {"id": "P003", "name": "Muhammad Hassan", "status": "critical"}
            ]
            self.wfile.write(json.dumps(patients).encode())
        elif self.path == '/api/doctors':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            doctors = [
                {"id": "D001", "name": "Dr. Sarah Ahmed", "specialization": "Cardiology"},
                {"id": "D002", "name": "Dr. Ali Hassan", "specialization": "Endocrinology"},
                {"id": "D003", "name": "Dr. Fatima Khan", "specialization": "Pediatrics"}
            ]
            self.wfile.write(json.dumps(doctors).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": "Not found"}
            self.wfile.write(json.dumps(response).encode())

if __name__ == "__main__":
    print(f"🏥 Starting EHB Healthcare HTTP Server on port {PORT}...")
    with socketserver.TCPServer(("", PORT), EHBHandler) as httpd:
        print(f"✅ Server running at http://localhost:{PORT}")
        httpd.serve_forever() 