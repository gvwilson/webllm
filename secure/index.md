# Securing the Site

## Goals

-   Understand what HTTPS and TLS certificates are and why browsers require them.
-   Install mkcert to create locally-trusted development certificates.
-   Generate a certificate for localhost.
-   Start the Litestar server in HTTPS mode.

## What the Browser Checks

*What is the difference between HTTP and HTTPS?*

-   When you visit `http://localhost:8000`, your browser and the server exchange plain text
    -   Anyone who can intercept the connection can read every request and response
    -   This is fine on your own machine, but a problem on a shared network or the public internet
-   [%g https "HTTPS" %] wraps HTTP in a layer called [%g tls "TLS" %] (Transport Layer Security)
    that encrypts every message
    -   The browser and server negotiate encryption keys before any data is exchanged
    -   What travels over the wire looks like random bytes to anyone watching

*What is a certificate, and what is a certificate authority?*

-   A [%g certificate "certificate" %] is a file that proves a server's identity
    -   It contains the server's hostname, a public key used for encryption, and a digital signature
    -   Think of it like a notarized ID: the information is only trustworthy because a recognized
        authority signed it
-   The signing organization is called a [%g certificate-authority "certificate authority" %] (CA)
    -   Every browser ships with a built-in list of CAs it trusts, such as Let's Encrypt and DigiCert
    -   When your browser connects to a server, it checks whether the certificate is signed by one
        of those CAs
    -   If the signature does not check out, the browser shows a security warning and stops loading
-   Real CAs do not issue certificates for `localhost` because that name means something different
    on every computer
    -   The tool `mkcert` solves this by creating its own CA and adding it to your machine's trust store
    -   Any certificate `mkcert` signs is then trusted by your browser,
        but only on your machine,
        because the CA lives in your trust store, not anyone else's

## Installing mkcert

*How do I install mkcert on macOS, Windows, and Linux?*

-   macOS:
    -   Install [Homebrew][homebrew] if you do not already have it, then run `brew install mkcert`
    -   If you use Firefox, also run `brew install nss`
-   Windows:
    -   Open a terminal and run `winget install FiloSottile.mkcert`
    -   If `winget` is not available, download the `.exe` from the [mkcert releases page][mkcert-releases]
        and move it somewhere on your `PATH`
-   Linux:
    -   Download the binary for your CPU architecture from the [mkcert releases page][mkcert-releases]
    -   Mark it executable: `chmod +x mkcert-*-linux-amd64`
    -   Move it onto your `PATH`: `sudo mv mkcert-*-linux-amd64 /usr/local/bin/mkcert`
    -   On Debian or Ubuntu, also run `sudo apt install libnss3-tools` so that Chrome and Firefox
        pick up the new certificate authority automatically

*What does `mkcert -install` do, and when do I need to run it?*

-   Run `mkcert -install` once per machine after installing the tool
    -   This creates a local certificate authority and registers it with your operating system,
        Chrome, and Firefox
    -   Your browser will now accept any certificate that `mkcert` signs, as long as the certificate
        matches the hostname you typed
-   You do not need to run `mkcert -install` again unless you reinstall your operating system
    or want to use mkcert on a different machine

## Generating and Using a Certificate

*How do I generate a certificate for localhost using mkcert?*

-   Change into your application directory and run `mkcert localhost`
    -   `mkcert` creates two files: `localhost.pem` (the certificate) and `localhost-key.pem`
        (the private key)
    -   The certificate is only valid for the hostname `localhost`; it will not work for `127.0.0.1`
        or any other address unless you include them explicitly
-   Treat `localhost-key.pem` as a secret
    -   Anyone who has the key can impersonate your server to browsers that trust your local CA
    -   Add `*-key.pem` to your `.gitignore` file so the key is never committed to a repository
        by accident

*How do I start a Litestar server with HTTPS enabled?*

-   Pass the certificate and key files to `litestar run`:

[%inc run_secure.sh %]

-   Open `https://localhost:8000` in the browser (note: `https`, not `http`)
    -   The browser shows a padlock icon, confirming the connection is encrypted and the certificate
        is trusted
-   The padlock tells you two things: the traffic is encrypted, and your machine vouches for the
    server's identity
    -   It does not mean the application itself is correct or secure
    -   An encrypted connection to a server with SQL injection vulnerabilities is still a server
        with SQL injection vulnerabilities

## Check Understanding

<details markdown="1">
<summary markdown="1">You run `mkcert localhost` but forget to run `mkcert -install` first. What does the browser show when you open `https://localhost:8000`?</summary>

The browser shows a security warning and refuses to load the page.
`mkcert -install` is what registers mkcert's certificate authority with your machine's trust store.
Without it, the browser has never heard of the CA that signed your certificate,
so it treats the certificate as untrusted.

</details>

<details markdown="1">
<summary markdown="1">A classmate sends you their `localhost-key.pem` file so you can run the same server. You copy the file, start the server, and open `https://localhost:8000`, but the browser still shows a security warning. What is wrong?</summary>

The certificate is only trusted on the machine where `mkcert -install` was run.
Your classmate's CA is in their machine's trust store, not yours.
You need to run `mkcert -install` on your own machine and then run `mkcert localhost`
to generate a fresh certificate that your browser will accept.

</details>

<details markdown="1">
<summary markdown="1">What does the padlock icon in the browser actually guarantee about the sightings application?</summary>

The padlock means the connection between the browser and the server is encrypted,
and that the server presented a certificate signed by a CA the browser trusts.
It says nothing about whether the application itself is correct, complete, or free of security bugs.
A server that leaks data through poorly written queries or missing access controls is still dangerous
even when the padlock is showing.

</details>

<details markdown="1">
<summary markdown="1">The `litestar run` command below is supposed to start a secure server, but the browser shows a connection error. What is wrong?</summary>

The two file arguments are swapped.
`--ssl-certfile` should point to `localhost.pem` (the certificate)
and `--ssl-keyfile` should point to `localhost-key.pem` (the private key).
Passing the key where the certificate is expected causes the TLS handshake to fail
before the browser can connect.

</details>

```
litestar run --ssl-certfile localhost-key.pem --ssl-keyfile localhost.pem --app server:app
```

## Exercises

### Generate a Certificate for Both localhost and 127.0.0.1

Run `mkcert localhost 127.0.0.1` to create a single certificate that covers both addresses.
Start the server with this certificate and confirm that both `https://localhost:8000` and
`https://127.0.0.1:8000` show the padlock.

### Add Key Files to .gitignore

Open or create a `.gitignore` file in your project directory and add a line that prevents any file
ending in `-key.pem` from being committed.
Run `git status` after creating a certificate and confirm that `localhost-key.pem` does not appear
as an untracked file.

### Inspect a Certificate

Visit `https://localhost:8000` in Chrome or Firefox, click the padlock icon, and find the option to
view the certificate details.
Identify the fields that show the issuer (which should be the mkcert CA you installed),
the subject (which should be `localhost`), and the expiry date.
