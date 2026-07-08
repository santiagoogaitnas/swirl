# brokenpkg

A tiny Python package deliberately full of lint problems (unused imports,
undefined names, `== None` comparisons, bare excepts, pointless f-strings).

It exists as the farm's test dummy: `farm demo` copies this directory into
`runs/demo-<timestamp>/` and points a small agent fleet at the copy. This
template itself should stay broken — never fix it in place.
