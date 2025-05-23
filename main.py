import os
from flask import Flask

app = Flask('')

@app.route('/')
def home():
    return "Test OK!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"Running on port {port}")
    app.run(host="0.0.0.0", port=port)

