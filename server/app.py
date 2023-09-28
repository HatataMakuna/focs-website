import sys
import time
import uuid

import boto3
import consts
from db_connection_pool import DbConnectionPool
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__, static_folder="../static", template_folder="../templates")
db_conn_pool = DbConnectionPool.get_instance()
sns = boto3.resource("sns", consts.AWS_REGION)
sys_abuse_topic = sns.Topic(consts.SYS_ABUSE_TOPIC_ARN)
lex = boto3.client("lexv2-runtime", consts.AWS_REGION)
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


# TODO: [N1] The website should be able to show the page regarding the information
# of an intended computing programme as a search result
@app.route("/programmes")
def programmes():
    return render_template("ProgrammeList.html")


@app.route("/search-programmes", methods=["GET"])
def search_programmes():
    search_query = request.args.get("search", "")

    db_conn = db_conn_pool.get_connection(pre_ping=True)
    cursor = db_conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM programmes WHERE UPPER(id) LIKE UPPER(%s) OR UPPER(name) LIKE UPPER(%s)",
            (f"%{search_query}%", f"%{search_query}%"),
        )
        programme_data = cursor.fetchall()

        programme_list = []
        for programme in programme_data:
            programme_info = {
                "id": programme[0],
                "name": programme[1],
            }
            programme_list.append(programme_info)

        return jsonify({"programme_list": programme_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        db_conn.close()


@app.route("/programmes/pcs")
def programme_pcs():
    return render_template("programmes/PCS.html")


@app.route("/programmes/pit")
def programme_pit():
    return render_template("programmes/PIT.html")


@app.route("/programmes/pms")
def programme_pms():
    return render_template("programmes/PMS.html")


@app.route("/programmes/mcs")
def programme_mcs():
    return render_template("programmes/MCS.html")


@app.route("/programmes/mit")
def programme_mit():
    return render_template("programmes/MIT.html")


@app.route("/programmes/mms")
def programme_mms():
    return render_template("programmes/MMS.html")


@app.route("/programmes/rds")
def programme_rds():
    return render_template("programmes/RDS.html")


@app.route("/programmes/rei")
def programme_rei():
    return render_template("programmes/REI.html")


@app.route("/programmes/ris")
def programme_ris():
    return render_template("programmes/RIS.html")


@app.route("/programmes/rit")
def programme_rit():
    return render_template("programmes/RIT.html")


@app.route("/programmes/rmm")
def programme_rmm():
    return render_template("programmes/RMM.html")


@app.route("/programmes/rsd")
def programme_rsd():
    return render_template("programmes/RSD.html")


@app.route("/programmes/rst")
def programme_rst():
    return render_template("programmes/RST.html")


@app.route("/programmes/rsw")
def programme_rsw():
    return render_template("programmes/RSW.html")


@app.route("/programmes/dcs")
def programme_dcs():
    return render_template("programmes/DCS.html")


@app.route("/programmes/dft")
def programme_dft():
    return render_template("programmes/DFT.html")


@app.route("/programmes/dis")
def programme_dis():
    return render_template("programmes/DIS.html")


@app.route("/programmes/dse")
def programme_dse():
    return render_template("programmes/DSE.html")


# TODO: [N9]
# Get the list of staffs : DONE
@app.route("/get-staff-list", methods=["GET"])
def get_staff_list():
    # Get the page number, items per page, and search query from the request parameters
    page_number = int(request.args.get("page", 1))  # default is 1st page
    items_per_page = int(request.args.get("itemsPerPage", 20))  # default is 20 staffs per page
    search_query = request.args.get("search", "")
    search_query = request.args.get("search", "")

    # Calculate the offset based on the page number and items per page
    offset = (page_number - 1) * items_per_page

    db_conn = db_conn_pool.get_connection(pre_ping=True)
    cursor = db_conn.cursor()
    try:
        # cursor.execute(
        #     """
        # cursor.execute(
        #     """
        #     SELECT * FROM staff WHERE UPPER(staff_name) LIKE UPPER(%s) OR UPPER(designation) LIKE UPPER(%s)
        #     OR UPPER(position) LIKE UPPER(%s) OR UPPER(department) LIKE UPPER(%s) LIMIT %s OFFSET %s
        # """,
        #     (
        #         f"%{search_query}%",
        #         f"%{search_query}%",
        #         f"%{search_query}%",
        #         f"%{search_query}%",
        #         items_per_page,
        #         offset,
        #     ),
        # )
        # """,
        #     (
        #         f"%{search_query}%",
        #         f"%{search_query}%",
        #         f"%{search_query}%",
        #         f"%{search_query}%",
        #         items_per_page,
        #         offset,
        #     ),
        # )
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


# @log
@app.route("/qna", methods=["GET"])
def list_qna():
    return render_template("Qna.html")


# @log
# get the staff details
@app.route("/staffs/<id>")
def staff(id: int):
    db_conn = db_conn_pool.get_connection(pre_ping=True)
    cursor = db_conn.cursor()
    try:
        cursor.execute(
            "SELECT s.staff_id, s.staff_name, s.avatar, s.designation, s.department, s.position,"
            + " s.email, d.publications, d.specialization, d.area_of_interest FROM staff s, staff_details d"
            + " WHERE s.staff_id = d.staff_id AND s.staff_id = %s",
            (id,),
        )
        staff_data = cursor.fetchone()
        if staff_data:
            current_staff_profile = {
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
        else:
            return jsonify({"message": "Staff not found"}), 404
        return render_template("StaffDetails.html", staffprofile=current_staff_profile), 200
    except Exception as e:
        return jsonify({"message": "Error while retrieving staff details: " + str(e)}), 500
    finally:
        cursor.close()
        db_conn.close()


# TODO: [N5] The website should be able to provide comparisons on the selected programme structure.
@app.route("/compare_programmes", methods=["POST"])
def compare_programmes():
    return {}


# [N6] There should be a robot to answer frequently asked questions (FAQ)
@app.route("/faq_ans", methods=["GET"])
def get_faq_answer():
    # Input
    q = request.args.get("q", ".")

    # Ensure query is not empty
    if q == "":
        q = "."

    # Get current time
    now = int(time.time())

    db_conn = db_conn_pool.get_connection(pre_ping=True)
    cursor = db_conn.cursor()

    try:
        # Try to get the chatbot session ID
        cursor.execute("SELECT id, created_at FROM chatbot_session WHERE ip_addr = %s", (request.remote_addr,))
        db_conn.commit()
        chatbot_session = cursor.fetchone()
        chatbot_session_id = str(uuid.uuid4())

        # Have established a chatbot session ?
        if chatbot_session:
            # Chatbot session almost expired ?
            if now - chatbot_session[1] > 290:
                # Renew the chatbot session
                cursor.execute(
                    "UPDATE chatbot_session SET id = %s, created_at = %s WHERE ip_addr = %s",
                    (chatbot_session_id, now, request.remote_addr),
                )
                db_conn.commit()

            else:
                chatbot_session_id = chatbot_session[0]

        else:
            # Establish a new chatbot session
            cursor.execute(
                "INSERT INTO chatbot_session VALUES (%s, %s, %s)",
                (request.remote_addr, chatbot_session_id, now),
            )
            db_conn.commit()

        # Talk with the chatbot
        chatbot_resp = lex.recognize_text(
            botId=consts.CHATBOT_ID,
            botAliasId=consts.CHATBOT_ALIAS_ID,
            localeId="en_US",
            sessionId=chatbot_session_id,
            text=q,
        )

        # Output
        return {"result": chatbot_resp["messages"][0]["content"]}

    finally:
        cursor.close()
        db_conn.close()


@app.errorhandler(404)
def catch_all(error):
    return render_template("404notfound.html")


@app.route("/about", methods=["GET"])
def about():
    return render_template("www.tarc.edu.my")


@app.route("/softwareEngineer", methods=["GET"])
def softwareEngineer():
    return render_template("TanKangHong/homepage.html")


@app.route("/softwareEngineer/display1", methods=["GET"])
def display1():
    return render_template("TanKangHong/applyPage.html")


@app.route("/softwareEngineer/display2", methods=["GET"])
def display2():
    return render_template("TanKangHong/apply2.html")


@app.route("/softwareEngineer/display3", methods=["GET"])
def display3():
    return render_template("TanKangHong/apply3.html")


@app.route("/softwareEngineer/display4", methods=["GET"])
def display4():
    return render_template("TanKangHong/apply4.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
