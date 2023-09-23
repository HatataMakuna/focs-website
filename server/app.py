import sys
import time

import boto3
import config
import consts
from db_connection_pool import DbConnectionPool
from flask import Flask, jsonify, redirect, render_template, request
from flask_cors import CORS

app = Flask(__name__, static_folder="../static", template_folder="../templates")
db_conn_pool = DbConnectionPool.get_instance()
sns = boto3.resource("sns", consts.AWS_REGION)
sys_abuse_topic = sns.Topic(consts.SYS_ABUSE_TOPIC_ARN)
CORS(app)

# Stream printed logs from EC2 to CloudWatch
# sys.stdout = open("/opt/aws/amazon-cloudwatch-agent/logs/amazon-cloudwatch-agent.log", "w")
# sys.stderr = sys.stdout


# [N8] The website should be able to track the IP (Internet Protocol) address of the visitor device.
@app.before_request
def on_req():
    # Get current time
    now = int(time.time())

    # Reopen the timed out database connection to avoid PyMySQL interface error
    db_conn = db_conn_pool.get_connection(pre_ping=True)
    cursor = db_conn.cursor()

    try:
        # Find out when the client first enters our system
        cursor.execute(
            "SELECT enter_count, first_enter_at, unblock_at, block_count FROM ip_addr WHERE `value` = %s",
            (request.remote_addr,),
        )
        db_conn.commit()
        db_row = cursor.fetchone()

        if db_row:
            enter_count = db_row[0]
            first_enter_at = db_row[1]
            unblock_at = db_row[2]
            block_count = db_row[3]

            # Is this client still being blocked ?
            if now < unblock_at:
                # Reject the request
                return {"message": "Forbidden"}, 403

            # The client has entered our system for 1 second ?
            if now != first_enter_at:
                # Reset the client's enter count in the database
                cursor.execute(
                    "UPDATE ip_addr SET enter_count = 1, first_enter_at = %s WHERE `value` = %s",
                    (now, request.remote_addr),
                )

            else:
                # The client enters our system
                cursor.execute(
                    "UPDATE ip_addr SET enter_count = enter_count + 1 WHERE `value` = %s", (request.remote_addr,)
                )

                # If the client enters our system 100 times within 1 second, block the client
                if enter_count == 99:
                    cursor.execute(
                        "UPDATE ip_addr SET unblock_at = %s, block_count = block_count + 1 WHERE `value` = %s",
                        (now + min(3600 * (1 << block_count), 86400), request.remote_addr),
                    )

                    # Send an email to the developer account when this event occurs
                    sys_abuse_topic.publish(
                        Message=f"User from {request.remote_addr} is trying to send too many requests to your server.",
                        Subject="Suspicious User Encountered",
                    )

        else:
            # The client enters our system
            cursor.execute("INSERT INTO ip_addr VALUES (%s, DEFAULT, %s, DEFAULT, DEFAULT)", (request.remote_addr, now))

        db_conn.commit()

    finally:
        cursor.close()
        db_conn.close()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/programmes", methods=["GET"])
def list_programmes():
    return render_template("ProgrammeList.html")


# TODO: [N1] The website should be able to show the page regarding the information
# of an intended computing programme as a search result
#
# If only ONE programme is returned as search result, redirect the user to the programme page
@app.route("/redirect-program", methods=["GET"])
def redirect_programme():
    program_name = request.args.get("program_name")
    # Implement your logic to determine the program URL based on the name
    # Example: program_url = get_program_url(program_name)
    program_url = f"/path/to/program/{program_name}"
    return redirect(program_url)


# TODO: [N9]
# Get the list of staffs : DONE
@app.route("/get-staff-list", methods=["GET"])
def get_staff_list():
    # Get the page number, items per page, and search query from the request parameters
    page_number = int(request.args.get("page", 1))  # default is 1st page
    items_per_page = int(request.args.get("itemsPerPage", 20))  # default is 20 staffs per page
    search_query = request.args.get("search", '')

    # Calculate the offset based on the page number and items per page
    offset = (page_number - 1) * items_per_page

    db_conn = db_conn_pool.get_connection(pre_ping=True)
    cursor = db_conn.cursor()
    try:
        cursor.execute("""
            SELECT * FROM staff WHERE UPPER(staff_name) LIKE UPPER(%s) OR UPPER(designation) LIKE UPPER(%s)
            OR UPPER(position) LIKE UPPER(%s) OR UPPER(department) LIKE UPPER(%s) LIMIT %s OFFSET %s
        """, (
            f"%{search_query}%", f"%{search_query}%", f"%{search_query}%", f"%{search_query}%",
            items_per_page, offset
        ))
        staff_data = cursor.fetchall()

        # Convert the result to a list of dictionaires
        staff_list = []
        for staff in staff_data:
            staff_info = {
                "staff_id": staff[0],
                "staff_name": staff[1],
                "avatar": staff[2],
                "designation": staff[3],
                "department": staff[4],
                "position": staff[5],
                "email": staff[6],
            }
            staff_list.append(staff_info)

        # Get the total count of staff members
        cursor.execute("SELECT COUNT(*) FROM staff")
        total_count = cursor.fetchone()[0]
        return jsonify({"staff_list": staff_list, "total_count": total_count})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        db_conn.close()


# route to Staff list
@app.route("/staffs", methods=["GET"])
def list_staffs():
    return render_template("StaffList.html")


# get the staff details
@app.route("/staffs/<id>")
def staff(id: int):
    db_conn = db_conn_pool.get_connection(pre_ping=True)
    cursor = db_conn.cursor()
    print(id)
    try:
        cursor.execute(
            "SELECT s.staff_id, s.staff_name, s.avatar, s.designation, s.department, s.position," +
            " s.email, d.publications, d.specialization, d.area_of_interest FROM staff s, staff_details d" +
            " WHERE s.staff_id = d.staff_id AND s.staff_id = %s",
            (id,)
        )
        staff_data = cursor.fetchone()
        if staff_data:
            data_to_pass = {
                "staff_id": staff_data[0],
                "staff_name": staff_data[1],
                "avatar": "/static/" + staff_data[2],
                "designation": staff_data[3],
                "department": staff_data[4],
                "position": staff_data[5],
                "email": staff_data[6],
                "publications": staff_data[7],
                "specialization": staff_data[8],
                "area_of_interest": staff_data[9],
            }
            return render_template("StaffDetails.html", staffprofile=data_to_pass), 200
        else:
            return jsonify({"message": "Staff not found"}), 404
    except Exception as e:
        return jsonify({"message": "Error while retrieving staff details" + str(e)}), 500
    finally:
        cursor.close()
        db_conn.close()


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
            bucket_location = boto3.client("s3").get_bucket_location(Bucket=config.custombucket)
            s3_location = bucket_location["LocationConstraint"]

            if s3_location is None:
                s3_location = ""
            else:
                s3_location = "-" + s3_location

            # object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
            #     s3_location, config.custombucket, emp_image_file_name_in_s3
            # )

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    return render_template("AddEmpOutput.html", name=emp_name)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
