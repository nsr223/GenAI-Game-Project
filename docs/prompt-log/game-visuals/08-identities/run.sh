cd "$1"; v=$2; i=$3
codex exec -m gpt-6.2-sol -c model_reasoning_effort='"medium"' --ignore-user-config --ephemeral --skip-git-repo-check -s read-only -C "$1/empty" --output-schema "$1/schema.json" -o "$1/out/$v$i.json" - < "$1/prompt-$v.md" > "$1/out/$v$i.log" 2>&1; echo "$v$i exit $?"
