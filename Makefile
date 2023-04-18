lint:
	pylint sanic_oauth
	pycodestyle sanic_oauth
	# mypy --ignore-missing-imports sanic_oauth
pytest:
	pytest tests