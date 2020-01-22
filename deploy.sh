#!/usr/bin/env sh
IDENTITY_FILE="$HOME/.ssh/wps12th.pem"
HOST="ubuntu@54.180.159.197"
ORIGIN_SOURCE="$HOME/projects/instagram/"
DEST_SOURCE="/home/ubuntu/projects/instagram"
SSH_CMD="ssh -i ${IDENTITY_FILE} ${HOST}"

# pip freeze
echo "pip freeze"
"$HOME"/.pyenv/versions/3.7.5/bin/pip freeze > "$HOME"/projects/instagram/requirements.txt

# 기존 폴더 삭제
echo "기존 폴더 삭제"
${SSH_CMD} sudo rm -rf ${DEST_SOURCE}

# 로컬에 있는 파일 업로드
echo "로컬 파일 업로드"
scp -q -i "${IDENTITY_FILE}" -r "${ORIGIN_SOURCE}" ${HOST}:${DEST_SOURCE}


# pip install
echo "pip install"
${SSH_CMD} pip3 install -q -r /home/ubuntu/projects/instagram/requirements.txt

# 실행중이던 screen 종료
${SSH_CMD} -C 'screen -X -S runserver quit'

# screen 실행
${SSH_CMD} -C 'screen -S runserver -d -m'

# 실행중인 세션에 명령어 전달
${SSH_CMD} -C "screen -r runserver -X stuff $'sudo python3 /home/ubuntu/projects/instagram/app/manage.py runserver 0:80\n'"

echo "배포 완료!"
