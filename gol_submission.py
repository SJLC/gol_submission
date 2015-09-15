#!/usr/bin/env python

import os, sys, re, itertools
import wikitextparser
import jinja2

## compatibility hacks: teach python2 to open files with an encoding
if sys.version_info[0] < 3:
    import codecs
    open = codecs.open

## input side of conversion: extract standard sections from file containing wiki draft
def read_wiki_data(input_filename):
    fp = open(input_filename, "r", encoding="utf-8")
    input_text = fp.readlines()
    fp.close()
    input_text = "".join(input_text)
    
    wikitextparser.WikiText(input_text)   
    parsed_text = wikitextparser.WikiText(input_text)
    
    article_sections = {}
    for section in parsed_text.sections:
        if section.title == " Intro paragraph ":
            article_sections["intro_paragraph"] = section.string
        elif section.title == " Losers ":
            article_sections["loser_paragraphs"] = section.string
        elif section.title == " Winners ":
            article_sections["winner_paragraphs"] = section.string
        elif section.title == " Biggies ":
            article_sections["biggie_paragraphs"] = section.string
        elif section.title == " Hidden Gems ":
            article_sections["gem_paragraphs"] = section.string
        elif section.title == " Conclusion ":
            article_sections["conclusion_paragraph"] = section.string

    return article_sections

def pairs(input_list):
    "s -> (s0,s1), (s2,s3), (s4, s5), ..."
    evens = itertools.islice(input_list, 0, len(input_list), 2)
    odds = itertools.islice(input_list, 1, len(input_list), 2)
    return zip(evens, odds)

def wiki_to_bbcode(text):
    # translate bold to bbcode
    text = re.sub(r"'''([^']+)'''",r"[b]\1[\\b]", text)

    # translate italics to bbcode
    text = re.sub(r"''([^']+)''",r"[i]\1[\\i]", text)

    # translate urls to bbcode
    text = re.sub(r"\[(http[^ ]+) ([^]]+)\]", r"[url=\1]\2[\\url]", text)

    return text


def reformat_wiki_data(input_filename):
    # pick out major sections
    article_sections = read_wiki_data(input_filename)

    # fix up the easy ones
    reformatted_sections = {}
    for section in ["intro_paragraph", "loser_paragraphs", "winner_paragraphs", "conclusion_paragraph"]:
        text = article_sections[section]
        # strip off section title
        text = re.sub(r"^=+[^=]+=+\n","", text)

        reformatted_sections[section] = wiki_to_bbcode(text)


    # translate gem and biggie sections into lists
    #for list_type in ["gem", "biggie"]:
    for list_type in ["gem"]:
        list_name = list_type + "_list" # e.g. gem_list 
        section_name = list_type + "_paragraphs" # e.g. gem_paragraphs
        paragraphs = article_sections[section_name]
        reformatted_sections[list_name] = []

        # strip off main section title
        paragraphs = re.sub(r"^=+[^=]+=+\n+","", paragraphs)
        #DBG#print(paragraphs.encode('utf-8'))

        # split into subsection for each project 
        projects = re.split(r"(===[^=]+===)", paragraphs)
        projects = filter(None, projects) # get rid of empty strings after split()
        for (proj_header, proj_body) in pairs(projects):
            entry = {}

            # pick out url from project header
            
            # "=== [http://some/url this is the name] ==="
            # grab http://some/url
            try:
                url = re.search(r"\[(http\S+)", proj_header).group(1)
            except:
                url = "INVALID_URL"
                print("Failed to find url in header:\n%s" % proj_header.encode('utf-8'))

            # pick out banner, screenshot, text1, text2 from the project body
            
            # "Banner http://banner/url blah blah"
            # grab http://banner/url
            try:
                banner = re.search(r"banner (http\S+)", proj_body, re.IGNORECASE).group(1)
            except:
                banner = "INVALID_BANNER"
                print("Failed to find banner in body:\n%s" % proj_body.encode('utf-8'))

            # "Screenshot http://screenshot/url blah blah"
            # grab http://screenshot/url
            try:
                screenshot = re.search(r"screenshot (http\S+)", proj_body, re.IGNORECASE).group(1)
            except:
                screenshot = "INVALID_SCREENSHOT"
                print("Failed to find screenshot in body:\n%s" % proj_body.encode('utf-8'))

            #@@@ TODO
            text1 = "PRE-SCREENSHOT PARAGRAPH"
            text2 = "POST-SCREENSHOT PARAGRAPH(S)"

            entry = { "url": url,
                      "banner": banner,
                      "screenshot": screenshot,
                      "text1": wiki_to_bbcode(text1),
                      "text2": wiki_to_bbcode(text2) }

            #DBG#print("HEADER:", proj_header.encode('utf-8'))
            #DBG#print("BODY:", proj_body.encode('utf-8'))
            #DBG#print("ENTRY:", entry.encode('utf-8'))

            reformatted_sections[list_name].append(entry)

    return reformatted_sections

## output side of conversion: insert extracted and bbcode-ized sections into template

# generate full set of test data to be substituted into template
def gen_test_data():
    test_gem1 = {"url": "http://kickstarter.com/gem1", 
                 "banner": "http://imgur.com/gem1_banner", 
                 "screenshot": "http://imgur.com/gem1_screenshot",
                 "text1": "Here comes the gem1 screenshot...",
                 "text2": "...there went the gem1 screenshot"}
    
    test_gem2 = {"url": "http://kickstarter.com/gem2", 
                 "banner": "http://imgur.com/gem2_banner", 
                 "screenshot": "http://imgur.com/gem2_screenshot",
                 "text1": "Here comes the gem2 screenshot...",
                 "text2": "...there went the gem2 screenshot"}
    
    test_gem_list = [test_gem1, test_gem2]
    
    test_biggie1 = {"url": "http://kickstarter.com/biggie1", 
                 "banner": "http://imgur.com/biggie1_banner", 
                 "screenshot": "http://imgur.com/biggie1_screenshot",
                 "text1": "Here comes the biggie1 screenshot...",
                 "text2": "...there went the biggie1 screenshot"}
    
    test_biggie2 = {"url": "http://kickstarter.com/biggie2", 
                 "banner": "http://imgur.com/biggie2_banner", 
                 "screenshot": "http://imgur.com/biggie2_screenshot",
                 "text1": "Here comes the biggie2 screenshot...",
                 "text2": "...there went the biggie2 screenshot"}
    
    test_biggie_list = [test_biggie1, test_biggie2]
    
    test_data = {}
    test_data["intro_paragraph"] = "Amusing introduction"
    test_data["gem_list"] = test_gem_list
    test_data["loser_paragraphs"] = "Bzzzzzt"
    test_data["winner_paragraphs"] = "YOU WON!"
    test_data["running_paragraphs"] = "You may or may not have already won"
    test_data["biggie_list"] = test_biggie_list
    test_data["closing_paragraph"] = "The usual plea for help"

    return test_data

## do the conversion!

progname = os.path.basename(__file__)
if len(sys.argv) != 3:
    print("Usage: %s <wiki draft file> <bbcode output file>" % progname)
    sys.exit(1)

input_filename = sys.argv[1]
output_filename = sys.argv[2]

# load template from same directory containing this script

parentdir = os.path.dirname(os.path.abspath(__file__))
loader = jinja2.FileSystemLoader(parentdir)
env = jinja2.Environment(loader=loader)
templ_filename = progname.replace(".py", ".tmpl")
template = env.get_template(templ_filename)

# test out template with test data 
#DBG#bbcode_sections = gen_test_data()

# import data from wiki draft
bbcode_sections = reformat_wiki_data(input_filename)
#DBG#for name in bbcode_sections.keys():
#DBG#  print("Section %s:\n%s" % (name, bbcode_sections[name]))

# insert imported data into template
bbcode_article = template.render(bbcode_sections)

# save result to output file
fp = open(output_filename, "w", encoding="utf-8")
fp.write(bbcode_article)
fp.close()
