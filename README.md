# Query Sequence Finder
> Goal: Find the longest contig that contains a query sequence given a set of next generation sequence reads. 

**The assignment for this homework:** _Create a program that takes as input the set of all next-generation sequencing reads identified in a sample and an initial query sequence and returns the largest sequence contig that can be constructed from the reads that contains the initial query sequence._

The outline of this project/algorithm is as follows:
- Read in a set of next generation sequence (NGS) reads and a query sequence.
- Break each of the NGS sequence reads into k-mers (all possible substrings of length k that are contained in a string).
- Construct a [De Bruijn Graph](https://en.wikipedia.org/wiki/De_Bruijn_graph) using the prefix and suffix of each k-mer. [Concept Overview](https://www.youtube.com/watch?v=TNYZZKrjCSk&list=PL2mpR0RYFQsBiCWVJSvVAO3OJ2t7DzoHA&index=51). 
- Construct contigs (contiguous sequences) by following all possible paths through the De Brujin Graph.
- Search each contig for the query string.
- Return the longest contig that contains the query string.


## Installation

OS X & Linux:

```sh
npm install my-crazy-module --save
```

Windows:

```sh
edit autoexec.bat
```

## Usage example

A few motivating and useful examples of how your product can be used. Spice this up with code blocks and potentially more screenshots.

_For more examples and usage, please refer to the [Wiki][wiki]._

## Development setup

Describe how to install all development dependencies and how to run an automated test-suite of some kind. Potentially do this for multiple platforms.

```sh
make install
npm test
```

## Requirements

* Python miniconda base environment
    * a


## Meta

Your Name – [@YourTwitter](https://twitter.com/dbader_org) – YourEmail@example.com

Distributed under the XYZ license. See ``LICENSE`` for more information.

[https://github.com/yourname/github-link](https://github.com/dbader/)

## Contributing

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/yourname/yourproject/wiki