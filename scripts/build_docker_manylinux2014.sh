#!/bin/bash
set -e
set -u

docker run -it -d --name manylinux2014 quay.io/pypa/manylinux2014_$(uname -m) &&
(cd .. && tar czf pyadms.tgz pyadms && docker cp pyadms.tgz manylinux2014:/root/) &&
docker exec manylinux2014 bash -c "git config --global --add safe.directory /root/pyadms"
docker exec manylinux2014 bash -c "cd /root && tar xzf pyadms.tgz";
docker exec manylinux2014 bash -c "cd /root/pyadms && bash scripts/build_manylinux2014.sh";
(for i in $(docker exec manylinux2014 bash -c "ls /root/pyadms/*.whl"); do docker cp manylinux2014:${i} .; done)
docker stop manylinux2014

