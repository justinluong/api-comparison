LOCUST_FILE=locustfile.py
FLASK_HOST=127.0.0.1:5000
FASTAPI_HOST=127.0.0.1:8000
NUM_WORKERS := 1

typecheck:
	poetry run mypy --strict --ignore-missing-imports comparison

test:
	poetry run pytest tests -s -v

fastapi:
	poetry run uvicorn comparison.main_fastapi:app --workers $(NUM_WORKERS) --port 8000

flask:
	poetry run gunicorn comparison.main_flask:app --workers $(NUM_WORKERS) --bind $(FLASK_HOST) --timeout 600 --log-level debug

test-flask:
	poetry run locust --host=http://$(FLASK_HOST) --headless --users=500 --spawn-rate=50 --run-time=30s --csv=results/flask

test-fastapi:
	poetry run locust --host=http://$(FASTAPI_HOST) --headless --users=500 --spawn-rate=50 --run-time=30s --csv=results/fastapi
