# 인천시청역 한신더휴

QUV 참고 사이트의 메뉴 경로와 페이지 흐름을 기준으로 구성한 독립 정적 사이트입니다. 본문의 주요 정보는 이미지로 구성하고, 사이트 글꼴은 Noto Sans KR로 변경했습니다.

## 구성

- `/` 메인: 전체 화면 히어로, 사업개요·입지환경·프리미엄·브랜드·오시는길 이미지, 관심등록
- `/info`, `/3`, `/4`, `/7`, `/5`, `/6`: 참고 사이트와 같은 메뉴 경로
- `functions/api/interest.js`: 통합 고객관리 접수 API로 전달하는 Cloudflare Pages Function
- 통합관리 현장 식별자: `incheoncityhall-hanshin-thehue`
- `generate_graphics.py`, `build.py`: 이미지와 HTML 재생성

## 배포 상태

Cloudflare Pages의 GitHub 연동 프로젝트 이름은 `thehue-incheoncityhall-git`입니다. `main` 변경 시 자동 배포되도록 구성되어 있습니다. 자동 배포 동작은 Cloudflare 배포 기록으로 검증합니다.

## 배포 준비

1. Cloudflare Pages에서 이 저장소의 `main`을 연결하고, 빌드 명령은 비우고 빌드 출력 디렉터리는 `.`으로 지정합니다. Pages가 `functions/` 디렉터리를 인식해야 합니다.
2. 통합 고객관리 `site-customer-admin`의 `management/sites.json`에 이 현장이 활성 상태로 등록되어 있어야 합니다. 접수는 사이트의 `/api/interest`를 거쳐 중앙 `/api/leads`로 전달됩니다.
3. 맞춤 도메인은 `thehue-incheoncityhall.site`이며, 중앙 접수와 관리자 목록의 실제 저장 결과를 확인합니다.
4. 고객 정보 열람과 삭제는 통합 고객관리 관리자 화면에서 진행합니다. 이 사이트에는 별도 고객 데이터베이스를 두지 않습니다.

## 개발 확인

`python build.py`로 HTML을 재생성합니다. `python -m http.server 4173`으로 정적 화면을 확인할 수 있지만, 정적 서버에서는 Pages Function이 작동하지 않습니다.

입지 지도는 위치 관계를 설명하기 위한 도식 이미지입니다. 실제 방문 주소와 교통 경로는 지도를 통해 확인해야 합니다. 이미지 속 안내 문구와 문의번호는 배포 전에 운영자가 최종 확인해야 합니다.
