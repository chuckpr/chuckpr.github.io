.PHONY = stop-jupyter get-url
DIR    = $(CURDIR)
TAG    = $(shell basename $(PWD))
NAME   = $(shell basename $(PWD))-$(shell id -u)
PORT  ?= 8888

build-image: Dockerfile
	docker build -t $(TAG) . && touch $<

run-jupyter: build-image
	docker run --rm -d \
		-w $(PWD) \
		-v $(PWD):$(PWD) \
		-p $(PORT):$(PORT) \
		--name $(NAME) \
		$(TAG) bash -c "jupyter lab --port $(PORT)" && touch $@

get-url: run-jupyter
	docker exec $(NAME) jupyter notebook list | sed 's/0\.0\.0\.0/localhost/'

stop-jupyter:
	docker stop $(NAME) || echo "Already stopped."
	@rm -f run-jupyter
