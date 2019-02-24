from FCClass.user import User
from FCClass.account_recovery_request import AccountRecoveryRequest
from flask import Response
from flask import request
from flask import Blueprint
from pyisemail import is_email

from .utils.env_variables import *
from .utils.response import success_response, error_response
from datetime import datetime,timedelta

account_recovery = Blueprint('account_recovery', __name__)

@account_recovery.route('/api/account_recovery/', methods=['POST'])
def send_recovery_link():
    received_form_response = json.loads(request.data.decode('utf-8'))

    user_details = {}
    username = received_form_response.get("username")
    if username:
        user_details.update({'username': username})
    email = received_form_response.get("email_address")
    if email:
        user_details.update({'email_address': email})
        if not is_email(email, check_dns=True):
            return error_response(
                message="Invalid email address"
            )
    if not user_details:
        return error_response(
            message="Please enter your username or email address"
        )

    user = User.fetch(user_details)
    if not user:
        return error_response(
            message="Sorry, we couldn't find an account associated with that {}".format(' and '.join(user_details.keys()))
        )

    #create account recovery token
    recovery_request = AccountRecoveryRequest(user.get('user_uuid'))
    recovery_token = recovery_request.insert_into_db(datastore_client)
    url = received_form_response.get("url")

    #send email
    email_success = send_email(user.get('email_address'), recovery_token, url)

    if email_success:
        return success_response(
           message="An account recovery link has been sent to the email address associated with your account."
        )
    else:
        return error_response(
            message="There was a problem sending your account recovery link. Please try again later or contact support."
        )


@account_recovery.route('/api/fetch_recovery_request/', methods=['POST'])
def fetch_recovery_request():
    received_form_response = json.loads(request.data.decode('utf-8'))
    recovery_fail = error_response(message="Account recovery failed. Please try again, or contact support@example.com")
    recovery_token = received_form_response.get("recovery_token")
    user_uuid, is_request_expired = check_valid_recovery_request(recovery_token)
    if not user_uuid:
        return error_response(message="Account recovery failed. Please try again, or contact support@example.com")
    if is_request_expired:
        error_response(message="Account recovery request has expired.")
 
    user = User.fetch({'user_uuid': user_uuid})
    username = user.get('username')
    if not username:
        error_response(message="Account recovery failed. Please try again, or contact support@example.com")

    return success_response(
       message="Please enter your new password",
       username=username
    )


@account_recovery.route('/api/change_password/', methods=['POST'])
def change_password():
    received_form_response = json.loads(request.data.decode('utf-8'))
    recovery_token = received_form_response.get("recovery_token")
    user_uuid, is_expired = check_valid_recovery_request(recovery_token)
    if is_expired:
        error_response(message="Account recovery request expired.")

    new_password = received_form_response.get("password")
    if not new_password:
        return error_response(message="Please enter a new password.")
    success = User.change_password(user_uuid, new_password)
    if not success:
        return error_response(message="There was an error resetting your password.")
    AccountRecoveryRequest.delete(datastore_client, recovery_token)
    return success_response(
       message="Your password was successfully changed."
    )


def send_email(email_address, recovery_token, url):
    recovery_link = '{url}/password_reset?rt={recovery_token}'.format(url=url, recovery_token=recovery_token)
    mail = get_email_client()
    msg = Message('Account Recovery Request - OpenAg Food Computer', recipients=[email_address])
    msg.html = ('<p>We recieved a request to reset the Food Computer account associated with this email. ' +
                'Please click the link below to reset your password.</p>' +
                '<p><a href="{recovery_link}">{recovery_link}</a></p>'.format(recovery_link=recovery_link) +
                '<p>This link will expire in 24 hours. Do not share this link. If you did not request a password reset, you may ignore this email.</p>')
    try:
        mail.send(msg)
    except Exception as e:
        app.logger.error('account recovery email send fail:\n'+repr(e))
        return False
    return True

# returns (user_uuid, is_expired) tuple
def check_valid_recovery_request(recovery_token):
    if not recovery_token:
        return None, False

    recovery_request = AccountRecoveryRequest.fetch(datastore_client, recovery_token)
    user_uuid = recovery_request.get('user_uuid')
    if not user_uuid:
        return None, False

    expiration = recovery_request.get('expiration_date')
    # e.g.'2019-02-25 12:49:32.573446'
    expiration_date = datetime.strptime(expiration, '%Y-%m-%d %H:%M:%S.%f')
    expired = datetime.now() > expiration_date
    if expired:
        return user_uuid, True
    return user_uuid, False

