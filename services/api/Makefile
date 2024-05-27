
build_base:

	docker build --no-cache -t api_base:latest -f base.dockerfile .

build_base_arm:

	docker build --no-cache -t api_base:latest -f base.arm.dockerfile .

build_service:

	tar -hczvf src.tar.gz src

	docker build --no-cache -t api:latest -f service.dockerfile .

	rm src.tar.gz