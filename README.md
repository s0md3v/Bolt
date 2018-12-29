<h1 align="center">
  <br>
  <a href="https://github.com/s0md3v/Bolt"><img src="https://i.ibb.co/2tnkLvt/bolt.png" alt="Bolt"></a>
  <br>
  Bolt
  <br>
</h1>

<h4 align="center">A dumb CSRF scanner</h4>

<p align="center">
  <a href="https://github.com/s0md3v/Bolt/releases">
    <img src="https://img.shields.io/github/release/s0md3v/Bolt.svg">
  </a>
  <a href="https://travis-ci.com/s0md3v/Bolt">
    <img src="https://img.shields.io/travis/com/s0md3v/Bolt.svg">
  </a>
  <a href="https://github.com/s0md3v/Bolt/issues?q=is%3Aissue+is%3Aclosed">
      <img src="https://img.shields.io/github/issues-closed-raw/s0md3v/Bolt.svg">
  </a>
</p>

![demo](https://i.ibb.co/mTtHTGP/Screenshot-2018-12-30-03-42-26.png)

### Important
Bolt is in alpha phase of development which means it's full of bugs. Any production use of this tool discouraged.
Pull requests and issues are welcome. I also suggest you to put this repo on watch if you are interested in it.

### Current Features
- Crawling
- Complete HTTP Support
- Checks
  - Entropy
  - Replay attack
  - Absence of CSRF protection when requested from a mobile
  - Removing CSRF token parameter from request
  - Removing CSRF token from parameter
  - Requesting resources with a fake token
  - Potenial race condition

### Features to be added
- Support CSRF tokens in cookies
- Referrer and Origin based checks
- Checks
  - True entropy of tokens
  - Checking if server checks the token to a specific length
 and more...

### Usage

Scanning a website for CSRF using Bolt is as easy as doing
```
python3 bolt.py -u https://github.com -l 2
```
Where `-u` is used to supply the URL and `-l` is used to specify the depth of crawling.

Other options and switches:

- `-t` number of threads
- `--delay` delay between requests
- `--timeout` http request timeout
- `--headers` supply http headers

#### Credits
Regular Expressions for detecting hashes are taken from [hashID](https://github.com/psypanda/hashID).
