# Flask Example

An example of how to integrate Krypton with flask.

Credit: this is a modified version of [this Digital Ocean article](https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login)

To extend this for MFA, please add an entry for MFA to the form, and pass it as a parameter to user.login. See [MFA in Krypton documentation](https://docs.krptn.dev/README-USER-AUTH.html#mfa)

Note: this example does not gard against brute force attacks. Please ensure rate limiting is configured on your server.
