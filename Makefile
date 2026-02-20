URL = http://localhost:5000

# Start the full demo and open the browser
demo:
	@echo "Launching Sentinel C2 at $(URL)..."
	@# The '-' tells make to ignore errors if the browser fails to open
	-@if command -v explorer.exe > /dev/null; then explorer.exe $(URL); \
	elif command -v open > /dev/null; then open $(URL); \
	elif command -v xdg-open > /dev/null; then xdg-open $(URL); fi
	docker exec -it sentinel_sentinel_1 bash -c "python3 app/web_control.py & sentinel python3 tests/mod_simulator.py"

# Quick command just to open the UI if it's already running
open:
	-@if command -v explorer.exe > /dev/null; then explorer.exe $(URL); \
	elif command -v open > /dev/null; then open $(URL); \
	elif command -v xdg-open > /dev/null; then xdg-open $(URL); fi

rebuild:
	docker-compose down
	docker-compose up -d --build

start:
	docker-compose up -d
	
clean:
	docker-compose down --volumes --remove-orphans

bash:
	docker exec -it sentinel_sentinel_1 /bin/bash