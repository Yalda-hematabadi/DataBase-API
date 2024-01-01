import psycopg2
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, static_url_path='/static')

db_params = {
    "dbname": "ai paper",
    "user": "postgres",
    "password": "8912",
    "host": "localhost",
    "port": "5432",
}

conn = psycopg2.connect(**db_params)

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
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)
