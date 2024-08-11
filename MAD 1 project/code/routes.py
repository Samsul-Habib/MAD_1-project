from flask import Flask, request, render_template,redirect, url_for,session, request, make_response
app = Flask(__name__)
from tables import *
app.secret_key='your_secret_key_here'

#------------------------------------------------login routing ------------------------------------------------

@app.route('/')    # URl for home page
def index():
    return render_template('start.html')

@app.route('/userlogin',methods=['GET','POST'])    # user login
def user():
    if request.method=='GET':
        return render_template('user_login.html')
    if request.method=='POST':
        username = request.form['username']
        session['username']=username
        password = request.form['password']
        role=request.form['role']
    user=User_Sign_Up.query.filter_by(user_name=username,password=password).first()
    if user:
        if user.role==role:
            if role=='influencer':
                return redirect(url_for('inf_dash',username=username))
            elif role=='sponsor':
                return redirect(url_for('spon_dash',username=username))
        else:
            return '<h1>Select correct role.</h1>'
    else:
        return '<h1>No username found. Please sign up first!!</h1><br><br> <a href="/adminlogin/sign_up">Sign Up</a>'


@app.route('/adminlogin',methods=['GET','POST'])   # admin login
def admin():
    if request.method=='GET':
        return render_template('admin_login.html')
    if request.method=='POST':
        username = request.form['username']
        session['username']=username
        password = request.form['password']
    user=Admin_Sign_Up.query.filter_by(user_name=username,password=password).first()
    if user:
        return redirect(url_for('admin_dash',username=username))
    else:
        return '<h1>No username found. Please sign up first!!</h1><br><br> <a href="/adminlogin/sign_up">Sign Up</a>'

#----------------Sign Up routing------------------------------------

@app.route('/adminlogin/sign_up',methods=["GET","POST"])
def admin_login_sign_up():
    if request.method=='GET':
        return render_template('admin_sign_up.html')
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            email=request.form['email']
            new_admin=Admin_Sign_Up(user_name=username,password=password,email=email)
            db.session.add(new_admin)
            db.session.commit()
            return redirect(url_for('admin_success'))
        except Exception as e:
            return str(e)
@app.route('/adminlogin/success')
def admin_success():
    return '<h1>Account created successfully!!</h1><br> <a href="/adminlogin">Login</a>'



@app.route('/adminlogin/reset_password',methods=['GET','POST'])
def admin_login_forget_password():
    if request.method=='GET':
        return render_template("admin_forgot_password.html")
    if request.method == 'POST':
        try:
            username = request.form['username']
            sk = request.form['securitykey']
            np=request.form['newpass']
            new_pass=Admin_Sign_Up.query.filter_by(user_name=username).first()
            if new_pass:
                new_pass.password=np
                new_pass.security_key=sk
                db.session.commit()
                return redirect(url_for('admin_pass_success'))
            else:
                return "<h1>User not found!</h1>"
        except Exception as e:
            return str(e)
@app.route('/adminlogin/reset_password/success')
def admin_pass_success():
    return '<h1>Password changed successfully!!</h1>'



@app.route('/userlogin/sign_up',methods=['GET','POST'])
def user_login_sign_up():
    if request.method=='GET':
        return render_template('user_sign_up.html')
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            email=request.form['email']
            role=request.form['role']
            industry=request.form['industry']
            new_user=User_Sign_Up(user_name=username,password=password,email=email,role=role,industry=industry)
            db.session.add(new_user)
            db.session.commit() 
            return redirect(url_for('user_success'))
        except Exception as e:
            return '<h2>User already exists!</h2>'
@app.route('/userlogin/success')
def user_success():
    return '<h1>Account created successfully!!</h1><br> <a href="/userlogin">Login</a>'


@app.route('/userlogin/reset_password',methods=['GET','POST'])
def user_login_forget_password():
    if request.method=='GET':
        return render_template("user_forgot_password.html")
    if request.method == 'POST':
        try:
            username = request.form['username']
            sk = request.form['securitykey']
            np=request.form['newpass']
            new_pass=User_Sign_Up.query.filter_by(user_name=username).first()
            if new_pass:
                new_pass.password=np
                new_pass.security_key=sk
                db.session.commit()
                return redirect(url_for('user_pass_success'))
            else:
                return "<h1>User not found!</h1>"
        except Exception as e:
            return str(e)
@app.route('/userlogin/reset_password/success')
def user_pass_success():
    return '<h1>Password changed successfully!!</h1>'


#-------------------Influencer Dashboard-----------------------------------------------------------------------------------------------

@app.route('/userlogin/inf_dash/<string:username>',methods=['GET','POST'])
def inf_dash(username):
    if request.method=='GET':
        all_camps=Camp.query.all()
        all_ads=Ad.query.all()
        return render_template('influencer_dashboard.html',username=username,all=all_camps,alll=all_ads,enumerate=enumerate)
    
@app.route('/userlogin/inf_dash/camps/<string:username>',methods=['GET','POST'])
def search_camps(username):
    return render_template('influencer_search_camps.html',username=username)

@app.route("/userlogin/inf_dash/other_camp_details/<int:camp_id>/<string:username>",methods=['GET','POST'])
def all_camp_details(camp_id,username):
    camp=Camp.query.get(camp_id)
    if camp!=None:
        flagged_camp=F_Camp.query.filter_by(camp_name=camp.camp_name).first()
    if camp:
        #flagged_camp=F_Camp.query.filter_by(camp_name=camp.camp_name).first()
        return render_template('all_camp_details.html',flagged_camp=flagged_camp,camp=camp,username=username)

@app.route("/userlogin/inf_dash/search_camp/<string:username>",methods=['GET','POST'])
def sorted_camp_details(username):
    niche=request.form['niche']
    reach=request.form['reach']
    followers=request.form['followers']
    campaigns=Camp.query.filter_by(category=niche,expected_reach=reach,expected_followers=followers).all()
    flagged_camp=F_Camp.query.filter(F_Camp.camp_name.in_([p.camp_name for p in campaigns])).all()
    flagged_camps={f.camp_name for f in flagged_camp}
    return render_template('sorted_camp_details.html',flagged_camps=flagged_camps,campaigns=campaigns,username=username)   

@app.route("/userlogin/inf_dash/camp_accept/<string:username>", methods=['GET','POST'])  # camps added on clicking 'Accept' button
def task_add_success(username):
    if request.method=='POST':
        username=username
        camp_id=request.form['camp_id']
        camp_name=request.form['camp_name']
        spon_username=request.form['spon_username']
        camp_details=request.form['camp_details']
        price=request.form['price']
        start_date=request.form['start_date']
        end_date=request.form['end_date']
        niche=request.form['niche']
        influencer_camp=Influ_Camp(camp_id=camp_id,username=username,spon_username=spon_username,camp_name=camp_name,camp_details=camp_details,price=price,start_date=start_date,end_date=end_date,category=niche)
        db.session.add(influencer_camp)
        db.session.commit()
        return redirect(url_for('task_add_success',username=username))
    return '<h1>Campaign addedd successfully.</h1>'

@app.route("/userlogin/inf_dash/your_camps/<string:username>",methods=['GET','POST']) #list of chosen camps by the influencer
def chosen_camps(username):
    influencer_camps=Influ_Camp.query.filter_by(username=username).all()
    flagged_camp=F_Camp.query.filter(F_Camp.camp_name.in_([p.camp_name for p in influencer_camps])).all()
    flagged_camps={f.camp_name for f in flagged_camp}
    return render_template('chosen_camps.html',influencer_camps=influencer_camps,username=username,flagged_camps=flagged_camps)

@app.route("/userlogin/inf_dash/your_camps/delete/<int:task_id>/<string:username>",methods=['GET',"POST"]) # Influencer task delete 
def delete_inf_task(task_id,username):
    to_delete=Influ_Camp.query.get(task_id)
    if to_delete:
          db.session.delete(to_delete)
          db.session.commit()     
    return redirect(url_for('chosen_camps',username=username))

@app.route('/userlogin/inf_dash/submit_your_like/<string:username>',methods=['POST','GET']) #Influencer submits his/her preferences 
def submit_your_like(username):
    if request.method=='POST':
        niche=request.form['niche']
        reach=request.form['reach']
        followers=request.form['followers']
        motto=request.form['motto']
        exp=request.form['exp']
        new_influencer=Influencer_Like(username=username,niche=niche,reach=reach,followers=followers,motto=motto,exp=exp)
        db.session.add(new_influencer)
        db.session.commit()
        return f'<h1>Successfully submitted.</h1><br><a href="/userlogin/inf_dash/submit_your_like/{username}">Back</a>'
    return render_template('influencer_preferences.html',username=username)
    
#-------------------Sponsor Dashboard---------------------------------------------------------------------------------------------------
@app.route('/userlogin/spon_dash/<username>',methods=['GET','POST'])
def spon_dash(username):
    if request.method=='GET' and username:
        other=Camp.query.filter(Camp.username!=username).all()
        otherr=Ad.query.filter(Ad.username!=username).all()
        return render_template('sponsor_dashboard.html',username=username,other_camps=other,other_ads=otherr,enumerate=enumerate)

@app.route("/userlogin/spon_dash/create_task/<username>",methods=['GET','POST']) #sponsor is creating camps
def create_task(username):
    if request.method=='GET':
        return render_template('sponsor_task_create.html',username=username)
    if request.method=='POST':
        camp_name = request.form['campaignName']
        camp_desc = request.form['campaignDescription']
        camp_price=request.form['campaignPrice']
        camp_start=request.form['campaignStart']
        camp_end=request.form['campaignEnd']
        camp_cat=request.form['campaignCategory']
        camp_followers=request.form['campaignFollowers']
        camp_reach=request.form['campaignReach']
        new_task=Camp(username=username,camp_name=camp_name,camp_details=camp_desc,price=camp_price,category=camp_cat,start_date=camp_start,end_date=camp_end,expected_reach=camp_reach,expected_followers=camp_followers)
        db.session.add(new_task)
        db.session.commit()
        html_response = f'''
            <h1>Task created successfully!!</h1>
            <a href="/userlogin/spon_dash/{username}">Home</a>
            <br>
            <br>
            <a href="/userlogin/spon_dash/create_task/{username}">Add more task</a>'''
        return html_response
        """except Exception as e:
            return str(e)"""
        

@app.route("/delete_task/<int:task_id>/<username>",methods=['GET',"POST"])  # Sponsor is deleting his/her created task
def delete_task(task_id,username):
    to_delete=Camp.query.get(task_id)
    delete_infcamp=Influ_Camp.query.filter_by(camp_name=to_delete.camp_name).first()
    if to_delete:
        db.session.delete(to_delete)
        db.session.commit()
    if delete_infcamp:
        db.session.delete(delete_infcamp)
        db.session.commit()
    return redirect(url_for('your_camp',username=username))

@app.route("/userlogin/spon_dash/search_influ/<username>",methods=['GET',"POST"])  # Sponsor is searching for influencer
def spon_search_inf_details(username):
    if request.method=='POST':
        niche=request.form['niche']
        reach=request.form['reach']
        followers=request.form['followers']
        sorted_influencers=Influencer_Like.query.filter_by(niche=niche,reach=reach,followers=followers).all()
        return render_template('sorted_influencer.html',sorted_influencers=sorted_influencers,username=username)
    return render_template('spon_search_inf.html',username=username)

@app.route("/userlogin/spon_dash/update_task/<int:task_id>/<username>",methods=['GET',"POST"]) #Sponsor is updating his/her created task
def update_task(task_id,username):
    task=Camp.query.get(task_id)
    inf_task=Influ_Camp.query.filter_by(camp_name=task.camp_name).first()
    if request.method=='POST' and task:
        task.camp_name = request.form['camp_name']
        task.camp_details = request.form['camp_details']
        task.price=request.form['price']
        task.start_date=request.form['start_date']
        task.end_date=request.form['end_date']
        task.category=request.form['category']
        db.session.commit()
        if inf_task:
            inf_task.camp_name = request.form['camp_name']
            inf_task.camp_details = request.form['camp_details']
            inf_task.price=request.form['price']
            inf_task.start_date=request.form['start_date']
            inf_task.end_date=request.form['end_date']
            inf_task.category=request.form['category']
            db.session.commit()
        return redirect(url_for('your_camp',username=username))
    return render_template("sponsor_task_update.html",task=task,username=username)
@app.route('/userlogin/spon_dash/your_camp/<username>',methods=["GET","POST"])
def your_camp(username):
    tasks=Camp.query.filter_by(username=username).all()
    task_list=''
    for p in tasks:
        flagged_camp=F_Camp.query.filter_by(camp_name=p.camp_name).first()
        msg=''
        if flagged_camp:
            msg='<p style="color:red; margin-top:30px">*This camp has been flagged by the admin</p>'
        task_list+=f'''
        <tr>
            <td>{p.camp_name}{msg}</td>
            <td>{p.camp_details}</td>
            <td>{p.price}</td>
            <td>{p.start_date}</td>
            <td>{p.end_date}</td>
            <td>{p.category}</td>
            <td><a href="/delete_task/{p.id}/{username}" class="delete-button">Delete</a></td>
            <td><a href="/userlogin/spon_dash/update_task/{p.id}/{username}" class="buttons">Update</a></td>
        </tr>
        '''
    html_response = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset='UTF-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <title>My Campaigns</title>
        <style>
            body {{
                font-family:Arial,sans-serif;
                background-color:#f4f4f9;
                margin:0;
                padding:20px;
            }}
            h1 {{
                font-size:24px;
                color:#333;
                text-align:center;
                margin-bottom:20px;
            }}
            table{{
                width:100%;
                border-collapse:collapse;
                margin:0 auto 20px auto;
                background-color:#fff;
                box-shadow:0 0 10px rgba(0,0,0,0.1);
                border-radius:8px;
            }}
            th,td{{
                padding:12px 15px;
                text-align:left;
                border-bottom:1px solid #ddd;
            }}
            th{{
                background-color:white
            }}
            tr:hover {{
                background-color:#f1f1f1
            }}
            a{{
                display:inline-block;
                margin-top:20px;
                padding:10px 15px;
                background-color:#007bff;
                color:#fff;
                text-decoration:none;
                border-radius:5px;
                transition:background-color 0.3s;
                text-align:center;
            }}
            a:hover {{
                background-color: #0056b3;
            }}
            .buttons {{
                text-align: center;
            }}
            .delete-button {{
            color: #fff;
            background-color: #dc3545;
            border: none;
            padding: 5px 10px;
            text-decoration: none;
            border-radius: 5px;
            transition: background-color 0.3s;
            }}
            .delete-button:hover {{
            background-color: #c82333;
            }}
        </style>
    </head>
    <body>
        <h1>Your Campaigns</h1>
        <table>
            <tr>
                <th>Campaign Name</th>
                <th>Campaign Description</th>
                <th>Price</th>
                <th>Start</th>
                <th>End</th>
                <th>Category</th>
            </tr>
            {task_list}
        </table>
        <div class='buttons'>
            <a href="/userlogin/spon_dash/{username}">Home</a>
            <br>
            <br>
            <a href="/userlogin/spon_dash/create_task/{username}">Add more task</a>
        </div>
    </body>
    </html>
    '''
    return html_response

@app.route("/userlogin/spon_dash/other_camp_details/<int:camp_id>/<username>",methods=['GET','POST'])
def other_camp_details(camp_id,username):
    camp=Camp.query.get(camp_id)
    flagged_camp=F_Camp.query.filter_by(camp_name=camp.camp_name).first()
    if camp:
        return render_template('other_camp_details.html',camp=camp,username=username,flagged_camp=flagged_camp)

#---------------------------------------Chatting part------------------------------------------------------------------------


#########################CHAT BOX FOR INFLUENCER################################################

@app.route("/userlogin/inf_dash/chat/<username>", methods=["GET","POST"])
def chat(username):
    current_user=username
    spon=request.form['select_recp']
    msg1=Message.query.filter_by(sender=current_user,recipient=spon).with_entities(Message.content)
    msg2=SponMessage.query.filter_by(sender=spon,recipient=current_user).with_entities(SponMessage.content)
    return render_template('new_chat_.html',username=username,spon=spon,msg1=msg1,msg2=msg2)

@app.route("/userlogin/inf_dash/chat/new_chat/<string:username>", methods=["GET","POST"])
def new_chat(username):
    if request.method=='POST':
        content=request.form['content']
        recipient=request.form['recipient']
        sender=request.form['sender']
        new_msg=Message(sender=sender,recipient=recipient,content=content)
        db.session.add(new_msg)
        db.session.commit()
        return '<h1>Message sent.</h1>'
    return render_template('chat_.html',username=username)
@app.route("/userlogin/inf_dash/select_recp/<string:username>", methods=["GET","POST"])
def select_recp(username):
    recp=User_Sign_Up.query.filter_by(role='sponsor').with_entities(User_Sign_Up.user_name).all()
    spons=[user.user_name for user in recp]
    return render_template('select_recipient.html',spons=spons,username=username)

############### CHAT BOX FOR SPONSOR #################################################

@app.route("/userlogin/spon_dash/chat/<username>", methods=["GET","POST"])
def chat_spon(username):
    #current_user=session.get('username')
    current_user=username
    spon=request.form['select_recp']
    msg1=SponMessage.query.filter_by(sender=current_user,recipient=spon).with_entities(SponMessage.content)
    msg2=Message.query.filter_by(sender=spon,recipient=current_user).with_entities(Message.content)
    return render_template('new_chat_spon.html',username=username,spon=spon,msg1=msg1,msg2=msg2)

@app.route("/userlogin/spon_dash/chat/new_chat/<username>", methods=["GET","POST"])
def new_chat_spon(username):
    if request.method=='POST':
        content=request.form['content']
        recipient=request.form['recipient']
        sender=request.form['sender']
        new_msg=SponMessage(sender=sender,recipient=recipient,content=content)
        db.session.add(new_msg)
        db.session.commit()
        return '<h1>Message sent.</h1><br>'
    return render_template('chat_spon.html',username=username)

@app.route("/userlogin/spon_dash/select_recp/<username>", methods=["GET","POST"])
def select_recp_spon(username):
    recp=User_Sign_Up.query.filter_by(role='influencer').with_entities(User_Sign_Up.user_name).all()
    spons=[user.user_name for user in recp]
    return render_template('select_recipient_spon.html',spons=spons,username=username)


#------------------------------------------------------Ad management------------------------------------------------------

@app.route("/userlogin/spon_dash/create_ad/<username>",methods=['GET','POST'])
def ad_create_spon(username):
    if request.method=='GET':
        return render_template('spon_ad_create.html',username=username)
    if request.method=='POST':
        ad_name=request.form['adName']
        ad_details=request.form['adDescription']
        camp_name=request.form['campName']
        ad_aud=request.form['adAud']
        ad_price=request.form['adPrice']
        ad_duration=request.form['adDur']
        new_ad=Ad(username=username,ad_name=ad_name,camp_name=camp_name,ad_details=ad_details,ad_aud=ad_aud,ad_price=ad_price,ad_duration=ad_duration)
        db.session.add(new_ad)
        db.session.commit()
        return '<h2>Ad created</h2>'
    return render_template('spon_ad_create.html',username=username)

@app.route("/userlogin/inf_dash/other_ad_details/<int:ad_id>/<username>",methods=['GET','POST']) # all the availabel ads visible to influencers
def all_ad_details(ad_id,username):
    ad=Ad.query.get(ad_id)
    flagged_ad=F_Ad.query.filter_by(ad_name=ad.ad_name).first()
    if ad:
        return render_template('all_ad_details.html',flagged_ad=flagged_ad,ad=ad,username=username)

@app.route('/userlogin/inf_dash/other_ad_details/share/<username>',methods=['GET','POST']) # influencer is sharing an ad
def promote(username):
    return f'<h1>Thank you for sharing!</h1><br><br><a href="/userlogin/inf_dash/{username}">Home</a>'

@app.route("/userlogin/spon_dash/other_ad_details/<int:ad_id>/<username>",methods=['GET','POST'])  # all the other ads visible to the sponsor
def other_ad_details(ad_id,username):
    ad=Ad.query.get(ad_id)
    flagged_ad=F_Ad.query.filter_by(ad_name=ad.ad_name).first()
    if ad:
        return render_template('other_ad_details.html',flagged_ad=flagged_ad,ad=ad,username=username)
    
@app.route("/delete_ad/<int:task_id>/<username>",methods=['GET',"POST"])  # Sponsor is deleting his/her ad
def delete_ad(task_id,username):
    to_delete=Ad.query.get(task_id)
    if to_delete:
          db.session.delete(to_delete)
          db.session.commit()     
    return redirect(url_for('your_ad',username=username))

@app.route("/userlogin/spon_dash/update_ad/<int:task_id>/<username>",methods=['GET',"POST"]) #Sponsor is updating his/her ad
def update_ad(task_id,username):
    task=Ad.query.get(task_id)
    if request.method=='POST':
        task.ad_name = request.form['ad_name']
        task.camp_name = request.form['camp_name']
        task.ad_price=request.form['ad_price']
        task.ad_details=request.form['ad_details']
        task.ad_duration=request.form['ad_duration']
        task.ad_aud=request.form['ad_aud']
        db.session.commit()
        return redirect(url_for('your_ad',username=username))
    return render_template("sponsor_ad_update.html",task=task,username=username)
    

@app.route('/userlogin/spon_dash/your_ad/<username>',methods=["GET","POST"])  #all the ads created by a sponsor
def your_ad(username):
    tasks=Ad.query.filter_by(username=username).all()
    task_list=''
    for p in tasks:
        flagged_ad=F_Ad.query.filter_by(ad_name=p.ad_name).first()
        msg=''
        if flagged_ad:
            msg='<p style="color:red; margin-top:30px">*This ad has been flagged by the admin</p>'
        task_list+=f'''
        <tr>
            <td>{p.ad_name}{msg}</td>
            <td>{p.camp_name}</td>
            <td>{p.ad_details}</td>
            <td>{p.ad_aud}</td>
            <td>{p.ad_price}</td>
            <td>{p.ad_duration}</td>
            <td><a href="/delete_ad/{p.id}/{username}" class="delete-button">Delete</a></td>
            <td><a href="/userlogin/spon_dash/update_ad/{p.id}/{username}" class="buttons">Update</a></td>
            <br>       
        </tr>   
        '''
    html_response = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset='UTF-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <title>My Ads</title>
        <style>
            body {{
                font-family:Arial,sans-serif;
                background-color:#f4f4f9;
                margin:0;
                padding:20px;
            }}
            h1 {{
                font-size:24px;
                color:#333;
                text-align:center;
                margin-bottom:20px;
            }}
            table{{
                width:100%;
                border-collapse:collapse;
                margin:0 auto 20px auto;
                background-color:#fff;
                box-shadow:0 0 10px rgba(0,0,0,0.1);
                border-radius:8px;
            }}
            th,td{{
                padding:12px 15px;
                text-align:left;
                border-bottom:1px solid #ddd;
            }}
            th{{
                background-color:white
            }}
            tr:hover {{
                background-color:#f1f1f1
            }}
            a{{
                display:inline-block;
                margin-top:20px;
                padding:10px 15px;
                background-color:#007bff;
                color:#fff;
                text-decoration:none;
                border-radius:5px;
                transition:background-color 0.3s;
                text-align:center;
            }}
            a:hover {{
                background-color: #0056b3;
            }}
            .buttons {{
                text-align: center;
            }}
            .delete-button {{
            color: #fff;
            background-color: #dc3545;
            border: none;
            padding: 5px 10px;
            text-decoration: none;
            border-radius: 5px;
            transition: background-color 0.3s;
            }}
            .delete-button:hover {{
            background-color: #c82333;
            }}
        </style>
    </head>
    <body>
        <h1>Your Ads</h1>
        <table>
            <tr>
                <th>Ad Name</th>
                <th>Campaign Name</th>
                <th>Details</th>
                <th>Audience</th>
                <th>Budget</th>
                <th>Duration</th>
            </tr>
            {task_list}
        </table>
        <div class='buttons'>
            <a href="/userlogin/spon_dash/{username}">Home</a>
            <br>
            <br>
            <a href="/userlogin/spon_dash/create_ad/{username}">Create new ad</a>
        </div>
    </body>
    </html>
    '''
    return html_response

#-------------------------------------------------Payment Portal------------------------------------------------

import time
@app.route('/userlogin/spon_dash/payment/<username>',methods=['GET','POST'])
def payment(username):
    if request.method=='GET':
        return render_template('payment_portal.html',username=username)
    elif request.method=='POST' and request.form['payment-method']=='upi':
        return render_template('UPI.html',username=username)
    elif request.method=='POST' and request.form['payment-method']=="bank-transfer":
        return render_template('bank_transfer.html',username=username)

@app.route('/userlogin/spon_dash/payment/upi',methods=['POST'])
def payment_done_upi():
    time.sleep(3)
    return '<h1>Payment successful. Thank you!</h1>'

@app.route('/userlogin/spon_dash/payment/bank_transfer',methods=['POST'])
def payment_done_bank():
    time.sleep(3)
    return '<h1>Payment successful. Thank you!</h1>'

#--------------------------------Admin dashboard-------------------------------------------------------------

@app.route('/adminlogin/admindash/<username>',methods=['GET','POST'])
def admin_dash(username):
    if request.method=='GET' and username:
        all_camps=Camp.query.all()
        all_ads=Ad.query.all()
        total_active_influencers = db.session.query(User_Sign_Up).filter_by(role='influencer').count()
        total_active_sponsors = db.session.query(User_Sign_Up).filter_by(role='sponsor').count()
        total_active_camps = db.session.query(Camp).count()
        total_active_ads = db.session.query(Ad).count()
        total_flagged_ads = db.session.query(F_Ad).count()
        total_flagged_camps = db.session.query(F_Camp).count()
        return render_template('admin_dashboard.html',total_flagged_camps=total_flagged_camps,total_flagged_ads=total_flagged_ads,username=username,all=all_camps,alll=all_ads,enumerate=enumerate,total_active_influencers=total_active_influencers,total_active_camps=total_active_camps,total_active_ads=total_active_ads,total_active_sponsors=total_active_sponsors)
    
@app.route("/adminlogin/admindash/other_camp_details_admin/<int:camp_id>/<username>",methods=['GET','POST']) # all available camps
def all_camp_details_admin(camp_id,username):
    camp=Camp.query.get(camp_id)
    if camp:
        if request.method=='POST':
            try:
                flagged_camp=F_Camp(id=camp.id,username=camp.username,camp_name=camp.camp_name,camp_details=camp.camp_details,price=camp.price,start_date=camp.start_date,end_date=camp.end_date,category=camp.category,expected_followers=camp.expected_followers,expected_reach=camp.expected_reach,flagged_by=username)
                db.session.add(flagged_camp)
                db.session.commit()
            except Exception as e:
                return '<h1>This camp has already been raised flagged</h1>'
            return '<h1>Camp flagged successfully</h1>'
        return render_template('all_camp_details_admin.html', camp=camp,username=username)

@app.route("/adminlogin/admindash/other_ad_details_admin/<int:ad_id>/<username>", methods=['GET', 'POST'])   #all available ads
def all_ad_details_admin(ad_id,username):
    ad = Ad.query.get(ad_id)
    if ad:
        if request.method == 'POST':
            try:
                flagged_ad = F_Ad(id=ad_id,username=ad.username,ad_name=ad.ad_name,camp_name=ad.camp_name,ad_details=ad.ad_details,ad_price=ad.ad_price,ad_aud=ad.ad_aud,ad_duration=ad.ad_duration,flagged_by=username)
                db.session.add(flagged_ad)
                db.session.commit()
            except Exception as e:
                return '<h1>This ad has already been raised flagged</h1>'
            return '<h1>Ad flagged successfully</h1>'
        return render_template('all_ad_details_admin.html', ad=ad,username=username)

@app.route("/adminlogin/admindash/flagged_ads/<username>",methods=['GET','POST'])   # route for all flagged ads 
def flagged_ads(username):
        ad=F_Ad.query.all()
        return render_template('flagged_ads.html',ad=ad,username=username)

@app.route("/adminlogin/admindash/flagged_camps/<username>",methods=['GET','POST'])   # route for all flagged camps 
def flagged_camps(username):
        camp=F_Camp.query.all()
        return render_template('flagged_camps.html',camp=camp,username=username)

@app.route("/adminlogin/admindash/unflagged_ads/<int:ad_id>/<username>",methods=['GET','POST'])  #unflagging an ad 
def unflagged_ads(ad_id,username):
    to_delete=F_Ad.query.get(ad_id)
    if to_delete:
        db.session.delete(to_delete)
        db.session.commit()
    return redirect(url_for('flagged_ads',username=username))

@app.route("/adminlogin/admindash/unflagged_camps/<int:camp_id>/<username>",methods=['GET','POST'])  # unflagging a camp 
def unflagged_camps(camp_id,username):
    to_delete=F_Camp.query.get(camp_id)
    if to_delete:
        db.session.delete(to_delete)
        db.session.commit()
    return redirect(url_for('flagged_camps',username=username))