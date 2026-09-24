# 인천시청역 한신더휴

QUV 참고 사이트의 메뉴 경로와 페이지 흐름을 기준으로 구성한 독립 정적 사이트입니다. 본문의 주요 정보는 이미지로 구성하고, 사이트 글꼴은 Noto Sans KR로 변경했습니다.

## 구성

- `/` 메인: 기존 히어로 아래 세대수·오픈일·바로가기, 온라인 방문예약과 입력폼, 지정된 이미지 여섯 장 순서
- `/info`, `/3`, `/4`, `/7`, `/5`, `/6`: 참고 사이트와 같은 메뉴 경로
- `/6`: 방문예약 전용 페이지. 이름·연락처·방문날짜·방문시간 입력
- `functions/api/interest.js`: 방문예약 정보를 통합 고객관리 API로 전달하는 Cloudflare Pages Function
- 통합관리 현장 식별자: `incheoncityhall-hanshin-thehue` (`visit` 유형)
- `generate_graphics.py`, `build.py`: 이미지와 HTML 재생성

## 배포 상태

Cloudflare Pages 프로젝트 `thehue-incheoncityhall-git`는 이 저장소 `main`을 자동 배포합니다. 맞춤 도메인은 `thehue-incheoncityhall.site`입니다. 방문예약 신청은 미리 접수하며, 방문날짜는 2026년 9월 28일부터 선택할 수 있습니다. 방문시간은 10:00~18:00 사이 30분 단위입니다.

통합 고객관리 `site-customer-admin`의 `management/sites.json`에 이 현장이 `visit` 유형으로 등록되어 있습니다. 예약은 이 사이트의 `/api/interest`에서 중앙 `/api/leads`로 전달됩니다. 고객 정보 열람과 삭제는 통합 관리자 화면에서 진행합니다.

## 개발 확인

`python build.py`로 HTML을 재생성합니다. `python -m http.server 4173`으로 정적 화면을 확인할 수 있지만, 정적 서버에서는 Pages Function이 작동하지 않습니다.

입지 지도는 위치 관계를 설명하기 위한 도식 이미지입니다. 실제 방문 주소와 교통 경로는 지도를 통해 확인해야 합니다. 이미지 속 안내 문구와 문의번호는 배포 전에 운영자가 최종 확인해야 합니다.
