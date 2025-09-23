from flask import Flask, request, jsonify

app = Flask(__name__)

validated_hwids = {
    "483939": "steve",
    "192837": "alex",
    "123456": "john",
    "40072e03db9e001159ba6f7fecdc48a469b0754af9d081cf8052073cca94a6a304e1eaebbae0d494cb40e3836dbe94f302add8da76f425d33af8ea7f45d1a91c": "Hwid Client"
}

def get_client_ip():
    if request.headers.get("X-Forwarded-For"):
        ip = request.headers.get("X-Forwarded-For").split(',')[0].strip()
    else:
        ip = request.remote_addr or "Unknown"
    return ip

@app.route('/validate', methods=['POST', 'GET', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def validate():
    ip = get_client_ip()
    method = request.method
    print(f"[Info] Received {method} from {ip}")
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
