.PHONY: setup run dashboard all clean

setup:
	uv venv
	uv pip install -r requirements.txt
	cp -n .env.example .env || true

run:
	python main.py

dashboard:
	streamlit run dashboard.py

all:
	make run & make dashboard

clean:
	rm -rf .venv __pycache__ workspace/data workspace/memory