build_dev:
	docker-compose -f docker-compose.yml up --build
dev:
	docker-compose -f docker-compose.yml down
	docker-compose -f docker-compose.yml up
test:
	docker-compose -f docker-compose.yml run web pytest

