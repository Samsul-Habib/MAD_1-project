from flask import Flask, request, render_template,redirect, url_for,session, request, make_response
app = Flask(__name__)
from tables import *
app.secret_key='your_secret_key_here'

#------------------------------------------------login routing ---------------------------------------------

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

#----------------logout routing-------------------------------------

"""@app.route('/logout')
def log_out():
    session.clear()
    response=make_response(redirect(url_for('user')))
    response.headers['Cache-Control']='no-cache,no-store, must-revalidate'
    response.headers['Pragma']='no-cache'
    response.headers['Expires']='0'
    return response"""

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

@app.route('/userlogin/inf_dash',methods=['GET','POST'])
def inf_dash():
    username=session.get('username')
    if username and request.method=='GET':
        all_camps=Camp.query.all()
        all_ads=Ad.query.all()
        return render_template('influencer_dashboard.html',username=username,all=all_camps,alll=all_ads,enumerate=enumerate)
@app.route('/userlogin/inf_dash/camps',methods=['GET','POST'])
def search_camps():
    return render_template('influencer_search_camps.html')

@app.route("/userlogin/inf_dash/other_camp_details/<int:camp_id>",methods=['GET','POST'])
def all_camp_details(camp_id):
    camp=Camp.query.get(camp_id)
    if camp:
        return render_template('all_camp_details.html',camp=camp)

@app.route("/userlogin/inf_dash/search_camp",methods=['GET','POST'])
def sorted_camp_details():
    niche=request.form['niche']
    reach=request.form['reach']
    followers=request.form['followers']
    campaigns=Camp.query.filter_by(category=niche,expected_reach=reach,expected_followers=followers).all()
    return render_template('sorted_camp_details.html',campaigns=campaigns)   

@app.route("/userlogin/inf_dash/camp_accept", methods=['GET','POST'])  # camps added on clicking 'Accept' button
def task_add_success():
    if request.method=='POST':
        username=session.get('username')
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
        return redirect(url_for('task_add_success'))
    return '<h1>Campaign addedd successfully.</h1>'

@app.route("/userlogin/inf_dash/your_camps",methods=['GET','POST']) #list of chosen camps by the influencer
def chosen_camps():
    username=session.get('username')
    influencer_camps=Influ_Camp.query.filter_by(username=username).all()
    return render_template('chosen_camps.html',influencer_camps=influencer_camps)

@app.route("/userlogin/inf_dash/your_camps/delete/<int:task_id>",methods=['GET',"POST"]) # Influencer task delete 
def delete_inf_task(task_id):
    to_delete=Influ_Camp.query.get(task_id)
    if to_delete:
          db.session.delete(to_delete)
          db.session.commit()     
    return redirect(url_for('chosen_camps'))

@app.route('/userlogin/inf_dash/submit_your_like',methods=['POST','GET']) #Influencer submits his/her preferences 
def submit_your_like():
    if request.method=='POST':
        username=session.get('username')
        niche=request.form['niche']
        reach=request.form['reach']
        followers=request.form['followers']
        motto=request.form['motto']
        exp=request.form['exp']
        new_influencer=Influencer_Like(username=username,niche=niche,reach=reach,followers=followers,motto=motto,exp=exp)
        db.session.add(new_influencer)
        db.session.commit()
        return '<h1>Successfully submitted.</h1><br><a href="/userlogin/inf_dash/submit_your_like">Back</a>'
    return render_template('influencer_preferences.html')

@app.route("/userlogin/inf_dash/stat",methods=['GET','POST'])
def inf_stat():
    return render_template('influencer_stat.html')
    
#-------------------Sponsor Dashboard---------------------------------------------------------------------------------------------------
@app.route('/userlogin/spon_dash',methods=['GET','POST'])
def spon_dash():
    username=session.get('username')
    if request.method=='GET' and username:
        other=Camp.query.filter(Camp.username!=username).all()
        otherr=Ad.query.filter(Ad.username!=username).all()
        return render_template('sponsor_dashboard.html',username=username,other_camps=other,other_ads=otherr,enumerate=enumerate)

@app.route("/userlogin/spon_dash/create_task",methods=['GET','POST'])
def create_task():
    if request.method=='GET':
        return render_template('sponsor_task_create.html')
    if request.method=='POST':
        try:
            username=session.get('username')
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
            <a href="/userlogin/spon_dash">Home</a>
            <br>
            <br>
            <a href="/userlogin/spon_dash/create_task">Add more task</a>'''
            return html_response
        except Exception as e:
            return str(e)
@app.route("/delete_task/<int:task_id>",methods=['GET',"POST"])  # Sponsor is deleting his/her created task
def delete_task(task_id):
    to_delete=Camp.query.get(task_id)
    if to_delete:
          db.session.delete(to_delete)
          db.session.commit()     
    return redirect(url_for('your_camp'))

@app.route("/userlogin/spon_dash/search_influ",methods=['GET',"POST"])  # Sponsor is searching for influencer
def spon_search_inf_details():
    if request.method=='POST':
        niche=request.form['niche']
        reach=request.form['reach']
        followers=request.form['followers']
        sorted_influencers=Influencer_Like.query.filter_by(niche=niche,reach=reach,followers=followers).all()
        return render_template('sorted_influencer.html',sorted_influencers=sorted_influencers)
    return render_template('spon_search_inf.html')

@app.route("/userlogin/spon_dash/update_task/<int:task_id>",methods=['GET',"POST"]) #Sponsor is updating his/her created task
def update_task(task_id):
    task=Camp.query.get(task_id)
    if request.method=='POST':
        task.camp_name = request.form['camp_name']
        task.camp_details = request.form['camp_details']
        task.price=request.form['price']
        task.start_date=request.form['start_date']
        task.end_date=request.form['end_date']
        task.category=request.form['category']
        db.session.commit()
        return redirect(url_for('your_camp'))
    return render_template("sponsor_task_update.html",task=task)
@app.route('/userlogin/spon_dash/your_camp',methods=["GET","POST"])
def your_camp():
    username=session.get('username')
    tasks=Camp.query.filter_by(username=username).all()
    #task_list = ''.join(f'<li>{task.camp_name} | {task.camp_details} | {task.start_date} | {task.end_date} | {task.price} | {task.duration}</li>' for task in tasks)
    task_list=''
    for p in tasks:
        task_list+=f'''
        <tr>
            <td>{p.camp_name}</td>
            <td>{p.camp_details}</td>
            <td>{p.price}</td>
            <td>{p.start_date}</td>
            <td>{p.end_date}</td>
            <td>{p.category}</td>
            <td><a href="/delete_task/{p.id}" class="delete-button">Delete</a></td>
            <td><a href="/userlogin/spon_dash/update_task/{p.id}" class="buttons">Update</a></td>
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
            <a href="/userlogin/spon_dash">Home</a>
            <br>
            <br>
            <a href="/userlogin/spon_dash/create_task">Add more task</a>
        </div>
    </body>
    </html>
    '''
    return html_response

@app.route("/userlogin/spon_dash/other_camp_details/<int:camp_id>",methods=['GET','POST'])
def other_camp_details(camp_id):
    camp=Camp.query.get(camp_id)
    if camp:
        return render_template('other_camp_details.html',camp=camp)
@app.route("/userlogin/spon_dash/stat",methods=['GET','POST'])
def spon_stat():
    return render_template('sponsor_stat.html')

#---------------------------------------Chatting part------------------------------------------------------------------------


############### CHAT BOX FOR INFLUENCER #################################################

@app.route("/userlogin/inf_dash/chat", methods=["GET","POST"])
def chat():
    current_user=session.get('username')
    spon=request.form['select_recp']
    msg1=Message.query.filter_by(sender=current_user,recipient=spon).with_entities(Message.content)
    msg2=SponMessage.query.filter_by(sender=spon,recipient=current_user).with_entities(SponMessage.content)
    return render_template('new_chat_.html',spon=spon,msg1=msg1,msg2=msg2)

@app.route("/userlogin/inf_dash/chat/new_chat", methods=["GET","POST"])
def new_chat():
    if request.method=='POST':
        content=request.form['content']
        recipient=request.form['recipient']
        sender=request.form['sender']
        new_msg=Message(sender=sender,recipient=recipient,content=content)
        db.session.add(new_msg)
        db.session.commit()
        return '<h1>Message sent.</h1>'
    return render_template('chat_.html')
@app.route("/userlogin/inf_dash/select_recp", methods=["GET","POST"])
def select_recp():
    recp=User_Sign_Up.query.filter_by(role='sponsor').with_entities(User_Sign_Up.user_name).all()
    spons=[user.user_name for user in recp]
    return render_template('select_recipient.html',spons=spons)

############### CHAT BOX FOR SPONSOR #################################################

@app.route("/userlogin/spon_dash/chat", methods=["GET","POST"])
def chat_spon():
    current_user=session.get('username')
    spon=request.form['select_recp']
    msg1=SponMessage.query.filter_by(sender=current_user,recipient=spon).with_entities(SponMessage.content)
    msg2=Message.query.filter_by(sender=spon,recipient=current_user).with_entities(Message.content)
    return render_template('new_chat_spon.html',spon=spon,msg1=msg1,msg2=msg2)

@app.route("/userlogin/spon_dash/chat/new_chat", methods=["GET","POST"])
def new_chat_spon():
    if request.method=='POST':
        content=request.form['content']
        recipient=request.form['recipient']
        sender=request.form['sender']
        new_msg=SponMessage(sender=sender,recipient=recipient,content=content)
        db.session.add(new_msg)
        db.session.commit()
        return '<h1>Message sent.</h1><br>'
    return render_template('chat_spon.html')
@app.route("/userlogin/spon_dash/select_recp", methods=["GET","POST"])
def select_recp_spon():
    recp=User_Sign_Up.query.filter_by(role='influencer').with_entities(User_Sign_Up.user_name).all()
    spons=[user.user_name for user in recp]
    return render_template('select_recipient_spon.html',spons=spons)


#------------------------------------------------------Ad management------------------------------------------------------

@app.route("/userlogin/spon_dash/create_ad",methods=['GET','POST'])
def ad_create_spon():
    if request.method=='GET':
        return render_template('spon_ad_create.html')
    if request.method=='POST':
        username=session.get('username')
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
    return render_template('spon_ad_create.html')

@app.route("/userlogin/inf_dash/other_ad_details/<int:ad_id>",methods=['GET','POST']) # all the availabel ads
def all_ad_details(ad_id):
    ad=Ad.query.get(ad_id)
    if ad:
        return render_template('all_ad_details.html',ad=ad)
@app.route('/userlogin/inf_dash/other_ad_details/share',methods=['GET','POST']) # influencer is sharing an ad
def promote():
    return '<h1>Thank you for sharing!</h1><br><br><a href="/userlogin/inf_dash">Home</a>'

@app.route("/userlogin/spon_dash/other_ad_details/<int:ad_id>",methods=['GET','POST'])
def other_ad_details(ad_id):
    ad=Ad.query.get(ad_id)
    if ad:
        return render_template('other_ad_details.html',ad=ad)
    
@app.route("/delete_ad/<int:task_id>",methods=['GET',"POST"])  # Sponsor is deleting his/her ad
def delete_ad(task_id):
    to_delete=Ad.query.get(task_id)
    if to_delete:
          db.session.delete(to_delete)
          db.session.commit()     
    return redirect(url_for('your_ad'))

@app.route("/userlogin/spon_dash/update_ad/<int:task_id>",methods=['GET',"POST"]) #Sponsor is updating his/her ad
def update_ad(task_id):
    task=Ad.query.get(task_id)
    if request.method=='POST':
        task.ad_name = request.form['ad_name']
        task.camp_name = request.form['camp_name']
        task.ad_price=request.form['ad_price']
        task.ad_details=request.form['ad_details']
        task.ad_duration=request.form['ad_duration']
        task.ad_aud=request.form['ad_aud']
        db.session.commit()
        return redirect(url_for('your_ad'))
    return render_template("sponsor_ad_update.html",task=task)
    

@app.route('/userlogin/spon_dash/your_ad',methods=["GET","POST"])  #all the ads created by a sponsor
def your_ad():
    username=session.get('username')
    tasks=Ad.query.filter_by(username=username).all()
    #task_list = ''.join(f'<li>{task.ad_name} | {task.camp_name} | {task.ad_details} | {task.ad_aud} | {task.ad_price} | {task.ad_duration}</li>' for task in tasks)
    task_list=''
    for p in tasks:
        task_list+=f'''
        <tr>
            <td>{p.ad_name}</td>
            <td>{p.camp_name}</td>
            <td>{p.ad_details}</td>
            <td>{p.ad_aud}</td>
            <td>{p.ad_price}</td>
            <td>{p.ad_duration}</td>
            <td><a href="/delete_ad/{p.id}" class="delete-button">Delete</a></td>
            <td><a href="/userlogin/spon_dash/update_ad/{p.id}" class="buttons">Update</a></td>
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
            <a href="/userlogin/spon_dash">Home</a>
            <br>
            <br>
            <a href="/userlogin/spon_dash/create_ad">Create new ad</a>
        </div>
    </body>
    </html>
    '''
    return html_response

#-------------------------------------------------Payment Portal------------------------------------------------

import time
@app.route('/userlogin/spon_dash/payment',methods=['GET','POST'])
def payment():
    if request.method=='GET':
        return render_template('payment_portal.html')
    elif request.method=='POST' and request.form['payment-method']=='upi':
        return render_template('UPI.html')
    elif request.method=='POST' and request.form['payment-method']=="bank-transfer":
        return render_template('bank_transfer.html')

@app.route('/userlogin/spon_dash/payment/upi',methods=['POST'])
def payment_done_upi():
    time.sleep(3)
    return '<h1>Payment successful. Thank you!</h1>'

@app.route('/userlogin/spon_dash/payment/bank_transfer',methods=['POST'])
def payment_done_bank():
    time.sleep(3)
    return '<h1>Payment successful. Thank you!</h1>'

#--------------------------------Admin dashboard-------------------------------------------------------------

@app.route('/adminlogin/admindash',methods=['GET','POST'])
def admin_dash():
    username=session.get('username')
    if request.method=='GET' and username:
        all_camps=Camp.query.all()
        all_ads=Ad.query.all()
        total_active_influencers = db.session.query(User_Sign_Up).filter_by(role='influencer').count()
        total_active_sponsors = db.session.query(User_Sign_Up).filter_by(role='sponsor').count()
        total_active_camps = db.session.query(Camp).count()
        total_active_ads = db.session.query(Ad).count()
        #total_flagged_camps = db.session.query(F_Camp).count()
        total_flagged_ads = db.session.query(F_Ad).count()
        total_flagged_camps = db.session.query(F_Camp).count()
        return render_template('admin_dashboard.html',total_flagged_camps=total_flagged_camps,total_flagged_ads=total_flagged_ads,username=username,all=all_camps,alll=all_ads,enumerate=enumerate,total_active_influencers=total_active_influencers,total_active_camps=total_active_camps,total_active_ads=total_active_ads,total_active_sponsors=total_active_sponsors)
    
@app.route("/adminlogin/admindash/other_camp_details_admin/<int:camp_id>",methods=['GET','POST']) # all available camps
def all_camp_details_admin(camp_id):
    camp=Camp.query.get(camp_id)
    if camp:
        if request.method=='POST':
            try:
                flagged_camp=F_Camp(id=camp.id,username=camp.username,camp_name=camp.camp_name,camp_details=camp.camp_details,price=camp.price,start_date=camp.start_date,end_date=camp.end_date,category=camp.category,expected_followers=camp.expected_followers,expected_reach=camp.expected_reach)
                db.session.add(flagged_camp)
                db.session.commit()
            except Exception as e:
                return '<h1>This camp has already been raised flagged</h1>'
            return '<h1>Camp flagged successfully</h1>'
        return render_template('all_camp_details_admin.html', camp=camp)

@app.route("/adminlogin/admindash/other_ad_details_admin/<int:ad_id>", methods=['GET', 'POST'])   #all available ads
def all_ad_details_admin(ad_id):
    ad = Ad.query.get(ad_id)
    if ad:
        if request.method == 'POST':
            try:
                flagged_ad = F_Ad(id=ad_id,username=ad.username,ad_name=ad.ad_name,camp_name=ad.camp_name,ad_details=ad.ad_details,ad_price=ad.ad_price,ad_aud=ad.ad_aud,ad_duration=ad.ad_duration)
                db.session.add(flagged_ad)
                db.session.commit()
            except Exception as e:
                return '<h1>This ad has already been raised flagged</h1>'
            return '<h1>Ad flagged successfully</h1>'
        return render_template('all_ad_details_admin.html', ad=ad)

@app.route("/adminlogin/admindash/flagged_ads",methods=['GET','POST'])   # route for all flagged ads 
def flagged_ads():
        ad=F_Ad.query.all()
        return render_template('flagged_ads.html',ad=ad)

@app.route("/adminlogin/admindash/flagged_camps",methods=['GET','POST'])   # route for all flagged camps 
def flagged_camps():
        camp=F_Camp.query.all()
        return render_template('flagged_camps.html',camp=camp)

@app.route("/adminlogin/admindash/unflagged_ads/<int:ad_id>",methods=['GET','POST'])  #unflagging an ad 
def unflagged_ads(ad_id):
    to_delete=F_Ad.query.get(ad_id)
    if to_delete:
        db.session.delete(to_delete)
        db.session.commit()
    return redirect(url_for('flagged_ads'))

@app.route("/adminlogin/admindash/unflagged_camps/<int:camp_id>",methods=['GET','POST'])  # unflagging a camp 
def unflagged_camps(camp_id):
    to_delete=F_Camp.query.get(camp_id)
    if to_delete:
        db.session.delete(to_delete)
        db.session.commit()
    return redirect(url_for('flagged_camps'))