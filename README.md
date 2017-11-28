WWWizer for Google App Engine
=============================

According to the DNS specification (see https://www.ietf.org/rfc/rfc1034.txt),
having a CNAME for the apex or root domain means that the domain cannot have any
other types of DNS records (not sure why but it is what it is). This means that
MX, SOA, CA, TXT values are invalid fit the apex is a CNAME. This is why the
majority of sites (google, facebook, etc.) force a redirect to 'www.' for the
root domain.

This is a tiny web service that does just that, running on Google App Engine.
The idea is that you deploy this app in it's entirety to a service and then use
your ``dispatch.yaml`` to force requests to ``example.com`` to
``www.example.com``.

Usage
-----

Deploy the application:

```bash
gcloud app deploy app/app.yaml --project=MY_PROJECT_ID
```

Don't forget to replace ``MY_PROJECT_ID`` with the correct version.

Create or update your ``dispatch.yaml``:

```yaml
dispatch:
- url: "example.com/*"
  service: wwwizer

- url: "www.example.com/*"
  service: default
```

And update:

```bash
gcloud app deploy dispatch.yaml
```

And that is it! If you hit ``http://example.com`` you will be redirected to
``https://www.example.com`` using [HTTP code
307](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/307).

Configuration
-------------

There are two values in ``app/config.py`` that you should be aware of.

Key | Value
--- | -----
DOMAINS | A list of domains that you want to respond to. If not supplied, all requests will be redirected.
FORCE_HTTPS | All redirected requests by default will be pushed to ``https``. Setting this to ``False`` will use the request scheme.
