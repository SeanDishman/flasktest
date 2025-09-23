from flask import Flask, request, jsonify

app = Flask(__name__)

validated_hwids = {
    "483939": "steve",
    "192837": "alex",
    "123456": "john"
}

@app.route('/validate', methods=['POST'])
def validate():
    data = request.get_json()
    hwid = data.get('hwid')
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
