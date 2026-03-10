import pymysql
pymysql.install_as_MySQLdb()  # Ha saglyat mahatvacha badal aahe

from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Frontend ani Backend connect honyasathi garjeche

# MySQL Configuration (Tuza Workbench setup)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'tuzapassword' # <--- Ith TUZA password tak
app.config['MYSQL_DB'] = 'grievance_system'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' # Jyamule data direct JSON madhe gheta yeto

mysql = MySQL(app)

# 1. New Complaint Submit Route
@app.route('/submit-complaint', methods=['POST'])
def submit_complaint():
    try:
        data = request.json
        cur = mysql.connection.cursor()
        
        query = """INSERT INTO complaints (user_email, category, description, image, status) 
                   VALUES (%s, %s, %s, %s, %s)"""
        
        cur.execute(query, (
            data.get('email'), 
            data.get('category'), 
            data.get('description'), 
            data.get('image'), 
            'Submitted'
        ))
        
        mysql.connection.commit()
        new_id = cur.lastrowid
        cur.close()
        
        return jsonify({"message": "Complaint Registered!", "id": new_id}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

# 2. Get All Complaints (For Admin Dashboard)
@app.route('/get-all-complaints', methods=['GET'])
def get_all_complaints():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, user_email, category, description, status, image FROM complaints ORDER BY id DESC")
        results = cur.fetchall() # DictCursor mule direct dictionary milte
        cur.close()
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3. Update Status (Resolve Button)
@app.route('/update-status/<int:id>', methods=['POST'])
def update_status(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE complaints SET status = 'Resolved' WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Status Updated Successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Port 5000 var run hoil
    app.run(debug=True, port=5000)