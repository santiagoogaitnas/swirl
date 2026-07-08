# brokenpkg

A tiny Python package that exists as the farm's test dummy: `farm demo`
copies this directory into `runs/demo-<timestamp>/` and points a small agent
fleet at the copy — never at this template itself.

If the copy has lint problems, the demo runs FIX mode and grinds them to
zero. If it's already clean (agents from past demos may have left it that
way), the demo runs GRIND mode instead: endless improvement passes until
stopped — which is a better show anyway.
