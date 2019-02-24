# Coding Challenge

##Emails

SMTP server is not included. Credentials are provided through environment variables:
```
$ export MAIL_SERVER='smtp.gmail.com'
$ export MAIL_PORT='465'
$ export MAIL_USERNAME='example@gmail.com'
$ export MAIL_PASSWORD='abc123'
$ ./run_local_flask_API.sh
```
`MAIL_SERVER` and `MAIL_PORT` are optional, since they're configured to fallback the default values for a gmail SMTP server.† The app can also be run with `FAKE_EMAIL=True` to skip sending emails altogether. If you're running the app with `FAKE_EMAIL`, you can look up your `AccountRecoveryRequest.recovery_token` in the database.†† Then continue the password reset flow by visiting http://food.computer.com:3000/password_reset?rt=your-recovery-token

† Note: to get my gmail account to send emails, I had to enable insecure access to my gmail account here: https://myaccount.google.com/lesssecureapps

†† openag-cloud-v1/UI-FlaskReact-AppEngineFlexVM/FlaskApiProvider/coding_challenge/fake_db.json

##User Auth
User sessions don't work, and login can be bypassed by going straight to http://food.computer.com:3000/. However, the password reset user flow otherwise works.


-Thank you :)