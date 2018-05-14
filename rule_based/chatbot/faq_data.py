# If message['text'] matches with K (Text modeled) or S(Synonyms), then associate the K or S to K-S Parent
# An example of FAQ data.

from .utilities import dict_key_tuple
user_input = {
    'hi': ["""Hello to you too. Ask stuff about merojob."""],
    'hello': ["""Hello to you too. Ask stuff about merojob."""],
    'register': ["""Registration is easy. Just sign up for a new account by filling in the form completely with your 
                 full name, a valid email id, mobile number, preferred job category and password. Click “Create my 
                 Account” and look for an email from us confirming your registration. Click the link in the email 
                 and you are now registered with merojob. You can also sign up with Facebook and twitter."""],
    'merojob': ["""merojob is a platform to find jobs of your choice. It is the leading career management site in 
                Nepal. It has started its venture since November 2009. Even if you are not actively looking for a 
                job, it can help you manage your career. This jobsite is a total recruitment solution to employers
                &amp; career management solutions for all jobseekers."""],
    'password': ["""Here is how to recover your password • Click “Forget Password” given in the “Sign up” box. • Enter 
                your login email id and click submit. You will receive an email with password reset link."""],
    'login': [""" Logging in is easy. Once you sign up, you have to provide your same exact email and password 
              credentials for you to be able to log in."""],
    'apply': ["""You can apply to any of your relevant job by simply clicking on Apply Now button."""],
    'bank': ["""If you are selected for the applied bank vacancy, Real solution or the concerned bank will inform you 
            via email and SMS. You'll also get a tracking code is number which is given automatically after the 
            successful applying procedure. It helps you to track your applications status."""],
    'card': ["""Please open the link that you have been provided in the SMS or Email. Insert your username and password,
            after the confirmation of attending the exam, please download the admit card."""]
}
