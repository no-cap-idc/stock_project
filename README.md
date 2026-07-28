# 📊 Daily Stock Briefing Kakao Alarm System (`stock_project`)

> **GitHub Actions와 KakaoTalk Open API를 활용한 Serverless 자동 주식 알림 파이프라인**

[![Daily Stock Kakao Alarm](https://github.com/no-cap-idc/stock_project/actions/workflows/stock_alarm.yml/badge.svg)](https://github.com/no-cap-idc/stock_project/actions/workflows/stock_alarm.yml)
![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 📌 1. 프로젝트 개요 (Overview)

매일 장 시작 전(08:30)과 장 마감 후(15:40)에 **주요 시장 지수(코스피/코스닥/나스닥)**, **개인 보유 종목의 평단 대비 실시간 수익률**, 그리고 **Google News 최신 헤드라인**을 수집하여 카카오톡 나에게 보내기 메시지로 자동 전송하는 클라우드 자동화 프로젝트입니다.

* **운영 비용 $0**: 별도의 24시간 개인 서버나 NAS 구축 없이 **GitHub Actions**로 동작.
* **보안 준수 (Security)**: Public 저장소에 코드를 공개하더라도 API Access Token 및 개인 금융 정보가 노출되지 않도록 **GitHub Secrets** 및 환경변수 주입 적용.

---

## 🛠️ 2. 기술 스택 (Tech Stack)

| 구분 | 기술 스택 | 설명 |
| :--- | :--- | :--- |
| **Language** | `Python 3.10` | 메인 데이터 수집 및 알림 로직 작성 |
| **Automation** | `GitHub Actions` | Serverless Cron 기반 스케줄링 및 CI/CD 파이프라인 |
| **Data Scraping** | `yfinance`, `BeautifulSoup4` | 주가/지수 시세 파싱 및 구글 뉴스 RSS 웹 크롤링 |
| **API Integration** | `Kakao REST API` | 카카오톡 나에게 보내기 API (`talk/memo/default/send`) |
| **Security** | `GitHub Repository Secrets` | Access Token 암호화 관리 |

---

## 🏗️ 3. 시스템 아키텍처 (Architecture)
