from flask import Flask, render_template, request
import sqlite3
import serial
from flask import jsonify

conn = sqlite3.connect('database.db', check_same_thread=False)
cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS data (
        id INTEGER PRIMARY KEY,
        data1 TEXT,
        data2 TEXT,
        data3 TEXT,
        data4 TEXT
    )
''')

app = Flask(__name__)

ser = serial.Serial('COM3', 9600)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Pagina2.html', methods=['GET', 'POST'])
def pagina2():
    if request.method == 'POST':
        data1 = request.form.get('input1')
        data2 = request.form.get('input2')
        data3 = request.form.get('input3')
        data4 = request.form.get('input4')
        cur.execute('''
            INSERT INTO data (data1, data2, data3, data4) VALUES (?, ?, ?, ?)
        ''', (data1, data2, data3, data4))
        print(data1)
        # Guarda los cambios
        conn.commit()
        return 'Datos recibidos'
    else:
        data = ser.readline().decode('utf-8').strip()
        return render_template('Pagina2.html', data=data)

@app.route('/data')
def data():
    data = ser.readline().decode('utf-8').strip()
    return jsonify({'data': data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
