# Mathematics Stack Exchange Datascraper
A Python data scraper for the Mathematics Stack Exchange

Run like so: `python3 scrape.py json_filepath.json num_concurrent_threads num_questions_to_scrape`, ie. `python3 scrape.py stack-exchange.json 200 50000`

I highly recommend running this on some faster hardware like Colab's GPU. It is far faster this way.

If you are indeed using a Colab GPU with a high-RAM runtime, the optimal value for `num_concurrent_threads` is approximately 20. With these parameter, it scrapes nearly 70 questions per second.

It will save a .json file to the specified filepath in the following format:

```
[{
  "url": "https://math.stackexchange.com/questions/6/",
  "title": "soft question - What is your favorite online graphing tool?",
  "question": "<p>I'm looking for a nice, quick online graphing tool. The ability to link to, or embed the output would be handy, too.</p>"
  },
  {
  "url": "https://math.stackexchange.com/questions/22/",
  "title": "linear algebra - Why is the matrix-defined Cross Product of two 3D vectors always orthogonal?",
  "question": "<p>By matrix-defined, I mean</p><p>$$\\left&lt;a,b,c\\right&gt;\\times\\left&lt;d,e,f\\right&gt; = \\left| \\begin{array}{ccc}i &amp; j &amp; k\\\\a &amp; b &amp; c\\\\d &amp; e &amp; f\\end{array}\\right|$$</p><p>...instead of the definition of the product of the magnitudes multiplied by the sign of their angle, in the direction orthogonal)</p><p>If I try cross producting two vectors with no $k$ component, I get one with only $k$, which is expected. But why?</p><p>As has been pointed out, I am asking why the algebraic definition lines up with the geometric definition.</p>"
  },
  {
  "url": "https://math.stackexchange.com/questions/20/",
  "title": "terminology - What is a real number (also rational, decimal, integer, natural, cardinal, ordinal...)?",
  "question": "<p>In mathematics, there seem to be a lot of different types of numbers. What exactly are:</p><ul><li>Real numbers</li><li>Integers</li><li>Rational numbers</li><li>Decimals</li><li>Complex numbers</li><li>Natural numbers</li><li>Cardinals</li><li>Ordinals</li></ul><p><em>And as</em> <strong>workmad3</strong> <em>points out, some more advanced types of numbers (I'd never heard of)</em></p><ul><li>Hyper-reals</li><li>Quaternions</li><li>Imaginary numbers</li></ul><p>Are there any other types of classifications of a number I missed?</p>"
  },
  {
  "url": "https://math.stackexchange.com/questions/1/",
  "title": "elementary set theory - What Does it Really Mean to Have Different Kinds of Infinities?",
  "question": "<p>Can someone explain to me how there can be different kinds of infinities?</p><p>I was reading \"<a href=\"http://en.wikipedia.org/wiki/The_Man_Who_Loved_Only_Numbers\" rel=\"noreferrer\">The man who loved only numbers</a>\" by <a href=\"http://en.wikipedia.org/wiki/Paul_Hoffman_(science_writer)\" rel=\"noreferrer\">Paul Hoffman</a> and came across the concept of countable and uncountable infinities, but they're only words to me.</p><p>Any help would be appreciated.</p>"
  }, ...
]
```

You can then load in the data like this:
```
import json

with open(json_filepath.json, "r") as f:
  data = json.load(f)
  
f.close()
```
