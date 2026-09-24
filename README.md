# 인천시청역 한신더휴

QUV 참고 사이트의 메뉴 경로와 페이지 흐름을 기준으로 구성한 독립 정적 사이트입니다. 본문의 주요 정보는 이미지로 구성하고, 사이트 글꼴은 Noto Sans KR로 변경했습니다.

## 구성

- `/` 메인: 전체 화면 히어로, 사업개요·입지환경·프리미엄·브랜드·오시는길 이미지, 관심등록
- `/info`, `/3`, `/4`, `/7`, `/5`, `/6`: 참고 사이트와 같은 메뉴 경로
- `functions/api/interest.js`: 관심등록 Cloudflare Pages Function
- `schema.sql`: 비공개 D1 데이터베이스 테이블
- `generate_graphics.py`, `build.py`: 이미지와 HTML 재생성

## 배포 상태

Cloudflare Pages의 GitHub 연동 프로젝트 이름은 `thehue-incheoncityhall-git`입니다. `main` 변경 시 자동 배포를 사용합니다.

## 배포 준비

1. Cloudflare Pages에서 이 저장소의 `main`을 연결하고, 빌드 명령은 비우고 빌드 출력 디렉터리는 `.`으로 지정합니다. Pages가 `functions/` 디렉터리를 인식해야 합니다.
2. D1 데이터베이스를 생성해 `schema.sql`을 적용하고, Pages 프로젝트의 프로덕션 D1 바인딩 이름을 `INTEREST_DB`로 지정합니다. 미연결 상태에서는 접수 API가 503을 반환하며 등록 성공으로 표시하지 않습니다.
3. 사용자 소유 도메인 `thehue-incheoncityhall.site`를 Pages 맞춤 도메인으로 연결하고, Pages의 정상 응답과 `/api/interest` 접수 흐름을 실제로 확인합니다.
4. 고객 정보 열람 권한과 보존·삭제 절차를 운영 환경에서 정한 뒤 접수를 공개합니다. D1 데이터를 공개 API로 조회하는 기능은 제공하지 않습니다.

## 개발 확인

`python build.py`로 HTML을 재생성합니다. `python -m http.server 4173`으로 정적 화면을 확인할 수 있지만, 정적 서버에서는 Pages Function이 작동하지 않습니다.

입지 지도는 위치 관계를 설명하기 위한 도식 이미지입니다. 실제 방문 주소와 교통 경로는 지도를 통해 확인해야 합니다. 이미지 속 안내 문구와 문의번호는 배포 전에 운영자가 최종 확인해야 합니다.
