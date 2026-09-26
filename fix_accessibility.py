r"""Fix Acrobat accessibility failures in LaTeX-tagged PDFs (post-processing).

Fix 1 — 'Lbl and LBody must be children of LI':
  Any /Lbl or /LBody element (literal or role-mapped, e.g. /footnotemark,
  /footnotelabel) whose role-resolved parent is not /LI is renamed to /Span.

Fix 2 — 'Headings: Appropriate nesting':
  a) LaTeX \paragraph run-in headings (role-mapped to /H5) are retagged as /P,
     removing them from the heading hierarchy.
  b) Any remaining heading that skips a level (e.g. H4 right after H2) is
     demoted, along with its immediately following same-level siblings, so
     levels never increase by more than one.

Usage: python3 fix_accessibility.py input.pdf output.pdf
"""
import re
import sys
import pikepdf

def main(inp, outp):
    pdf = pikepdf.open(inp)
    st = pdf.Root.StructTreeRoot
    rm = st.get("/RoleMap")
    rolemap = {str(k): str(rm[k]) for k in rm.keys()} if rm else {}
    eff = lambda t: rolemap.get(t, t)
    stats = {}
    def bump(key):
        stats[key] = stats.get(key, 0) + 1

    headings = []  # (node, original_level) in reading order

    def walk(node, parent_eff):
        raw = str(node.S) if "/S" in node else None
        e = eff(raw) if raw else None

        # ---- Fix 1: stray Lbl/LBody -> Span ----
        if e in ("/Lbl", "/LBody") and parent_eff != "/LI":
            node.S = pikepdf.Name("/Span")
            bump(f"{raw} (as {e}) under {parent_eff} -> /Span")
            e = "/Span"

        # ---- Fix 2a: \paragraph H5 run-in headings -> P ----
        if raw == "/paragraph" and re.fullmatch(r"/H\d+", e or ""):
            node.S = pikepdf.Name("/P")
            bump(f"/paragraph (as {e}) -> /P")
            e = "/P"

        # collect remaining headings in reading order
        m = re.fullmatch(r"/H(\d+)", e or "")
        if m:
            headings.append((node, int(m.group(1))))

        kids = node.get("/K")
        if kids is not None:
            items = list(kids) if isinstance(kids, pikepdf.Array) else [kids]
            for k in items:
                if isinstance(k, pikepdf.Dictionary) and "/S" in k:
                    walk(k, e)

    walk(st, None)

    # ---- Fix 2b: demote level-skipping headings (and same-level siblings) ----
    prev = 0
    demote_to = None      # active demotion: (orig_level, new_level)
    for node, lvl in headings:
        if demote_to and lvl == demote_to[0]:
            new = demote_to[1]
            node.S = pikepdf.Name(f"/H{new}")
            bump(f"H{lvl} demoted to H{new}")
            prev = new
            continue
        demote_to = None
        if prev and lvl > prev + 1:
            new = prev + 1
            node.S = pikepdf.Name(f"/H{new}")
            bump(f"H{lvl} demoted to H{new} (skip after H{prev})")
            demote_to = (lvl, new)
            prev = new
        else:
            prev = lvl

    total = sum(stats.values())
    print(f"Modified {total} elements:")
    for k, n in sorted(stats.items()):
        print(f"  {k}: {n}")
    pdf.save(outp)
    print(f"Saved: {outp}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
