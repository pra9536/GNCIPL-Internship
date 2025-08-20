import os
import json
from flask import Flask, request, jsonify, render_template, send_file
from scraper import scrape_reviews

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/scrape", methods=["POST"])
def api_scrape():
    data = request.get_json(force=True)
    product_url = data.get("product_url", "").strip()
    cookie = data.get("cookie", "").strip()
    use_proxy = data.get("use_proxy", False)
    proxy_username = data.get("proxy_username", "").strip()
    proxy_password = data.get("proxy_password", "").strip()
    pages = int(data.get("pages", 5))

    if not product_url:
        return jsonify({"ok": False, "error": "Product URL is required"}), 400

    try:
        df = scrape_reviews(
            product_url=product_url,
            cookie=cookie,
            pages=pages,
            use_proxy=use_proxy,
            proxy_username=proxy_username,
            proxy_password=proxy_password
        )
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

    # Save CSV for download
    csv_path = os.path.join(os.getcwd(), "flipkart_reviews.csv")
    df.to_csv(csv_path, index=False)

    # return small preview (first 100 rows) to the UI
    preview = df.head(100).to_dict(orient="records")
    return jsonify({"ok": True, "count": int(len(df)), "preview": preview})

@app.route("/download")
def download():
    csv_path = os.path.join(os.getcwd(), "flipkart_reviews.csv")
    if not os.path.exists(csv_path):
        return jsonify({"ok": False, "error": "No CSV found. Please run a scrape first."}), 404
    return send_file(csv_path, as_attachment=True, download_name="flipkart_reviews.csv")

if __name__ == "__main__":
    # For local dev. In production, use a proper WSGI server.
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
