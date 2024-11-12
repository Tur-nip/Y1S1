#Khoo Wenn Honn
#TP065779
def userlogin():
        print("\n"+"="*32+"Python Assignment Bank"+"="*32)
        userid = input("Please enter your User ID:")
        userpass = input("Please enter your password:")
        with open("userauthen.txt","r") as fh:
                access = "denied"
                for recline in fh:
                        reclist = recline.strip().split(":")
                        if reclist[0] == userid and reclist[1] == userpass:
                                access = reclist
                                break
                if access == "denied":
                        print("\n"+"Login is not successful...!!")
                else:
                        print("\n"+"Login is successful...")
        return access

def genid(perm):
    with open("id.txt","r") as idfh:
        rec = idfh.readline()
        reclist = rec.strip().split(":")
        if perm == "customer":
                acc = "CUS"
                oldid = reclist[0][3:]
        elif perm == "admin":
                acc = "ADM"
                oldid = reclist[1][3:]
        elif perm == "transaction":
                acc = "TRN"
                oldid = reclist[2][3:]
        nextid = int(oldid) + 1
        if len(str(nextid)) == 1:
                newid = "0000"+str(nextid)
        elif len(str(nextid)) == 2:
                newid = "000"+str(nextid)
        elif len(str(nextid)) == 3:
                newid = "00"+str(nextid)
        elif len(str(nextid)) == 4:
                newid = "0"+str(nextid)
        elif len(str(nextid)) == 5:
                newid = str(nextid)
        newid = acc+newid
        if perm == "customer":
                reclist[0] = newid
        elif perm == "admin":
                reclist[1] = newid
        elif perm == "transaction":
                reclist[2] = newid
        rec =":".join(reclist)
        with open("id.txt","w") as fh:
                fh.write(rec)
                return newid

def addadmin():
    userid = genid("admin")
    userpass = userid
    print("Admin ID: ",userid)
    print("Admin Password: ",userpass)
    username = input("Please enter your name: ")
    acctype = "2"
    with open("userauthen.txt","a") as fh:
        rec = userid+":"+userpass+":"+username+":"+acctype+"\n"
        print("Admin(",userid+ ")is successfully added!"+"\n")
        fh.write(rec)

def addcustomer():
        userid = genid("customer")
        userpass = userid
        print("Customer ID: ",userid)
        print("Customer Password: ",userpass)
        username = input("Please enter your name: ")
        acctype = "3"
        ic = input("Please enter the IC number: ")
        employ = input("Please enter the occupation: ")
        phoneno = input("Please enter the phone number: ")
        email = input("Please enter the email: ")
        type_acc = input("Please select [savings] or [current] account type: ")
        accbal = input("Please enter the balance of the account: ")
        authentication = ic.isdigit() and employ.isalpha() and phoneno.isnumeric() and (type_acc == "savings" or type_acc == "current") and accbal.isdigit()
        while authentication == False:
                print("Wrong Info Detected, Please Try Again!!!")
                username = input("Please enter your name: ")
                acctype = "3"
                ic = input("Please enter the IC number: ")
                employ = input("Please enter the occupation: ")
                phoneno = input("Please enter the phone number: ")
                email = input("Please enter the email: ")
                type_acc = input("Please select [savings] or [current] account type: ")
                accbal = input("Please enter the balance of the account: ")
                authentication = ic.isdigit() and employ.isalpha() and phoneno.isnumeric() and (type_acc == "savings" or type_acc == "current") and accbal.isdigit()
        with open("userauthen.txt","a") as fh:
                rec = userid+":"+userpass+":"+username+":"+acctype+"\n"
                print("Customer(",userid+ ")is successfully added!!!!")
                fh.write(rec)
        with open("database.txt","a") as fh:
                rec = userid+":"+username+":"+ic+":"+employ.upper()+":"+type_acc.lower()+":"+phoneno+":"+email+":"+accbal+"\n"
                print("Customer(",userid+")is successfully added into database!!!!"+"\n")
                fh.write(rec)
       
def findcus(cusid):#used to get a specific profile from userid into a list
        findrec = []
        with open("database.txt","r") as fh:
                for rec in fh:
                        reclist = rec.strip().split(":")
                        findrec.append(reclist) 
        norec = len(findrec)
        for cnt in range(0,norec):
                if cusid == findrec[cnt][0]:
                        return findrec[cnt]
       

def editbal(userid,newbal):
        #read all record in a list of lists
        allrec = []
        with open("database.txt","r") as fh:
                for rec in fh:
                        reclist = rec.strip().split(":")
                        allrec.append(reclist) #list of lists
        index = -1
        norec = len(allrec)
        for cnt in range(0,norec):
                if userid == allrec[cnt][0]:
                        index = cnt
                        break
        
        allrec[index][7] = str(newbal)
        with open("database.txt","w") as fh:
                norec = len(allrec)
                for cnt in range(0,norec):
                        rec =":".join(allrec[cnt])+"\n"
                        fh.write(rec)

def maketransaction(logindetails):
        import datetime as dt
        transid = genid("transaction")
        transtype = input("Please choose action[deposit(d)]/[withdraw(w)]: ")
        action_check = transtype != "d" or transtype != "deposit" or transtype != "w" or transtype != "withdraw"
        while action_check == False:
                transtype = input("No such action, please choose the correct action[deposit(d)]/[withdraw(w)]: ")
                action_check = (transtype != "d") or (transtype != "deposit") or (transtype != "w") or (transtype != "withdraw")
        date = dt.date.today()
        strdate = date.strftime("%d-%m-%Y")
        cusid = logindetails[0]
        cusdetailslist = findcus(cusid)
        acc_type = cusdetailslist[4]
        oldbal = cusdetailslist[7]
        if transtype.lower() == "deposit" or transtype.lower()=="d":
                with open("transactions.txt","a") as fh:
                        amount = input("Please enter the amount for deposit :(RM)")
                        authentication = amount.isnumeric()
                        while authentication == False:
                                amount = input("Non-numeric detected, Please enter the amount for deposit again :(RM)")
                                authentication = amount.isnumeric()
                        newbal = int(oldbal) + int(amount)
                        trans = transid+":"+"deposit"+":"+amount+":"+cusid+":"+strdate+":"+str(newbal)+"\n"
                        print("\n"+"="*87)
                        print("Deposit of " +"RM"+amount+ " is added into account!!! New total balance of account is " +"RM"+str(newbal))
                        print("="*87+"\n")
                        editbal(cusid,newbal)
                        fh.write(trans)

        elif transtype.lower() == "withdraw" or transtype.lower() =="w":
                if acc_type == "savings":
                        amount = input("Please enter the amount for withdrawal :(RM)")
                        authentication = amount.isnumeric()
                        while authentication == False:
                                amount = input("Non-numeric detected, Please enter the amount for deposit again :(RM)")
                                authentication = amount.isnumeric()
                        newbal = int(oldbal) - int(amount)
                        if int(newbal) < 100:
                                print("Transaction cannot be done as customer will go under RM 100 after transaction!! NOTE:MIN BALANCE = RM100")
                        elif int(newbal) >= 100:
                                with open("transactions.txt","a") as fh:
                                        trans = transid+":"+"withdrawal"+":"+amount+":"+cusid+":"+strdate+":"+str(newbal)+"\n"
                                        print("\n"+"="*87)
                                        print("Withdrawal of " +"RM"+amount+ " is taken from account!!! New total balance of account is " +"RM"+str(newbal))
                                        print("="*87+"\n")
                                        editbal(cusid,newbal)
                                        fh.write(trans)
                if acc_type == "current":
                        amount = input("Please enter the amount for withdrawal :(RM)")
                        authentication = amount.isnumeric()
                        while authentication == False:
                                amount = input("Non-numeric detected, Please enter the amount for deposit again :(RM)")
                                authentication = amount.isnumeric()
                        newbal = int(oldbal) - int(amount)
                        if int(newbal) < 500:
                                print("Transaction cannot be done as customer will go under RM 500 after transaction!! NOTE:MIN BALANCE = RM500")
                        elif int(newbal) >= 500:
                                with open("transactions.txt","a") as fh:
                                        trans = transid+":"+"withdrawal"+":"+amount+":"+cusid+":"+strdate+":"+str(newbal)+"\n"
                                        print("\n"+"="*87)
                                        print("Withdrawal of " +"RM"+amount+ " is taken from account!!! New total balance of account is " +"RM"+str(newbal))
                                        print("="*87+"\n")
                                        editbal(cusid,newbal)
                                        fh.write(trans)

def dispalluser():
        with open("userauthen.txt","r") as fh:
                print("="*87)
                print("|"+"User ID".ljust(15)+"|"+"User Password".ljust(15)+"|"+"User Name".center(40)+"|"+"Account Type"+"|")
                print("="*87)
                for rec in fh:
                        reclist = rec.strip().split(":")
                        print("|"+reclist[0].ljust(15)+"|"+reclist[1].ljust(15)+"|"+reclist[2].ljust(40)+"|"+reclist[3].center(12)+"|")
                print("="*87)

def changepass(logindetails):
        #read all record in a list of lists
        allrec = []
        with open("userauthen.txt","r") as fh:
                for rec in fh:
                        reclist = rec.strip().split(":")
                        allrec.append(reclist) #list of lists
        newpass = input("Please enter the new password: ")
        index = -1
        norec = len(allrec)
        for cnt in range(0,norec):
                if logindetails[0] == allrec[cnt][0]:
                        index = cnt
                        break
        
        allrec[index][1] = newpass
        with open("userauthen.txt","w") as fh:
                norec = len(allrec)
                for cnt in range(0,norec):
                        rec =":".join(allrec[cnt])+"\n"
                        fh.write(rec)
        
        print("\n"+"="*87)
        print("Password is changed successfully!".center(87))
        print("="*87+"\n")

def editinfo():
        allrec = []
        with open("database.txt","r") as fh:
                for rec in fh:
                        reclist = rec.strip().split(":")
                        allrec.append(reclist) #list of lists\
        cusid = input("Please enter the Customer ID to edit: ")
        newemploy = input("Please enter the new occupation: ")
        newacc_type = input("Please enter new account type (savings/current): ")
        newphno = input("Please enter new phone number: ")
        newemail = input("Please enter new email :")
        newbal = input("Please enter new balance :")
        authentication = newemploy.isalpha() and (newacc_type == "savings" or newacc_type == "current") and newphno.isdigit() and newbal.isdigit()
        while authentication == False:
                        print("Error detected with info given!!! Please check and try again!!!")
                        cusid = input("Please enter the Customer ID to edit: ")
                        newemploy = input("Please enter the new occupation: ")
                        newacc_type = input("Please enter new account type (savings/current): ")
                        newphno = input("Please enter new phone number: ")
                        newemail = input("Please enter new email :")
                        newbal = input("Please enter new balance :")
                        authentication = newemploy.isalpha() and (newacc_type == "savings" or newacc_type == "current") and newphno.isdigit() and newbal.isdigit()
        index = -1
        norec = len(allrec)
        for cnt in range(0,norec):
                if cusid == allrec[cnt][0]:
                        index = cnt
                        break
        
        allrec[index][3] = newemploy.upper()
        allrec[index][4] = newacc_type
        allrec[index][5] = newphno
        allrec[index][6] = newemail
        allrec[index][7] = newbal
        with open("database.txt","w") as fh:
                norec = len(allrec)
                for cnt in range(0,norec):
                        rec =":".join(allrec[cnt])+"\n"
                        fh.write(rec)
        
        print("\n"+"="*87)
        print(("Info for "+cusid+" is successfully editted!!").center(87))
        print("="*87+"\n")

def showcusprofile(logindetails):
        cusid = logindetails[0]
        profile = findcus(cusid)
        cusid = profile[0]
        name = profile [1]
        ic = profile [2]
        employ = profile [3]
        acc_type = profile [4]
        phno = profile [5]
        email = profile [6]
        acc_bal = profile [7]
        print("\n"+"="*87)
        print("|"+"CUSTOMER PROFILE".center(85)+"|")
        print("="*87)
        print("|"+"USER ID:"+cusid.ljust(77)+"|")
        print("|"+"NAME OF CUSTOMER: "+name.upper().ljust(67)+"|")
        print("|"+"IC NUMBER OF CUSTOMER: "+ic.ljust(62)+"|")
        print("|"+"OCCUPATION OF CUSTOMER: "+employ.ljust(61)+"|")
        print("|"+"TYPE OF ACCOUNT: "+acc_type.upper().ljust(68)+"|")
        print("|"+"PHONE NUMBER OF CUSTOMER: "+phno.ljust(59)+"|")
        print("|"+"EMAIL OF CUSTOMER: "+email.ljust(66)+"|")
        print("|"+"BALANCE OF ACCOUNT: RM"+acc_bal.ljust(63)+"|")
        print("="*87)

def statementofaccountheader(cusid,startdate,enddate):
        import datetime as dt
        new_datetime = dt.date.today()
        newdatestr = new_datetime.strftime('%Y-%m-%d')
        cusdetails = findcus(cusid)
        cusname = cusdetails[1]
        acctype = cusdetails[4]
        phno = cusdetails[5]
        email = cusdetails[6]
        print("\n"+"\n"+"Statement of Account")
        print("Customer Name: "+cusname)
        print("Statement Date: "+newdatestr)
        print("Emailed to: "+email)
        print("Statement duration: "+startdate+" to "+enddate)
        print("="*87)
        print("|"+"Date".center(22)+"|"+"Type".center(20)+"|"+"Amount".center(20)+"|"+"Balance".center(20)+"|")
        print("="*87)
        

def statementofaccount(logindetails):
        with open("transactions.txt","r") as fh:
                from datetime import datetime
                startdate = input("Enter start date (dd-mm-yyyy): ")
                enddate = input("Enter end date (dd-mm-yyyy): ")
                valid_date = True
                try:
                       startdate_date = datetime.strptime(startdate,"%d-%m-%Y")
                       enddate_date= datetime.strptime(enddate,"%d-%m-%Y")
                except ValueError:
                        valid_date = False
                while valid_date == False:
                        print("Error in date given!!! Invalid date!!!")
                        startdate = input("Please enter valid start date (dd-mm-yyyy): ")
                        enddate = input("Please enter valid end date (dd-mm-yyyy): ")
                        valid_date = True
                        try:
                               startdate_date = datetime.strptime(startdate,"%d-%m-%Y")
                               enddate_date= datetime.strptime(enddate,"%d-%m-%Y")
                        except ValueError:
                                valid_date = False
                cusid = logindetails[0]
                statementofaccountheader(cusid,startdate,enddate)
                for rec in fh:
                        reclist = rec.strip().split(":")
                        comp_str = reclist[4]
                        comp_date = datetime.strptime(comp_str,"%d-%m-%Y")
                        userid = reclist[3]
                        if comp_date >= startdate_date and comp_date <= enddate_date and cusid == userid:
                                print("|"+reclist[4].rjust(22)+"|"+reclist[1].rjust(20)+"|"+reclist[2].rjust(20)+"|"+reclist[5].rjust(20)+"|")
                print("="*87+"\n"+"\n")


def superusermenu():
    while True:
        print("="*35+"SUPER USER MENU"+"="*36)
        print("\n\t1. Add new admin account")
        print("\t2. Display all user accounts")
        print("\t3. Logout from the system"+"\n")
        choice = input("Please enter your choice: ")
        if choice == "1":
                addadmin()
        elif choice == "2":
                dispalluser()
        elif choice == "3":
                return
        else:
                print("Invalid choice!!! Please choose properly!!!")

def adminmenu(logindetails):
    while True:
        print("="*35+"ADMIN STAFF MENU for",logindetails[2]+"="*30)
        print("\n\t1. Add new customer account")
        print("\t2. Display all user accounts")
        print("\t3. Edit info of customer account")
        print("\t4. Change Admin Acc password")
        print("\t5. Logout from the system")
        choice = input("\n"+"Please enter your choice: ")
        if choice == "1":
                addcustomer()
        elif choice == "2":
                dispalluser()
        elif choice == "3":
                editinfo()
        elif choice == "4":
                changepass(logindetails)
        elif choice == "5":
                return
        else:
                print("Invalid choice!!! Please choose properly!!!")
        
def customermenu(logindetails):
    while True:
        print("="*37+"CUSTOMER MENU"+"="*37)
        print("|"+"1. Show customer profile".center(85)+"|")
        print("|"+"2. Change password".center(85)+"|")
        print("|"+"3. Make a transaction".center(85)+"|")
        print("|"+"4. Print statement of account".center(85)+"|")
        print("|"+"5. Logout from the system".center(85)+"|")
        print("="*87)
        choice = input("\n"+"Please enter your choice: ")
        if choice == "1":
                showcusprofile(logindetails)
        elif choice == "2":
                changepass(logindetails)
        elif choice == "3":
                maketransaction(logindetails)
        elif choice == "4":
                statementofaccount(logindetails)
        elif choice == "5":
                return
        else:
                print("Invalid choice!!! Please choose properly!!!")


#MAIN LOGIC
#==========
while True:
      loginstat = userlogin()
      if loginstat != "denied":
            print("Welcome to the System, "+loginstat[2])
            if loginstat[3] == "1":
                  superusermenu()
            elif loginstat[3] == "2":
                  adminmenu(loginstat)
            elif loginstat[3] == "3":
                  customermenu(loginstat)
      else:
          print("INVALID LOGIN CREDENTIALS...!!!!")
          ans = input("Press Y to Quit the SYSTEM.. Other keys to cancel....")
          if ans.upper() == "Y":
              break
            
