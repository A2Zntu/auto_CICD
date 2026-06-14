from flask import Flask, render_template, request
from bs_model import call_price, put_price, greeks

app = Flask(__name__)

DEFAULTS = dict(S=100, K=100, T=1.0, r=0.05, sigma=0.20)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    params = DEFAULTS.copy()
    error = None

    if request.method == "POST":
        try:
            params = {
                "S":     float(request.form["S"]),
                "K":     float(request.form["K"]),
                "T":     float(request.form["T"]),
                "r":     float(request.form["r"]),
                "sigma": float(request.form["sigma"]),
            }
            result = {
                "call":   round(call_price(**params), 4),
                "put":    round(put_price(**params), 4),
                "greeks": {k: round(v, 6) for k, v in greeks(**params).items()},
            }
        except ValueError as e:
            error = str(e)

    return render_template("index.html", params=params, result=result, error=error)


@app.route("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}


if __name__ == "__main__":
    app.run(debug=True)
