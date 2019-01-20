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
Bolt is in beta phase of development which means there can be bugs. Any production use of this tool discouraged.
Pull requests and issues are welcome. I also suggest you to put this repo on watch if you are interested in it.

### Workflow

#### Crawling
Bolt crawls the target website to the specified depth and stores all the HTML forms found in a database for further processing.

#### Evaluating
In this phase, Bolt finds out the tokens which aren't strong enough and the forms which aren't protected.

##### Comparing
This phase focuses on detection on replay attack scenarios and hence checks if a token has been issued more than one time.
It also calculates the average [levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) between all the tokens to see if they are similar.\
Tokens are also compared against a database of 250+ hash patterns.

##### Observing
In this phase, 100 simultaneous requests are made to a single webpage to see if same tokens are generated for the requests.

##### Testing
This phase is dedicated to active testing of the CSRF protection mechanism. It includes but not limited to checking if protection exsists for moblie browsers, submitting requests with self-generated token and testing if token is being checked to a certain length.

##### Analysing
Various statistical checks are performed in this phase to see if the token is really random.
Following tests are performed during this phase
- Monobit frequency test
- Block frequency test
- Runs test
- Spectral test
- Non-overlapping template matching test
- Overlapping template matching test
- Serial test
- Cumultative sums test
- Aproximate entropy test
- Random excursions variant test
- Linear complexity test
- Longest runs test
- Maurers universal statistic test
- Random excursions test

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
Regular Expressions for detecting hashes are taken from [hashID](https://github.com/psypanda/hashID).\
Bit level entropy tests are taken from [highfestiva](https://github.com/highfestiva)'s python implementation of statistical tests.
