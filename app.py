from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
import plotly.express as px

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        data = pd.read_csv(filepath)
        preview = data.head().to_html()
        stats = data.describe().to_html()
        columns = data.columns.tolist()
        return render_template('index.html', preview=preview, stats=stats, columns=columns, filename=file.filename)


@app.route('/visualize', methods=['POST'])
def visualize():
    x_column = request.form['x_column']
    y_column = request.form['y_column']
    graph_type = request.form['graph_type']
    filename = request.form['filename']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    data = pd.read_csv(filepath)

    color_discrete_sequence = ['#2ca02c']  # Green color for graphs

    if graph_type == 'scatter':
        graph = px.scatter(data, x=x_column, y=y_column, color_discrete_sequence=color_discrete_sequence).to_html()
    elif graph_type == 'line':
        graph = px.line(data, x=x_column, y=y_column, color_discrete_sequence=color_discrete_sequence).to_html()
    elif graph_type == 'bar':
        graph = px.bar(data, x=x_column, y=y_column, color_discrete_sequence=color_discrete_sequence).to_html()

    preview = data.head().to_html()
    stats = data.describe().to_html()
    columns = data.columns.tolist()
    return render_template('index.html', preview=preview, stats=stats, columns=columns, graph=graph, filename=filename)


if __name__ == '__main__':
    app.run(debug=True)