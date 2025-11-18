"""
Flask Web Application with Intentional Security Issues
for DevSecOps Practice
"""

import os
import pickle
import sqlite3
from flask import Flask, request, render_template_string, make_response
import subprocess

app = Flask(__name__)

# Security Issue 1: Hardcoded secret key
app.config['SECRET_KEY'] = 'hardcoded-secret-key-12345'

# Security Issue 2: Debug mode enabled in production
app.config['DEBUG'] = True

# Security Issue 3: Hardcoded database credentials
DB_HOST = 'localhost'
DB_USER = 'admin'
DB_PASSWORD = 'admin123'


@app.route('/')
def index():
    return '''
    <h1>DevSecOps Demo App</h1>
    <a href="/search">Search</a> |
    <a href="/upload">Upload</a> |
    <a href="/user">User Info</a>
    '''


@app.route('/search')
def search():
    query = request.args.get('q', '')

    # Security Issue 4: SQL Injection vulnerability
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    sql = f"SELECT * FROM products WHERE name LIKE '%{query}%'"
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()

    return str(results)


@app.route('/user')
def user_info():
    user_id = request.args.get('id', '1')

    # Security Issue 5: Command Injection vulnerability
    output = subprocess.check_output(f'echo User ID: {user_id}', shell=True)
    return output


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']

        # Security Issue 6: Unrestricted file upload
        filename = file.filename
        file.save(os.path.join('/uploads', filename))
        return f'File {filename} uploaded successfully'

    return '''
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit">
    </form>
    '''


@app.route('/render')
def render():
    # Security Issue 7: Server-Side Template Injection (SSTI)
    template = request.args.get('template', 'Hello World')
    return render_template_string(template)


@app.route('/deserialize')
def deserialize():
    # Security Issue 8: Insecure Deserialization
    data = request.args.get('data', '')
    obj = pickle.loads(data.encode())
    return str(obj)


@app.route('/redirect')
def redirect():
    # Security Issue 9: Open Redirect
    url = request.args.get('url', '/')
    return make_response('', 302, {'Location': url})


def connect_db():
    # Security Issue 10: Using eval()
    host = request.args.get('host', 'localhost')
    return eval(f"connect_to('{host}')")


# Code quality issues
def unused_function():
    x=1+2
    y=3+4
    z=x+y
    return z

def badly_formatted_function(a,b,c,d,e,f,g):
    if a:
        if b:
            if c:
                if d:
                    if e:
                        return f+g
    return None


if __name__ == '__main__':
    # Security Issue 11: Running with 0.0.0.0 in production
    app.run(host='0.0.0.0', port=5000, debug=True)
