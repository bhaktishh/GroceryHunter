from datetime import time
from flask import Flask, render_template, request
import backend.sql as SQ
import backend.matching as MC
app = Flask(__name__)
import backend.send_sms as SEND

# login page (default webpage)
@app.route("/", methods=['POST', 'GET'])
def index():
    # when login button is clicked
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']
        users = SQ.get_volunteer_user_pass()
        tmp = False
        for user in users:
            # correctly authenticated login
            if (phone == (user[0]) and password == user[1]): 
                tmp = True
                (phone, zipcode) = SQ.get_volunteer_zip(phone)
                # find requests for volunteers based on zipcode 
                info = MC.match(phone, zipcode)
                for one in info:
                    # assign requests to volunteer
                    SQ.assign_request(phone, one[0], zipcode, False)
                # render template for homepage for user with the relevant information passed
                return render_template("home.html", vtr=phone, info=SQ.get_requests_for_volunteer(phone))
        # incorrect login
        if tmp == False:
            # return to login page
            return render_template('login.html', flag=True)
    # default login page
    else:
        return render_template('login.html', flag=False)

# register a new user
@app.route("/register", methods=['POST', 'GET'])
def register():
    # when submit button is clicked
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']
        name = request.form['name']
        zipcode = int (request.form['zipcode'])
        # register a new volunteer in the database
        SQ.register_volunteer(phone, password, name, zipcode)
        # find requests for volunteers based on zipcode 
        info = MC.match(phone, zipcode)
        for one in info:
                # assign requests to volunteer
                SQ.assign_request(phone, one[0], zipcode, False)
        # render template for homepage for user with the relevant information passed
        return render_template("home.html", vtr=phone, info=SQ.get_requests_for_volunteer(phone))
    # default register page
    else:
        return render_template("register.html")

# volunteer accepts a request
@app.route("/accept/<string:vtr>/<string:rqstr>", methods=['POST', 'GET'])
def accept(vtr,rqstr):
    if request.method == 'POST':
        (rqid,) = SQ.get_req_id(vtr,rqstr)
        timeperiod = request.form['delivery']
        SQ.accept_request(rqid, timeperiod)
        rqstrName = SQ.get_req_name(rqstr)
        vtrName = SQ.get_vtr_name(vtr)
        # send a message confirming details to the requester.
        SEND.send_msg_to_requester(rqstr, vtr, rqstrName, vtrName)
        # render template for homepage
        return render_template("home.html", vtr=vtr, info=SQ.get_requests_for_volunteer(vtr))
    else:
        # default accept request page
        return render_template('accept.html', vtr=vtr, rqstr=rqstr)

# volunteer declines a requester
@app.route("/decline/<string:vtr>/<string:rqstr>")
def decline(vtr, rqstr):
    (rqid,) = SQ.get_req_id(vtr,rqstr)
    SQ.decline_request(rqid)
    # render template for homepage with updated requests
    return render_template("home.html", vtr=vtr, info=SQ.get_requests_for_volunteer(vtr))

# information page for requesters
@app.route("/requesters", methods=['POST', 'GET'])
def elderly():
    return render_template("requesters.html")

# terms and conditions
@app.route("/termsconditions")
def termsconditions():
    return render_template("termsconditions.html")

# change user details
@app.route("/settings/<string:vtr>", methods=['POST', 'GET'])
def settings(vtr):
    if request.method == 'POST':
        zipcode = request.form['zipcode']
        pw = request.form['password']
        name = request.form['name']
        info = []
        if (zipcode != ""):
            SQ.update_vtr_zip(zipcode,vtr)
            info = MC.match(vtr, zipcode)
        if (pw != ""):
            SQ.update_vtr_pw(pw, vtr)
        if (name != ""):
            SQ.update_vtr_name(name, vtr)
        # re-render home template with requests for new zipcode
        if info != []:
            return render_template("home.html", vtr=vtr, info=info)
        # render template without changing requests
        else:
            return render_template("home.html", vtr=vtr, info=SQ.get_requests_for_volunteer(vtr))
    # default settings page
    else:
        return render_template("settings.html", vtr=vtr, info=SQ.get_requests_for_volunteer(vtr))

if __name__ == "__main__":
    app.run(use_reloader = True, debug=True)