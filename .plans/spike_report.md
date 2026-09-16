# Step 6 — markdown rendering spike: comparison and recommendation

Run on macOS 26.7 (darwin, arm64) on 2026-09-16, against `markdown`
3.10.3, `tkinterweb` 4.25.4 (with `tkinterweb-tkhtml` 2.1.1) and
`tkhtmlview` 0.3.2, which were the newest releases of all three.

**Outcome: neither HTML widget was taken.** `tkinterweb` cannot run on
Tcl/Tk 9 and therefore not on Python 3.14, and `tkhtmlview` renders too
little of a note to be trusted. notesmgr draws the formatted note
itself instead. The evidence is below and the decision is at the end.

## What was run

- `.plans/spike_note.md` — one note holding every construct a
  notesmgr user is likely to write, and the awkward ones step 7 has
  to survive: nested lists, a fence holding markdown, a table with a
  missing cell and an overlong cell, a nested block quote, a link
  with no target, an image that is there, an image that is not,
  raw HTML, a hand-written entity, a horizontal rule and a very long
  unbroken line.
- `.plans/spike_widgets.py` — shows both widgets side by side on that
  note, and with `--check` prints the same facts without a window.
- `.plans/spike_image.png` — the 96×48 image that the note shows.

Both widgets are given exactly the same HTML, produced the way step 7
plans to produce it (`fenced_code`, `tables`, `sane_lists`).

## What the measurements say

| Python | Tcl/Tk | tkinterweb | tkhtmlview |
| --- | --- | --- | --- |
| 3.12.10 | 8.6.16 | works, 0.002 s per reload | works, 0.009 s per reload |
| 3.13.15 | 8.6.18 | works, 0.002 s per reload | works, 0.009 s per reload |
| 3.14.7 | 9.0.4 | **cannot be used** | works, 0.008 s per reload |

Both are fast enough: step 7 reloads the note about once a second and
neither is anywhere near that budget. Both show the same 2111
characters of text, so neither silently loses any *content* of the
note. The difference is entirely in what the content *looks like*.

## The decisive finding: tkinterweb does not run on Tcl/Tk 9

On Python 3.14 building the widget fails outright:

```text
OSError: No Tkhtml versions could be found for Tcl/Tk 9.
```

`tkinterweb` is a Python wrapper around Tkhtml3, a compiled Tcl
extension shipped as per-platform wheels by `tkinterweb-tkhtml`. Its
loader looks for a binary whose name carries a `-TclTk9` suffix when
`TclVersion >= 9`. I downloaded every wheel of `tkinterweb-tkhtml`
2.1.1 and of `tkinterweb-tkhtml-extras` 1.3.1 and checked what is
inside them:

| Wheel | Binaries it carries |
| --- | --- |
| macosx_11_0_arm64, macosx_10_6_x86_64 | `libTkhtml3.0.dylib` |
| win32, win_amd64 | `libTkhtml3.0.dll` |
| manylinux1_x86_64, i686, aarch64, armv7l | `libTkhtml3.0.so` |

There is **no Tcl/Tk 9 binary for any platform** in the published
releases. So this is not a macOS quirk: `tkinterweb` cannot work on
any Tcl/Tk 9 interpreter as currently published. It is a known,
still-open upstream issue, filed for this exact case:
<https://github.com/Andereoo/TkinterWeb/issues/159>
("need binaries for TK 9.0 - using python 3.14").

Python 3.14 on macOS (python.org framework build) ships Tcl/Tk 9.0.4,
so this is the default development and build interpreter of this
repository. notesmgr must support 3.12, 3.13 and 3.14, and the last
clean build of each step runs on 3.14.

I have **not** verified which Tcl/Tk the Windows and Linux builds of
Python 3.14 use; they may well still be on 8.6 today, in which case
`tkinterweb` would work there for now. That does not change the
conclusion, because it fails on the machine notesmgr is developed on,
and every platform follows Python to Tcl/Tk 9 eventually.

## What each library can actually render

`tkinterweb` is a real HTML and CSS engine. Tables get laid out,
block quotes get indented, a stylesheet can be handed to it, images
resolve against a base url, text can be selected and links can be
hooked. It is the right tool — where it runs.

`tkhtmlview` is not an engine. It is a 750-line `HTMLParser` that
inserts text into a `tkinter.Text` and applies tags. Its whole
supported tag list is `br ul ol li img a b strong i em u mark span
div p pre code h1…h6 table tr th td`. Everything else is ignored.
What that costs on the sample note, read straight out of the widget:

- **Tables** become tab characters. The table of the sample comes out
  as `\tConstruct\tSupported\tNote`, with no column widths and no
  alignment, and the overlong cell wraps and destroys what little
  alignment the tabs gave. `thead` and `tbody`, which the `tables`
  extension emits, are not known to it at all.
- **Block quotes are completely flat.** `blockquote` is not in the
  tag list, so `A quoted paragraph` and `A quote inside the quote`
  come out indistinguishable from ordinary paragraphs — no indent,
  no rule, no sign of nesting.
- **Horizontal rules vanish.** `hr` is not in the tag list, so the
  `---` between two sections leaves nothing on screen.

For a note that is mostly headings, prose and code it looks
acceptable. For a note that quotes something or holds a table it
quietly misleads, which is worse than showing raw text would be.

## What each library costs

| | tkinterweb | tkhtmlview |
| --- | --- | --- |
| Pulls in | `tkinterweb-tkhtml` (compiled Tcl extension) | `pillow` (4.8 MB, compiled), `requests` |
| Wheel per platform | yes, hand-built by one maintainer | pure Python, but `pillow` is per-platform |
| Type information | none, and no `types-*` package | none, and no `types-*` package |
| Project size | active, large | small, 0.3.2 |

Neither ships `py.typed`, so either way step 7's import needs
`# type: ignore[import-untyped]` with the untyped surface stopped at
a thin typed wrapper, which is what we agreed. `markdown` needs
`types-Markdown` in `install_requires` alongside it, the way
`types-Send2Trash` is already carried.

## Two findings about tkhtmlview that step 7 would have to live with

Both read out of `tkhtmlview/html_parser.py`, not guessed:

1. **It fetches remote images synchronously on the Tk main thread.**
   For any `src` starting `http://`, `https://` or `ftp://` it calls
   `requests.get(src)` with no timeout, inside the parse, wrapped in
   a bare `except:`. A note holding a remote image therefore freezes
   the whole window for as long as the request takes, and there is no
   option to turn it off. notesmgr would have to strip remote images
   out of the HTML before handing it over.
2. **It resolves a local image path against the current working
   directory**, not against the note, with a plain
   `os.path.exists(src)`. There is no base-url concept. An image
   beside a note is found only by luck. The spike script makes the
   note's folder current on purpose so that the two libraries could be
   compared fairly; notesmgr cannot do that, because the working
   directory is where the user started the program from.

## A finding that applies whichever way this goes

Python-Markdown passes raw HTML in the note straight through into its
output. The sample note's `<b>this must not turn bold</b>` really did
arrive at the widgets as markup. `README_pypi.md` and the step 7 plan
both say embedded HTML must be shown as text, and the way to get that
in Python-Markdown 3 (`safe_mode` is long gone) is to take the two
processors out:

```python
converter = markdown.Markdown(extensions=EXTENSIONS)
converter.preprocessors.deregister('html_block')
converter.inlinePatterns.deregister('html')
```

Verified: `<b>…</b>` then arrives escaped as `&lt;b&gt;…&lt;/b&gt;`.
The spike script does this, so the comparison was made on the HTML
step 7 will really produce.

## Recommendation

**Rule out `tkinterweb`.** It renders best, but it does not run on the
interpreter this project builds and tests on, the fix is a compiled
binary in someone else's project, and the issue is open. Taking a
dependency that breaks the default build is not a trade worth making
for prettier tables.

That leaves `tkhtmlview` as the only one of the two that can be used —
but the spike has shown it to be thin enough that I would not choose
it either. It silently flattens block quotes, drops horizontal rules,
fakes tables with tabs, freezes the window on a remote image, cannot
find a local one, and brings in `pillow` and `requests` for the
privilege.

**My recommendation is a third option that the plan did not consider:
render the note into a `tkinter.Text` with tags that notesmgr owns.**

That is what `tkhtmlview` does, only done correctly and for the
constructs notes actually use. Concretely: keep `markdown_render.py`
producing HTML (step 8's `Copy formatted` needs the HTML anyway), and
add a pure function from that HTML to a list of text-and-tag segments
using `html.parser` from the standard library; `note_view.py` then
applies the segments to the `Text` widget it already has.

Why I think it is the better and more general solution:

- **No new runtime dependency at all** beyond `markdown` itself. No
  compiled Tcl extension, no `pillow`, no `requests`.
- **It cannot break on a Tk upgrade**, which is precisely what has
  just happened to `tkinterweb`.
- **It fits the boundary the plan already set.** "If a question has a
  right answer, it belongs in the model." HTML to segments is a pure
  function with a right answer, tested headless over the markdown
  fixture corpus step 7 already plans — no widget needed to test the
  part that can be wrong.
- **Block quotes, rules and tables can be done properly**, because a
  `Text` widget has `lmargin1`/`lmargin2` for indentation, borders and
  background for quotes and code, and a monospace tag lines a table up
  better than the tabs `tkhtmlview` emits.
- **It is fully typed**, so no `# type: ignore` and no untyped surface
  anywhere.

The cost is that notesmgr writes and maintains the renderer, and I
would estimate roughly 150–250 lines over what step 7 planned, plus
its tests. Images are the one place it is genuinely more work:
`tkinter.PhotoImage` handles PNG and GIF without `pillow`, which
covers the common case, and anything else would be shown as its alt
text.

In order of preference:

1. Own `Text` renderer, no widget dependency. Best result, more work
   in step 7, no dependency risk.
2. `tkhtmlview`, as the plan is written. Least work, poor fidelity on
   quotes, rules and tables, and the two problems above to work
   around.
3. `tkinterweb`. Only if notesmgr were to drop Python 3.14, which it
   will not.

## Decision taken

**The recommendation was accepted: neither HTML widget.** notesmgr
draws the formatted note itself, into an ordinary `tkinter.Text`.
`tkhtmlview` stays named as the fallback, to be reconsidered if the
own renderer turns out to be much harder than this spike suggests;
everything needed to make that switch is in this report.

What step 6 therefore added:

- `setup.py`: `markdown >= 3.10.3` and
  `types-Markdown >= 3.10.2.20260712` in `install_requires`, and no
  widget dependency.
- `src/notesmgr/version_info.py`: `markdown` in `REPORTED_PACKAGES`,
  so `notesmgr --version` reports it. `types-Markdown` is stubs only
  and is not reported, the same way `types-Send2Trash` is not.
- `README_pypi.md`: `markdown` in "What notesmgr is built on", and a
  line saying the formatted preview is drawn by notesmgr itself and
  therefore cannot be broken by a new version of Tk.

Step 7 lands in two reviews: the pure HTML-to-segments function with
`note_view.py`'s tags and their tests first, so the rendering can be
looked at early, and the panel wiring with the `.txt`/`.md` switch
after it.

`pyproject.toml` was not touched: it takes `dependencies` from
`setup.py` through `dynamic`.

## How to see it for yourself

Neither candidate is a dependency of notesmgr, so a clean build leaves
neither in the venv and the spike then reports both as unusable. It
still runs, and `markdown` is there, so the note is still converted:

```sh
./venv/bin/python3 .plans/spike_widgets.py --check
```

To have the spike render again, put the candidates back. This lasts
only until the next clean build, which is what makes it safe:

```sh
./venv/bin/python3 -m pip install tkinterweb tkhtmlview
./venv/bin/python3 .plans/spike_widgets.py
```

On Python 3.14 that shows `tkhtmlview` rendering and `tkinterweb`
saying in its own pane why it cannot be used. To see the two of them
rendering side by side the script has to be run on a Tcl/Tk 8.6
interpreter, which on this machine is Python 3.12 or 3.13, and a venv
outside the repository keeps the repository venv out of it:

```sh
python3.13 -m venv /tmp/spike313
/tmp/spike313/bin/python3 -m pip install markdown tkinterweb tkhtmlview
/tmp/spike313/bin/python3 .plans/spike_widgets.py
```

`Reload both` loads the note again and prints the seconds it took,
which is what the file watch of step 7 will be doing once a second.
