git init -q -b main
git add -A -- . ":!setup-repo.sh"
git -c user.name=fixture -c user.email=fixture@example.invalid commit -q -m "Orders API"
