from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'nayana1912@gmail',
    'database': 'RegistrationDB'
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

@app.route('/registration', methods=['POST'])
def create_registration():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO Registration (Name, Email, DateOfBirth, PhoneNumber) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (data['Name'], data['Email'], data['DateOfBirth'], data.get('PhoneNumber')))
        conn.commit()
        return jsonify({'message': 'Registration created successfully', 'ID': cursor.lastrowid}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/registration/<int:id>', methods=['GET'])
def read_registration(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM Registration WHERE ID = %s"
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        if not result:
            return jsonify({'message': 'Registration not found'}), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/registration/<int:id>', methods=['PUT'])
def update_registration(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        UPDATE Registration
        SET Name = %s, Email = %s, DateOfBirth = %s, PhoneNumber = %s
        WHERE ID = %s
        """
        cursor.execute(query, (data['Name'], data['Email'], data['DateOfBirth'], data.get('PhoneNumber'), id))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({'message': 'Registration not found'}), 404
        return jsonify({'message': 'Registration updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/registration/<int:id>', methods=['DELETE'])
def delete_registration(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "DELETE FROM Registration WHERE ID = %s"
        cursor.execute(query, (id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({'message': 'Registration not found'}), 404
        return jsonify({'message': 'Registration deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
