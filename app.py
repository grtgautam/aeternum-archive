import os
import io
from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for
from encryption import generate_key, encrypt_data, decrypt_data
from database import init_db, store_capsule_key, get_key_by_email_and_id, DB_NAME
from datetime import datetime

app = Flask(__name__)

# Initialize DB on startup
if not os.path.exists(DB_NAME):
    init_db()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt_route():
    try:
        email = request.form.get('email')
        release_date = request.form.get('release_date')
        file = request.files.get('file')
        text_message = request.form.get('text_message')
        
        if not email or not release_date:
            return jsonify({'error': 'Email and Release Date are required'}), 400

        data_to_encrypt = b""
        filename = "capsule.enc"

        if file:
            data_to_encrypt = file.read()
            # Basic validation (100MB server-side limit for safety, though we want 10 min video)
            if len(data_to_encrypt) > 100 * 1024 * 1024:
                return jsonify({'error': 'File too large. Please keep it under 100MB.'}), 400
            filename = f"video_capsule_{datetime.now().strftime('%Y%m%d')}.enc"
        elif text_message:
            data_to_encrypt = text_message.encode('utf-8')
            filename = f"text_capsule_{datetime.now().strftime('%Y%m%d')}.enc"
        else:
            return jsonify({'error': 'No content provided'}), 400

        # Generate Key
        key = generate_key()
        
        # Encrypt
        encrypted_data = encrypt_data(data_to_encrypt, key)
        
        # Store metadata and key
        capsule_id = store_capsule_key(email, release_date, key)
        
        # Return encrypted file to user with a custom header containing the ID (or just let them know via UI)
        # Since we are doing a form post, we might want to return the file as a download.
        # But we also need to tell the user their Capsule ID.
        # Strategy: Return the file. The filename can contain the ID? Or we assume email is enough.
        # Let's attach the ID to the filename for easy reference: capsule_ID_123.enc
        
        download_name = f"FUTURE_CAPSULE_ID_{capsule_id}.enc"
        
        return send_file(
            io.BytesIO(encrypted_data),
            as_attachment=True,
            download_name=download_name,
            mimetype='application/octet-stream'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt_route():
    error = None
    decrypted_content = None
    is_text = False

    if request.method == 'POST':
        email = request.form.get('email')
        capsule_id = request.form.get('capsule_id')
        uploaded_file = request.files.get('file')
        manual_key = request.form.get('manual_key') # In case they have the key directly
        
        if not uploaded_file:
            error = "Please upload your .enc capsule file."
        
        else:
            encrypted_bytes = uploaded_file.read()
            key_bytes = None
            
            # Scenario A: User provides ID/Email, we fetch key from DB
            if capsule_id and email:
                record = get_key_by_email_and_id(email, capsule_id)
                if record:
                    stored_key, release_date_str = record
                    
                    # Check Date
                    release_date = datetime.strptime(release_date_str, '%Y-%m-%d')
                    if datetime.now() < release_date:
                        error = f"This capsule is locked until {release_date_str}. Please wait!"
                    else:
                        key_bytes = stored_key.encode('utf-8')
                else:
                    error = "Capsule record not found for this Email/ID."

            # Scenario B: User provides manual key (backup)
            elif manual_key:
                key_bytes = manual_key.encode('utf-8')
            
            if key_bytes and not error:
                try:
                    decrypted_data = decrypt_data(encrypted_bytes, key_bytes)
                    # Detect if it's text or binary (simple heuristic)
                    try:
                        decrypted_content = decrypted_data.decode('utf-8')
                        is_text = True
                    except UnicodeDecodeError:
                        # It's a file (video/audio). We should send it back for download/playback.
                        # For simplicity in this route, if it's binary, we send file.
                        return send_file(
                            io.BytesIO(decrypted_data),
                            mimetype="video/webm", # Default to webm for recorded video, could be generic
                            as_attachment=False, # Try to play in browser
                            download_name="restored_memory.webm"
                        )
                except Exception as e:
                    error = f"Decryption failed: {str(e)}"
            elif not error:
                 error = "Missing credentials (Email+ID) or Key."

    return render_template('decrypt.html', error=error, content=decrypted_content, is_text=is_text)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
