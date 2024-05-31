#!/bin/bash

# This is test script to run all checks at once.
# Commands:
# _______________________
# |-> chmod +x test.sh  |
# |-> ./test.sh         |
# |_____________________|

# Color codes
info="\033[33m"
fail="\033[31m"
success="\033[32m"
end="\033[0m"

# black formatting check
echo -e "${info}[INFO] black formatting check:${end}"
black . --check

# pytest check'
echo
echo -e "${info}[INFO] pytest check:${end}"
coverage run -m pytest -v
changed_files=$(git ls-files -mo -x "*.pyc" -x ".*" -x "*.db" -x "instance/")
coverage report -m $(echo $changed_files)

# pylint check
echo
echo -e "${info}[INFO] pylint check:${end}"
lint_score=$(pylint --rcfile .pylintrc src/ tests/)
echo "$lint_score"

# check if pylint score is < 9.0
rating=$(echo "$lint_score" | grep -oE "[0-9]+\.[0-9]+\/[0-9]+ " | grep -oE "[0-9]+\.[0-9]")
value=$(echo "$rating" | awk '{printf "%.1f", $0}')
awk "BEGIN {
      if (${value} < 9.0) print \"${fail}[INFO] Code can be improved.${end}\";
      else print \"${success}[INFO] Excellent code!${end}\n\"
    }"
