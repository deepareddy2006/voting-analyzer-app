from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os
import io
import base64

app = Flask(__name__)

# Route for Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Route to process uploaded CSV
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        df = pd.read_csv(file)

        # Count votes per candidate
        vote_counts = df['candidate'].value_counts()

        # Plot bar chart
        plt.figure(figsize=(8,5))
        vote_counts.plot(kind='bar', color='skyblue')
        plt.title("Votes per Candidate")
        plt.xlabel("Candidate")
        plt.ylabel("Votes")

        # Save plot to string buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        bar_chart = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close()

        # Plot pie chart
        plt.figure(figsize=(6,6))
        vote_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
        plt.ylabel('')
        plt.title("Vote Percentage per Candidate")

        buf2 = io.BytesIO()
        plt.savefig(buf2, format='png')
        buf2.seek(0)
        pie_chart = base64.b64encode(buf2.getvalue()).decode('utf-8')
        plt.close()

        return render_template('results.html', bar_chart=bar_chart, pie_chart=pie_chart)

# Updated app.run for cloud deployment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)