from flask import Blueprint, render_template, request, flash, url_for, current_app, redirect
from flask_login import login_required, current_user
from .models import Invitation, User
from . import db, UploadProfile
import os
import json
import re
import uuid
import base64
from werkzeug.utils import secure_filename
import uuid



def uuid_url64():
    rv = base64.b64encode(uuid.uuid4().bytes).decode('utf-8')
    return re.sub(r'[\=\+\/]', lambda m: {'+': '-', '/': '_', '=': ''}[m.group(0)], rv)


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.get(current_user.id)
    form = UploadProfile()
    file_url = None

    if form.validate_on_submit():
        profile_pic = request.files['profile_pic']
        # get image name
        filename = secure_filename(profile_pic.filename)
        # set UUID
        pic_name = str(uuid.uuid1()) + "_" + filename
        # save image
        pic_path =  os.path.join('website', current_app.config['UPLOAD_FOLDER'], pic_name)
        profile_pic.save(pic_path)
        # save image path to database
        user.profile_pic = pic_name
        db.session.commit()
        return redirect(url_for('views.profile'))

    elif request.method == 'POST':
        name = request.form.get('name')
        email1 = request.form.get('email1')
        phone_num = request.form.get('phone-num')
        email2 = request.form.get('email2')
        org_name = request.form.get('org-name')
        org_role = request.form.get('org-role')
        valid_date = request.form.get('valid-date')

        user.name = name
        user.email1 = email1
        user.phone_num = phone_num
        user.email2 = email2
        user.org_name = org_name
        user.org_role = org_role
        user.valid_date = valid_date

        db.session.commit()

    if user.profile_pic:
        file_url = url_for('get_file', filename=user.profile_pic, _external=True)

    return render_template("profile.html", user=current_user, form=form, file_url=file_url)


@views.route('/invite', methods=['GET','POST'])
@login_required
def invite():
    if request.method == 'POST': 
        name = request.form.get('name')
        email1 = request.form.get('email1')
        phone_num = request.form.get('phone-num')
        email2 = request.form.get('email2')
        org_name = request.form.get('org-name')
        org_role = request.form.get('org-role')
        valid_date = request.form.get('valid-date')

        user = User.query.filter_by(email1=email1).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email1) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        else:
            invite_id = str(uuid_url64())
            new_user = User(invite_id=invite_id, invitee=True, name=name, email1=email1, phone_num=phone_num,
                            email2=email2, org_name=org_name, org_role=org_role, valid_date=valid_date)
            db.session.add(new_user)
            db.session.commit()

            new_invite = Invitation(invite_id=invite_id, email=email1, name=name, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_invite)
            db.session.commit()

            flash('Invitation created!', category='success')

    return render_template("invite.html", user=current_user)


@views.route("/delete-invite", methods=['POST'])
def delete_invite():  
    invite = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    inviteId = invite['inviteId']
    invite = Invitation.query.get(inviteId)
    if invite:
        if invite.user_id == current_user.id:
            db.session.delete(invite)
            invitee = User.query.filter_by(invite_id=invite.invite_id).first()
            db.session.delete(invitee)
            db.session.commit()

    return render_template("invite.html", user=current_user)