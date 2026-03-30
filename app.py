from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        try:
            df = pd.read_csv(file)
            if 'Candidate' not in df.columns or 'Votes' not in df.columns:
                return "Invalid CSV format. Required columns: Candidate and Votes."
            
            top_idx = df['Votes'].idxmax()
            top_candidate = df.loc[top_idx]

            # Pie Chart
            fig = px.pie(df, names='Candidate', values='Votes', title='Vote Distribution',
                         color_discrete_sequence=px.colors.qualitative.Pastel, hole=0.3)
            fig.update_traces(pull=[0.1 if i==top_idx else 0 for i in range(len(df))],
                              textinfo='label+percent')
            chart_html = pio.to_html(fig, full_html=False)

            # Animated Gradient Bar Chart
            bar_colors = px.colors.sequential.Viridis
            bar_fig = go.Figure()
            for i, candidate in enumerate(df['Candidate']):
                bar_fig.add_trace(go.Bar(
                    x=[candidate],
                    y=[df.loc[i, 'Votes']],
                    marker=dict(color=bar_colors[i % len(bar_colors)], line=dict(color='black', width=1)),
                    hoverinfo='y+name'
                ))
            bar_fig.update_layout(title="Votes by Candidate", xaxis_title="Candidate", yaxis_title="Votes",
                                  template="plotly_dark", showlegend=False)
            bar_fig.update_traces(marker_line_width=1.5)
            bar_chart_html = pio.to_html(bar_fig, full_html=False)

            return render_template('results.html',
                                   chart_html=chart_html,
                                   bar_chart_html=bar_chart_html,
                                   data=df.to_dict(orient='records'),
                                   highest_votes_name=top_candidate['Candidate'],
                                   highest_votes_count=top_candidate['Votes'])
        except Exception as e:
            return f"Error reading CSV: {e}"
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)