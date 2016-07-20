#!/bin/bash
diff expected-child.n.02.txt <(python syngrep.py child.n.02 1984.en.txt)
diff expected-kid.v.02.txt <(python syngrep.py kid.v.02 1984.en.txt)

