.DEFAULT_GOAL := main

main:
	cd src && python3 main.py
	find . -type d -name __pycache__ -exec rm -rf {} +

	
