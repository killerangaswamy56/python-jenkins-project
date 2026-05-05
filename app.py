from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    print("Hello this is my Jenkins CICD pipeline with webhook trigger")
    print("V3 webhook")
    return "Hello, Jenkins! CI/CD is working."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
