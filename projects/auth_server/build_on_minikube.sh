#!/bin/bash

# .version 파일이 있는지 확인하고, 없으면 0으로 초기화
if [ ! -f .version ]; then
  echo 0 > .version
fi

# .version에서 버전 읽기
version=$(cat .version)

# 버전 업데이트 (하나 증가시키기)
new_version=$((version + 1))
echo $new_version > .version


echo -e "auth_server를 빌드합니다."
eval "$(minikube docker-env)" && docker build -t auth-server:latest .
echo -e "auth_server를 빌드가 완료되었습니다."