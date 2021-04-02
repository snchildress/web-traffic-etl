IMAGE_TAG="web-traffic-etl"

.PHONY: all
all: build

.PHONY: build
build:
	docker build --tag ${IMAGE_TAG} .

.PHONY: run
run:
	make build && docker run -it ${IMAGE_TAG}
