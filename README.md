# Krypton + FIDO Flask Example

An example of how to integrate Krypton with flask. You may want to use another database, in that case edit the config value in app.py.

Don't forget to install Krypton before:

```shell
pip install krptn
```

To extend this for TOTP MFA, please add an entry for TOTP MFA to the form, and pass it as a parameter to user.login. See [MFA in Krypton documentation](https://docs.krptn.dev/README-USER-AUTH.html#mfa)

Note: this example does not guard against brute force attacks. Please ensure rate limiting is configured on your server.

## Copyrights

This is a modified version of the [Digital Ocean article](https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login).

Some of this code was taken from [Google's WebAuthn tutorial on Glitch](https://glitch.com/edit/#!/webauthn-codelab-start?path=README.md%3A1%3A0).

This code was modified from these sources to work with Krypton's Auth Backends. These include changing auth URLs, base64 decoding/encoding, and modifying links on the webpage.

Here are the original copyright notices:

> Copyright 2019 Google Inc. All rights reserved.
>
> Licensed under the Apache License, Version 2.0 (the "License");
> you may not use this file except in compliance with the License.
> You may obtain a copy of the License at
>
>    https://www.apache.org/licenses/LICENSE-2.0
>
> Unless required by applicable law or agreed to in writing, software
> distributed under the License is distributed on an "AS IS" BASIS,
> WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
> See the License for the specific language governing permissions and
> limitations under the License

The Ditigal Ocean tutorial had no official copyright notice attached.
