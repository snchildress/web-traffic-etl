IMAGE_TAG="web-traffic-etl"

.PHONY: all
all: build

.PHONY: build
build:
	docker build --tag ${IMAGE_TAG} .

.PHONY: run
run:
	make build && docker run ${IMAGE_TAG}

.PHONY: test
test:
	make build && docker run ${IMAGE_TAG} sh -c "python -m unittest"
