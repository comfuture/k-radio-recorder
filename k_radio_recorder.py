#!/usr/bin/env python3
# ffmpeg는 별도 설치가 필요합니다.
# macOS: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg
# Windows: https://ffmpeg.org/download.html 참고

import argparse
import httpx
import subprocess
import sys
from datetime import datetime, timedelta
import time
import asyncio
import json

RADIO_STATIONS_JSON = "radio_stations.json"


async def get_kbs_stream_url(channel_code):
    url = f"https://cfpwwwapi.kbs.co.kr/api/v1/landing/live/channel_code/{channel_code}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        if resp.status_code != 200:
            raise Exception("KBS API 호출 실패")
        data = resp.json()
        return data["channel_item"][0]["service_url"]


async def get_mbc_stream_url(channel_code):
    url = f"https://sminiplay.imbc.com/aacplay.ashx?agent=webapp&channel={channel_code}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        if resp.status_code != 200:
            raise Exception("MBC API 호출 실패")
        return resp.text.strip()


async def get_sbs_stream_url(channel_code):
    if channel_code == "lovefm":
        url = "https://apis.sbs.co.kr/play-api/1.0/livestream/lovepc/lovefm?protocol=hls&ssl=Y"
    elif channel_code == "powerfm":
        url = "https://apis.sbs.co.kr/play-api/1.0/livestream/powerpc/powerfm?protocol=hls&ssl=Y"
    else:
        raise Exception("SBS 채널코드 오류")
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        if resp.status_code != 200:
            raise Exception("SBS API 호출 실패")
        data = resp.json()
        return data["onair"]["source"]["mediasource"]["mediaurl"]


async def get_stream_url(station, channel):
    if station == "kbs":
        return await get_kbs_stream_url(channel)
    elif station == "mbc":
        return await get_mbc_stream_url(channel)
    elif station == "sbs":
        return await get_sbs_stream_url(channel)
    else:
        raise Exception("지원하지 않는 방송국")


def load_radio_stations():
    with open(RADIO_STATIONS_JSON, encoding="utf-8") as f:
        return json.load(f)


def list_radio_stations():
    stations = load_radio_stations()
    print("라디오 스테이션 목록:")
    for idx, s in enumerate(stations, 1):
        print(f"{idx}. {s['name']}")
    return stations


def select_station():
    stations = list_radio_stations()
    while True:
        try:
            sel = int(input("스테이션 번호 선택: "))
            if 1 <= sel <= len(stations):
                return stations[sel - 1]
            else:
                print("잘못된 번호입니다.")
        except ValueError:
            print("숫자를 입력하세요.")


def make_output_filename(station, channel, format):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    ext = format.lower() if format else "mp3"
    return f"{station}_{channel}_{now}.{ext}"


def record_stream(station, channel, output=None, duration=None, format=None):
    print(f"[{station.upper()}] {channel} 스트림 URL 획득 중...")
    stream_url = asyncio.run(get_stream_url(station, channel))
    print(f"스트림 URL: {stream_url}")

    # 기본 포맷을 mp3로 설정
    if format is None:
        format = "mp3"

    # 파일명 자동 생성
    if not output:
        output = make_output_filename(station, channel, format)

    # ffmpeg 명령어 구성
    ffmpeg_cmd = ["ffmpeg", "-y", "-i", stream_url]

    # 포맷에 따른 인코딩 설정
    if format.lower() == "mp3":
        ffmpeg_cmd.extend(["-c:a", "libmp3lame"])
    elif format.lower() == "aac":
        ffmpeg_cmd.extend(["-c:a", "aac"])
    elif format.lower() == "wav":
        ffmpeg_cmd.extend(["-c:a", "pcm_s16le"])
    else:
        ffmpeg_cmd.extend(["-c:a", "copy"])

    if duration:
        ffmpeg_cmd.extend(["-t", str(duration)])

    ffmpeg_cmd.append(output)

    print(f"녹음 시작: {output} (포맷: {format})")
    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print("녹음 완료")
    except subprocess.CalledProcessError:
        print("ffmpeg 실행 오류")
        sys.exit(1)


def record_stream_by_station(station, duration=None, format=None):
    url = station["url"]
    name = station["name"]
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    ext = format.lower() if format else "mp3"
    output = f"{name}_{now}.{ext}"
    ffmpeg_cmd = ["ffmpeg", "-y", "-i", url]
    if format is None:
        format = "mp3"
    if format.lower() == "mp3":
        ffmpeg_cmd.extend(["-c:a", "libmp3lame"])
    elif format.lower() == "aac":
        ffmpeg_cmd.extend(["-c:a", "aac"])
    elif format.lower() == "wav":
        ffmpeg_cmd.extend(["-c:a", "pcm_s16le"])
    else:
        ffmpeg_cmd.extend(["-c:a", "copy"])
    if duration:
        ffmpeg_cmd.extend(["-t", str(duration)])
    ffmpeg_cmd.append(output)
    print(f"녹음 시작: {output} (포맷: {format})")
    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print("녹음 완료")
    except subprocess.CalledProcessError:
        print("ffmpeg 실행 오류")
        sys.exit(1)


def schedule_record_by_station(station, start_time, duration, format=None):
    now = datetime.now()
    target = datetime.strptime(start_time, "%H:%M")
    target = target.replace(year=now.year, month=now.month, day=now.day)
    if target < now:
        target += timedelta(days=1)
    wait_sec = (target - now).total_seconds()
    print(f"{start_time}까지 {int(wait_sec)}초 대기 후 녹음 시작")
    time.sleep(wait_sec)
    record_stream_by_station(station, duration=duration, format=format)


def interactive_mode():
    while True:
        print("\n==== 대한민국 라디오 방송 녹음기 ====")
        print("1. 라디오 스테이션 목록 보기")
        print("2. 녹음 시작")
        print("3. 예약 녹음")
        print("4. 종료")
        choice = input("메뉴 선택 (1/2/3/4): ").strip()
        if choice == "1":
            list_radio_stations()
        elif choice == "2":
            station = select_station()
            format = (
                input("출력 포맷 입력 (mp3/aac/wav, 엔터시 mp3): ").strip().lower()
                or "mp3"
            )
            duration = input("녹음 시간(초, 엔터시 무제한): ").strip()
            duration = int(duration) if duration else None
            record_stream_by_station(station, duration=duration, format=format)
        elif choice == "3":
            station = select_station()
            start_time = input("시작 시각 입력 (HH:MM): ").strip()
            duration = int(input("녹음 시간(초): ").strip())
            format = (
                input("출력 포맷 입력 (mp3/aac/wav, 엔터시 mp3): ").strip().lower()
                or "mp3"
            )
            schedule_record_by_station(station, start_time, duration, format=format)
        elif choice == "4":
            print("종료합니다.")
            break
        else:
            print("잘못된 입력입니다.")


def main():
    parser = argparse.ArgumentParser(description="대한민국 라디오 방송 스트림 녹음 CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list", help="라디오 스테이션 목록 출력")

    parser_record = subparsers.add_parser("record", help="녹음 시작")
    parser_record.add_argument(
        "--station", type=int, help="스테이션 번호 (list 명령으로 확인)"
    )
    parser_record.add_argument("--duration", type=int, help="녹음 시간(초)")
    parser_record.add_argument(
        "--format", help="출력 포맷 (예: mp3, aac, wav). 기본값: mp3"
    )

    parser_schedule = subparsers.add_parser("schedule", help="예약 녹음")
    parser_schedule.add_argument(
        "--station", type=int, help="스테이션 번호 (list 명령으로 확인)"
    )
    parser_schedule.add_argument("--time", required=True, help="시작 시각(HH:MM)")
    parser_schedule.add_argument(
        "--duration", type=int, required=True, help="녹음 시간(초)"
    )
    parser_schedule.add_argument(
        "--format", help="출력 포맷 (예: mp3, aac, wav). 기본값: mp3"
    )

    args = parser.parse_args()

    if args.command == "list":
        list_radio_stations()
    elif args.command == "record":
        stations = load_radio_stations()
        if args.station is None or not (1 <= args.station <= len(stations)):
            print("--station 인자에 올바른 번호를 입력하세요. (list 명령으로 확인)")
            sys.exit(1)
        station = stations[args.station - 1]
        record_stream_by_station(
            station,
            duration=args.duration,
            format=args.format,
        )
    elif args.command == "schedule":
        stations = load_radio_stations()
        if args.station is None or not (1 <= args.station <= len(stations)):
            print("--station 인자에 올바른 번호를 입력하세요. (list 명령으로 확인)")
            sys.exit(1)
        station = stations[args.station - 1]
        schedule_record_by_station(
            station,
            start_time=args.time,
            duration=args.duration,
            format=args.format,
        )
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
