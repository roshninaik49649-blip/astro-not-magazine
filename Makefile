all:
	.venv/bin/python build.py

figures:
	.venv/bin/python figures/make_figures.py

qr:
	.venv/bin/python qr/make_qr.py

test:
	.venv/bin/python missions/tests/test_missions.py
	.venv/bin/python qa/link_checker.py

qa:
	.venv/bin/python qa/qa_check.py

clean:
	rm -f figures/out/*.svg qr/out/*.svg output/*
