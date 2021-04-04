IMAGE_TAG="web-traffic-etl:latest"

.PHONY: all
all: build

.PHONY: build
build:
	mkdir -p output \
		&& docker build --tag ${IMAGE_TAG} . \
		&& make clean

.PHONY: clean
clean:
	docker container prune -f \
		&& docker image prune -f

.PHONY: run
run:
	make build \
		&& docker run \
			-v $$(pwd)/output:/usr/src/app/output \
			-it ${IMAGE_TAG}

.PHONY: test
test:
	make build \
		&& docker run \
			-it ${IMAGE_TAG} \
			sh -c "python -m unittest" 
