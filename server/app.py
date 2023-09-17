import boto3
import config
from db_connection_pool import DbConnectionPool
from flask import Flask, render_template, request
from flask_cors import CORS

app = Flask(__name__, static_folder="../static", template_folder="../templates")
db_conn_pool = DbConnectionPool.get_instance()
CORS(app)


# TODO: [N8] The website should be able to track the IP (Internet Protocol) address of the visitor device.
@app.before_request
def on_req():
    # Get the visitor public IPv4 address
    # TODO: Stream printed logs from EC2 to CloudWatch
    print(request.remote_addr)

    # TODO: Unblock the client address after 60 minutes
    # If the client address is being blocked the second time, the client address will be unblocked after 2 hours
    # If the client address is being blocked the third time, the client address will be unblocked after 4 hours
    # The time taken to unblock the client will increase exponentialy and capped at 24 hours

    # TODO: Block the client address if the client enters our system 2500 times within 1 second

    # TODO: Is this client address exists in our block list DB table ?
    # If exist, reject the request
    # Else proceed


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/programmes", methods=["GET"])
def list_programmes():
    return render_template("ProgrammeList.html")


@app.route("/staffs", methods=["GET"])
def list_staffs():
    return render_template("StaffList.html")


@app.errorhandler(404)
def catch_all(error):
    return render_template("404notfound.html")


@app.route("/about", methods=["GET"])
def about():
    return render_template("www.tarc.edu.my")


@app.route("/addemp", methods=["POST"])
def AddEmp():
    emp_id = request.form["emp_id"]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    pri_skill = request.form["pri_skill"]
    location = request.form["location"]
    emp_image_file = request.files["emp_image_file"]

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"

    # Reopen the timed out database connection to avoid PyMySQL interface error
    db_conn = db_conn_pool.get_connection(pre_ping=True)

    cursor = db_conn.cursor()

    if emp_image_file.filename == "":
        return "Please select a file"

    try:
        cursor.execute(insert_sql, (emp_id, first_name, last_name, pri_skill, location))
        db_conn.commit()
        emp_name = "" + first_name + " " + last_name
        # Uplaod image file in S3 #
        emp_image_file_name_in_s3 = "emp-id-" + str(emp_id) + "_image_file"
        s3 = boto3.resource("s3")

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(config.custombucket).put_object(Key=emp_image_file_name_in_s3, Body=emp_image_file)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=config.custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ""
            else:
                s3_location = "-" + s3_location

            object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
                config.custombucket,
                emp_image_file_name_in_s3)

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    return render_template("AddEmpOutput.html", name=emp_name)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
