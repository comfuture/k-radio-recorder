# 대한민국 라디오 방송 스트림 녹음 CLI (k-radio-recorder)

## 소개

`k-radio-recorder`는 대한민국 주요 라디오 방송(KBS, MBC, SBS 등)의 인터넷 스트림을 손쉽게 녹음할 수 있는 Python 기반 CLI 도구입니다. 방송국/채널 선택, 녹음 파일명 지정, 예약 녹음 등 다양한 기능을 제공합니다.

---

## 주요 기능
- 라디오 스테이션 목록을 번호와 함께 조회 (radio_stations.json 기반)
- 번호 선택만으로 간편하게 녹음/예약녹음 가능
- 다양한 출력 포맷 지원 (MP3, AAC, WAV)
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

### 2. 의존성 설치
```sh
uv venv --python 3.12
source .venv/bin/activate
uv sync
```

---

## 사용법

### 1. 라디오 스테이션 목록 확인
```sh
python k_radio_recorder.py list
```
- 번호와 함께 스테이션 목록이 출력됩니다.

### 2. 녹음 시작 (번호로 선택)
```sh
python k_radio_recorder.py record --station 5 --format mp3 --duration 60
```
- `--station`: 스테이션 번호 (list 명령으로 확인)
- `--format`: (선택) 출력 포맷(mp3, aac, wav). 기본값: mp3
- `--duration`: (선택) 녹음 시간(초)
- **저장 파일명은 자동으로 `스테이션이름_날짜시간.확장자` 형식으로 생성됩니다.**

### 3. 예약 녹음 (번호로 선택)
```sh
python k_radio_recorder.py schedule --station 2 --time 08:00 --duration 3600 --format aac
```
- `--station`: 스테이션 번호 (list 명령으로 확인)
- `--time`: 시작 시각 (HH:MM)
- `--duration`: 녹음 시간(초)
- `--format`: (선택) 출력 포맷(mp3, aac, wav). 기본값: mp3
- **저장 파일명은 자동으로 생성됩니다.**

### 4. 대화형 모드 (번호로 선택)
명령 인자 없이 실행하면 대화형 메뉴가 제공되며, 스테이션 번호를 선택해 녹음/예약녹음이 가능합니다.
```sh
python k_radio_recorder.py
```
- 스테이션 목록이 번호와 함께 출력되고, 번호를 입력해 녹음/예약녹음을 진행합니다.
- 출력 포맷(mp3/aac/wav)과 녹음 시간(초)도 입력받을 수 있습니다.

---

## radio_stations.json

라디오 스테이션 정보는 `radio_stations.json` 파일에 저장되어 있으며, 방송국/채널 코드 대신 번호로 선택할 수 있습니다.

---

## 저장 파일명 규칙
- 파일명은 `스테이션이름_YYYYMMDD_HHMMSS.확장자` 형식으로 자동 생성됩니다.
- 예시: `MBC FM4U_20250604_164046.mp3`

---

## 지원 출력 포맷

### 오디오 포맷 옵션
- **mp3** (기본값): MP3 형식으로 저장 (libmp3lame 인코더 사용)
- **aac**: AAC 형식으로 저장 (aac 인코더 사용)
- **wav**: WAV 형식으로 저장 (pcm_s16le 인코더 사용)

### 포맷 사용 예시
```sh
python k_radio_recorder.py record --station 1 --format mp3
python k_radio_recorder.py record --station 2 --format aac --duration 120
python k_radio_recorder.py schedule --station 3 --time 09:00 --duration 1800 --format wav
```

### 대화형 모드에서의 포맷 선택
대화형 모드에서는 다음과 같이 포맷을 선택할 수 있습니다:
```
출력 포맷 입력 (mp3/aac/wav, 엔터시 mp3): aac
```

---

## 참고 및 주의사항
- 스트림 URL은 일정 시간 후 만료될 수 있으므로, 녹음 직전 자동 갱신됩니다.
- ffmpeg가 시스템에 설치되어 있어야 정상 동작합니다.
- 방송사 정책 및 저작권을 준수하여 사용하세요.

---

## 라이선스
오픈소스 라이선스 및 각 방송사 정책을 준수합니다.
