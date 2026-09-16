# Spike note

This note holds every markdown construct that a notesmgr user is likely
to write, so that the two candidate widgets can be compared on the same
input. It is deliberately awkward in places.

## Inline styles

A paragraph with **bold**, *italic*, ***both***, `inline code`,
~~struck through~~ text and a line break at the end of this line,
followed by the rest of the paragraph.

## Lists

- First item
- Second item, with a nested list under it
  - Nested item
  - Another nested item
    1. Deeply nested and ordered
    2. Second deeply nested
- Third item

1. Ordered first
2. Ordered second
   - Unordered under ordered
3. Ordered third

- [ ] An unchecked task
- [x] A checked task

## Fenced code

```python
def greet(name: str) -> str:
    """Return a greeting, with characters that HTML minds: < > &."""
    return f'Hello, {name} <&>'
```

A fence holding markdown, which must not be rendered as markdown:

```markdown
# Not a heading
- Not a list item
```

An indented code block:

    indented code, four spaces

## Table

| Construct | Supported | Note |
| --- | :---: | ---: |
| Heading | yes | six levels |
| Table | ? | this table |
| Missing cell | |
| Long cell | yes | a cell with rather a lot of text in it, to see what the widget does when the column will not fit |

## Block quote

> A quoted paragraph, with **bold** inside it.
>
> > A quote inside the quote.
>
> - and a list inside the quote

## Links

An [ordinary link](https://example.com/), a [link with no target](),
a [relative link](spike_note.md), a bare URL <https://example.com/bare>,
and a [reference link][ref].

[ref]: https://example.com/reference

## Images

An image that is there:

![A checked pattern](spike_image.png)

An image that is not there:

![Missing on purpose](no_such_image.png)

## Embedded HTML

The next line is raw HTML in the note, and it must be shown as text
rather than obeyed:

<b>this must not turn bold</b> and <script>alert('no')</script>

An HTML entity written by hand: &amp; and &lt; and &#8212;

## Horizontal rule

---

## Long line

A single very long line without any newline in it, to see whether the widget wraps it or grows a horizontal scrollbar that the panel cannot afford: aaaaaaaaaa bbbbbbbbbb cccccccccc dddddddddd eeeeeeeeee ffffffffff gggggggggg hhhhhhhhhh iiiiiiiiii jjjjjjjjjj kkkkkkkkkk llllllllll.

## Headings of every level

# Level one
## Level two
### Level three
#### Level four
##### Level five
###### Level six
