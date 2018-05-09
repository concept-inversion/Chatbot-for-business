# If message['text'] matches with K (Text modeled) or S(Synonyms), then associate the K or S to K-S Parent
# An example of FAQ data.
user_input = {
    'register': ["""Registration is easy. Just sign up for a new account by filling in the form completely with your 
                 full name, a valid email id, mobile number, preferred job category and password. Click “Create my 
                 Account” and look for an email from us confirming your registration. Click the link in the email 
                 and you are now registered with merojob. You can also sign up with Facebook and twitter."""],
    'merojob': ["""merojob is a platform to find jobs of your choice. It is the leading career management site in 
                Nepal. It has started its venture since November 2009. Even if you are not actively looking for a 
                job, it can help you manage your career. This jobsite is a total recruitment solution to employers
                &amp; career management solutions for all jobseekers."""],
    'password': ["""Here is how to recover your password • Click “Forget Password” given in the “Sign up” box. • Enter 
                your login email id and click submit. You will receive an email with password reset link."""]
}
