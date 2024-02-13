.DEFAULT_GOAL := main

main:
	cd src && python3 application.py
	find . -type d -name __pycache__ -exec rm -rf {} +

	
