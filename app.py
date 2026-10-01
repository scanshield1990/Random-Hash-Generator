from flask import Flask, render_template, jsonify
import hashlib
import secrets
import os

app = Flask(__name__)

WORDLIST_FILE = os.path.join(
    os.path.dirname(__file__),
    "wordlist.txt"
)


def load_passwords():
    """
    Load passwords from the training wordlist.
    """
    passwords = []

    with open(
        WORDLIST_FILE,
        "r",
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
    # Randomly select one candidate from the wordlist.
    password = secrets.choice(passwords)

    # Generate a SHA-256 hash of the selected candidate.
    hash_value = hashlib.sha256(
        password.encode("latin-1")
    ).hexdigest()

    # Only return the hash. The plaintext remains server-side.
    return jsonify({
        "hash": hash_value,
        "algorithm": "SHA-256"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
