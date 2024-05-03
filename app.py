import os
import uuid
import pandas as pd
from flask import Flask, send_from_directory, jsonify, request, render_template, Response

app = Flask(__name__, template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')


    if username == "neuralnine" and password == "password":
        return "Success"

    else:
        return "Failure"


@app.route('/file_upload', methods=['POST'])
def file_upload():
    file = request.files['file']

    if file.content_type == 'text/plain':
        return file.read().decode()

    elif file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' or file.content_type == 'application/vnd.ms-excel':
        dataframe = pd.read_excel(file)
        return dataframe.to_html()


@app.route('/convert_csv', methods=['POST'])
def  convert_csv():
    file = request.files['file']
    dataframe = pd.read_excel(file)

    response = Response(
        dataframe.to_csv(),
        mimetype='text/csv',
        headers={
            'Content-Disposition': 'attachment; filename=result.csv'
        }
    )
    return response


@app.route('/convert_csv_two', methods=['POST'])
def convert_csv_two():
    file = request.files['file']

    dataframe = pd.read_excel(file)

    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    filename = f'{uuid.uuid4()}.csv'

    dataframe.to_csv(os.path.join('downloads', filename))

    return render_template('download.html', filename=filename)


@app.route('/download/<filename>')
def download(filename):
    return send_from_directory('downloads', filename, download_name='result.csv')


@app.route('/handle_post', methods=['POST'])
def handle_post():
    greeting = request.json['greeting']
    name = request.json['name']

    with open('file.txt', 'w') as f:
        f.write(f'{greeting}, {name}')

    return jsonify({'message': 'Secessfuly written!'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)



