.PHONY: eval session

eval:
	python3 eval/run_eval.py

session:
	@latest=$$(ls -1dt eval/out/* 2>/dev/null | head -n1); \
	if [ -n "$$latest" ]; then \
		echo $$latest; \
		cat $$latest/_README.md; \
	else \
		echo "No eval sessions found. Run 'make eval' first."; \
	fi