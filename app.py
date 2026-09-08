from flask import Flask, render_template, request
import psycopg2
from psycopg2.errors import UniqueViolation

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register_member():

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    phone = request.form["phone"]
    address = request.form["address"]
    occupation = request.form["occupation"]

    connection = None
    cursor = None

    try:
        connection = psycopg2.connect(
            dbname=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            host=os.environ["DB_HOST"],
            port=os.environ["DB_PORT"]
        )


        cursor = connection.cursor()


        cursor.execute(
            """
            INSERT INTO membership
            (first_name, last_name, email, phone, address, occupation)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                first_name,
                last_name,
                email,
                phone,
                address,
                occupation
            )
        )


        connection.commit()
    except UniqueViolation:

        connection.rollback()

        return render_template("error.html")

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

    return render_template("success.html")
    


if __name__ == "__main__":
    app.run(debug=True)
