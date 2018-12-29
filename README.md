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

### Important
Bolt is in alpha phase of development which means it's full of bugs. Any production use of this tool discouraged.

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
