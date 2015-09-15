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
Be careful that the editor you use to save the pasted text is in utf-8 mode, 
learned this lesson the hard way...

I've checked in an example as 'WIKI.txt' 

::

  ./gol_submission WIKI.txt BBCODE.txt

=====
TODO
=====

* Missing "gem" and "biggie" lists because they are not yet extracted from wiki draft
  (for now, just putting in blank lists, but the template part
  for gems & biggies does work because I tested it with fake data)
* Add proper unit tests
