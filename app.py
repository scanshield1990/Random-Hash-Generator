from flask import Flask, render_template, jsonify
import gzip
import hashlib
import secrets
import os

app = Flask(__name__)

ROCKYOU_FILE = os.path.join(
    os.path.dirname(__file__),
    "rockyou.txt.gz"
)


def load_passwords():
    """
    Load passwords from the compressed RockYou wordlist.
    latin-1 is used because RockYou contains bytes that may
    not decode correctly as UTF-8.
    """
    passwords = []

    with gzip.open(
        ROCKYOU_FILE,
        "rt",
        encoding="latin-1",
        errors="ignore"
    ) as file:
        for line in file:
            password = line.rstrip("\r\n")

            if password:
                passwords.append(password)

    return passwords


# Load the wordlist once when the application starts.
passwords = load_passwords()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate")
def generate_hash():
    # Select one password randomly from RockYou.
    password = secrets.choice(passwords)

    # Generate its SHA-256 hash.
    hash_value = hashlib.sha256(
        password.encode("latin-1")
    ).hexdigest()

    # Only the hash is returned to the browser.
    # The original password stays on the server.
    return jsonify({
        "hash": hash_value,
        "algorithm": "SHA-256"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
