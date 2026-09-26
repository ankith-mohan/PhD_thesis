"""Fix Acrobat's 'Lbl and LBody must be children of LI' accessibility failure.

v2: Resolves the structure tree RoleMap the same way Acrobat does, so it
catches both literal /Lbl and /LBody elements AND custom tags role-mapped
to them (e.g. LaTeX's /footnotemark, /footnotelabel). Any such element
whose (role-resolved) parent is not /LI is renamed to /Span.
Genuine list structures (L > LI > Lbl/LBody) are left untouched.

Usage: python3 fix_lbl.py input.pdf output.pdf
"""
import sys
import pikepdf

def main(inp, outp):
    pdf = pikepdf.open(inp)
    st = pdf.Root.StructTreeRoot
    rm = st.get("/RoleMap")
    rolemap = {str(k): str(rm[k]) for k in rm.keys()} if rm else {}

    def effective(tag):
        """Resolve a tag through the RoleMap (single level, like Acrobat)."""
        return rolemap.get(tag, tag)

    stats = {}

    def walk(node, parent_eff):
        raw = str(node.S) if "/S" in node else None
        eff = effective(raw) if raw else None
        if eff in ("/Lbl", "/LBody") and parent_eff != "/LI":
            node.S = pikepdf.Name("/Span")
            key = (raw, eff, parent_eff)
            stats[key] = stats.get(key, 0) + 1
            eff = "/Span"
        kids = node.get("/K")
        if kids is not None:
            items = list(kids) if isinstance(kids, pikepdf.Array) else [kids]
            for k in items:
                if isinstance(k, pikepdf.Dictionary) and "/S" in k:
                    walk(k, eff)

    walk(st, None)
    total = sum(stats.values())
    print(f"Renamed {total} elements to /Span:")
    for (raw, eff, parent), n in sorted(stats.items()):
        via = f" (role-mapped to {eff})" if raw != eff else ""
        print(f"  {raw}{via} under {parent}: {n}")
    pdf.save(outp)
    print(f"Saved: {outp}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
