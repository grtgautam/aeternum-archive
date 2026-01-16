# AETERNUM ARCHIVE 🚀⏳
### *Secure Your Legacy Across Time*

![Desktop UI](desktop_ui.png)

> "I knew there are other tools in the market, but I wanted to build one for me. Not feeling to sleep in night, so just started vibe coded."

**Aeternum Archive** (formerly Chronos) is a time capsule application that lets you record video, audio, or text messages for your future self. It encrypts your memories using military-grade protocols and ensures they remain locked until a date you choose.

---

## 🌌 Features

- **Standard Encryption**: Uses **Fernet (AES-128)** to lock your files.
- **Privacy First**: The server does NOT store your video/audio files. You download the encrypted "Capsule" (.enc) immediately. The server only keeps the key.
- **Space Theme UI**: Immersive dark mode design with rotating 3D planets (Mars & Earth).
- **Responsive**: "Vibe coded" to look amazing on both Laptops and Mobile phones.

### 📱 Mobile Experience
![Mobile UI](mobile_ui.png)

---

## 🔓 How to Decrypt Your Capsule

When the future arrives, the application retrieves your key from its **secure internal database** (`capsules.db`).

1.  **Launch the App**: Ensure the server is running.
2.  **Visit Decrypt Page**: Click **"DECRYPT EXISTING CAPSULE"**.
3.  **Upload**: Select your encrypted `.enc` file.
4.  **Authenticate**: Enter your **Email** and **Capsule ID**.
    *   *Note: The decryption key is fetched automatically from the database matching your credentials.*
5.  **Unlock**: Click **"Decrypt & Restore"**.
    *   If the Release Date has passed, your memory will be revealed! 🎥

---

## 🤓 For the Nerds: How it Works

1.  **Browser Recording**: We use the `MediaStream Recording API` to capture your webcam/microphone directly in the browser.
2.  **Encryption**: 
    *   We use the **Fernet** implementation from the `cryptography` Python library.
    *   **Algorithm**: AES in CBC mode with a 128-bit key for encryption; HMAC using SHA256 for authentication.
    *   **Why?** This ensures that even if someone gets your file, they cannot open it without the key. It also prevents tampering—if a single bit is changed in the file, it will fail to decrypt.
3.  **Key Storage**: Your specific decryption key is generated on the server and stored in a local SQLite database (`capsules.db`) alongside your chosen release date.
4.  **Zero-Knowledge Storage**: The heavy video file never stays on our server. It is encrypted in RAM and streamed back to you instantly.

---

## 🛠️ Run Locally

Want to run this on your own computer? It's designed to be plug-and-play.

### Prerequisites
- Python 3.7+
- A webcam/microphone (for recording)

### Setup

1.  **Clone the Repo**
    ```bash
    git clone https://github.com/YOUR_USERNAME/aeternum-archive.git
    cd aeternum-archive
    ```

2.  **Install Dependencies**
    ```bash
    pip install flask cryptography
    ```

3.  **Run the App**
    ```bash
    python app.py
    ```

4.  **Launch**
    Open your browser and explore the cosmos at:
    `http://127.0.0.1:5000`

---

*Built with Python, Flask, and Stardust.*

