# 대한민국 라디오 방송 스트림 녹음 CLI (k-radio-recorder)

## 소개

`k-radio-recorder`는 대한민국 주요 라디오 방송(KBS, MBC, SBS 등)의 인터넷 스트림을 손쉽게 녹음할 수 있는 Python 기반 CLI 도구입니다. 방송국/채널 선택, 녹음 파일명 지정, 예약 녹음 등 다양한 기능을 제공합니다.

---

## 주요 기능
- 방송국/채널 목록 조회
- 스트림 URL 자동 획득 및 ffmpeg로 녹음
- 녹음 파일명, 저장 경로 지정
- 예약 녹음(시작 시각, 녹음 시간 지정)
- 대화형 모드 지원(명령 인자 없이 실행 시)

---

## 설치 및 준비

### 1. Python 및 ffmpeg 설치
- Python 3.8 이상 필요
- ffmpeg 설치 필요
  - macOS: `brew install ffmpeg`
  - Ubuntu: `sudo apt install ffmpeg`
  - Windows: [ffmpeg 공식 다운로드](https://ffmpeg.org/download.html)

### 2. 의존성 설치 (uv 사용 권장)
```sh
uv venv --python 3.12
source .venv/bin/activate
uv pip install -r requirements.txt
```
또는 pyproject.toml 기반 설치:
```sh
uv pip install -r requirements.txt
```

---

## 사용법

### 1. 방송국/채널 목록 확인
```sh
python k_radio_recorder.py list
```

### 2. 녹음 시작
```sh
python k_radio_recorder.py record --station kbs --channel 21 --output myradio.mp3
```
- `--station`: 방송국 코드 (kbs, mbc, sbs)
- `--channel`: 채널 코드 (예: 21, sfm, lovefm 등)
- `--output`: 저장할 파일명
- `--duration`: (선택) 녹음 시간(초)

### 3. 예약 녹음
```sh
python k_radio_recorder.py schedule --station sbs --channel powerfm --output myradio.aac --time 08:00 --duration 3600
```
- `--time`: 시작 시각 (HH:MM)
- `--duration`: 녹음 시간(초)

### 4. 대화형 모드
명령 인자 없이 실행하면 대화형 메뉴가 제공됩니다.
```sh
python k_radio_recorder.py
```

---

## 지원 방송국/채널 예시
- KBS: 21(제1라디오), 24(1FM), 25(2FM)
- MBC: sfm(표준FM), mfm(FM4U)
- SBS: lovefm(러브FM), powerfm(파워FM)

---

## 참고 및 주의사항
- 스트림 URL은 일정 시간 후 만료될 수 있으므로, 녹음 직전 자동 갱신됩니다.
- ffmpeg가 시스템에 설치되어 있어야 정상 동작합니다.
- 방송사 정책 및 저작권을 준수하여 사용하세요.

---

## 라이선스
오픈소스 라이선스 및 각 방송사 정책을 준수합니다.
