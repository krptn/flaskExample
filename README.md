# Krptn integration with Flask (WebAuthn)

**Note:** for multiple reasons, this example is not production ready. Please do not use this in such an environment but rather take ideas from here on how to integrate Flask and Krptn.

Before running this app, please open `app.py` and set your origin and hostname as appropriate.

In case you recieve concurency errors from SQLite, please use a different database backend. See our docs about [databases](https://docs.krptn.dev/README-DATABASES.html).

Don't forget to install Krptn & Flask before:

```shell
pip install -r requirements.txt
flask run
```

Or:

```shell
docker build -t flask_example . && docker run --rm -p 8000:8000 -it flask_example
```

Note: this example does not guard against brute force attacks. Please ensure rate limiting is configured on your server.

## Copyrights

This is a modified version of the [Digital Ocean article](https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login).

Some of this code was taken from [Google's WebAuthn tutorial on Glitch](https://glitch.com/edit/#!/webauthn-codelab-start?path=README.md%3A1%3A0).

This code was modified from these sources to work with Krptn's Auth Backends. These include changing auth URLs, base64 decoding/encoding, and modifying URLs.

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
