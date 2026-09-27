# discovery-service-recording — 실행 예시

실행 대상: 크루 매거진 커뮤니티 앱 (2026-09-18 실행, 원본: `try_project_discovery_2/planner/260918-1754-crew-magazine-community-app/research/screenshots/`)

## 호출

당시에는 `planner(service-recording)` 커밋 접두어로 기록되었다. 아래 호출은 현재 명령 형식으로 다시 적은 것이다(재구성).

1차 실행에서는 references.md에 있는 서비스 5개를 모두 캡처했다. `Target`의 기본값이 all이다.

```
/dk-discovery-bundle:discovery-service-recording
```

그 뒤에 캡처 품질 규칙을 추가하고(커밋 57535db), 문토와 Meetup 두 서비스만 다시 캡처했다. trial-notes에 "`Target: 문토, Meetup`처럼 쉼표 구분 목록으로 해석해 두 서비스만 순차 실행"했다고 적혀 있다.

```
/dk-discovery-bundle:discovery-service-recording Target: 문토, Meetup
```

## Input

- `research/references.md`: 캡처할 서비스 5개(문토, 소모임, Meetup, 오운완, 트레바리)와 각 URL
- `research/handoff.json`: research 단계의 결과. 이 단계가 `recorded_services`를 덧붙여 갱신한다.
- 서비스당 캡처 상한 `MaxShots`는 기본값 8을 썼다.

## Output

```
research/
├── screenshots/
│   ├── munto/      landing.png, moim-club.png, entry-login.png, socialing-detail.png, shots.md
│   ├── somoim/     landing.png, groups-rcmd.png, group-detail.png, entry-appdownload.png, shots.md
│   ├── meetup/     landing.png, find-groups.png, group-detail.png, entry-register.png, shots.md
│   ├── ohwoonwan/  external-01-appstore.png, external-02-playstore.png, shots.md
│   └── trevari/    landing.png, clubs-list.png, club-detail.png, shots.md
├── analysis/*.md          # 각 파일 끝에 "스크린샷" 섹션(shots.md 링크) 추가
├── references.md          # 문토 URL 정정 메모 추가
├── handoff.json           # recorded_services 5개 추가
└── recording-results.tsv  # 서비스별 기록 로그
```

### 서비스별로 캡처한 화면 (shots.md 기준)

| 서비스 | case | 장수 | 점수 | 캡처한 화면 |
|--------|------|------|------|------------|
| 문토 | 웹 | 4 | 75 | 모임 추천 탭 메인 / 클럽 탭 카드 리스트 / 라운지 접근 시 뜨는 로그인 화면 / 소셜링 상세(스피치 모임) 전체 페이지 |
| 소모임 | 웹 | 4 | 100 | 지역 선택과 카테고리가 있는 홈 / 추천 모임 리스트 / 모임 상세('TRASH BOX') 전체 페이지 / 앱 다운로드 유도 화면 |
| Meetup | 웹 | 4 | 100 | 메인 히어로와 이벤트 카드 / 그룹 탐색(카테고리 탭, 그룹 카드) / 그룹 상세(Seoul Hiking Nature) 전체 페이지 / 회원가입 |
| 오운완 | 외부(앱 전용) | 2 | 75 | App Store KR 상세(앱 프리뷰 3장, 평점 3.8) / Google Play 상세 |
| 트레바리 | 웹 | 3 | 75 | 카테고리 내비와 큐레이션 배너가 있는 홈 / 클럽장 있는 클럽 리스트 / 클럽 상세(독서모임) 전체 페이지 |

점수는 "이 서비스를 모르는 사람이 이미지만 보고 파악할 수 있는가"를 네 가지 요소(서비스 정체, 진입 흐름, 핵심 기능, 콘텐츠 구조)로 채점한 것이다. 요소 하나당 25점이고, 75점 이상이면 통과다.

### shots.md 예시 — 소모임 (100점)

```markdown
# 소모임 — 화면 기록

캡처일: 2026-09-18
참조 URL: https://www.somoim.co.kr/
최종 URL: https://www.somoim.co.kr/ (리다이렉트 없음)
케이스: 웹 제공 (Case 1)
recording_score: 100/100

| 파일 | 화면 | 비고 |
| landing.png | 홈 — 지역 선택 + 카테고리 사이드바 + 모임 리스트 | |
| groups-rcmd.png | 추천 모임 리스트 | |
| group-detail.png | 모임 상세 (마포구 노래/보컬 'TRASH BOX') — 전체 페이지 | 소개·정모일정·운영진·멤버 33명·게시판/사진첩/채팅 탭·비슷한 모임 |
| entry-appdownload.png | 앱 다운로드 진입점 — 모임 만들기는 앱으로 유도 | 웹은 열람 전용, 개설·가입은 앱 |
```

### shots.md 예시 — 문토 (75점, 모자란 이유를 기록)

```markdown
최종 URL: https://www.munto.kr/ko/moim?type=recommend (루트 접속 시 리다이렉트 — references.md 정정 메모 반영)
recording_score: 75/100 (재채점 — 라운지 로그인 장벽 동일하여 유지)

| landing.png | 메인 — 모임 추천 탭 (기획전 배너 + 카테고리 아이콘 + 인기/취향 저격 소셜링 카드 리스트) | 재캡처: 뷰포트 1280x2000 줌아웃 — 히어로만 담기던 컷 폐기 |
…(생략)

## 미달 사유 (콘텐츠 구조)
라운지(멤버 피드)는 비로그인 접근 불가 → 콘텐츠 소비 화면 미확보. 4요소 중 3요소 충족(75)으로 종료 기준 통과.
```

### shots.md 예시 — 오운완 (웹이 없는 앱)

웹사이트가 없는 서비스는 앱스토어나 외부 글에서 화면을 찾아 캡처하고 출처를 적는다.

```markdown
케이스: 검색 캡처 (Case 2 — 앱 전용, 웹 미제공)
| external-01-appstore.png | App Store KR 상세 — 앱 프리뷰 3장(브랜드/모임 만들기·리스트/인증샷 피드), 평점 3.8(25개), 리뷰 2건 | https://apps.apple.com/kr/app/id6443483274 — 외부 저작물(Apple/개발사) |

## 기록
- 블로그/리뷰 캡처 검색 1회 — 앱 화면이 담긴 서드파티 글 미발견.
- letspl.me 프로젝트 페이지는 앱 화면 없음(모집글, 노출 제한 상태)이라 캡처 폐기.
```

### handoff.json에 추가된 부분 (발췌)

```json
"recorded_services": [
  { "name": "문토", "case": "web", "shots": 4, "recording_score": 75,
    "final_url": "https://www.munto.kr/ko/moim?type=recommend", "url_corrected": true,
    "recaptured": "2026-09-18 — landing·moim-club 뷰포트 1280x2000 줌아웃 재캡처 (캡처 품질 규칙), 점수 75 유지(라운지 로그인 장벽)" },
  { "name": "소모임", "case": "web", "shots": 4, "recording_score": 100, "url_corrected": false },
  …(생략)
],
"next_step": "project_discovery:hypothesize"
```

### recording-results.tsv (전문)

```
service    case  shots  recording_score  retries  note
munto      1     4      75               0        라운지 로그인 장벽 — 콘텐츠 피드 미확보
somoim     1     4      100              0        모임 상세가 웹에 완전 공개 — 4요소 전부 확보
meetup     1     4      100              0        그룹 상세 fullpage로 콘텐츠 구조 확보
ohwoonwan  2     2      75               0        앱 전용 — 스토어 프리뷰 2장, 서드파티 화면 미발견 (3~5장 기준 미달 기록)
trevari    1     3      75               0        로그인 404 — 진입점은 상세 신청 CTA로 갈음, 멤버 전용 콘텐츠 미확보
munto      1     4      75               0        재캡처 2장(landing·moim-club) — 뷰포트 1280x2000 줌아웃, 히어로 잘림 해소
meetup     1     4      100              0        재캡처 4장 — 쿠키 배너 Continue without accepting 클릭 후 전 화면 재촬영, 그룹 상세 fullPage
```

## 참고

- 1차 캡처에서는 문토 메인이 화면 위쪽 히어로만 잘려 찍혔고, Meetup은 쿠키 배너가 화면을 가렸다. 그래서 "뷰포트를 키우거나 전체 페이지로 찍고 잘린 컷은 버린다", "쿠키 배너는 동의하지 않는 버튼을 눌러 닫는다"는 규칙을 추가하고 두 서비스를 다시 찍었다. 다시 찍어도 점수는 그대로였다. trial-notes는 이 규칙이 점수가 아니라 같은 점수 안에서 이미지에 담기는 정보량을 늘렸다고 정리했다.
- 로그인해야 볼 수 있는 화면(문토 라운지, 트레바리 독후감)은 캡처하지 못한다. 이런 경우 점수가 75에 머무르며, 모자란 이유를 shots.md에 적고 넘어간다.
- 1차 실행 때 shots.md에는 문서 맨 위의 최종 URL 하나만 적게 되어 있었다. 그래서 다시 찍을 때 Meetup 그룹 상세의 주소를 검색으로 다시 찾아야 했다. 이후 컷마다 URL을 적도록 문서가 바뀌었다(커밋 06a040a).
