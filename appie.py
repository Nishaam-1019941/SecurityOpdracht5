from flask import Flask, render_template, request
from Crypto.Cipher import AES
import base64

app = Flask(__name__)

def encrypt(message, key):
    key = key[:16].encode('utf-8')  #16 bytes sleutel
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce  # Random gegenereerde waarde
    ciphertext, tag = cipher.encrypt_and_digest(message.encode('utf-8'))
    
    return base64.b64encode(nonce + ciphertext).decode('utf-8')

def decrypt(ciphertext, key):
    key = key[:16].encode('utf-8')
    
    encrypted_data = base64.b64decode(ciphertext.encode('utf-8'))
    
    nonce = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt(ciphertext).decode('utf-8')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt_message():
    message = request.form['message']
    key = request.form['key']
    encrypted_message = encrypt(message, key)
    return render_template('index.html', encrypted_message=encrypted_message)

@app.route('/decrypt', methods=['POST'])
def decrypt_message():
    encrypted_message = request.form['encrypted_message']
    key = request.form['key']
    try:
        decrypted_message = decrypt(encrypted_message, key)
        return render_template('index.html', decrypted_message=decrypted_message)
    except Exception as e:
        return render_template('index.html', error="Ontsleuteling mislukt. Controleer de sleutel of het versleutelde bericht.")

if __name__ == '__main__':
    app.run(debug=True)
