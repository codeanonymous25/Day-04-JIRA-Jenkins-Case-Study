from flask import Flask, request, jsonify, Response
import random

app = Flask(__name__)

@app.get("/")
def home():
    html_doc = """<!doctype html><html><head><meta charset="utf-8">
<title>Dice Game</title></head><body>
<h1>🎲 Simple Dice Game</h1>
<p>Try: <code>/roll?count=2&faces=6</code></p>
</body></html>"""
    return Response(html_doc, mimetype="text/html")

@app.get("/roll")
def roll():
    # Validate count and faces as integers
    try:
        count = int(request.args.get("count", 1))
        faces = int(request.args.get("faces", 6))
    except (TypeError, ValueError):
        return jsonify(error="count and faces must be integers"), 400

    # Validate ranges
    if not (1 <= count <= 20):
        return jsonify(error="count must be between 1 and 20"), 400
    if not (2 <= faces <= 20):
        return jsonify(error="faces must be between 2 and 20"), 400

    # Optional deterministic seeding without affecting global RNG state
    seed_param = request.args.get("seed")
    if seed_param is not None:
        try:
            seed_value = int(seed_param)
        except (TypeError, ValueError):
            return jsonify(error="seed must be an integer"), 400
        rng = random.Random(seed_value)
    else:
        rng = random

    # ✅ Correct off-by-one: use 1..faces inclusive
    rolls = [rng.randint(1, faces) for _ in range(count)]
    total = sum(rolls)

    return jsonify(count=count, faces=faces, rolls=rolls, total=total)


if __name__ == "__main__":
    # Bind to 0.0.0.0 to work in containers
    app.run(host="0.0.0.0", port=5000)
