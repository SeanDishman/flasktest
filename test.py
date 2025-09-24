from flask import Flask, request, jsonify
import time

app = Flask(__name__)

validated_hwids = {
    "483939": "steve",
    "192837": "alex",
    "123456": "john",
    "ea44c4c76ce8cc1f62e2a7760aa1c769b80f364b9828fce3386502b42caedc9a2f37cda48d36ef8bcd7b6cf6e16e7180153711454dcd676f3c7f0710ec2582f6": "Hwid Client"
}

rate_limits = {}

def get_client_ip():
    if request.headers.get("X-Forwarded-For"):
        ip = request.headers.get("X-Forwarded-For").split(',')[0].strip()
    else:
        ip = request.remote_addr or "Unknown"
    return ip

def is_rate_limited(ip):
    now = time.time()
    if ip not in rate_limits:
        rate_limits[ip] = []
    rate_limits[ip] = [t for t in rate_limits[ip] if now - t < 10]
    if len(rate_limits[ip]) >= 2:
        return True
    rate_limits[ip].append(now)
    return False

@app.route('/validate', methods=['POST', 'GET', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def validate():
    ip = get_client_ip()
    method = request.method
    print(f"[Info] Received {method} from {ip}")
    if is_rate_limited(ip):
        return "rate limited", 429
    if method != 'POST':
        return "Im sorry we only take POST here :(", 200
    data = request.get_json()
    hwid = data.get('hwid') if data else None
    if hwid in validated_hwids:
        return jsonify({
            "status": "authenticated",
            "username": validated_hwids[hwid]
        }), 200
    return jsonify({"status": "unauthorized"}), 401

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
