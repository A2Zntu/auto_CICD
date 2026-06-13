from flask import Flask, render_template, jsonify

app = Flask(__name__)

ITEMS = ["Apple", "Banana", "Cherry"]


@app.route("/")
def index():
    return render_template("index.html", items=ITEMS)


@app.route("/health")
def health():
    return jsonify({"status": "ok", "version": "1.0.0"})


@app.route("/items")
def items():
    return jsonify({"items": ITEMS})


if __name__ == "__main__":
    app.run(debug=True)
