#!/usr/bin/env bash -ex

# Check `README.md` is up to date
diff --brief docs/index.md README.md

# Check copy-paste errors in tutorials
if grep -r --include "*.md" "Usage: tutorial" ./docs; then
	echo "Incorrect console demo"
	exit 1
fi
if grep -r --include "*.md" "python tutorial" ./docs; then
	echo "Incorrect console demo";
	exit 1
fi
