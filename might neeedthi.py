@app.route('/results', methods=['GET', 'POST'])
#  Method to search for useres through the database : have to add more to this as only the gs and admin can do so 
def results():

    cursor = mydb.cursor(buffered=True, dictionary=True)

   
    if request.method == "POST":
        # print("Dont Work ")
        search = request.form["q"]
        # print(search)
        cursor.execute("SELECT * FROM users WHERE lastname LIKE %s",
                       ('%' + search + '%', ))

        no = cursor.fetchall()

    return render_template("dummy.html", x=no)