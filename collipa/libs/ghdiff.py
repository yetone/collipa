import difflib


default_css = """\
<style type="text/css">
    .diff {
        border: 1px solid #cccccc;
        background: none repeat scroll 0 0 #f8f8f8;
        font-family: 'Bitstream Vera Sans Mono','Courier',monospace;
        font-size: 12px;
        line-height: 1.4;
        white-space: normal;
    }
    .diff div:hover {
        background-color:#ffc;
    }
    .diff .control {
        background-color: #eaf2f5;
        color: #999999;
    }
    .diff .insert {
        background-color: #ddffdd;
        color: #000000;
    }
    .diff .insert .highlight {
        background-color: #aaffaa;
        color: #000000;
    }
    .diff .delete {
        background-color: #ffdddd;
        color: #000000;
    }
    .diff .delete .highlight {
        background-color: #ffaaaa;
        color: #000000;
    }
</style>
"""


def escape(text):
    '''
    return xml.sax.saxutils.escape(text, {" ": "&nbsp;"})
    '''
    return text


def diff(a, b, n=3, css=True):
    split_tag = '</p>'
    if isinstance(a, basestring):
        a = [e + split_tag for e in a.split(split_tag) if e]
    if isinstance(b, basestring):
        b = [e + split_tag for e in b.split(split_tag) if e]
    return colorize(list(difflib.unified_diff(a, b, n=n)), css=css)


def colorize(diff, css=True):
    css = default_css if css else ""
    return css + "\n".join(_colorize(diff))


def _colorize(diff):
    if isinstance(diff, basestring):
        lines = diff.splitlines()
    else:
        lines = diff
    lines.reverse()
    while lines and not lines[-1].startswith("@@"):
        lines.pop()
    yield '<div class="diff">'
    while lines:
        line = lines.pop()
        klass = ""
        if line.startswith("@@"):
            klass = "control"
        elif line.startswith("-"):
            klass = "delete"
            if lines:
                _next = []
                while lines and len(_next) < 2:
                    _next.append(lines.pop())
                if _next[0].startswith("+") and (len(_next) == 1
                                                 or _next[1][0] not in ("+", "-")):
                    aline, bline = _line_diff(line[1:], _next.pop(0)[1:])
                    yield '<div class="delete">-%s</div>' % (aline,)
                    yield '<div class="insert">+%s</div>' % (bline,)
                    if _next:
                        lines.append(_next.pop())
                    continue
                lines.extend(reversed(_next))
        elif line.startswith("+"):
            klass = "insert"
        yield '<div class="%s">%s</div>' % (klass, escape(line),)
    yield "</div>"


def _line_diff(a, b):
    aline = []
    bline = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b).get_opcodes():
        if tag == "equal":
            aline.append(escape(a[i1:i2]))
            bline.append(escape(b[j1:j2]))
            continue
        aline.append('<span class="highlight">%s</span>' % (escape(a[i1:i2]),))
        bline.append('<span class="highlight">%s</span>' % (escape(b[j1:j2]),))
    return "".join(aline), "".join(bline)


if __name__ == "__main__":
    import optparse
    import sys

    parser = optparse.OptionParser()
    parser.set_usage("%prog [options] file1 file2")
    parser.add_option("--no-css", action="store_false", dest="css",
                      help="Don't include CSS in output", default=True)

    options, args = parser.parse_args()

    if (len(args) != 2):
        parser.print_help()
        sys.exit(-1)

    a = open(sys.argv[1]).read().splitlines()
    b = open(sys.argv[2]).read().splitlines()
    print diff(a, b, css=options.css)
