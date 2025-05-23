import flask
import mysql.connector
import random
from flask import Flask, render_template, request, redirect, session, url_for, flash
#####################################################################################################################################
app= flask.Flask('app')
mydb = mysql.connector.connect(
    host = "instructor-1.cq4bugepeexy.us-east-1.rds.amazonaws.com",
    user = "admin",
    password = "testpass",
    database = "university"
)

app.secret_key = "pass"

# Searching for students in the database


################################################ LANDING PAGE ###############################################
@app.route('/',methods = ['GET','POST'])
def landing_page():
    return render_template('landingpage.html')

################################################  Applicant Register  ################################################
# The Page thjat allows for the applicant to create an account to access apply to the university 
######################################################################################################################

@app.route('/ApplicantRegister', methods=['GET', 'POST'])
def ApplicantRegister():

    cursor = mydb.cursor(buffered=True, dictionary=True)
    
    if request.method == 'POST':

        email = request.form['email']
        password = request.form ['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        type  = request.form['type_user']
        address = request.form['address']
        ssn = request.form['ssn']
        
        
        cursor.execute("SELECT * FROM users WHERE ssn = %s Or email = %s" , (ssn,email))

        row = cursor.fetchone()
        
        if row is None:
            # We Are Generating A Random Integer That Will Represent The Applicant UID And Are Checking To See If The Number Generated Already Exists In The Database
            uid = random.randint(10000000,99999999)
            cursor.execute("SELECT * FROM users WHERE uid = %s",(uid,))
            uid_check = cursor.fetchone()
            while (uid_check != None):
                uid = random.randint(10000000,99999999)
                cursor.execute("SELECT * FROM users WHERE uid = %s",(uid,))
                uid_check = cursor.fetchone()
            
            cursor.execute(
                "Insert INTO users(uid,  email, password, firstname,lastname,address, type,ssn,  status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s, 'Not Started') ",
                ( uid, email, password, firstname, lastname, address, type, ssn )
                )
            
            mydb.commit()
            
            session['email'] = email 
            session['password'] = password
            session['firstname'] = firstname 
            session['lastname'] = lastname 
            session['adress'] = address 
            session['user_type'] = type 
            session['ssn'] = ssn
    
            
            return redirect ('/login')
        else:
            flash("  SSN or Email Is Already in use ")
        return render_template ('ApplicantRegister.html', x = 1)
    return render_template('ApplicantRegister.html')


################################################  Admin Can Crxeate Users  ################################################
# The Page allows for the System Administrator to create all types of users and insert them direectly into the databaase
###########################################################################################################################

@app.route('/createapplicant', methods=['GET', 'POST'])
def adminCreateApplicant():
    
    cursor = mydb.cursor(buffered=True, dictionary=True)
    

    cursor.execute("SELECT type FROM users WHERE type = %s", (session['user_type'], ))

    Authority = cursor.fetchone()

    if Authority is not None: 
        Permission = Authority['type']
    else:
        Permission = None
    if Permission != 'Systems Administrator':
            flash('You Do Not Have Authorized Access To This Form')
            return redirect ('/login')
        
    if request.method == 'POST':
        
        email = request.form['email']
        password = request.form ['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        address = request.form['address']
        ssn = request.form['ssn']
   
        
        cursor.execute("SELECT * FROM users WHERE ssn = %s Or email = %s" , (ssn,email))

        row = cursor.fetchone()
      
        if row is None:

            uid = random.randint(10000000,99999999)
            cursor.execute("SELECT * FROM users WHERE uid = %s",(uid,))
            uid_check = cursor.fetchone()
            while (uid_check != None):
                uid = random.randint(10000000,99999999)
                cursor.execute("SELECT * FROM users WHERE uid = %s",(uid,))
                uid_check = cursor.fetchone()

            cursor.execute(
                "Insert INTO users(uid, email, password, firstname,lastname,address, type, status, ssn) VALUES (%s,%s,%s,%s,%s,%s,%s,'Not Started',%s) "
                , ( uid, email, password, firstname, lastname, address, type, ssn)
                )
            mydb.commit()
         
            # #insert into faculty 
            
            session['email'] = email
            session['password'] = password
            session['firstname'] = firstname
            session['lastname'] = lastname 
            session['adress'] = address 
            session['user_type'] = type 
            session['ssn'] = ssn
            
            return redirect ('/login')
        else: 
            flash("  SSN or Email Is Already in use ")
        return render_template ('adminCreateApplicant.html', x = 1)
    return render_template('adminCreateApplicant.html')

@app.route('/generate_applicant_list/<ID>', methods=['GET', 'POST'])
def generate_applicant_list(ID):
    print('five')
    cursor = mydb.cursor(buffered=True, dictionary=True)
    print ( ID )
    if request.method == 'POST':
        print('one')
        semester = request.form['semester']
        print(semester)
        print('two')
        Appyear = request.form['appYear']
        print(Appyear)
        print('three')
        degreetype = request.form['degreeType']
        print(degreetype)
        # Perform the query in the database
       
        cursor.execute( "SELECT * FROM studentapplication WHERE semester = %s or appYear = %s or degreeType = %s and studentUID = %s", (semester, Appyear, degreetype, ID))
        generate = cursor.fetchall()
        print(generate)
        print("hahahahahhahahahahahhahahahahahahaa")
        return render_template("applicant_list.html", generate=generate)
    return render_template("generate_applicant_list.html", ID = ID)

@app.route('/generate_admitted_list/<ID>', methods=['GET', 'POST'])
def generate_admitted_list(ID):
    # cursor = mydb.cursor(buffered=True, dictionary=True)
    # if request.method == 'POST':
    #     print('one')
    #     semester = request.form['semester']
    #     print ('two')
    #     appyear = request.form['appYear']
    #     print('theee')
    #     degreetype = request.form['degreeType']
        
    #     # Perform the query in the database

    #     cursor.execute(" SELECT * FROM studentapplication WHERE semester = %s or appYear = %s or degreeType = %s studentUID = %s and status = 'Admit'", (semester,appyear,degreetype, ID, 'Admit'  ) )
        
    #     generate = cursor.fetchall()
    #     return render_template("admitted_list.html", generate=generate)
    # return render_template("generate_admitted_list.html", ID = ID )
  
    cursor = mydb.cursor(buffered=True, dictionary=True)
    if request.method == 'POST':
        semester = request.form['semester']
        appyear = request.form['appYear']
        degreetype = request.form['degreeType']
        
        # Perform the query in the database
        query = "SELECT * FROM studentapplication WHERE semester = %s OR appYear = %s OR degreeType = %s AND studentUID = %s AND status = 'Admit'"
        cursor.execute(query, (semester, appyear, degreetype, ID))
        
        generate = cursor.fetchall()
        return render_template("admitted_list.html", generate=generate)
    
    return render_template("generate_admitted_list.html", ID=ID)

@app.route('/generate_statistics/<ID>', methods=['GET', 'POST'])
def generate_statistics(ID):
    cursor = mydb.cursor(buffered=True, dictionary=True)
    print ('here')
    print ('here')
    if request.method == 'POST':
        print ('here')
        semester = request.form['semester']
        print ('here')
        appyear = request.form['appYear']
        print ('here')
        degreetype = request.form['degreeType']
        print ('here')
        
        # Query to retrieve statistics
        query = "SELECT COUNT(*) as total_applicants, SUM(CASE WHEN status = 'Admit' or 'Admit with Aid' THEN 1 ELSE 0 END) as total_admitted, " \
                "SUM(CASE WHEN status = 'Reject' THEN 1 ELSE 0 END) as total_rejected, " \
                "AVG(CASE WHEN status = 'Admit' or 'Admit with Aid' THEN GREAdvanced ELSE NULL END) as avg_gre_score, " \
                "AVG(CASE WHEN status = 'Admit' or 'Admit with Aid' THEN GREVerbal ELSE NULL END) as avg_gre_vscore, " \
                "AVG(CASE WHEN status = 'Admit' or 'Admit with Aid' THEN GREQuantitative ELSE NULL END) as avg_qgre_score " \
                "FROM studentapplication " \
                "WHERE semester = %s OR appYear = %s OR degreeType = %s AND studentUID =%s"
        cursor.execute(query, (semester, appyear, degreetype, ID))
        
        statistics = cursor.fetchone()
        return render_template("statistics.html", statistics=statistics, ID = ID)
    
    return render_template("generate_statistics.html")



################################################  Admin Can Create Students ################################################
# The Page allows for the System Administrator to create either a Masters or PhD student
#########################################################################################################################
@app.route('/createstudent', methods = ['GET', 'POST'])
def adminCreateStudent():
    #create a connection
    cursor = mydb.cursor(buffered=True, dictionary=True)
   
    #make sure that only the systems admin should be able to do this page 
    cursor.execute("SELECT type FROM users WHERE type = %s", (session.get('user_type'),))
    Authority = cursor.fetchone()
    
    if Authority is not None: 
        Permission = Authority['type']
    else:
        Permission = None
    if Permission != 'Systems Administrator':
            flash('You Do Not Have Authorized Access To This Form')
            return redirect ('/login')
    

    if request.method == 'POST':
        email = request.form['email']
        password = request.form ['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        address = request.form['address']
        ssn = request.form['ssn']
        enrolledas  = request.form['enrolledas']
        type = 'Student'

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        row = cursor.fetchone()

        if row is None:
            #hooray! a new user is made, time to create their uid
            uid = random.randint(10000000,99999999)
            temp = uid
            cursor.execute("SELECT * FROM users WHERE uid = (%s)",(temp,))
            uid_check = cursor.fetchone()
            while (uid_check != None):
                uid = random.randint(10000000,99999999)
                cursor.execute("SELECT * FROM users WHERE uid = (%s)",(uid,))
                uid_check = cursor.fetchone()

            #insert into users table
            cursor.execute(
                        "Insert INTO users(uid, email, password, firstname,lastname,address, type,status, ssn) VALUES (%s,%s,%s,%s,%s,%s,%s,NULL,%s) "
                        , ( uid, email, password, firstname, lastname, address, type, ssn)
                        )
            mydb.commit()
            #insert into student
        

            cursor.execute("insert into students(uid, advisor_id, enrolledas, suspended) VALUES (%s, %s, %s, %s)", (uid, None, enrolledas,0))
            mydb.commit()

    
            faculty_type = {}
            if session.get('faculty_type'):
                faculty_type = session.get('faculty_type')

            return redirect(url_for('home', user_type = type, faculty_type = faculty_type))
        else: 
            return render_template ('adminCreateStudent.html', x = 1)
    return render_template('adminCreateStudent.html')



# ###############################  Admin Can Create Faculty ################################################

# The Page allows for the System Administrator to create an applicant
#########################################################################################################################
@app.route('/createfaculty', methods = ['GET', 'POST'])
def adminCreateFaculty():
        #create a connection
    cursor = mydb.cursor(buffered=True, dictionary=True)
    print(session.get('user_type'))
    #make sure that only the systems admin should be able to do this page 
    cursor.execute("SELECT type FROM users WHERE type = %s", (session.get('user_type'),))
    Authority = cursor.fetchone()
    
    if Authority is not None: 
        Permission = Authority['type']
    else:
        Permission = None
    if Permission != 'Systems Administrator':
            flash('You Do Not Have Authorized Access To This Form')
            return redirect ('/login')
    

    if request.method == 'POST':
        email = request.form['email']
        password = request.form ['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        address = request.form['address']
        ssn = request.form['ssn']
        type = 'Faculty'

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        row = cursor.fetchone()

        if row is None:
            #hooray! a new user is made, time to create their uid
            uid = random.randint(10000000,99999999)
            temp = uid
            cursor.execute("SELECT * FROM users WHERE uid = (%s)",(temp,))
            uid_check = cursor.fetchone()
            while (uid_check != None):
                uid = random.randint(10000000,99999999)
                cursor.execute("SELECT * FROM users WHERE uid = (%s)",(uid,))
                uid_check = cursor.fetchone()

            #insert into users table
            cursor.execute(
                        "Insert INTO users(uid, email, password, firstname,lastname,address, type, status, ssn) VALUES (%s,%s,%s,%s,%s,%s,%s,NULL,%s) "
                        , ( uid, email, password, firstname, lastname, address, type, ssn)
                        )
            mydb.commit()

            #types of faculty
            advisor = False
            grad_sec = False
            cac = False 
            reviewer = False 
            registrar = False
            #lets get the assigned role of each faculty
            type_list = request.form.getlist('type')
            if 'grad_sec' in type_list: 
                grad_sec = True
            if 'advisor' in type_list: 
                advisor = True
            if 'cac' in type_list: 
                cac = True 
            if 'reviewer' in type_list: 
                reviewer = True
            if 'registrar' in type_list: 
                register = True
            

            #now we must enter into the faculty table 
            cursor.execute("insert into faculty (uid, advisor, grad_sec, cac, reviewer, registrar) values (%s, %s, %s, %s, %s, %s)", (uid, advisor, grad_sec, cac, reviewer, registrar))
            mydb.commit()
            cursor.execute("select * from faculty")
            test = cursor.fetchall()
            print(test)
            faculty_type = {}
            if session.get('faculty_type'):
                faculty_type = session.get('faculty_type')
           
            return redirect(url_for('home', user_type = type, faculty_type = faculty_type))
        else: 
            return render_template ('adminCreateFaculty.html', x = 1)
    return render_template('adminCreateFaculty.html')
################################################ Applicant Dashboard  ##############################################################
# The Page Allows For the Applicant to get redirected so that there overall all status requirements to get completed gets displayed 
####################################################################################################################################

@app.route('/applicantDashboard/<ID>', methods=['GET', 'POST'])
def Applicant_Dashboard(ID):
    print ('there')
    cursor = mydb.cursor(dictionary=True)
    print(session.get('user_type'))
    if( (session.get('user_type') != 'Applicant') and (session.get('user_type') != 'Systems Administrator')):
        err_message = "You do not have access to this form bring up your clearance with Gordan"
        return render_template("error.html", err_message = err_message)

    # print('viewing review form:' + str(ID))
    # if session.get('user_type') != 'Applicant':
    #     print(session.get('user_type'))
    #     print ('theres')

    #     #user is not logged in so return all false
    #     return redirect('/')
    cursor = mydb.cursor(dictionary=True)


    # if 'uid' not in session:
    #     return redirect('/')
    
    print ('there')
    
    cursor.execute("SELECT status from users WHERE uid = %s", (session['id'],))
    print ('there')
    update = cursor.fetchall()
    print(update[0])
             
    if update:
        print ( update)
        cursor.execute("SELECT firstname , lastname FROM users WHERE uid = %s", (ID, ))
        names = cursor.fetchone()
             

        if update[0]['status'] == 'Not Started' or update[0]['status'] == 'Application Incomplete' or update[0]['status'] == 'Application Complete, Missing Transcript and Recomendation Letters' or update[0]['status'] == 'Application Complete, Missing Transcript and Recommendation Letters' or update[0]['status'] == 'Application, Transcript and Recomendation Letters Complete':
             print ('there')
             print ( 'there eksjdannds')
             test = ''
             print(update[0])
             
        elif update[0]['status'] == 'Admit' or 'Admit with Aid':
            test = ''
            print (update[0]['status'])
            print('SEKIE EE')
            AcceptedIntoUniversity = True
            print ('hence')
            print(AcceptedIntoUniversity)
            cursor.execute("SELECT rating FROM studentapplicationreviews WHERE studentUID = %s AND workerID = %s", (ID,session['id']))
            print(AcceptedIntoUniversity)
            exists = cursor.fetchone()
            print (exists)
            if exists != None:
                print('tooooooooo')
                paydeposit = True
            elif exists is None:
                print('no000000ssssssssss')
                paydeposit = False
                print(paydeposit)
                print("HHAHAAHAHAH")
                submittype = ''
                print('LOLOOL1')
                if request.method == 'POST' and 'submittype' in request.form:
                    
                    print('LOLOOL2')
                    submittype = request.form['admissionfinal']
                    print('LOLOOL3')
                print(paydeposit)
        ######### If Submitted Button Tupe Pushed was Save then it will Update the current responses but will contain the status of Incomplete therefore not allowing fr them to complete anything further than that ##################
                if submittype == 'Student':
                    print(submittype)
                    cursor.execute("UPDATE users SET type = 'Student' WHERE uid = %s", (ID,))
                    print('yuhyuh')
                    mydb.commit()
                    print('yuhyuh')
                    
                    
                if paydeposit:
                    cursor.execute("SELECT degreeType FROM studentapplication WHERE studentUID = %s", (ID,))
                    degree_type = cursor.fetchone()
                    print('poppy')
                    print(degree_type)
                    if degree_type is not None and degree_type['degreeType'] in ['Masters', 'PhD']:
                        print('KLKKKKKKKooooolllol')
                        cursor.execute("INSERT INTO students (uid, enrolledas) VALUES (%s, 'Student')", (ID,))
                        print('DEEEEEEZZZZZZZZZ')
                        mydb.commit()

            return render_template("ApplicantDashboard.html", update=update,names = names,  test=test, AcceptedIntoUniversity = AcceptedIntoUniversity, paydeposit = paydeposit)
       
                    
      
    cursor.execute("SELECT firstname , lastname FROM users WHERE uid = %s", (ID, ))
    names = cursor.fetchone()
    
    if 'email' in session:
        if not update :
            test  = 'Application Not Started'
        return render_template("ApplicantDashboard.html", update=update, test=test, names = names)
        
    return redirect('/login')
    
   # ###############################  Appl################################################
# The Page allows for the System Administrator to create an applicant
#########################################################################################################################

@app.route('/applicantPersonalInfo/<ID>')
def ApplicantPersonalInfo(ID):
    print(session.get(str(ID)))
    if session.get('user_type') != 'Applicant':
        print(session.get('user_type'))
        print ('theres')
    cursor = mydb.cursor(buffered=True, dictionary=True)
    #first get the student's name from the id 
    print('hey')
    print(session.get('id'))
    cursor.execute("SELECT * FROM users WHERE uid = %s", (ID, ))
    x = cursor.fetchone()
    print('hey')
    print ( x)

    return render_template("ApplicantPersonalinfo.html", x = x , ID = ID)

################################################  PERSONAL INFO APPLICANT UPDATE  ##############################################################
# Update the students personal info
##############################################################################################################################################
@app.route('/applicantPersonalInfo/<ID>/updates', methods=['POST'])
def update_applicant(ID):
    cursor = mydb.cursor(buffered=True, dictionary=True)

    # Update the users table
    print('hete')
    cursor.execute("UPDATE users SET firstname= %s , lastname= %s , email= %s  WHERE uid= %s ", 
                (    
        request.form['firstname'],
        request.form['lastname'],
        request.form['email'],
        ID
                )
               )
    mydb.commit()
    
    cursor.execute("SELECT firstname , lastname FROM users WHERE uid = %s", (ID, ))
    names = cursor.fetchone()
    

  
    cursor.execute("SELECT * FROM users WHERE uid=%s", (ID,))
    updated_row = cursor.fetchone()
    print(updated_row)
   # print("Updated row in users table:", updated_row)

    return redirect(url_for('Applicant_Dashboard', ID=ID, user_type = session['user_type'], names = names))


################################################ Applicant Requirments Page  ##############################################################
# The Page Allows For the Applicant to complete their requirements while tracking there progress when they either complete, did not finish 
# or have not started one of their requirements
###########################################################################################################################################

@app.route('/Apprequirements')
def Applicant_Requirements(): 
    print ('hi')
    if session.get('id') == None:
        print("Not in databse bozo ")
        print(session.get('id'))

        return redirect('/')
    print(session.get('id'))
    
    cursor = mydb.cursor( buffered= True, dictionary=True)
    
    if 'email' in session:

        cursor.execute("SELECT status FROM users WHERE uid = %s", (session['id'], ))
        status = cursor.fetchone()
        if status is not None: 
            print ('two')
            print (status['status'] )
            if status['status'] == 'Application, Transcript and Recomendations Complete':
                cansubmit = True
            elif status['status'] == 'Admit':
                cansubmit = False
                cursor.execute("SELECT decision, recommendedadvisor FROM studentapplication WHERE studentUID = %s", (session['id'],))
                app = cursor.fetchone()
                cursor.close()
                return render_template("Apprequirements.html", status = status,cansubmit = cansubmit, app = app)
            else:
                cansubmit = False
                print('tjusas')
                cursor.close()
                return render_template("Apprequirements.html", status = status,cansubmit = cansubmit, app = None)
        else: 
            cursor.close() 
            
    return redirect('/applicantDashboard/<ID>')


################################################ Applicant Requirements Submission  ##############################################################
# The Page Allows For the Applicant to submit their requirments when they have completed both there recommendations and there application
# Whilee flashing messages iff an applicant treis to continue to the next part without completeing their previou assignment
###################################################################################################################################################

@app.route('/Apprequirements/submit', methods=['GET', 'POST'])
def Applicant_Requirements_Submit(): 
   
    cursor = mydb.cursor(dictionary=True)
    if session.get('id') == None:
        return redirect('/')
    print ('twosee')
    if request.method == 'POST':
        
        cursor.execute("SELECT status FROM users WHERE uid = %s", (session['id'], ))

        st = cursor.fetchone()
        status = st['status']
        print('status: ' + str(status))
        
        if status == 'Not Started':
            flash('You must start your Application and submit atleast one rec letter.')
            print('t')
            return redirect ('/Apprequirements')
        
        elif status == 'Application Incomplete':
            flash('You must finish your Application and submit atleast one rec letter.')
            return redirect ('/Apprequirements')
        
        elif status == 'Application Complete, Missing Transcript and Recomendation Letters':
            flash("Cannot submit Application is complete but missing Transcript and  Recomendation letters!")
            return redirect ('/Apprequirements')
        
        elif status == 'Application and Transcript Complete but Missing Recomendation Letter':
            flash("\\Application and Transcript is complete but missing Recomendation letters!")
            print("say")
            return redirect ('/Apprequirements')
        
        elif status == 'Submitted':
            flash("Cannot submit Application more than Once!")
            return redirect ('/Apprequirements')
        
        elif status == 'Application, Transcript and Recomendations Complete':
            
            cursor.execute("UPDATE users SET status = 'Submitted' WHERE uid = %s", (session['id'],))
            mydb.commit()
            cursor.execute("UPDATE studentapplication SET status 'Application Complete and Under Review'")
            flash('Your application has been submitted and is now under review!.')
            
            return redirect ('/Apprequirements')
        
    return redirect(url_for('Applicant_Dashboard', ID = session['id'],user_type = session['user_type']))



################################################ Application Page   ##############################################################
# The Page Allows For the Applicant Appplication to get tracked, if a application has not been started or has not been fully completed, 
# the applicant will not be able to complete there rec letters therefore causing them to go back and complete the missing fields. 
#  However when an applicant submits there application they can no longer change there responses as it will then go under review 
# by the workers that have the ability to do so in our database
# Each specfic limitation containing a flash that willm be displayed to the Applicant when a wrong act was completed 
###################################################################################################################################################

@app.route('/application', methods=['GET', 'POST'])
def application():
    
    if session.get('id') == None:
        return redirect('/')
    print('hi sir')
    
    cursor = mydb.cursor(buffered=True, dictionary=True)
    
    print (session.get('id'))
    

    cursor.execute("SELECT status FROM users WHERE uid = %s", (session['id'], ))

    

    st = cursor.fetchone()
    status = st['status']
    print('status: ' + str(status))
    
    
    if status == 'Application Complete, Missing Transcript and Recomendation Letters':
        flash("Cannot view application after you submitted it ")
        return redirect ('/Apprequirements')
    
    elif status == 'Application and Transcript Complete but Missing Reccommendation Letter':
        flash("Cannot view application or transcript after you submitted it ")
        print('favio')
        return redirect ('/Apprequirements')

    
    elif status == 'Submitted':
        flash("Cannot view Application after submission")
        return redirect ('/Apprequirements')
    
    elif status == 'Application and Transcript Complete but Missing Recomendation Letters':
        flash("Cannot view application after you submitted it ")
        return redirect ('/Apprequirements')

    elif status == 'Application, Transcript and Recomendation Letters Complete':
        flash(flash("Cannot view Application after submission"))
        return redirect ('/Apprequirements')
    

    if session.get('id') != False:
        cursor.execute("""  SELECT * FROM studentapplication WHERE studentUID = %s""", (session['id'], ))

        
        test = cursor.fetchone()
    
        if test == None: 
            tests = 'Application Not Started'
            return render_template("Application.html" , tests = tests, app = None)
        
       
        if test['status'] == 'Application Incomplete':
             return render_template("Application.html", app = test)
         
        if test['status'] == 'Admit':
            return render_template("Application.html")
        
        if test['status'] == 'Rejected':
            return render_template("Application.html")
        
        if test['status'] == "Application Complete and Under Review" : 
            flash("Application Already submitted under Student ID ")
            return redirect ('/Apprequirements')
        
        if test['status'] == "Application Incomplete" :
            flash("Application Already submitted under Student ID ")
            return redirect ('/Apprequirements')

        
    
    return render_template("Application.html"  )


######################################## View Application Page  #########################################################################################
#The Page allows for the user to view tfeileds they inputed for there application 
#################################################################################################################################################################

@app.route('/viewapplication', methods=['GET', 'POST'])
def ViewApplication():
    if session.get('id') == None:
        print(session.get('id'))
        return redirect('/')
     
    
    cursor = mydb.cursor(buffered=True, dictionary=True)
    cursor.execute("SELECT status FROM users WHERE  uid = %s", ( session['id'], ))
    r = cursor.fetchone()
    st = r['status']
    print(r)
    print('hereerererere')
    print (st)
    if st == 'Application Complete' or st == 'Application Complete, Missing Transcript and Recomendation Letters' or st ==  'Application and Transcript Complete but Recomendation Letters' or st == 'Application and Transcript Complete, but Recomendation Letters' or  st == 'Application, Transcript, and Recomendation Letters Complete' :
        print (st)
        cursor.execute( " SELECT * FROM studentapplication")
        print('here')
        information = cursor.fetchall()
        return render_template("viewApplication.html", information = information)
    
    elif st == 'Not Started' or st == 'None' or st == '' or st == 'Admit' or st == 'Admit With Aid' or st == 'Admit with Aid' or st == 'Reject': 
        print('there')
        flash("Complete Application Before You Can View IT")
        return redirect ('/Apprequirements')
    else: 
        print ('hiis')
        flash("Complete Application Before You Can View IT")
    return redirect ('/Apprequirements')
        

######################################## View Application Page  #########################################################################################
#The Page allows for the user to view tfeileds they inputed for there application 
#################################################################################################################################################################

@app.route('/editapplication', methods=['GET', 'POST'])
def EditApplication():
    print ('YEEEEEEEHAAAAAWWWWWWWWWASSAS')
    if session.get('id') == None:
        print(session.get('id'))
        return redirect('/')
    
    cursor = mydb.cursor(buffered=True, dictionary=True)
    cursor.execute("SELECT status FROM users WHERE  uid = %s", ( session['id'], ))
    r = cursor.fetchone()
    st = r['status']
    print (st)
    cursor.execute("SELECT * FROM studentapplication WHERE studentUID = %s", (session['id'],))
    app =cursor.fetchall()
    if st == 'Application and Transcript Complete but Missing Reccommendation Letter' or    st == 'Application Complete' or  st =='Application Complete, Missing Transcript and Recomendation Letters' or  st =='Application and Transcript Complete but Recomendation Letters' or  st =='Application and Transcript Complete, but Recomendation Letters' or  st =='Application, Transcript, and Recomendation Letters Complete' or   st =='Application and Transcript Complete but Missing Reccommendation Letter' :
        if request.method == 'POST':
            
            update_fields = {}
            update_values = []
            
            # Check each field and add it to the update_fields dictionary if a value was provided
            if 'firstname' in request.form:
                update_fields['firstname'] = 'firstname=%s'
                update_values.append(request.form['firstname'])
            if 'lastname' in request.form:
                update_fields['lastname'] = 'lastname=%s'
                update_values.append(request.form['lastname'])
            if 'gender' in request.form:
                update_fields['gender'] = 'gender=%s'
                update_values.append(request.form['gender'])
            if 'address1' in request.form:
                update_fields['addressline1'] = 'addressline1=%s'
                update_values.append(request.form['address1'])
            if 'zipcode' in request.form:
                update_fields['zipcode'] = 'zipcode=%s'
                update_values.append(request.form['zipcode'])
            if 'datesubmitted' in request.form:
                update_fields['datesubmitted'] = 'datesubmitted=%s'
                update_values.append(request.form['datesubmitted'])
            if 'semester' in request.form:
                update_fields['semester'] = 'semester=%s'
                update_values.append(request.form['semester'])
            if 'appYear' in request.form:
                update_fields['appYear'] = 'appYear=%s'
                update_values.append(request.form['appYear'])
            if 'areasofinterest' in request.form:
                update_fields['areasofinterest'] = 'areasofinterest=%s'
                update_values.append(request.form['areasofinterest'])
            if 'experience' in request.form:
                update_fields['experience'] = 'experience=%s'
                update_values.append(request.form['experience'])
            if 'priordegrees' in request.form:
                update_fields['priordegrees'] = 'priordegrees=%s'
                update_values.append(request.form['priordegrees'])
            if 'gpa' in request.form:
                update_fields['gpa'] = 'gpa=%s'
                update_values.append(request.form['gpa'])
            if 'major' in request.form:
                update_fields['major'] = 'major=%s'
                update_values.append(request.form['major'])
            if 'gradyear' in request.form:
                update_fields['gradyear'] = 'gradyear=%s'
                update_values.append(request.form['gradyear'])
            if 'university' in request.form:
                update_fields['university'] = 'university=%s'
                update_values.append(request.form['university'])
            if 'degreetype' in request.form:
                update_fields['degreetype'] = 'degreetype=%s'
                update_values.append(request.form['degreetype'])
            if 'GREVerbal' in request.form:
                update_fields['GREVerbal'] = 'GREVerbal=%s'
                update_values.append(request.form['GREVerbal'])
            if 'GREAdvanced' in request.form:
                update_fields['GREAdvanced'] = 'GREAdvanced=%s'
                update_values.append(request.form['GREAdvanced'])
            if 'GRESubject' in request.form:
                update_fields['GRESubject'] = 'GRESubject=%s'
                update_values.append(request.form['GRESubject'])
            if 'GREQuantitative' in request.form:
                update_fields['GREQuantitative'] = 'GREQuantitative=%s'
                update_values.append(request.form['GREQuantitative'])
            if 'GREYear' in request.form:
                update_fields['GREYear'] = 'GREYear=%s'
                update_values.append(request.form['GREYear'])
            if 'TOEFLscore' in request.form:
                update_fields['TOEFLscore'] = 'TOEFLscore=%s'
                update_values.append(request.form['TOEFLscore'])
            if 'TOEFLdate' in request.form:
                update_fields['TOEFLdate'] = 'TOEFLdate=%s'
                update_values.append(request.form['TOEFLdate'])
            
            # Prepare the SET clause for updating specific fields
            set_clause = ', '.join(update_fields.values())
            
            # Construct the update query
            update_query = "UPDATE studentapplication SET " + set_clause + " WHERE studentUID=%s"
            
            # Add the studentUID to the update_values list
            update_values.append(session['id'])
            
            # Execute the update query
            cursor.execute(update_query, update_values)
            mydb.commit()
       
          
            
            # cursor.execute(
            #     "UPDATE studentapplication SET gender=%s, addressline1=%s, zipcode=%s,  datesubmitted=%s, semester=%s, appYear=%s, areasofinterest=%s, experience=%s, priordegrees=%s, gpa=%s, major=%s, gradyear=%s, university=%s, degreetype=%s, GREVerbal=%s, GREAdvanced=%s, GRESubject=%s, GREQuantitative=%s, GREYear=%s, TOEFLscore=%s, TOEFLdate=%s, firstname=%s, lastname=%s WHERE studentUID=%s", (gender, address1, zipcode, datesubmitted, semester, applicationyear, areasofinterest, experience, priordegrees, gpa, major, gradyear, university, degreetype, GREVerbal, GREAdvanced, GRESubject, GREQuantitative, GREYear, TOEFLscore, TOEFLdate, firstname, lastname, session['id'])
            # )
            
            # mydb.commit()
            submittype = request.form['submittype']
            if submittype == 'Save':
                cursor.execute("UPDATE users SET status = status WHERE uid = %s", (session['id'],))
                flash('Application Successfully Updated')
            
        
        print( 'hey')
        sapp = st
        print (app)
        
        return render_template("editApplication.html",app = app,  sapp = sapp)
    else: 
        flash("Cannot Update Application")
    return redirect ('/Apprequirements')

    

######################################## Application Confirmation Page  #########################################################################################
# The Page Allows For submission of fields in the application is requested so that it could be inserted into the respected fields in the database
# Where when an Applicant submits an incomplete application they are able to update there response when they go back in and submit there application fully
#################################################################################################################################################################

@app.route('/confirmation', methods=['GET', 'POST'])
def confirmation(): 
    
    if session.get('id') == None:
        return redirect('/')
    
    cursor = mydb.cursor(buffered=True, dictionary=True)

    if request.method == 'POST':

        firstname = request.form['firstname']
        lastname = request.form['lastname']
        gender = request.form['gender']
        address1 = request.form['address1']
        zipcode = request.form['zipcode']
        datesubmitted = request.form['datesubmitted']
        semester = request.form['semester']
        applicationyear= request.form['applicationyear']
        areasofinterest = request.form['aoi']
        experience = request.form['expo']
        priordegrees = request.form['priordegrees']
        gpa = request.form['gpa']
        major = request.form['major']
        gradyear = request.form['gradyear']
        university = request.form['university']
        degreetype = request.form['degreetype']
        GREVerbal= request.form['GREVerbal']
        GREAdvanced= request.form['GREAdvanced']
        GRESubject= request.form['GRESubject']
        GREQuantitative= request.form['GREQuantitative']
        GREYear= request.form['GREYear']
        status = 'Application Incomplete'
        studentstatus = ''
        TOEFLscore= request.form['TOEFLScore']
        TOEFLdate= request.form['TOEFLdate']
        
        
        cursor.execute( 
            "INSERT INTO studentapplication (studentUID,    gender,addressline1, zipcode, status, datesubmitted,  semester,appYear,        areasofinterest, experience, priordegrees, gpa, major, gradyear, university, degreetype, GREVerbal, GREAdvanced, GRESubject,GREQuantitative, GREYear, TOEFLscore, TOEFLdate, firstname, lastname ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)",
                                            (session['id'],gender,address1,     zipcode, status, datesubmitted,  semester,applicationyear,areasofinterest, experience,  priordegrees, gpa, major, gradyear, university, degreetype ,GREVerbal, GREAdvanced, GRESubject,GREQuantitative, GREYear, TOEFLscore, TOEFLdate, firstname, lastname )

            )
        

        ###############################################################################
        # Implementing the functionality of my button type onto the form
        ###############################################################################
        submittype = request.form['submittype']
        ######### If Submitted Button Tupe Pushed was Save then it will Update the current responses but will contain the status of Incomplete therefore not allowing fr them to complete anything further than that ##################
        if submittype == 'Save':
            status = 'Application Incomplete'
            studentstatus ='Application Incomplete'
            cursor.execute("UPDATE users SET status = 'Application Incomplete' WHERE uid = %s", (session['id'],))
            
        ######### If Submit type button pushed was Submit then It will Insert the neccessary value if  any field required for the Phd Or MS is left blank the application will be submitted however will contain the status of Incomplete unless they compete all of the neccessary required fields ##################
        if submittype == 'Submit':
            cursor.execute( " SELECT * FROM studentapplication")
            fetched = cursor.fetchall()
            print(fetched)
            if fetched[0]['degreeType'] == 'Masters':

                
                if gender == '' or address1 == '' or zipcode == '' or datesubmitted == '' or semester == '' or applicationyear == '' or areasofinterest == '' or  experience == '' or priordegrees == '' or  gpa == '' or major == '' or gradyear == '' or university == '' or  TOEFLdate == '' or TOEFLscore == '':
                 cursor.execute("DELETE FROM studentapplication WHERE studentUID = %s", (session['id'], ))
                 studentstatus = 'Application Incomplete'  
                 print('1')
                 
                elif gender != '' or address1 != '' or zipcode != '' or datesubmitted != '' or semester != '' or applicationyear != '' or areasofinterest != '' or  experience != '' or priordegrees != '' or  gpa != '' or major != '' or gradyear != '' or university != '' or  TOEFLdate != '' or TOEFLscore != '':
                 studentstatus = 'Application Complete, Missing Transcript and Recomendation Letters'
                 print('11')
            if fetched[0]['degreeType'] == 'PhD':
                 
                 if gender == '' or address1 == '' or zipcode == '' or datesubmitted == '' or semester == '' or applicationyear == '' or areasofinterest == '' or  experience == '' or priordegrees == '' or  gpa == '' or major == '' or gradyear == '' or university == '' or  TOEFLdate == '' or TOEFLscore == '' or GREVerbal == '' or GREAdvanced == '' or GREQuantitative == '' or GRESubject == '' or GREYear == '':
                  cursor.execute("DELETE FROM studentapplication WHERE studentUID = %s", (session['id'], ))
                  studentstatus = 'Application Incomplete' 
                  print('2')
                 
                 elif gender != '' or address1 != '' or zipcode != '' or datesubmitted != '' or semester != '' or applicationyear != '' or areasofinterest != '' or  experience != '' or priordegrees != '' or  gpa != '' or major != '' or gradyear != '' or university != '' or  TOEFLdate != '' or TOEFLscore != '' or GREVerbal != '' or GREAdvanced != '' or GREQuantitative != '' or GRESubject != '' or GREYear != '':
                  studentstatus = 'Application Complete, Missing Transcript and Recomendation Letters'
                  print('22')
                  
       
        cursor.execute("UPDATE users SET status = %s WHERE uid = %s", (studentstatus,session['id'],))
        print( studentstatus)
        print('heyooooooooooo')

        mydb.commit()
                
        cursor.execute( "SELECT * FROM users ")
        
        information = cursor.fetchall()
    
        
        
        return render_template("AppConfirmation.html", information = information)

    
################################################  Transcript Page ################################################
#
###############################################################################################################

@app.route('/sendtranscript/')
def SendTranscript():
   
    print('sendtranscript/:')
    cursor = mydb.cursor(buffered=True, dictionary=True)


 
    cursor.execute("SELECT status FROM users WHERE uid = %s", (session['id'], ))
    st = cursor.fetchone()
    status = st['status']
    print('status: ' + str(status))
    if status == 'Not Started':
        flash('You must start your Application before submitting a Transcript !')
        return redirect ('/Apprequirements')
    elif status == 'Application Incomplete':
        flash('You must finish your Application before submitting your Transcript!')
        return redirect ('/Apprequirements')
    elif status == 'Application and Transcript Complete but Missing Reccommendation Letter':
        flash("Cannot view application or transcript after you submitted it ")
        print('favivvvvvo')
        return redirect ('/Apprequirements')
    elif status == 'Application, Transcript and Recomendation Letters Complete':
        flash("Cannot view application or transcript after you submitted it ")
        print('favivvvvvoszs')
        return redirect ('/Apprequirements')
    elif status == 'Submitted':
        flash("Cannot View Transcript After Sending It in")
        return redirect ('/Apprequirements')
        
        
    cursor.execute("""SELECT status from users WHERE uid = %s""", (int(session['id']),))
    status = cursor.fetchone()
    if status == 'Not started' or status == 'Application Incomplete':
        print('status error')
        return redirect(url_for('ApplicantRequirements'))
    else:
        print('logged in ')
        #user is logged in.
        #get sent recomendation lettters.
        cursor.execute(""" Select sender, senderemail FROM transcript where studentUID = %s""", (session['id'],))
        reqs = cursor.fetchall()
        print(len(reqs))
        if len(reqs) < 1:
            return render_template("sendtranscript.html",showRecomender = False, recrequest = None, requests= reqs, cansend= True)
        else:
            return render_template("sendtranscript.html",showRecomender = False, recrequest = None, requests= reqs, cansend= False)

################################################  Transcript Send Page ################################################
#
###############################################################################################################
@app.route('/sendtranscript/send', methods=['GET', 'POST'])
def TranscriptSubmit():
   
    print('sendtranscript/send:')
   
    cursor = mydb.cursor(buffered=True, dictionary=True)
    if request.method == 'POST':
        cursor.execute("SELECT firstname, lastname FROM users WHERE uid = %s",(session['id'], ))
        
        namequery = cursor.fetchone()
        print(namequery)
        name = namequery['firstname'] + ' ' + namequery['lastname']
        #submited a new letter
        recrequest = dict()
        recrequest['writername'] = request.form['writername']
        recrequest['email'] = request.form['writeremail']
        recrequest['title'] = request.form['writertitle']
        recrequest['affiliation'] = request.form['writeraffiliation']
        recrequest['sentfrom'] = name
        if session.get('id') == None:
            print('not logged in')
            #user is not logged in so return all false
            return render_template("sendtranscript.html",showRecomender = False, recrequest = None, requests= None, cansend= False)
        else:
            print('logged in ')
            #user is logged in.
            #get sent recomendation lettters.
            cursor.execute(""" Select sender, senderemail FROM transcript where studentUID = %s""", (session['id'],))
            reqs = cursor.fetchall()
            print('Reqs')
            print(reqs)
            if len(reqs) < 1:
                return render_template("sendtranscript.html",showRecomender = True, recrequest = recrequest, requests= reqs, cansend= True)
            else:
                return render_template("sendtranscript.html",showRecomender = True, recrequest = recrequest, requests= reqs, cansend= False)
    else:
        if session.get('id') == None:
            #user is not logged in so return all false
            return render_template("sendtranscript.html",showRecomender = False, recrequest = None, requests= None, cansend= False)
        else:
            #user is logged in.
            #get sent recomendation lettters.
            cursor.execute(""" Select sender, senderemail FROM transcript where studentUID = %s""", (session['id'],))
            reqs = cursor.fetchall()
            print('Reqs')
            print(reqs)
            if len(reqs) < 1:
                return render_template("sendtranscript.html",showRecomender = False, recrequest = None, requests= reqs, cansend= True)
            else:
                return render_template("sendtranscript.html",showRecomender = False, recrequest = None, requests= reqs, cansend= False)


################################################  Transcript Submit Page ################################################
#
###############################################################################################################
@app.route('/sendtranscript/submit/recomender', methods=['GET', 'POST'])
def transcriptsubmitrecommender():
  
    #takes in the recomenders page.
    cursor = mydb.cursor(buffered=True, dictionary=True)
    if request.method == 'POST':
        sender = request.form['writername']
        senderemail = request.form['writeremail']
        letter = request.form['recomendationresponce']
        title = request.form['writertitle']
        affiliation = request.form['writeraffiliation']
        cursor.execute("INSERT INTO transcript (studentUID, sender, senderemail, letter, title, affiliation) VALUES (%s, %s, %s, %s,%s,%s)",(session['id'], sender, senderemail, letter, title, affiliation))
        mydb.commit()
        cursor.execute("UPDATE users SET status = 'Application and Transcript Complete but Missing Reccommendation Letter' WHERE uid = %s", (session['id'],))
        mydb.commit()
        flash('Submited Successfully')
        print ("errorsers1")
        return redirect(url_for('SendTranscript'))
    return redirect(url_for('SendTranscript'))

################################################  Recommendations Page ################################################
#
###############################################################################################################

@app.route('/sendletters/')
def recomendations():
    print ('thesis ')
   
    print('sendletters/:')
    #showRecomender - true shows the recomender view to write the recomendation
    #recrequest - dict - 'writername' , 'email' , 'sentfrom'- student first and last name
    #requests - list of dicts with ['sender'] ['email'] of the recomendation letters
    #cansend - changes weather the send recomendation letter displays or not.
    cursor = mydb.cursor(buffered=True, dictionary=True)


    
    # if session.get('id') == None:
    #     print('not logged in')
    #     #user is not logged in so return all false
    #     return redirect('/')
        #return render_template("sendletters.html", showRecomender = False, recrequest = None, requests= None, cansend= False)

    cursor.execute("SELECT status FROM users WHERE uid = %s", (session['id'], ))
    st = cursor.fetchone()
    status = st['status']
    print('status: ' + str(status))
    print('GWWW --> GDUB')
    if status == 'Not Started':
        print ("1")
        flash('You must start your Application before submitting a Recommendation letter!')
        return redirect ('/Apprequirements')
    if status == 'Application Incomplete':
        print ("1")
        flash('You must finish your Application before submitting a Recommendation letter!')
        return redirect ('/Apprequirements')
    
    if status == 'Application Complete, Missing Transcript and Recomendation Letters':
        print('hees')
        flash('You must finish your Transcript Submission before submitting a Recommendation letter!')
        return redirect ('/Apprequirements')
    
    if status == 'Application Complete, Missing Transcript and Recommendation Letters':
        print('hoers')
        flash('You must finish your Transcript Submission before submitting a Recommendation letter!')
        return redirect ('/Apprequirements')
    
    if status == 'Submitted':
        print('hoert')
        flash("Cannot View recommendation letters after submitting")
        return redirect ('/Apprequirements')
        
        
    print('hoer')
    cursor.execute("""SELECT status from users WHERE uid = %s""", (int(session['id']),))
    print('hoses')
    status = cursor.fetchone()
    print(status)
    if status == 'Not started' or status == 'Application Incomplete' or status == 'Application Complete, Missing Transcript and Recomendation Letters': 
        print('status error')
        flash("Complete Application and Transcript Before You can Access your recommendations")
        return redirect(url_for('Applicant_Requirements'))
    else: 
        print ('heyser')
        print('logged in ')
        #user is logged in.
        #get sent recomendation lettters.
        cursor.execute(""" Select sender, senderemail FROM recommendationletters where studentUID = %s""", (session['id'],))
        reqs = cursor.fetchall()
        print(len(reqs))
        if len(reqs) < 3:
            print(len(reqs))
        
            return render_template("sendletters.html",showRecomender = False, recrequest = None, requests= reqs, cansend= True)
        else:
            flash ("You have completed " + str(len(reqs)) + " out of 3 Recommendations ")
        return redirect ('/Apprequirements')
    
################################################  Recommendations Send Page ################################################
#
###############################################################################################################
@app.route('/sendletters/send', methods=['GET', 'POST'])
def recomendationsubmit():
   
    print('sendletters/send:')
    #showRecomender - true shows the recomender view to write the recomendation
    #recrequest - dict - 'writername' , 'email' , 'sentfrom'- student first and last name
    #requests - list of dicts with ['sender'] ['email'] of the recomendation letters
    #cansend - changes weather the send recomendation letter displays or not.
    cursor = mydb.cursor(buffered=True, dictionary=True)
    if request.method == 'POST':
        cursor.execute("SELECT firstname, lastname FROM users WHERE uid = %s",(session['id'], ))
        
        namequery = cursor.fetchone()
        print(namequery)
        name = namequery['firstname'] + ' ' + namequery['lastname']
        print('submitted new letter request')
        #submited a new letter
        recrequest = dict()
        recrequest['writername'] = request.form['writername']
        recrequest['email'] = request.form['writeremail']
        recrequest['title'] = request.form['writertitle']
        recrequest['affiliation'] = request.form['writeraffiliation']
        recrequest['sentfrom'] = name
        if session.get('id') == None:
            print('not logged in')
            #user is not logged in so return all false
            return render_template("sendletters.html",showRecomender = False, recrequest = None, requests= None, cansend= False)
        else:
            print('logged in ')
            #user is logged in.
            #get sent recomendation lettters.
            cursor.execute(""" Select sender, senderemail FROM recommendationletters where studentUID = %s""", (session['id'],))
            reqs = cursor.fetchall()
            print('Reqs')
            print(reqs)
            if (len(reqs)+1)  < 3:
                return render_template("sendletters.html",showRecomender = True, recrequest = recrequest, requests= reqs, cansend= True)
            else:
                return render_template("sendletters.html",showRecomender = True, recrequest = recrequest, requests= reqs, cansend= False)
    else:
        if session.get('id') == None:
            #user is not logged in so return all false
            return render_template("sendletters.html",showRecomender = False, recrequest = None, requests= None, cansend= False)
        else:
            #user is logged in.
            #get sent recomendation lettters.
            cursor.execute(""" Select sender, senderemail FROM recommendationletters where studentUID = %s""", (session['id'],))
            reqs = cursor.fetchall()
            print('Reqs')
            print(reqs)
            if len(reqs) == 3:
                return render_template("sendletters.html",showRecomender = False, recrequest = None, requests= reqs, cansend= True)
            else:
                return render_template("sendletters.html",showRecomender = False, recrequest = None, requests= reqs, cansend= False)


################################################  Recommendations Submit Page ################################################
#
###############################################################################################################
@app.route('/sendletters/submit/recomender', methods=['GET', 'POST'])
def recomendationsubmitrecomender():
  
    #takes in the recomenders page.
    cursor = mydb.cursor(buffered=True, dictionary=True)
    if request.method == 'POST':
        sender = request.form['writername']
        senderemail = request.form['writeremail']
        letter = request.form['recomendationresponce']
        title = request.form['writertitle']
        affiliation = request.form['writeraffiliation']
        cursor.execute("INSERT INTO recommendationletters (studentUID, sender, senderemail, letter, title, affiliation) VALUES (%s, %s, %s, %s,%s,%s)",(session['id'], sender, senderemail, letter, title, affiliation))
        mydb.commit()
        
        cursor.execute(" SELECT COUNT(*) AS count_letter FROM recommendationletters WHERE studentUID = %s" ,(session['id'],))
        fetched = cursor.fetchone()
        count_letter = fetched['count_letter']
        if count_letter < 3:
            status = 'Appliicantion and Transcript Completed, issing Recommendation Letters'
            
        elif count_letter == 3: 
            status = "Application, Transcript and Recommendation Letters Completed"
        else: 
            print('kick rocks')
        cursor.execute("UPDATE users SET status = 'Application, Transcript and Recomendation Letters Complete' WHERE uid = %s", (session['id'],))
        mydb.commit()
        flash('Submited Successfully')
        return redirect(url_for('recomendations'))
    return redirect(url_for('recomendations'))

################################################  Applicant Search  ################################################
#
###############################################################################################################
@app.route('/applicantSearch', methods = ['POST'])
def applicantSearch():
    if( (session.get('user_type') != 'Systems Administrator') and (session.get('user_type') != 'Faculty')):
        err_message = "You do not have access to this form bring up your clearance with Gordan"
        return render_template("error.html", err_message = err_message)
    mydb = mysql.connector.connect(
        host = "instructor-1.cq4bugepeexy.us-east-1.rds.amazonaws.com",
        user = "admin",
        password = "testpass",
        database = "university"
    )
    cur = mydb.cursor()
    if request.method == 'POST':
        name = request.form["name"]
        cur.execute("SELECT uid, firstname, lastname FROM users WHERE type = 'Applicant' and (uid LIKE %s or firstname LIKE %s or lastname LIKE %s)",('%'+name+'%','%'+name+'%','%'+name+'%'))
        all_app = cur.fetchall()
        applicants = {}
        cnt = 0
        for app in all_app:
            applicants[cnt] = {'uid' : app[0], 'name' : app[1] + " "+app[2]}
            cnt=cnt+1
        if len(all_app)==0:
            applicants = None
        return render_template('app_search.html',applicants=applicants,name = name)
    return redirect(url_for('home'))
################################################  Pending Review  ################################################
# 
###############################################################################################################

@app.route('/pendingreview/')
def pending_review():
    
    cursor = mydb.cursor(buffered=True, dictionary=True)
    
    if session.get('id') == None:
        print('not logged in')
        #user is not logged in so return all false
        return redirect('/')
    
    
    if session.get('id') == None:
        print (' kick rockz')

        return render_template("apps_pend_review.html",rev= None)
    else:
        print('session ' + str(session['id']))

        print('session ' + str(session['id']))
        cursor.execute("""SELECT studentapplication.studentUID, studentapplication.firstname, studentapplication.lastname, studentapplication.studentUID FROM studentapplication
            LEFT JOIN studentapplicationreviews on studentapplication.studentUID  = studentapplicationreviews.studentUID 
            INNER JOIN users ON studentapplication.studentUID = users.uid
            WHERE NOT EXISTS (SELECT workerID FROM studentapplicationreviews WHERE workerID = %s AND studentUID = studentapplication.studentUID) AND users.status = 'Application, Transcript and Recomendation Letters Complete'
             """,(int(session['id']),))



         #cursor.execute("""SELECT studentapplication.studentUID, studentapplication.firstname, studentapplication.lastname, studentapplication.studentUID FROM studentapplication
         #   LEFT JOIN studentapplicationreviews on  studentapplication.studentUID  = studentapplicationreviews.studentUID
         #   WHERE studentapplicationreviews.workerID != %s """, (int(session['workerID']),))
  
       
        pend = cursor.fetchall()
        
        cursor.execute("""SELECT studentapplication.studentUID, studentapplication.firstname, studentapplication.lastname, studentapplication.studentUID FROM studentapplication
            LEFT JOIN studentapplicationreviews on  studentapplication.studentUID  = studentapplicationreviews.studentUID
            WHERE studentapplicationreviews.workerID != %s """, (int(session['id']),))


        prevreviewed = cursor.fetchall()

        
        return render_template("apps_pend_review.html", rev=pend,prevreviewed = prevreviewed)
    
################################################  Application Review Page ################################################
#
###############################################################################################################
@app.route('/appreview/<ID>', methods=['GET', 'POST'])
def appreview(ID):

    print('viewing review form:' + str(ID))
    cursor = mydb.cursor(buffered=True, dictionary=True)
    #get app from db
    cursor.execute("SELECT * FROM studentapplication WHERE studentUID = %s", (ID,))
    app = cursor.fetchone()
    print(app)
    cursor.execute("SELECT * FROM transcript WHERE studentUID = %s", (ID,))
    transcripts = cursor.fetchall()
    print(transcripts)
    #get letters from DB
    cursor.execute("SELECT * FROM recommendationletters WHERE studentUID = %s", (ID,))
    letters = cursor.fetchall()
    print(letters)
    #get reviews
    cursor.execute("SELECT * FROM studentapplicationreviews WHERE studentUID = %s", (ID,))
    reviews = cursor.fetchall()
    print(reviews)
    #get permissions
    cursor.execute("SELECT type FROM users WHERE uid = %s", (session['id'],))
    perms = cursor.fetchall()

    print(perms)

    if perms:
     print(perms[0]['type'])

     if perms[0]['type'] == 'Systems Administrator':
         print('System Adminstrator')
         canViewReviews = True
         canAddReview = True
         canChageStatus = True
     elif perms[0]['type'] == 'Faculty':
        cursor.execute("select * from faculty where uid = %s", (session['id'],))
        faculty = cursor.fetchall()
        print(faculty)
        # Grad Secretary -> Access 
        if faculty and len(faculty) <= 6 and faculty[0]['advisor'] == 0 and faculty[0]['grad_sec'] == 1 and faculty[0]['cac'] == 0 and faculty[0]['reviewer'] == 0 and faculty[0]['registrar'] == 0:
         canViewReviews = True
         canAddReview = True
         canChageStatus = True
        # registrar --> totally useless here lol
        elif faculty and len(faculty) <= 6 and faculty[0]['advisor'] == 0 and faculty[0]['grad_sec'] == 0 and faculty[0]['cac'] == 0 and faculty[0]['reviewer'] == 0 and faculty[0]['registrar'] == 1:
         canViewReviews = False
         canAddReview = False
         canChageStatus = False
        #  Chair Of Admissions Committee
        elif faculty and len(faculty) <= 6 and faculty[0]['advisor'] == 0 and faculty[0]['grad_sec'] == 0 and faculty[0]['cac'] == 1 and faculty[0]['reviewer'] == 0 and faculty[0]['registrar'] == 0:
         canViewReviews = True
         canAddReview = True
         canChageStatus = True
         #  Chair Of Admissions Committee
        elif faculty and len(faculty) <= 6 and faculty[0]['advisor'] == 0 and faculty[0]['grad_sec'] == 0 and faculty[0]['cac'] == 1 and faculty[0]['reviewer'] == 1 and faculty[0]['registrar'] == 0:
         canViewReviews = True
         canAddReview = True
         canChageStatus = True
         #  Chair Of Admissions Committee
        elif faculty and len(faculty) <= 6 and faculty[0]['advisor'] == 0 and faculty[0]['grad_sec'] == 0 and faculty[0]['cac'] == 1 and faculty[0]['reviewer'] == 1 and faculty[0]['registrar'] == 1:
         canViewReviews = True
         canAddReview = True
         canChageStatus = True
        elif faculty and len(faculty) <= 6 and faculty[0]['advisor'] == 1 and faculty[0]['grad_sec'] == 0 and faculty[0]['cac'] == 1 and faculty[0]['reviewer'] == 1 and faculty[0]['registrar'] == 1:
         canViewReviews = True
         canAddReview = True
         canChageStatus = True
        elif faculty and len(faculty) <= 6 and faculty[0]['advisor'] == 0 and faculty[0]['grad_sec'] == 0 and faculty[0]['cac'] == 0 and faculty[0]['reviewer'] == 0 and faculty[0]['registrar'] == 0:
         canViewReviews = False
         canAddReview = False
         canChageStatus = False
        elif faculty and len(faculty) <= 6 and faculty[0]['advisor'] == 1 and faculty[0]['grad_sec'] == 0 and faculty[0]['cac'] == 0 and faculty[0]['reviewer'] == 0 and faculty[0]['registrar'] == 0:
         canViewReviews = True
         canAddReview = True
         canChageStatus = True
        #  Reviewer 
        #  System Adminsitrator --> This is uneccessary 
        elif faculty and len(faculty) <= 6 and faculty[0]['advisor'] == 1 and faculty[0]['grad_sec'] == 1 and faculty[0]['cac'] == 1 and faculty[0]['reviewer'] == 1 and faculty[0]['registrar'] == 1:
         canViewReviews = True
         canAddReview = True
         canChageStatus = True
        #  Reviewer 
        elif faculty and len(faculty) <= 6 and faculty[0]['advisor'] == 0 and faculty[0]['grad_sec'] == 0 and faculty[0]['cac'] == 0 and faculty[0]['reviewer'] == 1 and faculty[0]['registrar'] == 0:
         canViewReviews = False
         canAddReview = True
         canChageStatus = False
        #  Advisor --> Unneccessary Serves no purpose in my code lol 
        elif faculty and len(faculty) <= 6 and faculty[0]['advisor'] == 1 and faculty[0]['grad_sec'] == 0 and faculty[0]['cac'] == 0 and faculty[0]['reviewer'] == 0 and faculty[0]['registrar'] == 0:
         canViewReviews = False
         canAddReview = False
         canChageStatus = False
        elif faculty and len(faculty) <= 6 and faculty[0]['advisor'] == 1 and faculty[0]['grad_sec'] == 1 and faculty[0]['cac'] == 1 and faculty[0]['reviewer'] == 0 and faculty[0]['registrar'] == 1:
         canViewReviews = True
         canAddReview = True
         canChageStatus = True
        elif faculty and len(faculty) <= 6 and faculty[0]['advisor'] == 0 and faculty[0]['grad_sec'] == 0 and faculty[0]['cac'] == 1 and faculty[0]['reviewer'] == 0 and faculty[0]['registrar'] == 0:
         canViewReviews = True
         canAddReview = True
         canChageStatus = True
        #  Reviewer 
        elif faculty and len(faculty) <= 6 and faculty[0]['advisor'] == 1 and faculty[0]['grad_sec'] == 0 and faculty[0]['cac'] == 0 and faculty[0]['reviewer'] == 1 and faculty[0]['registrar'] == 1:
         print('no3')
         canViewReviews = False
         canAddReview = True
         canChageStatus = False
        elif faculty and len(faculty) <= 6 and faculty[0]['advisor'] == 0 and faculty[0]['grad_sec'] == 0 and faculty[0]['cac'] == 0 and faculty[0]['reviewer'] == 1 and faculty[0]['registrar'] == 1:
         print('no3')
         canViewReviews = False
         canAddReview = True
         canChageStatus = False
        elif faculty and len(faculty) <= 6 and faculty[0]['advisor'] == 0 and faculty[0]['grad_sec'] == 1 and faculty[0]['cac'] == 1 and faculty[0]['reviewer'] == 1 and faculty[0]['registrar'] == 0:
         print('no3')
         canViewReviews = True
         canAddReview = True
         canChageStatus = True
        elif faculty and len(faculty) <= 6 and faculty[0]['advisor'] == 1 and faculty[0]['grad_sec'] == 0 and faculty[0]['cac'] == 0 and faculty[0]['reviewer'] == 1 and faculty[0]['registrar'] == 0:
         print('no3')
         canViewReviews = False
         canAddReview = True
         canChageStatus = False
        elif faculty and len(faculty) <= 6 and faculty[0]['advisor'] == 1 and faculty[0]['grad_sec'] == 0 and faculty[0]['cac'] == 0 and faculty[0]['reviewer'] == 0 and faculty[0]['registrar'] == 0:
         canViewReviews = True
         canAddReview = True
         canChageStatus = True
        #  Reviewer 
    else:
         print('theregoes')
         canViewReviews = False
         canAddReview = False
         canChageStatus = False
    # if len(perms) > 0:
    #     canViewReviews = perms[0]['canViewReviews']
    #     canAddReview = perms[0]['canAddReview']
    #     canChangeApllicantStatus = perms[0]['canChangeApllicantStatus']
    #check if a review exists from this wid
    cursor.execute("SELECT rating FROM studentapplicationreviews WHERE studentUID = %s AND workerID = %s", (ID,session['id']))
    exists = cursor.fetchone()
    cursor.execute("SELECT * FROM transcript WHERE studentUID = %s ", (ID,))
    anything = cursor.fetchall()
    print("EEeeeeeeeeeegegegeggegeeggeggeegegegegegegegegege")
    print( anything )
    print(anything[0]['recieved'])
    cursor.execute("SELECT * FROM studentapplication WHERE studentUID = %s ", (ID,))
    decisionloop = cursor.fetchall()
    print(decisionloop[0]['decision'])
    print('YEEEEEEEHHHHAHAHHAHAHAHAHAHAHA')
    print(decisionloop[0]['decision'])
    print (canChageStatus)

    if exists is None:
            previouslyReviewed = False
            showdecision = False
            previouslyTranscript = False
    else:
            print('no00000000oooooooooo')
            previouslyReviewed = True
            showdecision = True
            previouslyTranscript = False
    return render_template("applicationreview.html",app=app,decisionloop=decisionloop,anything = anything, transcripts = transcripts, letters=letters,reviews=reviews,canViewReviews=canViewReviews,canAddReview=canAddReview,canChageStatus=canChageStatus,previouslyReviewed=previouslyReviewed, showdecision = showdecision, previouslyTranscript = previouslyTranscript)

################################################  Application Revew Rec Letter Page ################################################
#
###############################################################################################################
@app.route('/appreview/<ID>/reviewletter', methods=['GET', 'POST'])
def appreviewletter(ID):
    # if 'workerID' not in session :
    #     return redirect('/')
    cursor = mydb.cursor(buffered=True, dictionary=True)
    print('submit on form review letter on review form')
    if request.method == 'POST':
        print('submitresdfsd')
        
        print('here')
        rating = request.form['rating']
        letterID = request.form['letterID']
        print('here2')
        generic = request.form['generic']
        print('here3')
        credible = request.form['credible']
        print('here4')
        cursor.execute("UPDATE recommendationletters SET rating = %s, generic = %s, credible = %s WHERE letterID = %s",(int(rating),generic,credible,int(letterID)))
        mydb.commit()
    return redirect('/appreview/'+str(ID))

################################################  Application Rec Review Submit Page ################################################
#
############################################################################################################### 
@app.route('/appreview/<ID>/reviewsubmit', methods=['GET', 'POST'])
def appreviewsubmit(ID):
    # if 'workerID' not in session :
    #     return redirect('/')
    cursor = mydb.cursor(buffered=True, dictionary=True)
    print('submit on form review ')
    if request.method == 'POST':
        print('submit')
        workerID = request.form['workerID']
        print(workerID)
        studentUID = int(ID)
        print('being')
        print(studentUID)
        rating = int(request.form['rating'])
        
        deficiencycourses = request.form['deficiencycourses']
        reasonsforreject = request.form['reasonsforreject']
        comments = request.form['comments']
        print('heyyyo')
        cursor.execute("INSERT INTO studentapplicationreviews (workerID,studentUID,rating,deficiencycourses,reasonsforreject,comments) VALUES (%s,%s,%s,%s,%s,%s)",(session['id'],studentUID,rating,deficiencycourses,reasonsforreject,comments))
        print('hellllllows')
       
        mydb.commit()
    return redirect('/appreview/'+str(ID))

################################################  Application Revew Transcript  Page ################################################
#
###############################################################################################################
@app.route('/appreview/<ID>/sendtranscript', methods=['GET', 'POST'])
def appreviewtranscript(ID):
    cursor = mydb.cursor(buffered=True, dictionary=True)
    print('submit on form review letter on review form')
    if request.method == 'POST':
        print('submitresdfsd')
        print('here')
       
        print('here3')
        studentUID = int(ID.split("_")[0])
        recieved = request.form['recieved']
        print('here4')
        
        cursor.execute("UPDATE transcript SET recieved = %s WHERE studentUID = %s", (recieved, studentUID))
        # cursor.fetchone()
        # if read is not None:
        #  print(read)
        # else:
        #      print("No rows fetched.")
        #      return
    return redirect('/appreview/' + str(ID))



################################################  Application Transcript  Submit Page ################################################
#
############################################################################################################### 
@app.route('/appreview/<ID>/sendtranscripts', methods=['GET', 'POST'])
def appreviewtranscriptsubmit(ID):
    # if 'workerID' not in session :
    #     return redirect('/')
    print('zezez')
    cursor = mydb.cursor(buffered=True, dictionary=True)
    print('submit on form review ')
    if request.method == 'POST':
        print('submit')
        
        print('submit')
        studentUID = int(ID)
        print(studentUID)
        print('submit')
        recieved = request.form['recieved']
        print(recieved)
        
       
        
        cursor.execute("UPDATE transcript SET studentUID = %s,recieved = %s ",(studentUID,recieved))
        mydb.commit()
    return redirect('/appreview/'+str(ID))

################################################  Decison Page ################################################
#
###############################################################################################################
@app.route('/appreview/<ID>/submitdecision', methods=['GET', 'POST'])
def appreviewsubmitdecision(ID):
    # if 'workerID' not in session :
    #     return redirect('/')
    print ('hi')
    cursor = mydb.cursor(buffered=True, dictionary=True)
    print('submit on form review on final dicision')
    if request.method == 'POST':
        print('submitters')
        studentUID = int(ID)
        print(studentUID)
        decision = request.form['decision']
        recommendedadvisor = request.form['recommendedadvisor']
        if decision == 'Admit with Aid' or decision == 'Admit':
            status = 'Admit'
        else:
            status = 'Reject'
        print(status)
        cursor.execute("UPDATE studentapplication SET  studentUID = %s ,status = %s, decision = %s, recommendedadvisor = %s WHERE studentUID = %s",(studentUID, status,decision,recommendedadvisor,ID))
        cursor.execute("UPDATE users SET  uid = %s ,status = %s WHERE uid = %s",(studentUID, status,ID))

        mydb.commit()
        
    return redirect('/appreview/'+str(ID))




################################################  LOGIN PAGE  ################################################
#First page you see when loaded, it allows one to log in
###############################################################################################################
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    cur = mydb.cursor(buffered=True, dictionary=True)
    
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]

        #If we are able to perform a successful SQL query
        cur.execute(
            "SELECT email, password, type, uid FROM users WHERE email = (%s) AND password = (%s)",
            (email, password,))
        x = cur.fetchone()
        print(x)
       
        #if they are not in the db
        if x == None:
            flash('Username and/or password is incorrect')
            return render_template("login.html")
        

        if x:

            session['email'] = email
            session['password'] = password
            session['user_type'] = x['type']
            session['id']= x['uid']
            #find what faculty it is 
            if (session.get('user_type') == 'Faculty') or (session.get('user_type') == 'Systems Administrator'):
                uid = session.get('id')
                print(uid)
                cur.execute("SELECT * FROM faculty")
                data = cur.fetchall()
                print(data)
                cur.execute("select * from faculty where faculty.uid = (%s)", (uid,))
                session['faculty_type'] = cur.fetchone()
            

            print('user type = ', session.get('user_type'))

            #Sends to graduate student directory
            if session.get('user_type') == 'Applicant':
                # return redirect('/applicantDashboard/<ID>')
                print('got tihs')
                return redirect(url_for('Applicant_Dashboard', ID = x['uid'], user_type = session['user_type']))

            if session.get('user_type') == 'Student':
                return redirect(url_for('studentdirectory', id = x['uid'], user_type = session['user_type']))
            
            #Sends to alumni directory
            if session.get('user_type') == 'Alumni':
                return redirect(url_for('alumnidirectory', id = x['uid']))

            #Sends to system administrator directory
            if (session['user_type'] in {"Faculty","Systems Administrator"}):
                return redirect(url_for('home', user_type = session['user_type'], faculty_type = session.get('faculty_type')))
            

        return render_template("login.html")        

        # Else, give an error message and redirect them to the same login page
        
        #return render_template("login.html")
    return render_template("login.html")


################################################  HOME ROUTE  ################################################
#This Route contains all the information, basically the admin pass homepage
##############################################################################################################
@app.route('/faculty')
def home():
    if session.get('user_type') != 'Faculty'  and session.get('user_type') != 'Systems Administrator':
        err_message = "You do not have access to this form bring up your clearance with Gordan"
        print( session.get('user_type'))
        return render_template("error.html", err_message = err_message)
    email = session.get('email')
    password = session.get('password')
    user_type = session.get('user_type')
    faculty_type = {}
    if session.get('faculty_type'):
        faculty_type = session.get('faculty_type')
    cursor = mydb.cursor(dictionary = True)
    # cursor.execute("select * from faculty")
    # test = cursor.fetchall()
    # print(test)

    return render_template("faculty.html", user_type = user_type, faculty_type = faculty_type)

################################################  STUDENT SEARCH  ###################################################
@app.route('/studentSearch', methods = ['POST'])
def studentSearch():
    if( (session.get('user_type') != 'Systems Administrator') and (session.get('user_type') != 'Faculty')):
        err_message = "You do not have access to this form bring up your clearance with Gordan"
        return render_template("error.html", err_message = err_message)
    mydb = mysql.connector.connect(
        host = "instructor-1.cq4bugepeexy.us-east-1.rds.amazonaws.com",
        user = "admin",
        password = "testpass",
        database = "university"
    )
    cur = mydb.cursor()
    if request.method == 'POST':
        name = request.form["name"]
        cur.execute("SELECT uid, firstname, lastname FROM users WHERE type = 'Student' and (uid LIKE %s or firstname LIKE %s or lastname LIKE %s)",('%'+name+'%','%'+name+'%','%'+name+'%'))
        all_std = cur.fetchall()
        students = {}
        cnt = 0
        for std in all_std:
            students[cnt] = {'uid' : std[0], 'name' : std[1] + " "+std[2]}
            cnt=cnt+1
        if len(all_std)==0:
            students = None
        return render_template('std_search.html',students=students,name = name)
    return redirect(url_for('home'))
#####################################################################################################################

################################################  STUDENT DIRECTORY  ################################################
#Show all the info of said student
#####################################################################################################################
@app.route('/student/<id>', methods = ['GET'])
def studentdirectory(id):
    #if they are a student but this isnt their directory they cannot see this 
    if 'id' not in session or (session['user_type'] not in  {"Student","Systems Administrator","Faculty"}):
        
        return redirect(url_for('landing_page'))
    if session['user_type'] != "Systems Administrator" and int(session['id']) != int(id):
        return redirect(url_for('landing_page'))
    
    print(session.get('id'), id)
    print(session.get('firstname'))
    cur = mydb.cursor(buffered=True, dictionary=True)
    
    cur.execute("select * from students where uid =  (%s)", (id,))
    test = cur.fetchone()
    if not test:
        cur.execute("SELECT degreeType FROM studentapplication WHERE studentUID = %s", (id,))
        degree_type = cur.fetchone()
        print('poppy')
        print(degree_type)
        if degree_type is not None and degree_type['degreeType'] in ['Masters', 'PhD']:
            print('KLKKKKKKKooooolllol')
            cur.execute("INSERT INTO students (uid, enrolledas) VALUES (%s, %s)", (id, degree_type['degreeType']))
            print('DEEEEEEZZZZZZZZZ')
            mydb.commit()

    #get all the info from the student
    cur.execute("select students.suspended, users.* from users inner join students on users.uid = students.uid where users.uid = (%s)", (id,))
    x = cur.fetchone()

    cur.execute("select c_history.fgrade, c_catalogue.cred from c_history inner join c_catalogue on c_history.cid = c_catalogue.cid where uid = (%s)", (id,))
    x = cur.fetchall()
    # print(x)
    e = None

    cur.execute("SELECT advising_status, form_status FROM students WHERE uid = %s",(id,))    
    form_status = cur.fetchone()
    print(form_status)
    # #code to get the total credit hours and gpa 
    # if x: 
    #     total_credit = 0
    #     for i in x: 
    #         total_credit += i['cred']
    #     #call the function 
    #     # print(total_credit)
    #     #insert the total number of credit hours and GPA  into the database
    
    #     g = gpa(total_credit, x)
    #     # print(g)
    #     # cur.execute("update students set total_credit = (%s), GPA = (%s)  where user_id = (%s) ", (total_credit, g ,id))
    #     # mydb.commit()

    #     #check if they are under academic suspension
    #     grades_below_b(id,x)
    #Get student info

    cur.execute("SELECT * FROM students JOIN users ON students.uid = users.uid WHERE students.uid = (%s)", (id,))
    z = cur.fetchone()
    #enrolled as what kind of student? 
    e = z['enrolledas']
    #Get advisor name
    cur.execute("select firstname, lastname from users where uid = (%s)", (z['advisor_id'],))
    adname = cur.fetchone()

    cur.execute("select * from form1 where uid = (%s)", (id,))
    has_form1 = False
    y = cur.fetchone()
    
    #Check if form one has already been filled out
    if y:
        has_form1 = True
    cur.execute("select * from gradrequests where advisee_id = (%s)", (id,))
    grad_request = cur.fetchone()

   

    return render_template("student.html", x = z, has_form1 = has_form1, grad_request = grad_request, user_type = session['user_type'], adname = adname, enrolledas = e,id=id,form_status=form_status)



############################### ALL STUDENT IN SOME COURSE ###################################
@app.route('/all_std/<cid>', methods=['GET', 'POST'])
def all_std_in_course(cid):
    print(session['user_type'])
    if 'id' not in session or (session['user_type'] not in  {"Systems Administrator","Faculty"}):
        return redirect(url_for('landing_page'))
    mydb = mysql.connector.connect(
        host = "instructor-1.cq4bugepeexy.us-east-1.rds.amazonaws.com",
        user = "admin",
        password = "testpass",
        database = "university"
    ) 
    cur = mydb.cursor()
    cur.execute("SELECT users.uid, users.firstname, users.lastname, c_history.fgrade FROM c_history JOIN users ON c_history.uid = users.uid WHERE cid = %s",(cid,))
    all_std = cur.fetchall()
    students = {}
    cnt = 0
    cur.execute("SELECT dept, cnum, title FROM c_catalogue WHERE cid = %s",(cid,))
    course_init = cur.fetchone()
    course= course_init[0]+ " "+ str(course_init[1])+ " "+ course_init[2]
    for std in all_std:
        students[cnt] = {'uid' : std[0], 'name' : std[1] + " "+std[2] , 'fgrade' : std[3]}
        cnt=cnt+1
    if len(all_std)==0:
        students = None
    return render_template("all_std.html",students=students,course=course,cid=cid)
##############################################################################################

################################# COURSE CATALOGUE  ##########################################

@app.route('/c_catalogue/<id>', methods=['GET', 'POST'])
def c_catalogue(id):

    if 'id' not in session or (session['user_type'] not in  {"Student","Systems Administrator","Faculty"}):
        return redirect(url_for('landing_page'))
    if session['user_type'] != "Systems Administrator" and int(session['id']) != int(id):
        return redirect(url_for('landing_page'))
    mydb = mysql.connector.connect(
        host = "instructor-1.cq4bugepeexy.us-east-1.rds.amazonaws.com",
        user = "admin",
        password = "testpass",
        database = "university"
    ) 
    cur = mydb.cursor()

    cur.execute("SELECT form_status,advising_status FROM students WHERE uid = %s",(id,))
    form_status = cur.fetchone()
    
    print(form_status)

    if request.method == 'POST':
        if session['user_type']=="Faculty" and session['faculty_type']['grad_sec'] == 0:
            c_id =request.form['c_id']
            cur.execute("SELECT c_schedule.day,c_schedule.time, c_schedule.cid,c_catalogue.dept,c_catalogue.cnum,c_catalogue.title, c_catalogue.cred, c_catalogue.prone, c_catalogue.prtwo,users.firstname, users.lastname,c_catalogue.loc FROM c_schedule JOIN c_catalogue ON c_schedule.cid=c_catalogue.cid JOIN users ON c_catalogue.snum = users.uid WHERE (c_catalogue.cid LIKE %s or c_catalogue.cnum LIKE %s or c_catalogue.title = %s) and snum = %s ORDER BY c_schedule.cid",('%'+c_id+'%','%'+c_id+'%','%'+c_id+'%',session['id']))
            catalogue_init = cur.fetchall()
            search = 1
        else:
            c_id =request.form['c_id']

            cur.execute("SELECT c_schedule.day,c_schedule.time, c_schedule.cid,c_catalogue.dept,c_catalogue.cnum,c_catalogue.title, c_catalogue.cred, c_catalogue.prone, c_catalogue.prtwo,users.firstname, users.lastname,c_catalogue.loc FROM c_schedule JOIN c_catalogue ON c_schedule.cid=c_catalogue.cid JOIN users ON c_catalogue.snum = users.uid WHERE c_catalogue.cid LIKE %s or c_catalogue.cnum LIKE %s or c_catalogue.title LIKE %s ORDER BY c_schedule.cid",('%'+c_id+'%','%'+c_id+'%','%'+c_id+'%'))

            catalogue_init = cur.fetchall()
            search = 1
    else:
        if session['user_type']=="Faculty" and session['faculty_type']['grad_sec'] == 0:
            cur.execute("SELECT c_schedule.day,c_schedule.time, c_schedule.cid,c_catalogue.dept,c_catalogue.cnum,c_catalogue.title, c_catalogue.cred, c_catalogue.prone, c_catalogue.prtwo,users.firstname, users.lastname,c_catalogue.loc FROM c_schedule JOIN c_catalogue ON c_schedule.cid=c_catalogue.cid JOIN users ON c_catalogue.snum = users.uid WHERE snum = %s ORDER BY c_schedule.cid",(session['id'],))
            catalogue_init = cur.fetchall()
            search = 0
        else:   
            cur.execute("SELECT c_schedule.day,c_schedule.time, c_schedule.cid,c_catalogue.dept,c_catalogue.cnum,c_catalogue.title, c_catalogue.cred, c_catalogue.prone, c_catalogue.prtwo,users.firstname, users.lastname,c_catalogue.loc FROM c_schedule JOIN c_catalogue ON c_schedule.cid=c_catalogue.cid JOIN users ON c_catalogue.snum = users.uid ORDER BY c_schedule.cid")
            catalogue_init = cur.fetchall()
            search = 0
    catalogue = {}
    cnt = 0
    for course in catalogue_init:
        catalogue[cnt] = {'day' : course[0], 'time' : course[1], 'cid' : course[2],'dept' : course[3], 'cnum' : course[4], 'title' : course[5], 'cred' : course[6], 'prone' : course[7], 'prtwo' : course[8], 'ins_name' : course[9]+" "+course[10], 'loc': course[11]}
        cnt=cnt+1

    if form_status == None:
        return render_template('c_catalogue.html',catalogue=catalogue,search=search,form_status=1,id=id,able_reg=0)
    return render_template('c_catalogue.html',catalogue=catalogue,search=search,form_status=form_status[0],id=id,able_reg=1)

###########################################################################################################

###################################  UPDATE GRADE   #######################################################
@app.route('/AssignGrades2/<cid>', methods = ["GET", "POST"])
def assign_grades2(cid):


    if ("id" not in session or session["user_type"] not in {"Faculty","Systems Administrator"}):
        return "RESTRICTED ACCESS"
    if session['user_type'] != "Systems Administrator" and session['id'] != id:
        return redirect(url_for('landing_page'))
    mydb = mysql.connector.connect(
        host = "instructor-1.cq4bugepeexy.us-east-1.rds.amazonaws.com",
        user = "admin",
        password = "testpass",
        database = "university"
    )
    cursor = mydb.cursor()

    if (request.method == "POST"):
        grade = request.form.get("grade")
        cid = request.form["cid"]
        uid = request.form["uid"]

        cursor.execute("UPDATE c_history SET fgrade = %s WHERE cid = %s AND uid = %s", (grade, cid, uid))
        mydb.commit()

        if (session["user_type"] in {"Faculty", "Systems Administrator"}):
            return redirect(url_for("all_std_in_course",cid=cid))
        
        return redirect(url_for('assign_grades'))

###########################################################################################################

###################################  UPDATE GRADE   #######################################################
@app.route('/AssignGrades', methods = ["GET", "POST"])
def assign_grades():


    if ("id" not in session or session["user_type"] not in {"Faculty","Systems Administrator"}):
        return "RESTRICTED ACCESS"

    mydb = mysql.connector.connect(
        host = "instructor-1.cq4bugepeexy.us-east-1.rds.amazonaws.com",
        user = "admin",
        password = "testpass",
        database = "university"
    )
    cursor = mydb.cursor()

    if (request.method == "POST"):
        grade = request.form.get("grade")
        cid = request.form["cid"]
        uid = request.form["uid"]

        cursor.execute("UPDATE c_history SET fgrade = %s WHERE cid = %s AND uid = %s", (grade, cid, uid))
        mydb.commit()

        if (session["user_type"] in {"Faculty", "Systems Administrator"}):
            return redirect(url_for("transcriptSearch"))
        
        return redirect(url_for('assign_grades'))

###########################################################################################################

###################################  STUDENT DROP COURSE      #############################################

@app.route('/drop/<cid>/<id>', methods = ['GET','POST'])
def drop (cid,id):

    if 'id' not in session or session['user_type'] not in {"Student","Systems Administrator"}: 
        return redirect(url_for('landing_page'))
    if session['user_type'] != "Systems Administrator" and int(session['id']) != int(id):
        return redirect(url_for('landing_page'))
    mydb = mysql.connector.connect(
        host = "instructor-1.cq4bugepeexy.us-east-1.rds.amazonaws.com",
        user = "admin",
        password = "testpass",
        database = "university"
    ) 
    cur = mydb.cursor()

    cur.execute("DELETE FROM c_history WHERE uid = %s AND cid = %s",(id,cid))
    mydb.commit()
    return redirect (url_for('registered_course',id=id))
###########################################################################################################

###################################  STUDENT DROP ALL COURSE      #############################################
@app.route('/drop_all/<id>', methods = ['GET','POST'])
def drop_all (id):
    if 'id' not in session or session['user_type'] not in {"Student","Systems Administrator"}: 
        return redirect(url_for('landing_page'))
    if session['user_type'] != "Systems Administrator" and int(session['id']) != int(id):
        return redirect(url_for('landing_page'))
    mydb = mysql.connector.connect(
        host = "instructor-1.cq4bugepeexy.us-east-1.rds.amazonaws.com",
        user = "admin",
        password = "testpass",
        database = "university"
    ) 
    cur = mydb.cursor()
    cur.execute("DELETE FROM c_history WHERE uid = %s ",(id,))
    mydb.commit()
    return redirect (url_for('registered_course',id=id))
###########################################################################################################

###################################  STUDENT VIEW TRANSCRIPT  #############################################
@app.route('/transcript', methods = ['GET'])
def transcript():
    if 'id' not in session or session['user_type'] not in {"Student","Systems Administrator","Alumni"}:

        return redirect(url_for('landing_page'))
    
    mydb = mysql.connector.connect(
        host = "instructor-1.cq4bugepeexy.us-east-1.rds.amazonaws.com",
        user = "admin",
        password = "testpass",
        database = "university"
    )

    cur = mydb.cursor()
    cur.execute("SELECT c_history.cid, c_catalogue.dept, c_catalogue.cnum, c_catalogue.title, c_catalogue.cred, c_history.fgrade FROM c_history JOIN c_catalogue ON c_history.cid = c_catalogue.cid WHERE c_history.uid = %s", (session['id'],))
    transcript_data = cur.fetchall()

    transcript = {}
    count = 0
    for course in transcript_data:
        transcript[count] = {'cid' : course[0], 'dept' : course[1], 'cnum' : course[2], 'title' : course[3], 'cred' : course[4], 'grade' : course[5]}
        count += 1

    return render_template('transcript.html', transcript = transcript)

###########################################################################################################


###################################### STUDENT COURSE REGISTRATION ########################################

@app.route('/register/<cid>/<id>', methods = ['GET','POST'])
def register (cid,id):
    if 'id' not in session or session['user_type'] not in {"Student","Systems Administrator"}:

        return redirect(url_for('landing_page'))
    if session['user_type'] != "Systems Administrator" and int(session['id']) != int(id):
        return redirect(url_for('landing_page'))
    mydb = mysql.connector.connect(
        host = "instructor-1.cq4bugepeexy.us-east-1.rds.amazonaws.com",
        user = "admin",
        password = "testpass",
        database = "university"
    )  
    cur = mydb.cursor()

    cur.execute ("SELECT * FROM c_history WHERE cid = %s and uid = %s",(cid,id))
    prev = cur.fetchone()
    if prev != None:
        return render_template ('register.html',err_msg = "Already taken the course",id=id)

    cur.execute("SELECT c_schedule.cid, c_schedule.time, c_schedule.day, c_catalogue.sem, c_catalogue.year, c_catalogue.snum,c_catalogue.prone, c_catalogue.prtwo FROM c_schedule JOIN c_catalogue ON c_schedule.cid= c_catalogue.cid WHERE c_schedule.cid = %s",(cid,))
    course_time = cur.fetchone()
    print(course_time)
    if course_time[6] != None:
        dept_pr1 = course_time[6][0:4]
        cnum_pr1 = int(course_time[6][5:9])
        cur.execute("SELECT c_history.fgrade FROM c_history JOIN c_catalogue ON c_history.cid = c_catalogue.cid WHERE c_history.uid = %s AND c_catalogue.dept = %s AND c_catalogue.cnum = %s",(session['id'],dept_pr1,cnum_pr1))
        pr1 = cur.fetchone()
        if pr1 == None:

            return render_template ('register.html',err_msg = "Prerequest needed: "+ course_time[6],id=id)
        if pr1[0] == "IP":
            return render_template ('register.html',err_msg = "Prerequest needed: "+ course_time[6],id=id)

        if course_time[7] != None:
            dept_pr2 = course_time[7][0:4]
            cnum_pr2 = int(course_time[7][5:9])
            cur.execute("SELECT c_history.fgrade FROM c_history JOIN c_catalogue ON c_history.cid = c_catalogue.cid WHERE c_history.uid = %s AND c_catalogue.dept = %s AND c_catalogue.cnum = %s",(session['id'],dept_pr2,cnum_pr2))
            pr2 = cur.fetchone()
            if pr2 == None:

                return render_template ('register.html',err_msg = "Prerequest needed: "+ course_time[7],id=id)
            if pr2[0] == "IP":
                return render_template ('register.html',err_msg = "Prerequest needed: "+ course_time[7],id=id)

        
    st_h = course_time[1][0:2]
    st_min = course_time[1][2:4]
    st_final = 60 * int(st_h)+int(st_min)
    ed_h= course_time[1][5:7]
    ed_min = course_time[1][7:9]
    ed_final = 60 * int(ed_h)+int(ed_min)

    cur.execute("SELECT c_history.cid, c_schedule.time, c_schedule.day FROM c_history JOIN c_schedule ON c_history.cid = c_schedule.cid WHERE c_history.uid = %s AND c_history.fgrade = %s",(id,"IP"))

    student_schedule = cur.fetchall()
    if student_schedule == None :
        cur.execute ("INSERT INTO c_history (uid, cid, fgrade,sem, year, snum) VALUES (%s,%s,%s,%s,%s,%s)",(session['id'],course_time[0],"IP",course_time[3],course_time[4],course_time[5]))
        mydb.commit()
    for c_registered in student_schedule:
        r_st = 60* int (c_registered[1][0:2]) + int (c_registered[1][2:4])
        r_ed = 60* int (c_registered[1][5:7]) + int (c_registered[1][7:9])
        if c_registered[2]==course_time[2]:
            if ed_final+30 > r_st:
                #return render_template ('register.html',err_msg = "Unable to Register: Time Conflict")
                if r_ed + 30 > st_final:

                    return render_template ('register.html',err_msg = "Unable to Register: Time Conflict",id=id)
    cur.execute ("INSERT INTO c_history (uid, cid, fgrade,sem, year, snum) VALUES (%s,%s,%s,%s,%s,%s)",(id,course_time[0],"IP",course_time[3],course_time[4],course_time[5]))
    mydb.commit()
    return render_template ('register.html',err_msg = "Register Success",id=id)


###########################################################################################################

######################################   STUDENT REGISTERED COURSE ########################################

@app.route('/c_registered/<id>', methods = ['GET','POST'])
def registered_course(id):

    if 'id' not in session or session['user_type'] not in {"Student","Systems Administrator"}:
        return redirect(url_for(landing_page))
    if session['user_type'] != "Systems Administrator" and int(session['id']) != int(id):
        return redirect(url_for('landing_page'))
    mydb = mysql.connector.connect(
        host = "instructor-1.cq4bugepeexy.us-east-1.rds.amazonaws.com",
        user = "admin",
        password = "testpass",
        database = "university"
    ) 
    cur = mydb.cursor()

    uid =id
    
    cur.execute("SELECT c_history.cid, c_catalogue.dept, c_catalogue.cnum, c_catalogue.title, c_catalogue.cred, c_schedule.day, c_schedule.time, users.firstname, users.lastname,c_catalogue.loc FROM c_history JOIN c_catalogue ON c_history.cid = c_catalogue.cid JOIN c_schedule ON c_history.cid = c_schedule.cid JOIN users ON c_history.snum = users.uid WHERE c_history.uid = %s AND c_history.fgrade = %s",(id,"IP"))   
    catalogue_init = cur.fetchall()
    if len(catalogue_init) == 0:
        return render_template ('c_registered.html',catalogue=None,id=id)  

    catalogue = {}
    cnt = 0
    for course in catalogue_init:
        catalogue[cnt] = {'day' : course[5], 'time' : course[6], 'cid' : course[0],'dept' : course[1], 'cnum' : course[2], 'title' : course[3], 'cred' : course[4], 'ins_name' : course[7]+" "+course[8],'loc':course[9]}

        cnt=cnt+1     
  
    return render_template ('c_registered.html',catalogue=catalogue,id=id)   

###########################################################################################################

###################################### LOGOUT FUNCTION ####################################################
@app.route('/logout', methods =["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for('landing_page'))
###########################################################################################################

###################################### FACULTY VIEW TRANSCRIPT 1 SEARCH ABLE TO EDIT GRADE #########################################
@app.route('/transcriptSearch', methods=["GET","POST"])
def transcriptSearch():
    if ("id" not in session or session["user_type"] not in {"Faculty", "Systems Administrator"}):
        return "RESTRICTED ACCESS"
        
    mydb = mysql.connector.connect(
        host = "instructor-1.cq4bugepeexy.us-east-1.rds.amazonaws.com",
        user = "admin",
        password = "testpass",
        database = "university"
    )

    uid = request.form["uid"]

    cur = mydb.cursor()
    cur.execute(
        "SELECT c_history.cid, c_catalogue.dept, c_catalogue.cnum, c_catalogue.title, c_catalogue.cred, c_history.fgrade FROM c_history JOIN c_catalogue ON c_history.cid = c_catalogue.cid WHERE c_history.uid = %s", (uid,))
    transcript_data = cur.fetchall()

    transcript = {}
    count = 0
    for course in transcript_data:
        transcript[count] = {'cid': course[0], 'dept': course[1], 'cnum': course[2],
                             'title': course[3], 'cred': course[4], 'grade': course[5]}
        count += 1

    return render_template('transcriptSearch.html', transcript=transcript, uid=uid)

###########################################################################################################

#########################################  ADVISING FROM ##################################################
@app.route('/advising_form/<id>',methods = ['GET','POST'])
def advising_form(id):
    if 'id' not in session or session['user_type'] not in {"Student","Systems Administrator"}:
        return redirect(url_for(landing_page))
    if session['user_type'] != "Systems Administrator" and int(session['id']) != int(id):
        return redirect(url_for('landing_page'))
    mydb = mysql.connector.connect(
        host = "instructor-1.cq4bugepeexy.us-east-1.rds.amazonaws.com",
        user = "admin",
        password = "testpass",
        database = "university"
    )
    cur = mydb.cursor()
    parameters = []
    for i in range(1, 13):
        dept_subject = request.form.get('dept_subject_{}'.format(i))
        course_number = request.form.get('course_number_{}'.format(i))
        #if the course and dept# are there insert into the form1db 
        if dept_subject and course_number:
            #need to find the cid of the class the user just enteree
            cur.execute("SELECT cid from c_catalogue where dept = (%s) and cnum = (%s)", (dept_subject, course_number))
            course_id = cur.fetchone()
            parameters.append(course_id[0])
        # else:
        #     parameters.append(None)
    #make a loop that we can go through each course and insert it into our database 
    for k in parameters: 
        #now we must insert that into our form1 table 
        cur.execute("INSERT into advising_form (uid, cid) values (%s, %s)", (id, k))
        #commit to the db
        mydb.commit()
    cur.execute("UPDATE students SET advising_status = 1 WHERE uid = %s",(id,))
    mydb.commit()
    
    
    if session['user_type'] == "Systems Administrator":
        return redirect('studentdirectory',id=id)
    return redirect(url_for('studentdirectory',id=id))
###########################################################################################################

########################################## ROUTE TO ADVISING FOM ##########################################
@app.route('/ad_form/<id>',methods = ['GET','POST'])
def ad_form(id):
    if 'id' not in session or session['user_type'] not in {"Student","Systems Administrator"}:
        return redirect(url_for(landing_page))
    if session['user_type'] != "Systems Administrator" and int(session['id']) != int(id):
        return redirect(url_for('landing_page'))
    mydb = mysql.connector.connect(
        host = "instructor-1.cq4bugepeexy.us-east-1.rds.amazonaws.com",
        user = "admin",
        password = "testpass",
        database = "university"
    )
    
    cur = mydb.cursor(buffered=True, dictionary=True)
    cur.execute("SELECT advising_status, form_status FROM students WHERE uid = %s",(session['id'],))
    status = cur.fetchone()
    print(status)
    cur.execute("SELECT DISTINCT dept FROM c_catalogue")
    courses_dept = cur.fetchall()
    cur.execute("SELECT cnum  FROM c_catalogue")
    courses_number = cur.fetchall()
    return render_template('advising_form.html',status=status,courses_dept=courses_dept,courses_number=courses_number,id=id)
###########################################################################################################

########################################## FACULTY VIEW ADVISING FORM #####################################
@app.route('/fac_ad_form/<sid>',methods=['GET','POST'])
def fac_ad_form(sid):
    if ("id" not in session or session['user_type'] not in {"Faculty","Systems Administrator"}):
        return "RESTRICTED ACCESS"
    mydb = mysql.connector.connect(
        host = "instructor-1.cq4bugepeexy.us-east-1.rds.amazonaws.com",
        user = "admin",
        password = "testpass",
        database = "university"
    )
    cur = mydb.cursor()
    cur.execute("SELECT c_schedule.day,c_schedule.time, c_schedule.cid,c_catalogue.dept,c_catalogue.cnum,c_catalogue.title, c_catalogue.cred, c_catalogue.prone, c_catalogue.prtwo,users.firstname, users.lastname,c_catalogue.loc FROM advising_form JOIN c_catalogue ON advising_form.cid=c_catalogue.cid JOIN users ON c_catalogue.snum = users.uid JOIN c_schedule ON advising_form.cid=c_schedule.cid WHERE advising_form.uid = %s",(sid,))
    catalogue_init = cur.fetchall()
    catalogue = {}
    cnt = 0
    for course in catalogue_init:
        catalogue[cnt] = {'day' : course[0], 'time' : course[1], 'cid' : course[2],'dept' : course[3], 'cnum' : course[4], 'title' : course[5], 'cred' : course[6], 'prone' : course[7], 'prtwo' : course[8], 'ins_name' : course[9]+" "+course[10], 'loc': course[11]}
        cnt=cnt+1
    cur.execute("SELECT firstname, lastname FROM users WHERE uid = %s",(sid,))
    name_init = cur.fetchone()
    if len(catalogue_init) == 0:
        catalogue=None
    name = name_init[0]+" "+name_init[1]
    return render_template('fac_view_ad_form.html',name=name,catalogue=catalogue,id=sid)
###########################################################################################################

########################################## CLEAR FORM #####################################################
@app.route('/clear_ad_form/<id>',methods=['GET','POST'])
def clear_ad_form(id):
    if ("id" not in session or session['user_type'] not in {"Faculty","Systems Administrator"}):
        return "RESTRICTED ACCESS"
    mydb = mysql.connector.connect(
        host = "instructor-1.cq4bugepeexy.us-east-1.rds.amazonaws.com",
        user = "admin",
        password = "testpass",
        database = "university"
    )
    cur = mydb.cursor()
    cur.execute("UPDATE students SET form_status = 0,advising_status = 0 WHERE uid = %s",(id,))
    cur.execute("DELETE FROM advising_form WHERE uid = %s",(id,))
    mydb.commit()
    return redirect(url_for('facultyviewstudents'))
###########################################################################################################

########################################## APPROVE FORM ###################################################
@app.route('/approve_form/<id>',methods=['GET','POST'])
def approve_form(id):
    if ("id" not in session or session['user_type'] not in {"Faculty","Systems Administrator"}):
        return "RESTRICTED ACCESS"
    mydb = mysql.connector.connect(
        host = "instructor-1.cq4bugepeexy.us-east-1.rds.amazonaws.com",
        user = "admin",
        password = "testpass",
        database = "university"
    )
    cur = mydb.cursor()
    cur.execute("UPDATE students SET form_status = 1 WHERE uid = %s",(id,))
    cur.execute("DELETE FROM advising_form WHERE uid = %s",(id,))
    mydb.commit()
    return redirect(url_for('facultyviewstudents'))
###########################################################################################################

########################################## REJECT FORM ####################################################
@app.route('/reject_form/<id>',methods=['GET','POST'])
def reject_form(id):
    if ("id" not in session or session['user_type'] not in {"Faculty","Systems Administrator"}):
        return "RESTRICTED ACCESS"
    mydb = mysql.connector.connect(
        host = "instructor-1.cq4bugepeexy.us-east-1.rds.amazonaws.com",
        user = "admin",
        password = "testpass",
        database = "university"
    )
    cur = mydb.cursor()
    cur.execute("DELETE FROM advising_form WHERE id = %s",(id,))
    mydb.commit()
    return redirect(url_for('facultyviewstudents'))

###########################################################################################################

########################################## FACULTY VIEW TRANSCIPT 2 DIRECT CLITCK ABLE TO EDIT GRADE ########################
@app.route('/transcript/<uid>',methods = ['GET','Post'])
def transSearch(uid):

    if ("id" not in session or session['user_type'] not in {"Faculty","Systems Administrator","Alumni"}):
        return "RESTRICTED ACCESS"
    if session['user_type'] == "Alumni" and session['id'] != id:
        return redirect(url_for('landing_page'))
    mydb = mysql.connector.connect(
        host = "instructor-1.cq4bugepeexy.us-east-1.rds.amazonaws.com",
        user = "admin",
        password = "testpass",
        database = "university"
    )
    cur = mydb.cursor()
    cur.execute(
        "SELECT c_history.cid, c_catalogue.dept, c_catalogue.cnum, c_catalogue.title, c_catalogue.cred, c_history.fgrade FROM c_history JOIN c_catalogue ON c_history.cid = c_catalogue.cid JOIN users ON c_history.uid = users.uid WHERE c_history.uid = %s or users.firstname LIKE %s or users.lastname LIKE %s ORDER BY c_history.cid", (uid,'%'+uid+'%','%'+uid+'%'))
    transcript_data = cur.fetchall()

    transcript = {}
    count = 0
    for course in transcript_data:
        transcript[count] = {'cid': course[0], 'dept': course[1], 'cnum': course[2],
                             'title': course[3], 'cred': course[4], 'grade': course[5]}
        count += 1

    return render_template('transcriptAssign.html', transcript=transcript, uid=uid)
###########################################################################################################


################################################  FULL STUDENT PAGE  ################################################
#Show an entire list of all the students, their info, and a link to their directory (Admin View, Grad Secretary View)
#####################################################################################################################
@app.route('/students', methods = ['GET'])
def students():
    cur = mydb.cursor(buffered=True, dictionary=True)

    cur.execute("SELECT * FROM students inner join users on students.uid = users.uid")
    x=cur.fetchall()

    print(session['user_type'])
    if session.get('user_type') == 'Systems Administrator': 
        cur.execute("select students.uid, users.firstname, users.lastname from students inner join users on students.uid = users.uid where advisor_id = advisor_id")
        f = cur.fetchall()
        print("advisees", f)

    user_type = session['user_type']
    return render_template("students.html", x = x, user_type = user_type)

################################################  FACULTY ADVISOR STUDENT PAGE  ################################################
#Show an  list of all the advisors' students, their info, and a link to their directory (Admin View, Grad Secretary View)
################################################################################################################################
@app.route('/facultyviewstudents')
def facultyviewstudents():
    cur = mydb.cursor(buffered=True, dictionary=True)
    id = session.get('id')
    user_type = session['user_type']
    faculty_type = {}
    if session.get('faculty_type')['advisor']:
        #get the students and their names
            cur.execute("select students.uid, students.advisor_id, users.firstname, users.lastname, users.email from students inner join users on users.uid = students.uid where students.advisor_id = (%s)", (id,))
            x = cur.fetchall()   
            print('advisor')
    else:
        cur.execute("SELECT users.* FROM students inner join users on users.uid = students.uid")
        x=cur.fetchall()
    
    cur.execute("SELECT * FROM phdthesis")
    y = cur.fetchall()

    return render_template("facultystudentview.html", x = x, user_type = user_type, y = y, faculty_type = faculty_type)

################################################  FORM 1 PAGE  ##############################################################
#This is where form1 is filled in for the student
#############################################################################################################################
@app.route('/form1/<id>', methods = ['GET'])
def form1(id):
    email = session.get('email')
    password = session.get('password')
    user_type = session.get('user_type')
    faculty_type = {}
    if session.get('faculty_type'): 
        faculty_type = session.get('faculty_type')

    cur = mydb.cursor(buffered=True, dictionary=True)


    cur.execute("select c_history.*, c_catalogue.* from c_history inner join c_catalogue on c_history.cid = c_catalogue.cid where uid = (%s)", (id,))
    x = cur.fetchall()
    #present error page if there is no transcript 
    if x == None: 
        err_message = "No transcript so Form 1 cannot be submitted talk to your advisor to address this issue"
        return render_template("error.html", err_message = err_message)
    
    cur.execute("select * from users where uid = (%s)", (id,))
    student = cur.fetchall()

    cur.execute("SELECT DISTINCT dept FROM c_catalogue")
    
    courses_dept = cur.fetchall()

    cur.execute("SELECT cnum  FROM c_catalogue")
    
    courses_number = cur.fetchall()

    return render_template("form1.html", student = student, courses_dept = courses_dept, courses_number=courses_number, id=id, user_type = user_type, faculty_type = faculty_type)

################################################  FORM 1 SUBMISSION  ##############################################################
#This is where form1 is submitted and added to database
###################################################################################################################################
@app.route('/submitForm1/<id>', methods=['POST'])
def submit_form(id):
    cur = mydb.cursor(buffered=True, dictionary=True)
    # get the form data
    user_id = request.form['user_id']
    lname = request.form['lname']
    fname = request.form['fname']
    parameters = []
    for i in range(0, 12):
        
        dept_subject = request.form.get('dept_subject_{}'.format(i))
        course_number = request.form.get('course_number_{}'.format(i))
        #if the course and dept# are there insert into the form1db 
        if dept_subject and course_number:
            #need to find the cid of the class the user just enteree
            cur.execute("select cid from c_catalogue where dept = (%s) and cnum = (%s)", (dept_subject, course_number))
            course_id = cur.fetchone()
            if course_id != None:
                parameters.append(course_id['cid'])
        # else:
        #     parameters.append(None)
    #make a loop that we can go through each course and insert it into our database 
    for k in parameters: 
        #now we must insert that into our form1 table 
        cur.execute("insert into form1 (uid, cid) values (%s, %s)", (id, k))
        #commit to the db
        mydb.commit()
    
   
           
    #cur = mydb.cursor(dictionary = True)
    #now time to check to make sure that form1 is true 
    #this checks all necesarry values to see if they can graduate
    #  TALIA LEIGH NOVACK DO NOT FORGET TO UN-COMMENT THIS OUT ##############
    cur.execute("select * from students where uid = (%s)", (id,))
    x = cur.fetchone()
    advisor_id = x['advisor_id']
    if(advisor_id == None):
        cur.execute("delete from form1 where uid = (%s)", (id,))
        mydb.commit()
        err_message = "No advisor ID found"
        return render_template("error.html", err_message = err_message)
    print(comparef1andtranscript(id))

    #######TALIA LEIGH DO NOT FORGET TO UNCOMMENT THIS########################
    #Masters student 
    if x['enrolledas'] == 'Masters':
        if ((prereqmatch(id) == 0) or (comparef1andtranscript(id)==0)):
            cur.execute("delete from form1 where uid = (%s)", (id,))
            mydb.commit()
            err_message = "Your Form1 Does NOT fufil the requirements and/or match your transcript please try again :)"
            return render_template("error.html", err_message = err_message)
    #PHD student
    if x['enrolledas'] == 'PhD':
        if((prereqmatch(id) == 0) or (comparef1andtranscript(id)==0)): 
            cur.execute("delete from form1 where uid = (%s)", (id,))
            mydb.commit()
            err_message = "Your Form1 Does NOT fufil the requirements and/or match your transcript please try again :)"
            return render_template("error.html", err_message = err_message)

    return render_template("success.html", id = id)

################################################  FORM 1 VIEW  ##############################################################
# View the form 1 of said student
#############################################################################################################################
@app.route("/viewform1/<id>", methods = ['GET'])
def view_form1(id):
    cur = mydb.cursor(buffered=True, dictionary=True)
    faculty_type = {}
    if session.get('faculty_type'): 
        faculty_type = session.get('faculty_type')
    cur.execute("select c_catalogue.dept, c_catalogue.cnum, c_catalogue.title from form1 inner join c_catalogue on form1.cid = c_catalogue.cid where uid = (%s)", (id,))
    x = cur.fetchall()
    #get the name of the student
    cur.execute("select firstname, lastname from users where uid = (%s)", (id,))
    name= cur.fetchone()
    user_type = session['user_type']

    return render_template("viewform1.html", x = x, id = id, user_type = user_type, name = name, faculty_type = faculty_type)

################################################  APPLY FOR GRADUATION  ##############################################################
# Student applies for graduation here
######################################################################################################################################
@app.route('/applyforGrad/<id>')
def applyforgrad(id):
    #do the auditing and then change button name to pending graduation approval
    
    cur = mydb.cursor(buffered=True, dictionary=True)
    
    #this checks all necesarry values to see if they can graduate
    cur.execute("select * from students where uid = (%s)", (id,))
    x = cur.fetchone()
    advisor_id = x['advisor_id']

    if(advisor_id == None):
        err_message = "No advisor ID found"
        return render_template("error.html", err_message = err_message)
    
    #calculate total credit and gpa 
    total_credit = 0 
    g = 0
    cur.execute("select c_history.fgrade, c_catalogue.cred from c_history inner join c_catalogue on c_history.cid = c_catalogue.cid where uid = (%s)", (id,))
    y = cur.fetchall()
    print(y)
    #if they actually have a transcript calculate it 
    if y: 
        for i in y: 
            if i['cred'] == 'IP':
                flash("You cannot Apply for Graduation If You Have Courses In Progress")
                return redirect(url_for('studentdirectory', id=id, user_type = session['user_type']))
            total_credit += i['cred']
        
        
        g = gpa(total_credit, y)
    

    cur.execute("select * from gradrequests where advisee_id = (%s)", (id,))
    t = cur.fetchone()
    print(num_of_non_cs(id))
    print(grades_below_b(id, y))
    print(prereqmatch(id))
    print(comparef1andtranscript(id))
    print(g)
    print(total_credit)
    #if the student is as a masters student 
    if x['enrolledas'] == 'Masters':
        if t: 
            if ((num_of_non_cs(id) == 0) or (total_credit < 30) or (g < 3.0) or (grades_below_b(id, y) == 0) or (prereqmatch(id) == 0) or (comparef1andtranscript(id)==0)):
                cur.execute("update gradrequests set approved = (%s) where advisee_id =(%s)", (0,id))
                mydb.commit()

                return redirect(url_for('studentdirectory', id=id))
            
            cur.execute("update gradrequests set approved = (%s) where advisee_id =(%s)", (1,id))
            mydb.commit() 
            return redirect(url_for('studentdirectory', id=id))
        #fail
        if ((num_of_non_cs(id) == 0) or (total_credit < 30) or (g < 3.0) or (grades_below_b(id,y) == 0) or (prereqmatch(id) == 0) or (comparef1andtranscript(id)==0)):
            cur.execute("insert into gradrequests (advisee_id, advisor_id, approved) values ((%s), (%s), (%s))", (id, advisor_id, 0,))
            mydb.commit()
            
            return redirect(url_for('studentdirectory', id=id, user_type = session['user_type']))

        #pass
        cur.execute("insert into gradrequests (advisee_id, advisor_id, approved) values ((%s), (%s), (%s))", (id, advisor_id, 1,))
        mydb.commit() 
        return redirect(url_for('studentdirectory', id=id, user_type = session['user_type'])) 
    elif x['enrolledas'] == 'PhD':
        #if the student is a PHD student
        #need to get the approval status of their thesis
        cur.execute("select approved from phdthesis where uid = (%s)", (id,))
        q = cur.fetchone()
        appr = q['approved']
        #if this is the second gradrequest for the pHd student
        if t: 
            #fail
            if((total_credit < 36) or  (g < 3.5) or (appr == 0) or (grades_below_b(id,y) == 0) or (prereqmatch(id) == 0) or (comparef1andtranscript(id)==0)): 
                # print("fail")
                cur.execute("update gradrequests set approved = (%s) where advisee_id =(%s)", (0,id))
                mydb.commit()
                return redirect(url_for('studentdirectory', id=id))
            #pass
            cur.execute("update gradrequests set approved = (%s) where advisee_id =(%s)", (1,id))        
            mydb.commit()  

            return redirect(url_for('studentdirectory', id=id, user_type = session['user_type']))
        #if they fail the audit
        if((total_credit < 36) or  (g < 3.5) or (appr == 0) or (grades_below_b(id,y) == 0) or (prereqmatch(id) == 0) or (comparef1andtranscript(id)==0)): 
            print("fail")
            cur.execute("insert into gradrequests (advisee_id, advisor_id, approved) values ((%s), (%s), (%s))", (id, advisor_id, 0,))
            mydb.commit()
            return redirect(url_for('studentdirectory', id=id, user_type = session['user_type']))
        #if they pass the audit 
        cur.execute("insert into gradrequests (advisee_id, advisor_id, approved) values ((%s), (%s), (%s))", (id, advisor_id, 1,))
        mydb.commit()  

    return redirect(url_for('studentdirectory', id=id, user_type = session['user_type']))

################################################  GPA FUNCTION  ##############################################################
# Calculate the total gpa of the student
##############################################################################################################################
def gpa(total_credit, clist): 
    #list of grades w numbers
    grade_point = {'A+': 4.00, 'A': 4.00, 'A-': 3.67, 'B+': 3.33, 'B':3.00, 'B-':2.67, 'C+': 2.33, 'C': 2.00, 'C-': 1.67, 'D+':1.33, 'D': 1.00, 'D-': 0.67, 'F': 0.00}
    # g = cur.fetchall()
    grade_total = 0.00
    for i in clist:  
        #find the corresponding grade total w dictionary and add it to our GPA total
        grade_total += grade_point.get(i['fgrade']) * i['cred']

    gpa = round(grade_total/total_credit, 2)
    return gpa

################################################  NUM OF NON CS COURSES  ##############################################################
# Calculate the total numebr of non computer science courses in transcript
#######################################################################################################################################
def num_of_non_cs(id):
    cur = mydb.cursor(buffered=True, dictionary=True)
    cur.execute("select c_catalogue.dept from c_history inner join c_catalogue on c_history.cid = c_catalogue.cid where uid = (%s)", (id,))
    x = cur.fetchall()
    num_non_cs = 0
    for i in x:
        if(i['dept'] != 'CSCI'):
            num_non_cs = num_non_cs + 1

    if(num_non_cs > 2):
        return 0
    return 1

################################################  GRADES BELOW B  ##############################################################
# Checks how many grades are below b, if two are below b then badbad
################################################################################################################################
def grades_below_b(id, x):

    cur = mydb.cursor(buffered=True, dictionary=True)
    # cur.execute("select grade1, grade2, grade3, grade4, grade5, grade6, grade7, grade8, grade9, grade10, grade11, grade12 from transcript where user_id = (%s)", (id,))
    # x = cur.fetchone()
    num_below = 0
    for i in x:
        letter = i['fgrade']
        if((letter == 'B-') or (letter == 'C+') or (letter == 'C') or (letter == 'C-') or (letter == 'D+') or (letter == 'D') or (letter == 'D-') or (letter == 'F')):
            num_below = num_below + 1
    #now lets see if the user is a masters or a PHD grad 
    cur.execute("select enrolledas from students where uid = (%s)", (id,))
    enrolled = cur.fetchone()
    if enrolled == 'Masters':
        if (num_below > 2):
            return 0
    if enrolled == 'PhD':
        if num_below > 1: 
            return 0

    if (num_below > 3): 
        cur.execute("UPDATE students SET suspended = 1 WHERE uid = (%s)", (id,))
        mydb.commit()

    return 1

################################################  GRADUATION REQUESTS VIEW  ##############################################################
# View all graduation requests
##########################################################################################################################################
@app.route('/gradrequests', methods = ['GET', 'POST'])
def gradrequests():
    cur = mydb.cursor(buffered=True, dictionary=True)
    #the only people that can see this page are the sys admin and gradsec 
    if(session.get('user_type') != 'Systems Administrator') and (session.get('faculty_type')['grad_sec']) == False:
        err_message = "You do not have access to this form bring up your clearance with Gordan"
        return render_template("error.html", err_message = err_message)

    #now select the names using the user_ids
    cur.execute("select users.firstname, users.lastname, gradrequests.advisee_id, gradrequests.advisor_id, gradrequests.approved from users inner join gradrequests on users.uid = gradrequests.advisee_id")
    x = cur.fetchall()
    user_type = session['user_type']
    return render_template("gradrequests.html", x = x, user_type = user_type)

################################################  GRADUATION ACTION ##############################################################
# Allow student to graduate manually
#################################################################################################################################
@app.route('/graduate/<id>')
def graduate(id):

    cur = mydb.cursor(buffered=True, dictionary=True)
    cur.execute("update users set type = 'Alumni' where uid = (%s)", (id,))
    mydb.commit()
    cur.execute("delete from gradrequests where advisee_id = (%s)", (id,))
    mydb.commit()
    cur.execute('select students.enrolledas from students where uid = (%s)', (id,))
    enrolledas = cur.fetchone()
    cur.execute('select max(c_catalogue.year) as year, c_history.sem from c_history inner join c_catalogue on c_history.cid = c_catalogue.cid where c_history.uid = (%s)', (id,))
    grad = cur.fetchone()
    year = int(grad['year'])
    sem = grad['sem']
    cur.execute('insert into alumni(uid, enrolledas, gradYear, gradSem) values (%s, %s,%s, %s) ', (id, enrolledas['enrolledas'], year, sem ))
    mydb.commit()
    cur.execute("delete from students where uid = (%s)", (id,))
    mydb.commit()
    return redirect(url_for('gradrequests'))

################################################  ALUMNI VIEW ##############################################################
# View all alumni
############################################################################################################################
@app.route('/alumni', methods = ['GET', 'POST'])
def alumni():
    cur = mydb.cursor(buffered=True, dictionary=True)
    print(session.get('faculty_type'))
    #the only people that can see this page are the sys admin and gradsec 
    if(session.get('user_type') != 'Systems Administrator') and (session.get('faculty_type')['grad_sec']) == False:
        err_message = "You do not have access to this form bring up your clearance with Gordan"
        return render_template("error.html", err_message = err_message)
    #be able to insert the correct data into the drop down menus: 
    #Grad Year
    cur.execute('select distinct(gradYear) from alumni')
    years = cur.fetchall()
    #grad sem 
    cur.execute('select distinct(gradSem) from alumni')
    sems = cur.fetchall()
    user_type = session['user_type']
    if request.method == 'POST': 
        degree = request.form['Degree']
        gradYear = request.form['Year']
        gradSem = request.form['sem']
        if 'all' ==  degree and 'all' == gradYear and 'all' == gradSem:
            cur.execute("SELECT * FROM users WHERE type = 'Alumni'")
            x=cur.fetchall()
        elif 'all' == degree and 'all' == gradYear and 'all' != gradSem: 
            cur.execute('select users.uid, users.firstname, users.lastname, users.email, alumni.* from users inner join alumni on users.uid = alumni.uid where alumni.gradSem = (%s)',(gradSem,))
            x = cur.fetchall()
        elif 'all' == degree and 'all' != gradYear and 'all'== gradSem : 
            cur.execute('select users.uid, users.firstname, users.lastname, users.email, alumni.* from users inner join alumni on users.uid = alumni.uid where alumni.gradYear = (%s)', (gradYear,))
            x = cur.fetchall()
        elif 'all' != degree and 'all' == gradYear and 'all' == gradSem:
            cur.execute('select users.uid, users.firstname, users.lastname, users.email, alumni.* from users inner join alumni on users.uid = alumni.uid where alumni.enrolledas = (%s)',(degree,))
            x = cur.fetchall()
        elif 'all' != degree and 'all' != gradYear and 'all' == gradSem:
            cur.execute('select users.uid, users.firstname, users.lastname, users.email, alumni.* from users inner join alumni on users.uid = alumni.uid where alumni.enrolledas = (%s) and alumni.gradYear = (%s)', (degree, gradYear))
            x = cur.fetchall()
        elif  'all' == degree and 'all' != gradYear and 'all' != gradSem:
            cur.execute('select users.uid, users.firstname, users.lastname, users.email, alumni.* from users inner join alumni on users.uid = alumni.uid where alumni.gradYear = (%s) and alumni.gradSem = (%s)',(gradYear, gradSem))
            x = cur.fetchall()
        elif 'all' != degree and 'all' == gradYear and 'all' != gradSem:
            cur.execute('select users.uid, users.firstname, users.lastname, users.email, alumni.* from users inner join alumni on users.uid = alumni.uid where alumni.enrolledas = (%s) and alumni.gradSem = (%s)', (degree, gradSem))
            x = cur.fetchall()
        else: 
            cur.execute('select users.uid, users.firstname, users.lastname, users.email, alumni.* from users inner join alumni on users.uid = alumni.uid where alumni.enrolledas = (%s) and alumni.gradSem = (%s) and alumni.gradYear = (%s) ', (degree, gradSem, gradYear))
            x = cur.fetchall()

        
    else: 
        cur.execute("SELECT users.* , alumni.* FROM users inner join alumni on users.uid = alumni.uid")
        x = cur.fetchall()
        
 

    return render_template("alumni.html", x = x, user_type = user_type, sems = sems, years = years)


################################################  ALUMNI DIRECTORY  ################################################
#Show all the info of said alumni
#####################################################################################################################
@app.route('/alumnidirectory/<id>', methods=['GET'])
def alumnidirectory(id):
    cur = mydb.cursor(buffered=True, dictionary=True)
    print(session.get('user_type'))
    # if session.get('user_type') != "Systems Administrator": 
    #     err_message = "You do not have access to this form bring up your clearance with Gordan"
    #     return render_template("error.html", err_message = err_message)
    if int(session.get('id')) != int(id )and session.get('user_type') != "Systems Administrator": 
        err_message = "You do not have access to this form bring up your clearance with Gordan"
        return render_template("error.html", err_message = err_message)
    #the only people that can see this page are the sys admin and gradsec and the actual alumni 
    # if(session.get('user_type') != 'Systems Administrator') and ((session.get('faculty_type')['grad_sec']) == False or session.get('id') != id) :
    #     err_message = "You do not have access to this form bring up your clearance with Gordan"
    #     return render_template("error.html", err_message = err_message)
    cur.execute("SELECT * FROM users WHERE uid = (%s)", (id,))
    y = cur.fetchone()
    
    return render_template("alumnidirectory.html", x=y)


################################################  PERSONAL ALUMNI INFO  ##############################################################
# View the users personal info of alumni such as email, name, etc
###############################################################################################################################
@app.route('/alumnipersonalinfo/<id>')
def alumnipersonalinfo(id):
    cur = mydb.cursor(buffered=True, dictionary=True)
    #the only people that can see this page are the sys admin and gradsec and the actual alumni 

    if(session.get('user_type') != 'Systems Administrator' and (session.get('faculty_type')['grad_sec']) == False and session.get('user_type')):

        err_message = "You do not have access to this form bring up your clearance with Gordan"
        return render_template("error.html", err_message = err_message)
    cur.execute("SELECT * FROM users WHERE uid = (%s)", (id,))
    x = cur.fetchone()

    return render_template("alumnipersonalinfo.html", x = x)

################################################  PERSONAL INFO ALUMNI UPDATE  ##############################################################
# Update the alumni personal info
##############################################################################################################################################
@app.route('/alumnidirectory/<id>/update', methods=['POST'])
def update_alumni(id):
    cur = mydb.cursor(buffered=True, dictionary=True)
    
    # Update the users table
    cur.execute("UPDATE users SET firstname=%s,lastname=%s, email=%s WHERE uid=%s", (
        request.form['fname'],
        request.form['lname'],
        request.form['email'],
        id
    ))
    mydb.commit()
    
    cur.execute("SELECT * FROM users WHERE uid=%s", (id,))
    updated_row = cur.fetchone()
   # print("Updated row in users table:", updated_row)

    return redirect(url_for('alumnidirectory', id=id))

################################################  ADVISOR - STUDENT MATCH  ##############################################################
# Display the advisor match ups with their students
#########################################################################################################################################
@app.route('/asmatch', methods = ['GET', 'POST'])
def asmatch():
    cur = mydb.cursor(buffered=True, dictionary=True)
    #if the user is a student they should not be able to see thematches 
    if session.get('user_type') == 'Alumni' or session.get('user_type') == 'Student':
        err_message = "You do not have access to this form bring up your clearance with Gordan"
        return render_template("error.html", err_message = err_message)
    # Fetch all advisors from the users table
    cur.execute("SELECT * FROM users inner join faculty on users.uid = faculty.uid WHERE faculty.advisor = true and type != 'Systems Administrator'")
    advisors = cur.fetchall()
    # Modify the SQL query to include a join with the users table to get the advisor's information
    cur.execute("SELECT users.firstname as advisor_fname, users.lastname as advisor_lname, users.uid as advisor_uid FROM students inner join users ON students.advisor_id = users.uid")
    x = cur.fetchall()
    if request.method == 'POST': 
        filtered = request.form['advisorName']
        if filtered == 'all': 
            cur.execute("select students.uid, students.advisor_id, users.firstname as stu_fname, users.lastname as stu_lname from students inner join users on users.uid = students.uid")
            students = cur.fetchall()
            length = len(students)
        else:
            cur.execute("select students.uid, students.advisor_id, users.firstname as stu_fname, users.lastname as stu_lname from students inner join users on users.uid = students.uid where students.advisor_id = (%s)", (filtered,))
            students = cur.fetchall()
            length = len(students)
    else:
        #get the students and their names
        cur.execute("select students.uid, students.advisor_id, users.firstname as stu_fname, users.lastname as stu_lname from students inner join users on users.uid = students.uid")
        students = cur.fetchall()
        length = len(students)
    user_type = session['user_type']

    return render_template("asmatch.html", x = x, user_type = user_type, y = students, length = length, advisors = advisors)

################################################  CHANGE ADVISOR - STUDENT MATCH  #######################################################
# Change the advisor of a student
#########################################################################################################################################
@app.route('/changeadvisor/<id>', methods = ['GET'])
def changeadvisor(id):
     #the only people that can see this page are the sys admin and gradsec 
    if(session.get('user_type') != 'Systems Administrator') and (session.get('faculty_type')['grad_sec']) == False:
        err_message = "You do not have access to this form bring up your clearance with Gordan"
        return render_template("error.html", err_message = err_message)

    
    cur = mydb.cursor(buffered=True, dictionary=True)
    cur.execute("select users.firstname as advisor_fname, users.lastname as advisor_lname FROM students LEFT JOIN users ON students.advisor_id = users.uid WHERE students.uid = %s", (id,))
    x = cur.fetchall()
    #get just the student infor
    cur.execute("select firstname, lastname from users where uid = (%s)", (id,))
    y = cur.fetchone()

    # Fetch all advisors from the users table
    cur.execute("SELECT * FROM users inner join faculty on users.uid = faculty.uid WHERE faculty.advisor = true and type != 'Systems Administrator'")
    advisors = cur.fetchall()
    print(advisors)

    return render_template("changeadvisor.html", x=x, advisors=advisors, id = id, y=y)

################################################ PREREQUISITE CHECK  #######################################################
# Check if prerquisites are met
############################################################################################################################
def prereqmatch(id): 
    result = 0
     #connect to database
    cur = mydb.cursor(buffered=True, dictionary=True)
    #first get the courses that have prereqs
    cur.execute("select cnum, prone, prtwo from c_catalogue where prone != 'None'")
    coursecatalog = cur.fetchall()
    #next get all the course numbers in the users transcript
    cur.execute("select c_catalogue.cnum from c_history inner join c_catalogue on c_history.cid = c_catalogue.cid where c_history.uid = (%s)", (id,))
    transcript = cur.fetchall()
    # print(transcript)
    #get the actual coursenumbers from the coursecatalog
    #course = coursecatalog.values()
   # print(coursecatalog)
    #goal is to make a list of only the course numbers in the coursecatalog that have prereqs 
    courses = []
    c_num = []
    for i in coursecatalog: 
        courses.append(i.get('cnum'))
    #get the actual c_nums from the transcript 
    for i in range(len(transcript)):
        c_num.append(transcript[i].get('c_num'))
    for c in c_num: 
        if c in courses: 
            for k in coursecatalog: 
                if k.get('c_num') == c: 
                    if int(k.get('prone')[5:]) not in c_num: 
                        return 0
                    elif(k.get('prtwo') != 'None') and (int(k.get('prtwo')[5:]) not in c_num):
                       # print(k.get('prereq_2'))
                        return 0
    return 1

################################################ UPDATE ADVISOR  #######################################################
# Update the advisor of such student in the database
#########################################################################################################################
@app.route('/update_advisor/<id>', methods=['POST'])
def update_advisor(id):
    advisor_id = request.form['advisorName']
    cur = mydb.cursor(buffered=True, dictionary=True)
    cur.execute('UPDATE students SET advisor_id = %s WHERE uid = %s', (advisor_id, id,))
    mydb.commit()

    #match the statements 
    # Modify the SQL query to include a join with the users table to get the advisor's information
    cur.execute("SELECT students.*, users.firstname as advisor_fname, users.lastname as advisor_lname FROM students LEFT JOIN users ON students.advisor_id = users.uid")
    x = cur.fetchall()

    user_type = session['user_type']

    return redirect(url_for('asmatch', x=x, user_type = user_type))

################################################  COMPARE 1F AND TRANSCRIPT #############################################
#Function to check Form 1 and Transcript :) 
#########################################################################################################################
def comparef1andtranscript(id):
    #establish a connection
    cur = mydb.cursor(buffered=True, dictionary=True)
    #select every cid from the transcript 
    cur.execute("select cid from c_history where uid = (%s)", (id,))
    transcript = cur.fetchall()
    #now lets get every CID from form 1
    cur.execute("select cid from form1 where uid = (%s)", (id,))
    f1 = cur.fetchall()
    
    for k in transcript:
        cur.execute("select form1.cid from form1 where uid = (%s) and cid = (%s)", (id,k['cid']))
        match = cur.fetchone()
        if match == None:
            return 0

    return 1
    
################################################  REJECT GRAD #############################################
#This rejects a grad student and removes them from the grad request table
###########################################################################################################
@app.route('/rejectgrad/<id>')
def rejectgrad(id):
    cur = mydb.cursor(buffered=True, dictionary=True)
    #update database 
    cur.execute("update gradrequests set approved = 2 where advisee_id = (%s)", (id,))
    mydb.commit()
    cur.execute("delete from form1 where uid = (%s)", (id,))
    mydb.commit()
    return redirect(url_for('gradrequests'))

#faculty advisors view thesis
################################################  APPROVE THESIS #############################################
#This approves the thesis of the phd student! 
##############################################################################################################
@app.route('/approvethesis/<id>')
def approvethesis(id):
    cur = mydb.cursor(buffered=True, dictionary=True)
    cur.execute("SELECT * FROM phdthesis WHERE uid = (%s)", (id,))
    x = cur.fetchone()
    return render_template('thesis.html', x = x)

#faculty advisors can approve thesis
################################################  APPROVE HERE? #############################################
#Updates the database!
#############################################################################################################
@app.route('/approvehere/<id>')
def approvehere(id):
    cur = mydb.cursor(buffered=True, dictionary=True)
    cur.execute("UPDATE phdthesis SET approved = 1 WHERE uid = (%s)", (id,))
    mydb.commit()

    return redirect(url_for('approvethesis', id = id))
    
#students can view and change thesis
@app.route('/studentaccessthesis/<id>', methods = ['GET','POST'])
def studentaccessthesis(id):

    # #the only people who can view this page are the sys admin, the grad sec and the pHd student's 
    # if(session.get('user_type') != 'Systems Administrator') or (session.get('faculty_type')['grad_sec']) == False or session.get('id') != id:
    #     err_message = "You do not have access to this form bring up your clearance with Gordan"
    #     return render_template("error.html", err_message = err_message)


    
    cur = mydb.cursor(buffered=True, dictionary=True)
    cur.execute("SELECT * FROM phdthesis WHERE uid = (%s)", (id,))
    x = cur.fetchone()

    if request.method == 'POST':
        newthesis = request.form['thesis']

        cur.execute("UPDATE phdthesis SET thesis = (%s), approved = (%s) WHERE uid = (%s)", (newthesis, 0, id,))
        mydb.commit()
        return redirect(url_for('studentdirectory', id = id))

    return render_template('studentthesis.html', x = x)
################################################  PERSONAL INFO  ##############################################################
# View the users personal info such as email, name, etc
###############################################################################################################################
@app.route('/personalinfo/<id>')
def personalinfo(id):
    cur = mydb.cursor(buffered=True, dictionary=True)
    #first get the student's name from the id 
    cur.execute("SELECT * FROM students JOIN users ON students.uid = users.uid WHERE students.uid = (%s)", (id,))
    x = cur.fetchone()

    return render_template("personalinfo.html", x = x)

################################################  PERSONAL INFO STUDENT UPDATE  ##############################################################
# Update the students personal info
##############################################################################################################################################
@app.route('/studentdirectory/<id>/update', methods=['POST'])
def update_student(id):
    cur = mydb.cursor(buffered=True, dictionary=True)

    # # Update the students table
    # cur.execute("UPDATE students SET firstname=%s,lastname=%s, email=%s WHERE uid=%s", (
    #     request.form['fname'],
    #     request.form['lname'],
    #     request.form['email'],
    #     id
    # # ))
    # mydb.commit()
    
    # Update the users table
    cur.execute("UPDATE users SET firstname=%s, lastname=%s, email=%s WHERE uid=%s", (
        request.form['firstname'],
        request.form['lastname'],
        request.form['email'],
        id
    ))
    mydb.commit()

    # Retrieve the updated row from the database and display its current values
    cur.execute("SELECT * FROM students WHERE uid=%s", (id,))
    updated_row = cur.fetchone()
   # print("Updated row in students table:", updated_row)
    
    cur.execute("SELECT * FROM users WHERE uid=%s", (id,))
    updated_row = cur.fetchone()
   # print("Updated row in users table:", updated_row)

    return redirect(url_for('studentdirectory', id=id, user_type = session['user_type']))

################################################  RESET DB  ##############################################################
# Reset the database 
##############################################################################################################################################

@app.route('/reset')
def reset_db():
    cur = mydb.cursor(buffered=True, dictionary=True)
    # Delete all the data from the tables
    cur.execute('delete from studentapplicationreviews')
    mydb.commit()
    cur.execute('delete from transcript')
    mydb.commit()
    cur.execute('delete from recommendationletters')
    mydb.commit()
    cur.execute('DELETE FROM phdthesis')
    mydb.commit()
    cur.execute('delete from gradrequests')
    mydb.commit()
    cur.execute('DELETE FROM studentapplication')
    mydb.commit()
    cur.execute('DELETE FROM form1')
    mydb.commit()
    cur.execute('delete from advising_form')
    mydb.commit()
    cur.execute('DELETE FROM c_history')
    mydb.commit()
    cur.execute('DELETE FROM faculty')
    mydb.commit()
    cur.execute('DELETE FROM alumni')
    mydb.commit()
    cur.execute('DELETE FROM students')
    mydb.commit()
    cur.execute('DELETE FROM users')
    mydb.commit()

    # Insert the initial data into the tables
    #insert users
    #narahari
    cur.execute("insert into users (uid,  email, password, firstname,lastname,address, type,ssn,  status)values(50505050, 'bn@mcu.edu', 'adminpass', 'Professor', 'Narahari', 'a house', 'Faculty', null, 068983937)")
    mydb.commit()
    
    #choi 
    cur.execute("insert into users (uid,  email, password, firstname,lastname,address, type,ssn,  status)values(91217439, 'choi@mcu.edu', 'adminpass', 'Professor', 'Choi', 'a home', 'Faculty', null, 587132839 )")
    mydb.commit()

    #parmer
    cur.execute(
    "INSERT INTO users(uid, email, password, firstname, lastname, address, type,status, ssn) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
    (51515151, 'parmer@mcu.edu', 'adminpass', 'Professor', 'Parmer', 'Elliot', 'Faculty', None, 836760235))
    mydb.commit()
    #elvis
    cur.execute(
    "INSERT INTO users(uid, email, password, firstname, lastname, address, type, status, ssn) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
    (30253003, 'elvis@mcu.edu', 'adminpass', 'Elvis', 'Presley', 'Graceland', 'Faculty', None, 102995910))
    mydb.commit()
    #billie
    cur.execute(
        "INSERT INTO users(uid, email, password, firstname, lastname, address, type,status, ssn) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (88888888, 'billie@mcu.edu', 'adminpass', 'Billie', 'Holiday', 'Ill be seeing you', 'Student', 'Admitted', 295741305)
    )
    mydb.commit()
    #diana
    cur.execute(
        "INSERT INTO users(uid, email, password, firstname, lastname, address, type, status, ssn) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (99999999, 'diana@mcu.edu', 'adminpass', 'Diana', 'Krall', 'SEH 4th Floor', 'Student', 'Admitted', 688205810)
    )
    mydb.commit()
    #johnny l 
    cur.execute(
        "INSERT INTO users(uid, email, password, firstname, lastname, address, type, status, ssn ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (12312312, 'johnlennon@mcu.edu', 'adminpass', 'John', 'Lennon', "Yoko's House", 'Applicant', 'Application, Transcript and Recomendation Letters Complete', 111111111)
    )
    mydb.commit()
    #ringo starr
    cur.execute(
        "INSERT INTO users(uid, email, password, firstname, lastname, address, type, status, ssn) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (66666666, 'ringo@mcu.edu', 'adminpass', 'Ringo', 'Starr', 'Drums Avenue', 'Applicant', 'Not Started', 222111111)
    )
    mydb.commit()
    #paully 
    cur.execute(
        "INSERT INTO users(uid, email, password, firstname, lastname, address, type, status, ssn ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (55555555, 'paul@mcu.edu', 'adminpass', 'Paul', 'McCartney', 'Penny Lane', 'Student', 'Admitted', 491936718)
    )
    mydb.commit()
    cur.execute(
        "INSERT INTO users(uid, email, password, firstname, lastname, address, type, ssn, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (66666667, 'george@mcu.edu', 'adminpass', 'George', 'Harrison', 'Strawberry Fields', 'Student', 509250028, 'Admitted')
    )
    mydb.commit()
    cur.execute(
        "INSERT INTO users(uid, email, password, firstname, lastname, address, type,  ssn, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (66666689, 'ringo2@mcu.edu', 'adminpass', 'Ringo2', 'Starr', 'Glass Onion Way', 'Student', 831055135, 'Admitted')
    )
    mydb.commit()   
    cur.execute(
        "INSERT INTO users(uid, email, password, firstname, lastname, address, type, ssn, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (77777777, 'eric@mcu.edu', 'adminpass', 'Eric', 'Clapton', 'Tears in Heaven Blvd', 'Alumni', 681782622, 'Admitted')
    )
    mydb.commit()
    cur.execute(
    "INSERT INTO users(uid, email, password, firstname, lastname, address, type, status, ssn ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
    (109999999, 'ryanreynolds@gwu.edu', 'adminpass', 'Ryan', 'Reynolds', "yo mama's house", 'Systems Administrator', None, 987654321)
    )
    mydb.commit()
    cur.execute(
    "INSERT INTO users(uid, email, password, firstname, lastname, address, type, status, ssn) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
    (88833888, 'drpepper@gwu.edu', 'adminpass', 'Dr', 'Pepper', 'ur mom st', 'Faculty', None, 123456789)
    )
    mydb.commit()

    #insert into faculty 
    cur.execute("insert into faculty (uid, advisor, grad_sec, cac, reviewer, registrar) values(50505050, true, false, false, true, false)")
    mydb.commit()
    cur.execute("insert into faculty (uid, advisor, grad_sec, cac, reviewer, registrar) values(91217439, false, false, false, false, false)")
    mydb.commit()

    faculty = [
    (88833888, False, True, False, False, False),
    (109999999, True, True, True, True, True),
    (51515151, True, False, False, False, False),
    (30253003, False, False, True, False, False)
    ]

    # execute the INSERT statement for each row of data
    for row in faculty:
        cur.execute("INSERT INTO faculty (uid, advisor, grad_sec, cac, reviewer, registrar) VALUES (%s, %s, %s, %s, %s, %s)", row)
        mydb.commit()

    #insert into students 
    #insert into c_history
    c_history = [
        (88888888, 2, 'IP', 'F', 2023,50505050),
        (88888888, 3, 'IP', 'F', 2023,88888888), 
        (55555555, 1, 'A', 'S', 2023, 0),
        (55555555, 3, 'A', 'S', 2022, 91217439), 
        (55555555, 2, 'A', '', 2023, 50505050),
        (55555555, 5, 'A', 'S', 2023, 0), 
        (55555555, 6, 'A', 'S', 2023, 0), 
        (55555555, 7, 'B', 'S', 2023, 0), 
        (55555555, 9, 'B', 'S', 2023, 0), 
        (55555555, 13, 'B', 'S', 2023, 0), 
        (55555555, 14, 'B', 'S', 2023, 0), 
        (55555555, 8, 'B', 'S', 2023, 0),  
        (66666667, 21, 'C', 'F', 2023, 0), 
        (66666667, 1, 'B', 'S', 2023, 0), 
        (66666667, 2, 'B', 'S', 2023, 50505050), 
        (66666667, 3, 'B', 'S', 2023, 91217439), 
        (66666667, 5, 'B', 'S', 2023, 0), 
        (66666667, 6, 'B', 'S', 2023, 0), 
        (66666667, 7, 'B', 'S', 2023, 0), 
        (66666667, 8, 'B', 'S', 2023, 0), 
        (66666667, 14, 'B', 'S', 2023, 0), 
        (66666667, 15, 'B', 'S', 2023, 0), 
        (66666689, 1, 'A','F', 2022, 0), 
        (66666689, 2, 'A','F', 2022, 50505050), 
        (66666689, 3, 'A','F', 2022, 91217439), 
        (66666689, 4, 'A','F', 2022, 0), 
        (66666689, 5, 'A','F', 2022, 0), 
        (66666689, 6, 'A','F', 2022, 0), 
        (66666689, 7, 'A','F', 2022, 0), 
        (66666689, 8, 'A','F', 2022, 0), 
        (66666689, 9, 'A','F', 2022, 0), 
        (66666689, 10, 'A','F', 2022, 0), 
        (66666689, 11, 'A','F', 2022, 0), 
        (66666689, 12, 'A','S', 2023, 0), 
        (77777777, 1, 'B', 'S', 2013, 0), 
        (77777777, 3, 'B', 'S', 2012, 91217439), 
        (77777777, 2, 'B', 'F', 2012, 50505050), 
        (77777777, 5, 'B', 'S', 2014, 0), 
        (77777777, 6, 'B', 'S', 2014, 0), 
        (77777777, 7, 'B', 'S', 2014, 0), 
        (77777777, 8, 'B', 'S', 2014, 0), 
        (77777777, 14, 'A', 'S', 2014, 0), 
        (77777777, 15, 'A', 'S', 2014, 0), 
        (77777777, 16, 'A', 'S', 2014, 0)
    ]
    for row in c_history: 
        cur.execute('insert into c_history(uid, cid, fgrade, sem, year, snum) values(%s, %s, %s, %s,%s, %s)', row)
        mydb.commit()
    #insert into phd thesis
    
    # Insert the initial data into the tables dummy data below



    #--regs starting data

    

    
    #--Diana Krall    
    cur.execute("insert into students values(99999999, NULL, 'Masters', 0,0,0)")
    mydb.commit()

    #--ADS STARTING DATA
    #--Paul

    
    cur.execute("insert into students values(55555555,50505050, 'Masters', 0, 1,1)")
    mydb.commit()
    

    #--George Student
    cur.execute("insert into students values(66666667, 51515151, 'Masters', 0, 1,1)")
    mydb.commit()
    #--ringo2 Student, PHD thesis
    cur.execute("insert into students values(666666689, 51515151, 'PhD', 0,1,1)")
    mydb.commit()
    
    cur.execute("insert into phdthesis (uid, thesis, approved) values (%s, %s, %s)", (66666689, "Desmond has a barrow in the marketplace Molly is the singer in a bandDesmond says to Molly, 'Girl, I like your face'And Molly says this as she takes him by the handOb-la-di, ob-la-daLife goes on, brahLa, la, how the life goes onOb-la-di, ob-la-daLife goes on, brahLa, la, how the life goes onDesmond takes a trolley to the jeweler's storeBuys a 20 carat golden ring (ring)Takes it back to Molly waiting at the door And as he gives it to her, she begins to sing (sing)", 0))
    mydb.commit()
    #--eric clapton
    cur.execute("insert into alumni values(77777777, 'Masters', 2014, 'S')")
    mydb.commit()

    cur.execute("INSERT INTO transcript VALUES (12312312, '', 'University Of Tulane', 'Registrar Office', 'Previous College', 'tulane@tulane.university', '', NULL);")
    mydb.commit()

    cur.execute("INSERT INTO recommendationletters VALUES (12312312, NULL, NULL, NULL, 'University Of Tulane', 'Registrar Office', 'Previous College', 'tulane@tulane.university', '', NULL);")
    mydb.commit()

    cur.execute("INSERT INTO recommendationletters VALUES (12312312, NULL, NULL, NULL,'Professor Khalid', 'Department OF Science', 'Tulane University', 'Khalid@tulane.university', '', NULL);")
    mydb.commit()

    cur.execute("INSERT INTO recommendationletters VALUES (12312312, NULL, NULL, NULL,'Daisy Simons', 'Department of Health', 'Therapists', 'Therapists@tulane.university', '', NULL);")
    mydb.commit()

    cur.close()

    return redirect(url_for('landing_page'))

app.run(host= '0.0.0.0', port = 8080)

