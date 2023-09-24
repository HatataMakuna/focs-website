import sys
import fitz

def mark_word(page, text):
    """Underline each word that contains 'text'.
    """
    found = 0
    wlist = page.get_text("words")  # make the word list
    for w in wlist:  # scan through all words on page
        if text in w[4]:  # w[4] is the word's string
            found += 1  # count
            r = fitz.Rect(w[:4])  # make rect from word bbox
            page.add_underline_annot(r)  # underline
    return found

fname = sys.argv[1]  # filename
text = sys.argv[2]  # search string
doc = fitz.open(fname)

print("underlining words containing '%s' in document '%s'" % (word, doc.name))

new_doc = False  # indicator if anything found at all

for page in doc:  # scan through the pages
    found = mark_word(page, text)  # mark the page's words
    if found:  # if anything found ...
        new_doc = True
        print("found '%s' %i times on page %i" % (text, found, page.number + 1))

if new_doc:
    doc.save("marked-" + doc.name)
