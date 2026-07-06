from flask import Flask, request, render_template_string
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

HTML_LOGIN = '''
<h2>System Login</h2>
<form method="POST">
    Tài khoản: <input type="text" name="username"><br><br>
    Mật khẩu: <input type="password" name="password"><br><br>
    <input type="submit" value="Vô">
</form>
<p style="color:red;">{{ message }}</p>
<hr>
<a href="/search">Chuyển sang trang Tìm kiếm</a>
'''

HTML_SEARCH = '''
<h2>Tìm kiếm Sản phẩm</h2>
<form method="GET">
    Nhập tên sản phẩm: <input type="text" name="q">
    <input type="submit" value="Tìm">
</form>
<ul>
    {% for item in ket_qua %}
        <li>Sản phẩm số {{ item[0] }}: {{ item[1] }}</li>
    {% endfor %}
</ul>
<p style="color:red;">{{ loi_he_thong }}</p>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    thong_bao = ""
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        
        # Bugged code
        query = f"SELECT * FROM users WHERE username = '{user}' AND password = '{pwd}'"
        c.execute(query)
        
        ket_qua = c.fetchone()
        conn.close()
        
        if ket_qua:
            thong_bao = f"Hi {ket_qua[1]}!"
        else:
            thong_bao = "Incorrect username or password!"
            
    return render_template_string(HTML_LOGIN, message=thong_bao)

@app.route('/search', methods=['GET'])
def search():
    tu_khoa = request.args.get('q', '')
    ket_qua = []
    loi = ""
    
    if tu_khoa:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        
        # Code lỗi: Cộng chuỗi trực tiếp
        query = f"SELECT id, name FROM products WHERE name LIKE '%{tu_khoa}%' AND is_hidden = 0"
        
        try:
            c.execute(query)
            ket_qua = c.fetchall()
        except Exception as e:
            loi = f"Lỗi Database: {e}"
            
        conn.close()
        
    return render_template_string(HTML_SEARCH, ket_qua=ket_qua, loi_he_thong=loi)

if __name__ == '__main__':
    app.run(debug=True)