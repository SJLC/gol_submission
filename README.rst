============
What is this
============

A single-purpose hack script that I'm sharing with a couple friends.
Probably should have made it a bit better example by including
proper unit tests instead of tests in commented-out '#DBG#' lines,
since they are learning python... maybe I will eventually.

==============
Prerequisites
==============

Requires non-standard-library modules jinja2, wikitextparser

Instead of installing every random module needed by a python script 
systemwide, I like to use virtualenv to make a local copy of modules within the
working dir for that particular python script

::

  virtualenv venv
  . venv/bin/activate
  pip wikitextparser
  pip jinja2 

=======
Running
=======

Edit the draft page in the wiki and copy-paste all the wikitext as the input file.
I've checked in an example as 'WIKI.txt' (actually 'WIKI.txt.non-asscii is my original,
but I had to hack it a bit till non-ascii characters from the wiki are handled, see
TODO)

::

  ./gol_submission WIKI.txt BBCODE.txt

=====
TODO
=====

* Non-ascii characters such as '£' are not yet handled, 
  need to figure out what character encoding is being used 
  (I tried utf-8 but that didn't seem to work)?
* Missing "gem" and "biggie" lists because they are not yet extracted from wiki draft
  (for now, just putting in blank lists, but the template part
  for gems & biggies does work because I tested it with fake data)
* Add proper unit tests
