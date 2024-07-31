# -*- coding:utf-8 -*-

import pymysql
import hashlib
import datetime
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from pymysql import IntegrityError
from pymysql.constants import ER

app = Flask(__name__)
app.secret_key = "SECRET KEY"

mysql = pymysql.connect(host='localhost',
                       user='root',
                       password='12345678',
                       db='airline',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

# welcom page
@app.route('/', methods=['GET', 'POST'])
def index():

    if session.get("email"):
        return redirect(url_for("cusHomePage"))
    elif session.get("baemail"):
        return redirect(url_for("baHomePage"))
    elif session.get("username"):
        return redirect(url_for("staffHomePage"))

    cursor = mysql.cursor()
    query = "SELECT * FROM airport;"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    cityAirportList = ["Any city"]
    for i in data:
        #cityAirportList.append(i["airport_city"] + "-" + i["airport_name"])
        cityAirportList.append(i["city"] + "-" + i["name"])
        #print(i)
    print(cityAirportList)
    return render_template("index.html", cityAirportList=cityAirportList)

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


#ajax
@app.route("/publicSearch", methods=["GET","POST"])
def publicSearch():
    try:
        departureCity = request.form["departureCity"]
        arrivalCity = request.form["arrivalCity"]
        flightDate = request.form["flightDate"]
        flightNum = request.form["flightNum"]

    except:
        return "Bad form" #change
    cursor = mysql.cursor()
    query = '''SELECT airline_name,flight_num,departure_airport,departure_time,
                arrival_airport,arrival_time,price,status FROM flight '''
    flag = True
    if departureCity != "" and departureCity != 'Any city':
        dept_airport = departureCity.split('-')
        dept_airport = dept_airport[-1]
        if flag:
            query += "WHERE departure_airport = '%s' " % dept_airport
            flag = False

    if flightNum != "" and flightNum != 'Any':
        if flag:
            query += "WHERE flight_num = %s " % flightNum
            flag = False
        else:
            query += "AND flight_num = %s " % flightNum

    if arrivalCity != "" and arrivalCity != 'Any city':
        arriv_airport = arrivalCity.split('-')
        arriv_airport = arriv_airport[-1]
        if flag:
            query += "WHERE arrival_airport = '%s' " % arriv_airport
            flag = False
        else:
            query += "AND arrival_airport = '%s' " % arriv_airport

    if flightDate != "":
        if flag:
            query += "WHERE DATE(departure_time) = '%s' " % flightDate
        else:
            query += "AND DATE(departure_time) = '%s' " % flightDate
    
    cursor.execute(query)
    qRes = cursor.fetchall()
    cursor.close()
    th=["Airline Company",'Flight Number','Departure','Departure Time','Arrival','Arrival Time','Price','Status']
    thtemp=['airline_name','flight_num','departure_airport','departure_time',
                    'arrival_airport','arrival_time','price','status']

    res=[]
    if len(qRes) == 0:
        return render_template("publicSearch.html",a=[["No Flight Available"]],th=[])
    for i in qRes:
        temp = [str(i[j]) for j in thtemp]
        res += [temp]
    # return jsonify({'data':res})
    return render_template("publicSearch.html",a=res,th=th)



@app.route("/upComingSearch", methods=["GET","POST"])
def upComingSearch():
    if request.method == "POST":
        cursor = mysql.cursor()
        try:
            departureCity = request.form["departureCity"]
            arrivalCity = request.form["arrivalCity"]
            flightDate = request.form["flightDate"]
            flightNum = request.form["flightNum"]
        except:
            return "Bad form"  # change

        cursor = mysql.cursor()

        insertname = {
            'flightDate': flightDate
        }


        query = '''SELECT airline_name,flight_num,departure_airport,departure_time,
                arrival_airport,arrival_time,price,status 
                FROM flight 
                WHERE status = "Upcoming" '''

        if departureCity != "" and departureCity != 'Any city':
            dept_airport = departureCity.split('-')
            dept_airport = dept_airport[-1]
            query += "AND departure_airport = '%s' " % dept_airport

        if flightNum != "" and flightNum != 'Any':
            query += "AND flight_num = %s " % flightNum

        if arrivalCity != "" and arrivalCity != 'Any city':
            arriv_airport = arrivalCity.split('-')
            arriv_airport = arriv_airport[-1]
            query += "AND arrival_airport = '%s' " % arriv_airport

        if flightDate != "":
            query += "AND DATE(departure_time) = %(flightDate)s"

        cursor.execute(query,insertname)
        qRes = cursor.fetchall()
        cursor.close()

        th = ["Airline Company", 'Flight Number', 'Departure',
            'Departure Time', 'Arrival', 'Arrival Time', 'Price', 'Status']

        thtemp=['airline_name','flight_num','departure_airport','departure_time',
                    'arrival_airport','arrival_time','price','status']
        res = []
        if len(qRes) == 0:
            return render_template("upComingSearch.html", a=[["No Flight Available"]], th=[])
        for i in qRes:

            temp = [str(i[j]) for j in thtemp]
            res += [temp]

    return render_template("upComingSearch.html", flight_data=qRes, th=th)







def check_empty(*args):
    for e in args:
        try:
            if len(str(e)) == 0:
                return True
        except:
            return True
    return False


""" user registration """

# ------------------------------------------------ register pages --------------------------------------------------
@app.route("/register")
def register():
    return render_template("register.html")


# posting register form
@app.route("/registerHandle", methods=["POST", "GET"])
def registerHandle():
    try:
        user_type = request.form["user_type"]
    except:
        return "Wrong"

    if user_type == "customer":  # username duplication and other IO requirements waiting to be handled later

        # get info from form
        try:
            email = request.form["email"]
            username = request.form["username"]
            password = request.form["password"]
            building_number = request.form["building_number"]
            street = request.form["street"]
            city = request.form["city"]
            state = request.form["state"]
            phone_number = int(request.form["phone_number"])
            passport_number = request.form["passport_number"]
            passport_expiration = request.form["passport_expiration"]
            passport_country = request.form["passport_country"]
            date_of_birth = request.form["date_of_birth"]
        except:
            return "Bad form"
        # print(email,username,building_number,street,city,state,passport_number,passport_country,passport_expiration,date_of_birth)
        if check_empty(email,username,building_number,street,city,state,passport_number,passport_country,passport_expiration,date_of_birth):
            return "Bad Form"
        m = hashlib.md5()
        m.update(password.encode(encoding="UTF-8"))
        hashed_pwd = m.hexdigest()

        cursor = mysql.cursor()
        # check email duplicate
        cursor.execute("SELECT * FROM customer")
        data = cursor.fetchall()
        for e in data:
            if email == e["email"]:
                return render_template("register.html", error="EMAIL ALREADY EXISTS")
                # insert user data into db
        query = "INSERT INTO customer VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (email, username, hashed_pwd, building_number, street, city,
                               state, phone_number, passport_number, passport_expiration,
                               passport_country, date_of_birth))
        mysql.commit()
        cursor.close()
        return redirect(url_for("customerLoginPage"))

    elif user_type == "agent":
        try:
            email = request.form["agemail"]
            password = request.form["agpassword"]
            ba_id = int(request.form["booking_agent_id"])
        except:
            return "Bad form"

        if check_empty(email,password,ba_id):
            return "Bad Form"

        m = hashlib.md5()
        m.update(password.encode(encoding="UTF-8"))
        hashed_pwd = m.hexdigest()

        cursor = mysql.cursor()
        # check email duplicate
        cursor.execute("SELECT * FROM booking_agent")
        data = cursor.fetchall()
        for e in data:
            if email == e["email"]:
                return render_template("register.html", error="EMAIL ALREADY EXISTS")
            if ba_id == int(e["booking_agent_id"]):
                return render_template("register.html", error="ID ALREADY EXISTS")

        query = "INSERT INTO booking_agent VALUES(%s,%s,%s)"
        cursor.execute(query, (email, hashed_pwd, ba_id))
        mysql.commit()
        cursor.close()
        # print('agenttest',email,password,ba_id)
        return render_template("agentLoginPage.html")

    elif user_type == "staff":
        try:
            username = request.form["stusername"]
            password = request.form["stpassword"]
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            date_of_birth = request.form["stdate_of_birth"]
            airline_name = request.form["airline_name"]
        except:
            return "Bad form"
        if check_empty( ):
            return "Bad Form"

        m = hashlib.md5()
        m.update(password.encode(encoding="UTF-8"))
        hashed_pwd = m.hexdigest()

        cursor = mysql.cursor()
        # check username duplicate
        cursor.execute("SELECT * FROM airline_staff")
        data = cursor.fetchall()
        #check if airline valid
        cursor.execute("SELECT * From airline")
        data2 = cursor.fetchall()
        for e in data:
            if username == e["username"]:
                return render_template("register.html", error="USERNAME ALREADY EXISTS")
        if airline_name not in data2:
            return render_template("register.html", error="AIRLINE DOESN'T EXISTS")

        query = "INSERT INTO airline_staff VALUES(%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (username, hashed_pwd, first_name, last_name,
                               date_of_birth, airline_name))
        mysql.commit()
        cursor.close()
        return render_template("staffLoginPage.html")
    else:
        return "Bad form"

# login pages
@app.route("/customerLoginPage")
def customerLoginPage():
    if session.get("email"):
        return redirect(url_for("cusHomePage"))
    return render_template("customerLoginPage.html")


@app.route("/agentLoginPage")
def agentLoginPage():
    if session.get("baemail"):
        return redirect(url_for("baHomePage"))
    return render_template("agentLoginPage.html")


@app.route("/staffLoginPage")
def staffLoginPage():
    if session.get("username"):
        return redirect(url_for("staffHomePage"))
    return render_template("staffLoginPage.html")


# login authentification
@app.route('/loginAuth', methods=["POST", "GET"])
def loginAuth():

    try:
        user_type = request.form["user_type"]
    except:
        return "Bad form"

    if user_type == "customer":

        try:
            email = request.form["email"]
            password = request.form["password"]
        except:
            return "Bad form"

        if check_empty(email,password):
            return "Bad Form"

        m = hashlib.md5()
        m.update(password.encode(encoding="UTF-8"))
        hashed_pwd = m.hexdigest()
        cursor = mysql.cursor()
        cursor.execute("SELECT * FROM customer WHERE email = %s", email)
        data = cursor.fetchone()
        cursor.close()

        if data:
            if str(data["password"]) == str(hashed_pwd):
                session["email"] = email
                return redirect(url_for("cusHomePage"))
            else:
                return render_template("customerLoginPage.html",error="Wrong Password")
        else:
            return render_template("customerLoginPage.html",error="Cannot Find the Email")

    elif user_type == "agent":
        try:
            email = request.form["baemail"]
            password = request.form["password"]
        except:
            return "Bad form"

        if check_empty(email, password):
            return "Bad Form"

        m = hashlib.md5()
        m.update(password.encode(encoding="UTF-8"))
        hashed_pwd = m.hexdigest()
        cursor = mysql.cursor()
        cursor.execute("SELECT * FROM booking_agent WHERE email = %s", email)
        data = cursor.fetchone()
        cursor.close()
        if data:
            if data["password"] == hashed_pwd:
                session["baemail"] = email
                return redirect(url_for("baHomePage"))
            else:
                return render_template("agentLoginPage.html", error="Wrong Password")
        else:
            return render_template("agentLoginPage.html", error="Cannot Find the Email")

    elif user_type == "staff":
        try:
            username = request.form["username"]
            password = request.form["password"]
        except:
            return "Bad form"

        if check_empty(username,password):
            return "Bad Form"

        m = hashlib.md5()
        m.update(password.encode(encoding="UTF-8"))
        hashed_pwd = m.hexdigest()
        cursor = mysql.cursor()
        cursor.execute("SELECT * FROM airline_staff WHERE username = %s", username)
        data = cursor.fetchone()
        cursor.close()

        if data:
            if data["password"] == hashed_pwd:
                session["username"] = username
                return redirect(url_for("staffHomePage"))
            else:
                return render_template("staffLoginPage.html", error="Wrong Password")
        else:
            return render_template("staffLoginPage.html", error="Cannot Find the Username")
    else:
        return "Bad form"

# --------------------------------------- Logout -----------------------------------------
@app.route('/logout', methods=["GET"])
def logout():
    if session.get("email"):
        session.pop("email")
    elif session.get("baemail"):
        session.pop("baemail")
    elif session.get("username"):
        session.pop("username")
    else:
        return "Bad form"
    return redirect(url_for("index"))






# -------------------------------------  Customer Case ---------------------------------------


# -------------------------------------  Customer Hompage---------------------------------------
@app.route("/cusHomePage", methods=["GET", "POST"])
def cusHomePage():
    if session.get("email"):
        email = session["email"]
        if check_empty(email):
            return "Bad Session"
        # send all airports to the page refresh
        cursor = mysql.cursor()
        query = '''SELECT name from customer where email = %s'''
        cursor.execute(query,email)
        name = []
        nameArray = cursor.fetchall()
        for i in nameArray:
            name.append(i["name"])

        query = "SELECT * FROM airport;"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        cityAirportList = ["Any city"]
        for i in data:
            cityAirportList.append(i["airport_city"] + "-" + i["airport_name"])
        # print(cityAirportList)
        return render_template("cusHomePage.html", name = name, cityAirportList=cityAirportList)
    else:
        return redirect(url_for("index"))



# -------------------------------------  Customer View Booked Flight ---------------------------------------
@app.route("/cusViewFlight", methods=["GET", "POST"])
def cusViewFlight():
    if session.get("email") and request.method == "GET":
        email = session["email"]
        if check_empty(email):
            return "Bad Session"

        query = "SELECT customer.name FROM customer WHERE email = %s;"
        cursor = mysql.cursor()
        cursor.execute(query, email)
        name = cursor.fetchone()["name"]

        # get city_airport_list
        query = "SELECT * FROM airport;"
        cursor.execute(query)
        d = cursor.fetchall()
        city_airport_list = ["Any city"]
        for e in d:
            s = e["airport_city"]+'-'+e["airport_name"]
            city_airport_list.append(s)

        # get flight_data
        query = '''SELECT f.airline_name,f.flight_num,f.departure_airport,f.departure_time,
                    f.arrival_airport,f.arrival_time,f.price,f.status
                    FROM flight AS f, ticket AS t, purchases AS p
                    WHERE p.customer_email = %s
                    AND f.status = "Upcoming"
                    AND p.ticket_id = t.ticket_id
                    AND (t.airline_name,t.flight_num) = (f.airline_name,f.flight_num);'''

        cursor.execute(query, email)
        flight_data = cursor.fetchall()
        result = []
        for e in flight_data:
            temp = e
            temp["airline_name"] = str(e["airline_name"])
            temp["flight_num"] = int(str(e["flight_num"]))
            temp["departure_airport"] = str(e["departure_airport"])
            temp["departure_time"] = str(e["departure_time"])
            temp["arrival_airport"] = str(e["arrival_airport"])
            temp["arrival_time"] = str(e["arrival_time"])
            temp["price"] = int(str(e["price"]))
            temp["status"] = str(e["status"])
            result.append(temp)
        flight_data = result

        th1 = ["Airline Company", 'Flight Number', 'Departure Airport',
               'Departure Time', 'Arrival Airport', 'Arrival Time', 'Price', 'Status']


        return render_template("cusViewFlight.html", email=email,
                               cityAirportList=city_airport_list,
                               flight_data=flight_data, th1=th1)


    elif session.get("email") and request.method == "POST":
        email = session["email"]
        if check_empty(email):
            return "Bad Session"

        query = "SELECT name FROM customer WHERE email = %s;"
        cursor = mysql.cursor()
        cursor.execute(query, email)
        name = cursor.fetchone()["name"]

        try:
            departureCity = request.form["departureCity"]
            arrivalCity = request.form["arrivalCity"]
            date1 = request.form["date1"]
            date2 = request.form["date2"]
            flightNum = request.form["flightNum"]
        except:
            return "Bad form"  # change
        print('d',departureCity)
        cursor = mysql.cursor()

        insertname = {
            'email': email,
            'date1': date1,
            'date2': date2,
        }

        print('insertname',insertname)

        query = '''SELECT f.airline_name,f.flight_num,f.departure_airport,f.departure_time,
                    f.arrival_airport,f.arrival_time,f.price,f.status
                    FROM flight AS f, ticket AS t, purchases AS p
                    WHERE p.customer_email = %(email)s
                    AND f.status = "Upcoming"
                    AND p.ticket_id = t.ticket_id
                    AND (t.airline_name,t.flight_num) = (f.airline_name,f.flight_num) '''

        if departureCity != "" and departureCity != 'Any city':
            dept_airport = departureCity.split('-')
            dept_airport = dept_airport[-1]
            query += "AND departure_airport = '%s' " % dept_airport

        if flightNum != "" and flightNum != 'Any':
            query += "AND flight_num = %s " % flightNum

        if arrivalCity != "" and arrivalCity != 'Any city':
            arriv_airport = arrivalCity.split('-')
            arriv_airport = arriv_airport[-1]
            query += "AND arrival_airport = '%s' " % arriv_airport

        if date1 != "" and date2 != "":
            query += "AND DATE(departure_time) BETWEEN %(date1)s AND %(date2)s "
        cursor.execute(query,insertname)
        qRes = cursor.fetchall()
        cursor.close()

        th = ["Airline Company", 'Flight Number', 'Departure',
            'Departure Time', 'Arrival', 'Arrival Time', 'Price', 'Status']
        thtemp=['airline_name','flight_num','departure_airport','departure_time',
                    'arrival_airport','arrival_time','price','status']
        res = []
        if len(qRes) == 0:
            return render_template("cusSearch.html", a=[["No Flight Available"]], th=[])
        for i in qRes:

            temp = [str(i[j]) for j in thtemp]
            res += [temp]
        print('cusRes',qRes,res)
        return render_template("cusSearch.html", flight_data=qRes, th=th)


    else:
        return redirect(url_for("index"))




# -------------------------------------  Customer Purchase Ticket---------------------------------------
@app.route("/cusPurchase", methods=["GET", "POST"])
def cusPurchase():
    if session.get('email'):
        email = session['email']
        cursor = mysql.cursor()
        query = '''SELECT name from customer where email = %s'''
        cursor.execute(query,email)
        name = []
        nameArray = cursor.fetchall()
        for i in nameArray:
            name.append(i["name"])
            
        if request.method == "GET":
            return render_template("cusPurchase.html", name = name)

        if request.method == 'POST':
            try:
                email = session["email"]
                AirlineCompany = request.form["AirlineCompany"]
                FlightNumber = int(request.form["FlightNumber"])
            except:
                return "Bad Form"

            if check_empty(email,AirlineCompany,FlightNumber):
                return "Bad Form"

            cursor = mysql.cursor()

            #check if input flight_num is valid
            cursor.execute("SELECT * FROM flight WHERE airline_name = %s AND flight_num = %s AND status = 'Upcoming';",(AirlineCompany,FlightNumber))
            d = cursor.fetchall()
            if len(d) == 0:
                return redirect(url_for("cusPurchaseResult", result="There's no such Flight or it's not Upcoming !", name = name))

            query = '''SELECT COUNT(ticket_id) as num FROM ticket WHERE airline_name = %s
                    AND flight_num = %s
                    AND ticket_id in (SELECT ticket_id FROM purchases);'''

            cursor.execute(query, (AirlineCompany, FlightNumber))
            num_dic = cursor.fetchall()
            for e in num_dic:
                existed_ticket_num = int(str(e["num"]))

            query = '''SELECT airplane_id as plane_id FROM flight WHERE airline_name = %s
                    AND flight_num = %s;'''

            cursor.execute(query, (AirlineCompany, FlightNumber))
            id_dic = cursor.fetchall()
            for e in id_dic:
                plane_id = int(str(e["plane_id"]))
            print("id", plane_id)

            query = '''SELECT ticket_id as ticket_id
                    from ticket 
                    order by ticket_id DESC limit 1'''

            cursor.execute(query)
            ticket_dic = cursor.fetchall()
            for e in ticket_dic:
                ticket_id = int(str(e["ticket_id"]))
            print("id", ticket_id)


            query = '''SELECT DISTINCT airplane.seats as seats_num from airplane, flight where flight.airplane_id = airplane.airplane_id and flight.airplane_id = %s'''

            cursor.execute(query, plane_id)
            seats_dic = cursor.fetchall()
            for e in seats_dic:
                seats = int(str(e["seats_num"]))

            
            if existed_ticket_num >=  seats:
                return redirect(url_for("cusPurchaseResult", result = "Oops, Sold out!"))

            ticket_id += 1
            #try insertion if there is still ticket left at the moment of purchase
        
            date = datetime.datetime.now().strftime('%Y-%m-%d')
            insert={
                'itd':ticket_id,
                'airline':AirlineCompany,
                'fn':FlightNumber,
                'email':email,
                'date':date,
            }

            
            query1 = '''
            INSERT INTO ticket (ticket_id, airline_name, flight_num) 
                    VALUES(%(itd)s, %(airline)s, %(fn)s);'''
            
            query2 = '''INSERT INTO purchases (ticket_id,customer_email,purchase_date) 
                        VALUES(%(itd)s, %(email)s, %(date)s);'''
                        
            print('que',ticket_id, AirlineCompany, FlightNumber, ticket_id, email, date)
            
            query = ''' SELECT purchases.ticket_id as x from ticket, purchases 
                WHERE ticket.ticket_id = purchases.ticket_id 
                AND purchases.customer_email = %(email)s 
                AND ticket.airline_name = %(airline)s
                AND ticket.flight_num = %(fn)s; '''
            
            cursor.execute(query, insert)
            ticket_booked = cursor.fetchall()
            a = []

            for i in ticket_booked:
                a.append(str(i["x"]))

            if len(a) != 0:
                return redirect(url_for("cusPurchaseResult", name = name, result= "You've already bought this tickect!"))


            try:
                cursor.execute(query1, insert)
                cursor.execute(query2, insert)

            except:
                print('try fails')
                cursor.close()
                return redirect(url_for("cusPurchaseResult", name = name, result= "Oops,AOU,HHHAm, Sold out!"))

            mysql.commit()
            cursor.close()

            return redirect(url_for("cusPurchaseResult",result = "success", name = name))
            
        return render_template("cusPurchase.html",name = name)
    else:
        return redirect('/index')




@app.route("/cusPurchaseResult?<string:result>",methods = ["GET"])
def cusPurchaseResult(result):
    try:
        result = str(result)
    except:
        return "Bad form"
    return render_template("cusPurchaseResult.html", result=result)



# -------------------------------------  Customer Track Spending---------------------------------------

@app.route("/cusTrackSpending", methods=["POST","GET"])
def cusTrackSpending():
    if session.get("email"):
        email = session["email"]

        if check_empty(email):
            return "Bad Session"
        cursor = mysql.cursor()
        #get username
        cursor.execute("SELECT email, name FROM customer WHERE email = %s", email)
        user_data = cursor.fetchone()
        #get annual_spending
        now = datetime.datetime.now()
        year = now.year

        #get year option
        cursor.execute("SELECT distinct year(purchase_date) FROM purchases WHERE customer_email = %s", email)
        year_option = [i["year(purchase_date)"] for i in cursor.fetchall()]
        if len(year_option) == 0:
            year_option = []

        query = '''SELECT SUM(price) AS total FROM flight,purchases,ticket
                    WHERE purchases.customer_email = %s
                    AND year(purchases.purchase_date) = %s
                    AND purchases.ticket_id = ticket.ticket_id
                    AND (ticket.airline_name,ticket.flight_num) = (flight.airline_name,flight.flight_num)
                    '''

        cursor.execute(query, (email, year))
        annual_spending = cursor.fetchone()["total"]
        if annual_spending == None:
            annual_spending = 0

        #get monthly-wise spending of last 6 months
        month = now.month
        search_list = []
        month_list = []
        for i in range(6):
            m = month - i
            if m <= 0:
                m = 12+m
                search_list.append((email,year-1,m))
                month_list.append(str(year-1) + ".%d" % m)
            else:
                search_list.append((email,year,m))
                month_list.append(str(year)+".%d" % m)

        search_list.reverse()
        month_list.reverse()

        query = '''SELECT SUM(price) AS total FROM flight,purchases,ticket
                            WHERE purchases.customer_email = %s
                            AND year(purchases.purchase_date) = %s
                            AND month(purchases.purchase_date) = %s
                            AND purchases.ticket_id = ticket.ticket_id
                            AND (ticket.airline_name,ticket.flight_num) = (flight.airline_name,flight.flight_num)
                            '''
        monthly_spending = []
        for s in search_list:
            cursor.execute(query,s)
            spending =cursor.fetchone()["total"]
            if spending == None:
                spending = 0
            monthly_spending.append(int(str(spending)))
        total_spending_in_range = sum(monthly_spending)
        cursor.close()

        return render_template("cusTrackSpending.html", user_data=user_data, year_option = year_option,
                               annual_spending = annual_spending, monthly_spending = monthly_spending,
                                month_list = month_list,total_spending_in_range = total_spending_in_range)
    else:
        return redirect(url_for("index"))


@app.route('/Trackbar1')
def Trackbar1():
    if session.get("email"):
        email = session["email"]
        if check_empty(email):
            return "Bad Session"
        
        cursor = mysql.cursor()
        #get username
        cursor.execute("SELECT email, name FROM customer WHERE email = %s", email)
        user_data = cursor.fetchone()
        #get annual_spending
        now = datetime.datetime.now()
        year = now.year

        #get year option
        cursor.execute("SELECT distinct year(purchase_date) FROM purchases WHERE customer_email = %s", email)
        year_option = [i["year(purchase_date)"] for i in cursor.fetchall()]
        if len(year_option) == 0:
            year_option = []

        query = '''SELECT SUM(price) AS total FROM flight,purchases,ticket
                    WHERE purchases.customer_email = %s
                    AND year(purchases.purchase_date) = %s
                    AND purchases.ticket_id = ticket.ticket_id
                    AND (ticket.airline_name,ticket.flight_num) = (flight.airline_name,flight.flight_num)
                    '''

        cursor.execute(query, (email, year))
        annual_spending = cursor.fetchone()["total"]
        if annual_spending == None:
            annual_spending = 0

        #get monthly-wise spending of last 6 months
        # year += 1
        month = now.month
        search_list = []
        month_list = []
        for i in range(6):
            m = month - i
            if m <= 0:
                m = 12+m
                search_list.append((email,year-1,m))
                month_list.append(str(year-1) + ".%d" % m)
            else:
                search_list.append((email,year,m))
                month_list.append(str(year)+".%d" % m)

        search_list.reverse()
        month_list.reverse()

        query = '''SELECT SUM(price) AS total FROM flight,purchases,ticket
                            WHERE purchases.customer_email = %s
                            AND year(purchases.purchase_date) = %s
                            AND month(purchases.purchase_date) = %s
                            AND purchases.ticket_id = ticket.ticket_id
                            AND (ticket.airline_name,ticket.flight_num) = (flight.airline_name,flight.flight_num)
                            '''
        monthly_spending = []
        for s in search_list:
            cursor.execute(query,s)
            spending =cursor.fetchone()["total"]
            if spending == None:
                spending = 0
            monthly_spending.append(int(str(spending)))
        total_spending_in_range = sum(monthly_spending)
        cursor.close()

        bar_labels = month_list
        bar_values = monthly_spending
        return render_template('bar_chart2.html', title='Customer Track Spending', max=1000, labels=bar_labels, values=bar_values)
    else:
        return redirect(url_for("index"))


@app.route("/cusTrackSearch", methods = ["POST","GET"])
def cusTrackSearch():
    if session.get("email") and request.method=="POST":
        try:
            email = session["email"]
            print('em',email,)
            smonth = request.form["start_month"]
            start_month = datetime.datetime.strptime(smonth,"%Y-%m-%d").month
            year = datetime.datetime.strptime(smonth,"%Y-%m-%d").year
            print('s',start_month)
            end_month = request.form["end_month"]
            end_month = datetime.datetime.strptime(end_month,"%Y-%m-%d").month
            
            print("TEST",email,start_month,end_month )

        except:
            return "Bad form"
        if (not start_month in range(1,13)) or (not end_month in range(1,13)):
            return "Bad form"

        year = request.form["Year"]
        cursor = mysql.cursor()
        cursor.execute("SELECT name from customer WHERE email = %s;", email)
        name = cursor.fetchone()["name"]
        if not year:
            res = {}
            res["monthly_spending"] = [0]
            res["month_list"] = ["No data found"]
            res["total_spending_in_range"] = '0'
            res["title"] = name + "'s Monthly Spending"

        else:
            try:
                year = int(year)
            except:
                return "Bad Form"

        # get monthly-wise spending of specified range
        search_list = []
        month_list = []
        for i in range(start_month,end_month+1):
            search_list.append((email,year,i))
            month_list.append("%d.%d" %(year,i))


        query = '''SELECT SUM(price) AS total FROM flight,purchases,ticket
                    WHERE purchases.customer_email = %s
                    AND year(purchases.purchase_date) = %s
                    AND month(purchases.purchase_date) = %s
                    AND purchases.ticket_id = ticket.ticket_id
                    AND (ticket.airline_name,ticket.flight_num) = (flight.airline_name,flight.flight_num)
                    '''


        monthly_spending = []
        for s in search_list:
            cursor.execute(query, s)
            spending = cursor.fetchone()["total"]
            if spending == None:
                spending = 0
                monthly_spending.append(int(str(spending)))

        total_spending_in_range = sum(monthly_spending)
        cursor.close()
        res = {}

        res["monthly_spending"] = monthly_spending
        res["month_list"] = month_list
        res["total_spending_in_range"] = str(total_spending_in_range)
        res["title"] = name + "'s Monthly Spending"

        th = ["monthly_spending","month_list","total_spending_in_range"]

        return render_template("cusTrackSearch.html" ,th = th, res = res)

    else:
        return redirect(url_for("index"))



# -------------------------------------  Booking Agent Case ---------------------------------------




# -------------------------------------  Booking Agent Hompage ---------------------------------------
#Booking Agent Hompage
@app.route("/baHomePage", methods=["GET", "POST"])
def baHomePage():
    if session.get("baemail"):
        baemail = session["baemail"]
        if check_empty(baemail):
            return "Bad Session"
        # send all airports to the page refresh
        cursor = mysql.cursor()

        query = "SELECT * FROM airport;"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        cityAirportList = ["Any city"]
        for i in data:
            cityAirportList.append(i["airport_city"] + "-" + i["airport_name"])
        # print(cityAirportList)
        return render_template("baHomePage.html", cityAirportList=cityAirportList)
    else:
        return redirect(url_for("index"))



# -------------------------------------  Booking Agent Ticket Purchase---------------------------------------
@app.route("/baPurchase", methods=["GET", "POST"])
def baPurchase():
    if session.get('baemail'):
        baemail = session['baemail']
        cursor = mysql.cursor()
        query = '''SELECT booking_agent_id as ba_id FROM booking_agent WHERE email = %s'''
        cursor.execute(query,baemail)
        ba_id = []
        ba_id_Array = cursor.fetchall()
        for i in ba_id_Array:
            ba_id.append(i["ba_id"])
            
        if request.method == "GET":
            return render_template("baPurchase.html", ba_id = ba_id)


        if request.method == 'POST':
            try:
                baemail = session["baemail"]
                AirlineCompany = request.form["AirlineCompany"]
                FlightNumber = int(request.form["FlightNumber"])
                email = request.form["Customter_Email"]
            except:
                return "Bad Form"

            if check_empty(baemail,AirlineCompany,FlightNumber,email):
                return "Bad Form"

            cursor = mysql.cursor()

            #check if input flight_num is valid
            cursor.execute("SELECT * FROM flight WHERE airline_name = %s AND flight_num = %s AND status = 'Upcoming';",(AirlineCompany,FlightNumber))
            d = cursor.fetchall()
            if len(d) == 0:
                return redirect(url_for("baPurchaseResult", result="There's no such Flight or it's not Upcoming !", name = name))


            query = '''SELECT COUNT(ticket_id) as num FROM ticket WHERE airline_name = %s
                    AND flight_num = %s
                    AND ticket_id in (SELECT ticket_id FROM purchases);'''

            cursor.execute(query, (AirlineCompany, FlightNumber))
            num_dic = cursor.fetchall()
            for e in num_dic:
                existed_ticket_num = int(str(e["num"]))

            query = '''SELECT airplane_id as plane_id FROM flight WHERE airline_name = %s
                    AND flight_num = %s;'''

            cursor.execute(query, (AirlineCompany, FlightNumber))
            id_dic = cursor.fetchall()
            for e in id_dic:
                plane_id = int(str(e["plane_id"]))
            print("id", plane_id)

            query = '''SELECT ticket_id as ticket_id
                    from ticket 
                    order by ticket_id DESC limit 1'''

            cursor.execute(query)
            ticket_dic = cursor.fetchall()
            for e in ticket_dic:
                ticket_id = int(str(e["ticket_id"]))
            print("id", ticket_id)
            



            query = '''SELECT DISTINCT airplane.seats as seats_num from airplane, flight where flight.airplane_id = airplane.airplane_id and flight.airplane_id = %s'''

            cursor.execute(query, plane_id)
            seats_dic = cursor.fetchall()
            for e in seats_dic:
                seats = int(str(e["seats_num"]))
            
            if existed_ticket_num >=  seats:
                return redirect(url_for("baPurchaseResult", result = "Oops, Sold out!"))

            ticket_id += 1
            #try insertion if there is still ticket left at the moment of purchase
        
            date = datetime.datetime.now().strftime('%Y-%m-%d')
            insert={
                'itd':ticket_id,
                'airline':AirlineCompany,
                'fn':FlightNumber,
                'email':email,
                'date':date,
                'ba_id': ba_id
            }

            
            query1 = '''
            INSERT INTO ticket (ticket_id, airline_name, flight_num) 
                    VALUES(%(itd)s, %(airline)s, %(fn)s);'''
            
            query2 = '''INSERT INTO purchases (ticket_id,customer_email,purchase_date, booking_agent_id) 
                        VALUES(%(itd)s, %(email)s, %(date)s, %(ba_id)s);'''
                        
            print('que',ticket_id, AirlineCompany, FlightNumber, ticket_id, email, date)
            
            query = ''' SELECT purchases.ticket_id as x from ticket, purchases 
                WHERE ticket.ticket_id = purchases.ticket_id 
                AND purchases.customer_email = %(email)s 
                AND ticket.airline_name = %(airline)s
                AND ticket.flight_num = %(fn)s; '''
            
            cursor.execute(query, insert)
            ticket_booked = cursor.fetchall()
            a = []

            for i in ticket_booked:
                a.append(str(i["x"]))

            if len(a) != 0:
                return redirect(url_for("baPurchaseResult", result= "The Customer has already bought this tickect!"))


            try:
                cursor.execute(query1, insert)
                cursor.execute(query2, insert)

            except:
                print('try fails')
                cursor.close()
                return redirect(url_for("baPurchaseResult", result= "Oops,AOU,HHHAm, Sold out!"))

            mysql.commit()
            cursor.close()

            return redirect(url_for("baPurchaseResult",result = "success"))
            
        return render_template("baPurchase.html")
    else:
        return redirect('/index')






@app.route("/baPurchaseResult?<string:result>",methods = ["GET"])
def baPurchaseResult(result):
    try:
        result = str(result)
    except:
        return "Bad form"
    return render_template("baPurchaseResult.html", result=result)



# -------------------------------------  Booking Agent View Commisions  ---------------------------------------



@app.route('/baViewCommission', methods=['GET', 'POST'])
def baViewMyCommission():
    if session.get('baemail'):
        email = session['baemail']
        if request.method == 'GET':
            cursor = mysql.cursor()  
            query = '''select sum(price * 0.1), avg(price * 0.1), count(*)
                from flight, ticket, purchases, booking_agent
                where booking_agent.booking_agent_id = purchases.booking_agent_id AND purchases.ticket_id = ticket.ticket_id 
                AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num 
                AND booking_agent.email = '{}'
                AND purchase_date between DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) and CURRENT_DATE() '''

            cursor.execute(query.format(email))
            rows = cursor.fetchall()
            for i in rows:
                print(i)
            cursor.close()
            print(rows)
            return render_template('baViewCommission.html', rows = rows, )
    else:
        return redirect('index')


#ajax refresh for ba Commission
@app.route('/baCommissionSearch', methods=['GET', 'POST'])
def baCommissionSearch():
    try:
        email = session["baemail"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
    except:
        return "Bad form" #change
    cursor = mysql.cursor()
    query = '''SELECT SUM(price*0.1) AS total_commission FROM ticket, purchases, flight
                    WHERE ticket.ticket_id = purchases.ticket_id
                    AND (ticket.airline_name, ticket.flight_num) = (flight.airline_name, flight.flight_num)
                    AND purchases.booking_agent_id = (SELECT booking_agent_id FROM booking_agent WHERE email = '%s')
                    AND  purchases.purchase_date >= "%s"
                    AND purchases.purchase_date <= "%s" ;''' %(email,start_date,end_date)
    cursor.execute(query)
    total_commission = cursor.fetchone()["total_commission"]
    if not total_commission:
        total_commission = 0
    else:
        total_commission = float(total_commission)
    query = '''SELECT COUNT(ticket_id) sold_ticket_num FROM purchases 
                WHERE booking_agent_id = (SELECT booking_agent_id FROM booking_agent WHERE email = '%s')
                AND  purchase_date >= "%s"
                AND purchase_date <= "%s";''' %(email,start_date,end_date)
    cursor.execute(query)
    sold_ticket_num = cursor.fetchone()["sold_ticket_num"]
    cursor.close()
    th = ["total_commission","sold_ticket_num", "commission_average"]
    if sold_ticket_num != 0:
        commission_average = total_commission/sold_ticket_num
    else:
        commission_average = 0
    return render_template("baCommissionSearch.html",th = th, total_commission = total_commission, sold_ticket_num = sold_ticket_num,commission_average = commission_average)
            


# -------------------------------------  Booking Agent Top Customers ---------------------------------------

@app.route("/baTopCustomers",methods = ["GET"])
def baTopCustomers():
    if session.get("baemail"):
        email = session["baemail"]
        if check_empty(email):
            return "Bad Session"

        #get top 5 customer by ticket_num
        query = '''SELECT customer_email, name, COUNT(ticket_id) AS ticket_num
                    FROM purchases, customer
                    WHERE customer.email = purchases.customer_email
                    AND booking_agent_id = (SELECT booking_agent_id FROM booking_agent WHERE email = %s)
                    AND purchase_date between DATE_SUB(CURRENT_DATE(), INTERVAL 180 DAY) and CURRENT_DATE()
                    GROUP BY customer_email
                    ORDER BY ticket_num DESC
                    LIMIT 5;'''

        cursor = mysql.cursor()
        cursor.execute(query,(email))
        cust_info = cursor.fetchall()
        top5_tickets = []
        c1xAxis_categories_email = []
        c1xAxis_categories_name = []

        for e in cust_info:
            top5_tickets.append(e["ticket_num"])
            c1xAxis_categories_email.append(e["customer_email"])
            c1xAxis_categories_name.append(e["name"])

        #get top 5 customer by total commission
        query = '''SELECT customer_email, name, SUM(price*0.1) total_commission
                    FROM purchases, customer, flight, ticket
                    WHERE purchases.booking_agent_id = (SELECT booking_agent_id FROM booking_agent 
                                                            WHERE email = %s)
                    AND customer.email = purchases.customer_email
                    AND purchases.ticket_id = ticket.ticket_id
                    AND (ticket.airline_name, ticket.flight_num) = (flight.airline_name, flight.flight_num)
                    AND purchase_date between DATE_SUB(CURRENT_DATE(), INTERVAL 180 DAY) and CURRENT_DATE()
                    GROUP BY customer_email
                    ORDER BY total_commission DESC
                    LIMIT 5;'''

        cursor.execute(query,email)
        top5_commission = []
        c2xAxis_categories_email = []
        c2xAxis_categories_name = []
        cust_info = cursor.fetchall()
        cursor.close()

        for e in cust_info:
            top5_commission.append(float(e["total_commission"]))
            c2xAxis_categories_email.append(e["customer_email"])
            c2xAxis_categories_name.append(e["name"])

        return render_template("baTopCustomers.html", email=email, top5_tickets = top5_tickets,
                                c1xAxis_categories_name = c1xAxis_categories_name,
                                c1xAxis_categories_email = c1xAxis_categories_email ,top5_commission = top5_commission,c2xAxis_categories_name = c2xAxis_categories_name,c2xAxis_categories_email = c2xAxis_categories_email)

    else:
        return redirect(url_for("index"))

@app.route('/commission_bar1')
def commission_bar1():
    if session.get("baemail"):
        email = session["baemail"]
        if check_empty(email):
            return "Bad Session"
        query = '''SELECT customer_email, name, COUNT(ticket_id) AS ticket_num
        FROM purchases, customer
        WHERE customer.email = purchases.customer_email
        AND booking_agent_id = (SELECT booking_agent_id FROM booking_agent WHERE email = %s)
        AND purchase_date between DATE_SUB(CURRENT_DATE(), INTERVAL 180 DAY) and CURRENT_DATE()
        GROUP BY customer_email
        ORDER BY ticket_num DESC
        LIMIT 5;'''
        cursor = mysql.cursor()
        cursor.execute(query,(email))
        cust_info = cursor.fetchall()
        top5_tickets = []
        c1xAxis_categories_email = []
        c1xAxis_categories_name = []
        for e in cust_info:
            top5_tickets.append(e["ticket_num"])
            c1xAxis_categories_email.append(e["customer_email"])
            c1xAxis_categories_name.append(e["name"])

        bar_labels = c1xAxis_categories_name
        bar_values = top5_tickets
        return render_template('bar_chart1.html', title='Ticket', max=5, labels=bar_labels, values=bar_values)


@app.route('/commission_bar2')
def commission_bar2():
    if session.get("baemail"):
        email = session["baemail"]
        if check_empty(email):
            return "Bad Session"
        query = '''SELECT customer_email, name, SUM(price*0.1) total_commission
            FROM purchases, customer, flight, ticket
            WHERE purchases.booking_agent_id = (SELECT booking_agent_id FROM booking_agent 
            WHERE email = %s)
            AND customer.email = purchases.customer_email
            AND purchases.ticket_id = ticket.ticket_id
            AND (ticket.airline_name, ticket.flight_num) = (flight.airline_name, flight.flight_num)
            AND purchase_date between DATE_SUB(CURRENT_DATE(), INTERVAL 180 DAY) and CURRENT_DATE()
            GROUP BY customer_email
            ORDER BY total_commission DESC
            LIMIT 5;'''

        cursor = mysql.cursor()
        cursor.execute(query,email)
        top5_commission = []
        c2xAxis_categories_email = []
        c2xAxis_categories_name = []
        cust_info = cursor.fetchall()
        cursor.close()

        for e in cust_info:
            top5_commission.append(float(e["total_commission"]))
            c2xAxis_categories_email.append(e["customer_email"])
            c2xAxis_categories_name.append(e["name"])

        bar_labels = c2xAxis_categories_name
        bar_values = top5_commission
        return render_template('bar_chart1.html', title='Commission', max=200, labels=bar_labels, values=bar_values)


#--------------------------------------------- Booking Agent View Booked Flights ---------------------------------------------
@app.route("/baViewMyFlight", methods=["GET", "POST"])
def baViewMyFlight():

    if session.get("baemail") and request.method == "GET":
        baemail = session["baemail"]
        
        cursor = mysql.cursor()
        query = '''SELECT booking_agent_id as ba_id FROM booking_agent WHERE email = %s'''
        cursor.execute(query,baemail)
        ba_id = []
        ba_id_Array = cursor.fetchall()
        for i in ba_id_Array:
            ba_id.append(i["ba_id"])
        
        ba_id = ba_id[0]
        

        if check_empty(baemail):
            return "Bad Session"


        # get city_airport_list
        query = "SELECT * FROM airport;"
        cursor.execute(query)
        d = cursor.fetchall()
        city_airport_list = ["Any city"]
        for e in d:
            s = e["airport_city"]+'-'+e["airport_name"]
            city_airport_list.append(s)

        # get flight_data
        query = '''SELECT p.customer_email, f.airline_name,f.flight_num,f.departure_airport,f.departure_time,
                    f.arrival_airport,f.arrival_time,f.price,f.status
                    FROM flight AS f, ticket AS t, purchases AS p
                    WHERE p.booking_agent_id = %s
                    AND f.status = "Upcoming"
                    AND p.ticket_id = t.ticket_id
                    AND (t.airline_name,t.flight_num) = (f.airline_name,f.flight_num);'''

        cursor.execute(query, ba_id)
        flight_data = cursor.fetchall()
        result = []
        for e in flight_data:
            temp = e
            temp["airline_name"] = str(e["airline_name"])
            temp["flight_num"] = int(str(e["flight_num"]))
            temp["departure_airport"] = str(e["departure_airport"])
            temp["departure_time"] = str(e["departure_time"])
            temp["arrival_airport"] = str(e["arrival_airport"])
            temp["arrival_time"] = str(e["arrival_time"])
            temp["price"] = int(str(e["price"]))
            temp["status"] = str(e["status"])
            temp["customer_email"] = str(e["customer_email"])
            result.append(temp)
        flight_data = result

        th1 = ["Airline Company", 'Flight Number', 'Departure Airport',
               'Departure Time', 'Arrival Airport', 'Arrival Time', 'Price', 'Status',"Customer Email"]

        return render_template("baViewMyFlight.html", baemail=baemail,
                               cityAirportList=city_airport_list,
                               flight_data=flight_data, th1=th1)


    

    if session.get("baemail") and request.method == "POST":
        baemail = session["baemail"]
        if check_empty(baemail):
            return "Bad Session"

        cursor = mysql.cursor()

        try:
            departureCity = request.form["departureCity"]
            arrivalCity = request.form["arrivalCity"]
            date1 = request.form["date1"]
            date2 = request.form["date2"]
            flightNum = request.form["flightNum"]
        except:
            return "Bad form"  # change
            
        cursor = mysql.cursor()

        insertname = {
            'email': baemail,
            'date1': date1,
            'date2': date2,
        }

        print('insertname',insertname)

        query = '''SELECT flight.airline_name,flight.flight_num,departure_airport,
                    departure_time,arrival_airport,arrival_time,price,status, customer_email
                    FROM flight, ticket, purchases
                    WHERE purchases.booking_agent_id = (SELECT booking_agent_id FROM
                    booking_agent WHERE email = %(email)s)
                    AND flight.status = "Upcoming"
                    AND purchases.ticket_id = ticket.ticket_id
                    AND (ticket.airline_name,ticket.flight_num) = (flight.airline_name,
                    flight.flight_num)'''

        if departureCity != "" and departureCity != 'Any city':
            dept_airport = departureCity.split('-')
            dept_airport = dept_airport[-1]
            query += "AND departure_airport = '%s' " % dept_airport

        if flightNum != "" and flightNum != 'Any':
            query += "AND flight_num = %s " % flightNum

        if arrivalCity != "" and arrivalCity != 'Any city':
            arriv_airport = arrivalCity.split('-')
            arriv_airport = arriv_airport[-1]
            query += "AND arrival_airport = '%s' " % arriv_airport

        if date1 != "" and date2 != "":
            query += "AND DATE(departure_time) BETWEEN %(date1)s AND %(date2)s "
        cursor.execute(query,insertname)
        qRes = cursor.fetchall()
        cursor.close()
        th = ["Airline Company", 'Flight Number', 'Departure',
            'Departure Time', 'Arrival', 'Arrival Time', 'Price', 'Status',"Customer Email"]
        if len(qRes) == 0:
            return render_template("baSearch.html", a=[["No Flight Available"]], th=[])
        return render_template("baSearch.html", flight_data=qRes, th=th)


    else:
        return redirect(url_for("index"))






# Airline Staff Home Page
@app.route("/staffHomePage", methods=["GET", "POST"])
def staffHomePage():
    if session.get("username") and request.method == "GET":
        username = session["username"]
        if check_empty(username):
            return "Bad Session"

        query = "SELECT airline_name FROM airline_staff WHERE username = %s;"
        cursor = mysql.cursor()
        cursor.execute(query, username)
        try:
            airline_name = cursor.fetchone()["airline_name"]
        except:
            return "Your information has been removed from the database. Please contact your admin for further info."

        # get city_airport_list
        query = "SELECT * FROM airport;"
        cursor.execute(query)
        d = cursor.fetchall()
        city_airport_list = ["Any city"]
        for e in d:
            s = e["airport_city"]+'-'+e["airport_name"]
            city_airport_list.append(s)

        # get flight_data
        query = '''SELECT airline_name,flight_num,departure_airport,departure_time,
                    arrival_airport,arrival_time,price,status
                    FROM flight
                    WHERE airline_name = %s and date(departure_time) between CURRENT_DATE() and DATE_ADD(CURRENT_DATE(), INTERVAL 30 DAY) ;'''
        cursor.execute(query, airline_name)
        flight_data = cursor.fetchall()
        result = []
        for e in flight_data:
            temp = e
            temp["flight_num"] = int(str(e["flight_num"]))
            temp["price"] = int(str(e["price"]))
            temp["departure_time"] = str(e["departure_time"])
            temp["arrival_time"] = str(e["arrival_time"])
            result.append(temp)
        flight_data = result
        th1 = ["Airline Company", 'Flight Number', 'Departure',
               'Departure Time', 'Arrival', 'Arrival Time', 'Price', 'Status']
        # get airplane
        query = '''SELECT * FROM airplane WHERE airline_name = %s;'''
        cursor.execute(query, airline_name)
        airplane = cursor.fetchall()
        cursor.close()
        return render_template("staffHomePage.html", username=username, airline_name=airline_name,
                               cityAirportList=city_airport_list,
                               flight_data=flight_data, airplane=airplane, th1=th1)

    elif session.get("username") and request.method == 'POST' and 'departureCity' in request.form:
        username = session["username"]
        if check_empty(username):
            return "Bad Session"

        query = "SELECT airline_name FROM airline_staff WHERE username = %s;"
        cursor = mysql.cursor()
        cursor.execute(query, username)
        try:
            airline_name = cursor.fetchone()["airline_name"]
        except:
            return "Your information has been removed from the database. Please contact your admin for further info."
        try:
            departureCity = request.form["departureCity"]
            arrivalCity = request.form["arrivalCity"]
            date1 = request.form["date1"]
            date2 = request.form["date2"]
            flightNum = request.form["flightNum"]
        except:
            return "Bad form"  # change
        cursor = mysql.cursor()
        insertname = {
            'airline_name': airline_name,
            'date1': date1,
            'date2': date2,
        }
        query = '''SELECT airline_name,flight_num,departure_airport,departure_time,
                    arrival_airport,arrival_time,price,status FROM flight WHERE airline_name=%(airline_name)s'''

        if departureCity != "" and departureCity != 'Any city':
            dept_airport = departureCity.split('-')
            dept_airport = dept_airport[-1]
            query += "AND departure_airport = '%s' " % dept_airport

        if flightNum != "" and flightNum != 'Any':
            query += "AND flight_num = %s " % flightNum

        if arrivalCity != "" and arrivalCity != 'Any city':
            arriv_airport = arrivalCity.split('-')
            arriv_airport = arriv_airport[-1]
            query += "AND arrival_airport = '%s' " % arriv_airport

        if date1 != "" and date2 != "":
            query += "AND DATE(departure_time) BETWEEN %(date1)s AND %(date2)s "

        cursor.execute(query, insertname)
        qRes = cursor.fetchall()
        cursor.close()
        th = ["Airline Company", 'Flight Number', 'Departure',
              'Departure Time', 'Arrival', 'Arrival Time', 'Price', 'Status']
        thtemp=['airline_name','flight_num','departure_airport','departure_time',
                    'arrival_airport','arrival_time','price','status']
        res = []
        if len(qRes) == 0:
            return render_template("staffSearch.html", a=[["No Flight Available"]], th=[])
        for i in qRes:
            temp = [str(i[j]) for j in thtemp]
            res += [temp]
        print('res', res)
        # return jsonify({'data':res})
        return render_template("staffSearch.html", a=res, th=th)

    elif session.get("username") and request.method == 'POST' and 'flightNum1' in request.form:
        try:
            flightNum = request.form["flightNum1"]
            if check_empty(username):
                return "Bad Form"
        except:
            # return "Bad Form"
            pass
        cursor = mysql.cursor()
        query = '''SELECT name,email,t.flight_num
                    FROM customer c,ticket t,purchases p
                    WHERE p.ticket_id = t.ticket_id AND p.customer_email=c.email AND flight_num =%s'''
        cursor.execute(query, flightNum)
        qRes = cursor.fetchall()
        cursor.close()
        th = ["Customer Name", 'Email', 'Flight Number']
        thtemp=['name','email','flight_num']
        res = []
        if len(qRes) == 0:
            return render_template("staffSearch.html", a=[["No Customer Available"]], th=[])
        for i in qRes:
            temp = [str(i[j]) for j in thtemp]
            res += [temp]
        # return jsonify({'data':res})
        return render_template("staffSearch.html", a=res, th=th)

    elif session.get("username") and request.method == 'POST':
        return "Bad Form"

    else:
        return redirect(url_for("index"))

@app.route("/editFlight")
def editFlight():
    return render_template("editFlight.html")

@app.route("/editSystem")
def editSystem():
    return render_template("editSystem.html")

@app.route("/staffChangeFlight",methods = ["POST","GET"])
def staffChangeFlight():
    if session.get("username") and request.method=="POST":
        try:
            username = session["username"]
            flight_num = int(request.form["flight_num"])
            status = request.form["status"]
        except:
            return "Bad form"

        # if status not in ["Upcoming","Delayed","In-progress","Cancelled","Canceled"]:
        #     return "Bad form"

        cursor = mysql.cursor()
        query = "SELECT airline_name FROM airline_staff WHERE username = %s;"
        cursor.execute(query, username)
        try:
            airline_name = cursor.fetchone()["airline_name"]
        except:
            return "Your information has been removed from the database. Please contact your admin for further info."
        query = '''UPDATE flight SET status = %s
                    WHERE airline_name = %s
                    AND flight_num = %s ;'''
        cursor = mysql.cursor()
        cursor.execute(query,(status,airline_name,flight_num))
        mysql.commit()
        query = '''SELECT airline_name,flight_num,departure_airport,departure_time,
                    arrival_airport,arrival_time,price,status 
                    FROM flight 
                    WHERE airline_name = %s;'''
        cursor.execute(query,airline_name)
        data = cursor.fetchall()
        result = []
        for e in data:
            temp = e
            temp["flight_num"] = int(str(e["flight_num"]))
            temp["price"] = int(str(e["price"]))
            temp["departure_time"] = str(e["departure_time"])
            temp["arrival_time"] = str(e["arrival_time"])
            result.append(temp)
        data = result
        cursor.close()
        th = ["Airline Company", 'Flight Number', 'Departure',
              'Departure Time', 'Arrival', 'Arrival Time', 'Price', 'Status']
        # print('changeF',data)
        return render_template("editResult.html",th=th,flight_data=data)
    elif session.get("username"):
        try:
            username = session["username"]
        except:
            return redirect(url_for("index"))
        return render_template("staffChangeFlight.html")
    else:
        
        return redirect(url_for("index"))


@app.route("/staffCreateFlight",methods =  ["POST","GET"])
def staffCreateFlight():
    if session.get("username") and request.method=='POST':
        try:
            username = session["username"]
            flight_num = int(request.form["flight_num"])
            departure_airport = request.form["departure_airport"]
            departure_date = request.form["departure_date"]
            departure_time = request.form["departure_time"]
            arrival_airport = request.form["arrival_airport"]
            arrival_date = request.form["arrival_date"]
            arrival_time = request.form["arrival_time"]
            price = int(request.form["price"])
            status = request.form["status"]
            airplane_id = int(request.form["airplane_id"])
        except:
            return "Bad form"

        if check_empty(username,departure_date,departure_time,arrival_airport,arrival_date,arrival_time,status):
            return "Bad Form"

        if price < 0 or flight_num < 0:
            return "Bad form"

        cursor = mysql.cursor()
        query = "SELECT airline_name FROM airline_staff WHERE username = %s;"
        cursor.execute(query, username)
        try:
            airline_name = cursor.fetchone()["airline_name"]
        except:
            return "Your information has been removed from the database. Please contact your admin for further info."
        #check flight_num duplicate
        query = '''SELECT * FROM flight WHERE airline_name = %s AND flight_num = %s;'''
        cursor.execute(query,(airline_name,flight_num))
        d = cursor.fetchall()
        if len(d) > 0:
            return redirect(url_for("staffCreateResult",result = "This flight number already exists!"))

        #check if airport inputs are valid
        query = '''SELECT airport_name FROM airport'''
        cursor.execute(query)
        d = cursor.fetchall()
        l = []
        for e in d:
            l.append(e["airport_name"])

        if not(arrival_airport  in l):
            return redirect(url_for("staffCreateResult",result = "Please enter a valid arrival airport"))
        if not(departure_airport  in l):
            return redirect(url_for("staffCreateResult", result="Please enter a valid departure airport"))

        #check if plane_id is valid
        query = '''SELECT * FROM airplane WHERE airline_name = %s AND airplane_id = %s;'''
        cursor.execute(query,(airline_name,airplane_id))
        d = cursor.fetchall()
        if len(d) == 0:
            return redirect(url_for("staffCreateResult", result="Invalid airplane id!"))

        departure_time = departure_date+' '+ departure_time+":00"
        arrival_time = arrival_date + ' ' +  arrival_time+":00"
        query = '''INSERT INTO flight VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
        cursor.execute(query,(airline_name,
                                flight_num,
                                departure_airport,
                                departure_time,
                                arrival_airport,
                                arrival_time,
                                price,
                                status,
                                airplane_id))
        mysql.commit()
        cursor.close()
        return redirect(url_for("staffCreateResult",result = "Success"))


    elif session.get("username"):
        username = session["username"]
        if check_empty(username):
            return "Bad Session"
        query = "SELECT airline_name FROM airline_staff WHERE username = %s;"
        cursor = mysql.cursor()
        cursor.execute(query,username)
        airline_name = cursor.fetchone()["airline_name"]
        cursor.close()
        return render_template("staffCreateFlight.html",username = username, airline_name = airline_name)
    else:
        return redirect(url_for("index"))

@app.route("/staffCreateResult?<string:result>",methods = ["GET"])
def staffCreateResult(result):
    if session.get("username"):
        return render_template("staffCreateResult.html",result = result)
    else:
        return redirect(url_for("index"))

@app.route("/staffAddAirport1")
def staffAddAirport1():
    if session.get("username"):
        return render_template("staffAddAirport.html")
    else:
        return redirect(url_for("index"))

@app.route("/staffAddAirport",methods = ["POST","GET"])
def staffAddAirport():
    if session.get("username") and request.method == "POST":
        try:
            airport_name = request.form["airport_name"]
            airport_city = request.form["airport_city"]
        except:
            return "Bad form"
        if check_empty(airport_name,airport_city):
            return "Bad Form"
        query = "SELECT airport_name, airport_city FROM airport;"
        cursor = mysql.cursor()
        cursor.execute(query)
        d = cursor.fetchall()
        for e in d:
            if e["airport_name"] == airport_name:
                return jsonify({"data":"Error: Airport name already exists!"})
        query = "INSERT INTO airport VALUES(%s,%s);"
        cursor.execute(query,(airport_name,airport_city))
        mysql.commit()
        cursor.close()
        return jsonify({'data':"Success"})
    else:
        return redirect(url_for("index"))

@app.route("/staffAddAirplane1")
def staffAddAirplane1():
    if session.get("username"):
        return render_template("staffAddAirplane.html")
    else:
        return redirect(url_for("index"))


@app.route("/staffAddAirplane",methods = ["POST","GET"])
def staffAddAirplane():
    if session.get("username"):
        try:
            username = session["username"]
            airplane_id = int(request.form["airplane_id"])
            seats = int(request.form["seats"])
        except:
            return "Bad form"
        if airplane_id < 0 or seats < 0:
            return  "Bad form"

        cursor = mysql.cursor()
        query = "SELECT airline_name FROM airline_staff WHERE username = %s;"
        cursor.execute(query, username)
        try:
            airline_name = cursor.fetchone()["airline_name"]
        except:
            return "Your information has been removed from the database. Please contact your admin for further info."

        query = "SELECT airline_name,airplane_id FROM airplane;"
        cursor.execute(query)
        d = cursor.fetchall()
        for e in d:
            if e["airline_name"] == airline_name and int(e["airplane_id"]) == int(airplane_id):
                return jsonify({"data":"Error: airplane_id duplicate"})

        query = "INSERT INTO airplane VALUES(%s,%s,%s);"
        cursor.execute(query,(airline_name,airplane_id,seats))
        mysql.commit()
        cursor.close()
        return jsonify({"data":"Success"})

    else:
        return redirect(url_for("index"))

@app.route("/staffViewBA",methods = ["GET"])
def staffViewBA():
    if session.get("username"):
        username = session["username"]
        if check_empty(username):
            return "Bad Session"

        #get airline
        query = '''SELECT airline_name FROM airline_staff WHERE username = %s;'''
        cursor = mysql.cursor()
        cursor.execute(query,username)
        airline_name = cursor.fetchone()["airline_name"]

        #get top5 ba by tickets sold last month
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month - 1
        if month == 0:
            month = 12
            year -= 1

        query = '''SELECT b.email, COUNT(b.email) num_of_ticket
                    FROM booking_agent b, ticket t, purchases p
                    WHERE p.booking_agent_id = b.booking_agent_id
                    AND p.ticket_id = t.ticket_id
                    AND t.airline_name = %s
                    AND MONTH(p.purchase_date) = %s
                    AND YEAR(p.purchase_date) = %s
                    GROUP BY b.email
                    ORDER BY num_of_ticket DESC
                    LIMIT 5;'''
        cursor.execute(query,(airline_name,month,year))
        top5_ba_tickets_m = []
        c1xAxis_categories_email_m = []
        d = cursor.fetchall()
        for e in d:
            top5_ba_tickets_m.append(int(e["num_of_ticket"]))
            c1xAxis_categories_email_m.append(e["email"])

        # get top5 ba by tickets sold last year
        year = datetime.datetime.now().year - 1
        query = '''SELECT b.email, COUNT(b.email) num_of_ticket
                            FROM booking_agent b, ticket t, purchases p
                            WHERE p.booking_agent_id = b.booking_agent_id
                            AND p.ticket_id = t.ticket_id
                            AND t.airline_name = %s
                            AND YEAR(p.purchase_date) = %s
                            GROUP BY b.email
                            ORDER BY num_of_ticket DESC
                            LIMIT 5;'''
        cursor.execute(query, (airline_name,year))
        top5_ba_tickets_y = []
        c1xAxis_categories_email_y = []
        d = cursor.fetchall()
        for e in d:
            top5_ba_tickets_y.append(int(e["num_of_ticket"]))
            c1xAxis_categories_email_y.append(e["email"])

        #get top5 ba by commission earned last year
        query = '''SELECT b.email, SUM(f.price*0.1) commission
                        FROM flight f, purchases p, booking_agent b, ticket t
                        WHERE b.booking_agent_id = p.booking_agent_id
                        AND p.ticket_id = t.ticket_id
                        AND (t.airline_name,t.flight_num) = (f.airline_name,f.flight_num)
                        AND YEAR(p.purchase_date) = %s
                        AND t.airline_name = %s
                        GROUP BY b.email
                        ORDER BY commission DESC
                        LIMIT 5;'''
        cursor.execute(query,(year,airline_name))
        d = cursor.fetchall()
        top5_ba_commission = []
        c2xAxis_categories_email = []
        for e in d:
            top5_ba_commission.append(float(e["commission"]))
            c2xAxis_categories_email.append(e["email"])
        cursor.close()
        return render_template("staffViewBA.html",username= username,
                               top5_ba_tickets_m = top5_ba_tickets_m,
                               c1xAxis_categories_email_m = c1xAxis_categories_email_m,
                               top5_ba_tickets_y = top5_ba_tickets_y,
                               c1xAxis_categories_email_y = c1xAxis_categories_email_y,
                               top5_ba_commission = top5_ba_commission,
                               c2xAxis_categories_email	 = c2xAxis_categories_email,
                               )
    else:
        return redirect(url_for("index"))

@app.route('/view', )
def view():
    return render_template("view.html")


@app.route("/staffViewCustomers",methods = ["GET"])
def staffViewCustomers():
    if session.get("username"):
        username = session["username"]
        if check_empty(username):
            return "Bad Session"

        year = datetime.datetime.now().year 
        query = '''SELECT c.name,p.customer_email,COUNT(*) ticket_num
                    FROM purchases p , ticket t,customer c
                    WHERE p.ticket_id = t.ticket_id
                    AND c.email = p.customer_email
                    AND t.airline_name = (SELECT airline_name FROM airline_staff WHERE username = %s)
                    AND YEAR(p.purchase_date) = %s
                    GROUP BY p.customer_email
                    ORDER BY ticket_num DESC
                    LIMIT 1;'''
        cursor = mysql.cursor()
        cursor.execute(query,(username,year))
        most_frequent_cust = {}
        d = cursor.fetchone()
        cursor.close()
        if d:
            most_frequent_cust["email"] = d["customer_email"]
            most_frequent_cust["name"] = d["name"]
        else:
            most_frequent_cust["email"] = None
            most_frequent_cust["name"] = None

        return render_template("staffViewCustomers.html", username = username,
                               most_frequent_cust = most_frequent_cust)
    else:
        return redirect(url_for("index"))

@app.route("/staffProcessCustomers",methods = ["POST","GET"])
def staffProcessCustomers():
    if session.get("username"):
        try:
            username = session["username"]
            customer_email = request.form["customer_email"]
        except:
            return "Bad form"

        if check_empty(username,customer_email):
            return "Bad Form"

        query = '''SELECT distinct f.airline_name,f.flight_num,departure_airport,departure_time,
                    arrival_airport,arrival_time,price,status 
                    FROM flight f, ticket t, purchases p
                    WHERE (t.airline_name,t.flight_num) = (f.airline_name,f.flight_num)
                    AND p.ticket_id = t.ticket_id
                    AND p.customer_email = %s
                    AND f.airline_name = (SELECT airline_name FROM airline_staff 
                                          WHERE username = %s); '''
        cursor = mysql.cursor()
        try:
            cursor.execute(query,(customer_email,username))
        except:
            return "Customer email does not exist!"

        d = cursor.fetchall()
        cursor.close()
        res = []
        for e in d:
            temp = e
            temp["arrival_time"] = str(e["arrival_time"])
            temp["departure_time"] = str(e["departure_time"])
            temp["price"] = float(e["price"])
            res.append(temp)

        return jsonify({"data":res})
    else:
        return redirect(url_for("index"))

@app.route('/pie1', methods=[ "GET"])
def pie1():
    if session.get("username"):
        # if check_empty(username):
        #     return "Bad Session"

        query1 = '''SELECT A.direct, B.indirect FROM (SELECT sum(D.ticketcnt*F.price) AS direct FROM (SELECT count(t.ticket_id) as ticketcnt,flight_num FROM ticket t JOIN flight USING (flight_num) WHERE t.ticket_id in (SELECT ticket_id FROM purchases WHERE booking_agent_id IS Null AND purchase_date between DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) and CURRENT_DATE()) GROUP BY flight_num) D JOIN flight F USING(flight_num)) A, (SELECT sum(D.ticketcnt*F.price) AS indirect FROM (SELECT count(t.ticket_id) as ticketcnt,flight_num FROM ticket t JOIN flight USING (flight_num) WHERE t.ticket_id in (SELECT ticket_id FROM purchases WHERE booking_agent_id IS NOT Null AND purchase_date between DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) and CURRENT_DATE()) GROUP BY flight_num) D JOIN flight F USING(flight_num)) B'''
        
        cursor = mysql.cursor()
        cursor.execute(query1)
        d1 = cursor.fetchall()
        cursor.close()
        
 

        values = [int(d1[0]['direct']) if d1[0]['direct'] else 0,int(d1[0]['indirect']) if d1[0]['indirect'] else 0]
        labels = ['direct income','indirect income']
        colors = [
            "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
            "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
            "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

        return render_template('pie.html', title='Revenue from last 30 days', max=17000, set=zip(values, labels, colors))

@app.route('/pie2', methods=[ "GET"])
def pie2():
    if session.get("username"):
        # if check_empty(username):
        #     return "Bad Session"

        query1 = '''SELECT A.direct, B.indirect FROM (SELECT sum(D.ticketcnt*F.price) AS direct FROM (SELECT count(t.ticket_id) as ticketcnt,flight_num FROM ticket t JOIN flight USING (flight_num) WHERE t.ticket_id in (SELECT ticket_id FROM purchases WHERE booking_agent_id IS Null AND purchase_date between DATE_SUB(CURRENT_DATE(), INTERVAL 365 DAY) and CURRENT_DATE()) GROUP BY flight_num) D JOIN flight F USING(flight_num)) A, (SELECT sum(D.ticketcnt*F.price) AS indirect FROM (SELECT count(t.ticket_id) as ticketcnt,flight_num FROM ticket t JOIN flight USING (flight_num) WHERE t.ticket_id in (SELECT ticket_id FROM purchases WHERE booking_agent_id IS NOT Null AND purchase_date between DATE_SUB(CURRENT_DATE(), INTERVAL 365 DAY) and CURRENT_DATE()) GROUP BY flight_num) D JOIN flight F USING(flight_num)) B'''
        cursor = mysql.cursor()
        cursor.execute(query1)
        d1 = cursor.fetchall()
        cursor.close()
 

        values = [int(d1[0]['direct']) if d1[0]['direct'] else 0,int(d1[0]['indirect']) if d1[0]['indirect'] else 0]
        labels = ['direct income','indirect income']
        colors = [
            "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
            "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
            "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]
        return render_template('pie.html', title='Revenue from last year', max=17000, set=zip(values, labels, colors))

@app.route("/staffViewReport",methods = ["GET"])
def staffViewReport():
    if session.get("username"):
        username = session["username"]
        if check_empty(username):
            return "Bad Session"
        return render_template('staffViewReport.html')

@app.route("/top3y",methods = ["GET"])
def top3y():
    if session.get("username"):
        username = session["username"]
        if check_empty(username):
            return "Bad Session"

        query = "SELECT airline_name FROM airline_staff WHERE username = %s;"
        cursor = mysql.cursor()
        try:
            cursor.execute(query, username)
            airline_name = cursor.fetchone()["airline_name"]
        except:
            return "Your information has been removed from the database. Please contact your admin for further info."

        # get top3 destination last year
        last_year = datetime.datetime.now().year 
        query = '''SELECT airport_city, COUNT(*) traffic_num
                            FROM airport a, flight f,ticket t
                            WHERE a.airport_name = f.arrival_airport
                            AND (f.airline_name, f.flight_num) = (t.airline_name,t.flight_num)
                            AND f.status != "Cancelled"
                            AND f.airline_name = %s
                            AND year(f.arrival_time) = %s
                            AND t.ticket_id in (SELECT ticket_id FROM purchases)
                            GROUP BY airport_city
                            ORDER BY traffic_num DESC
                            LIMIT 3;'''
        cursor.execute(query, (airline_name, last_year))
        cursor.close()
        top3_destinations_y = cursor.fetchall()
        return render_template("reportResult.html",a=top3_destinations_y,b='ONE YEAR')
    
    else:
        return redirect(url_for("index"))





@app.route("/top6m",methods = ["GET"])
def top6m():
    if session.get("username"):
        username = session["username"]
        if check_empty(username):
            return "Bad Session"

        query = "SELECT airline_name FROM airline_staff WHERE username = %s;"
        cursor = mysql.cursor()
        try:
            cursor.execute(query, username)
            airline_name = cursor.fetchone()["airline_name"]
        except:
            return "Your information has been removed from the database. Please contact your admin for further info."
        # get top3 destination during last 6 months
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        endmark = datetime.date(year, month, 1)
        endmark = str(endmark) + " 00:00:00"
        month -= 6
        if month <= 0:
            month += 12
            year -= 1
        startmark = datetime.date(year, month, 1)
        startmark = str(startmark) + " 00:00:00"
        query = '''SELECT airport_city, COUNT(*) traffic_num
                                    FROM airport a, flight f, ticket t
                                    WHERE a.airport_name = f.arrival_airport
                                    AND (f.airline_name, f.flight_num) = (t.airline_name, t.flight_num)
                                    AND f.status != "Cancelled"
                                    AND f.airline_name = %s
                                    AND f.arrival_time < %s
                                    AND f.arrival_time >= %s
                                    AND t.ticket_id in (SELECT ticket_id FROM purchases)
                                    GROUP BY airport_city
                                    ORDER BY traffic_num DESC
                                    LIMIT 3;'''
        cursor.execute(query, (airline_name, endmark, startmark))
        cursor.close()
        top3_destinations_m = cursor.fetchall()
        return render_template("reportResult.html",a=top3_destinations_m,b='6 MONTHS')
    else:
        return redirect(url_for("index"))


@app.route("/monthTicket",methods = ["GET"])
def monthTicket():
    if session.get("username"):
        username = session["username"]
        if check_empty(username):
            return "Bad Session"

        query = "SELECT airline_name FROM airline_staff WHERE username = %s;"
        cursor = mysql.cursor()
        try:
            cursor.execute(query, username)
            airline_name = cursor.fetchone()["airline_name"]
        except:
            return "Your information has been removed from the database. Please contact your admin for further info."
        #get month-wise tickets sold num
        query = '''SELECT COUNT(t.ticket_id) total_ticket_num
                    FROM ticket t, purchases p
                    WHERE airline_name = (SELECT airline_name FROM airline_staff WHERE username = %s)
                    AND t.ticket_id = p.ticket_id
                    AND YEAR(p.purchase_date) = %s
                    AND MONTH(p.purchase_date) = %s;'''
        xAxis_categories = []
        year = datetime.datetime.now().year 
        monthly_ticket_breakdown = []
        for i in range(1,13):
            cursor.execute(query,(username,year,i))
            ticket_num = cursor.fetchone()["total_ticket_num"]
            if not ticket_num:
                ticket_num = 0
            xAxis_categories.append("%s-%s"%(year,i))
            monthly_ticket_breakdown.append(ticket_num)
        #ttl TIcket    
        query = '''SELECT COUNT(t.ticket_id) total_ticket_num
                    FROM ticket t, purchases p
                    WHERE airline_name = (SELECT airline_name FROM airline_staff WHERE username = %s)
                    AND t.ticket_id = p.ticket_id
                    AND YEAR(p.purchase_date) = %s;'''
        cursor.execute(query,(username,year))
        total_ticket_num = cursor.fetchone()["total_ticket_num"]
        if not total_ticket_num:
            total_ticket_num = 0
        cursor.close()
        return render_template("bar.html",title='Ticket Amount By Month', a=total_ticket_num, max=10, labels=xAxis_categories,values=monthly_ticket_breakdown)
    else:
        return redirect(url_for("index"))



if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
