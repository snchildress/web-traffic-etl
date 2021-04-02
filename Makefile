IMAGE_TAG="web-traffic-etl:latest"

.PHONY: all
all: build

.PHONY: build
build:
	docker build --tag ${IMAGE_TAG} . \
		&& make clean

.PHONY: clean
clean:
	docker container prune -f \
		&& docker image prune -f

.PHONY: run
run:
	make build \
		&& docker run ${IMAGE_TAG}

.PHONY: test
test:
	make build \
		&& docker run ${IMAGE_TAG} sh -c "python -m unittest"
