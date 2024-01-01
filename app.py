import psycopg2
from psycopg2 import pool
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, static_url_path='/static')

db_params = {
    "dbname": "ai paper",
    "user": "postgres",
    "password": "XXXXXX",
    "host": "localhost",
    "port": "5432",
}

connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10, **db_params)

def get_connection():
    return connection_pool.getconn()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ai_paper', methods=['POST'])
def execute_query():
    cursor = None
    try:
        data = request.get_json()
        sql_query = data.get('sql_query')

        if not sql_query:
            resp = jsonify({"error": "SQL query parameter is required"})
            resp.status_code = 400
            return resp

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql_query)

        result = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]

        result_list = [dict(zip(column_names, row)) for row in result]

        resp = jsonify(result_list)
        resp.status_code = 200
        return resp

    except Exception as e:
        print(e)
        resp = jsonify({"error": str(e)})
        resp.status_code = 500
        return resp

    finally:
        if cursor is not None:
            cursor.close()
            connection_pool.putconn(conn)

if __name__ == "__main__":
    app.run(debug=True)
