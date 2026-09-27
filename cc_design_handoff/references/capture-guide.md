# 화면 캡처 가이드 — playwright 실전 규칙

(project_discovery의 service-recording에서 실전 검증된 규칙의 사본 — 이 폴더에서 자립)

## 도구 로딩

```
ToolSearch는 키워드 검색만으로 부족하다. 정확한 도구명으로 로딩:
ToolSearch("select:mcp__playwright__browser_navigate,mcp__playwright__browser_take_screenshot,mcp__playwright__browser_snapshot,mcp__playwright__browser_click,mcp__playwright__browser_resize,mcp__playwright__browser_close")
```

## 캡처 품질 규칙

```
줌아웃 — 내용이 파악될 정도로 찍는다:
  화면 상단 히어로만 담기고 실제 내용(리스트·피드·본문)이 잘려 있으면,
  뷰포트 확대(browser_resize) 또는 풀페이지 캡처로 다시 찍고 잘린 컷은 폐기한다.
  권장 뷰포트: 리스트·피드형 페이지는 1280×2000.
  세로가 짧은 페이지(가입 폼 등)는 원래 뷰포트(1280×720)로 복귀해 여백 과다를 피한다.

쿠키/동의 배너 — 내용을 가리면 캡처 전에 한 번 거부(Decline) 클릭:
  버튼 문구는 사이트마다 다르다 — "Decline", "거부", "Continue without accepting",
  "필수만 허용" 등 거부 계열을 찾는다.
  거부로 닫히지 않아 내용이 계속 가려지면, 그 상태를 shots.md 비고에 기록하고 넘어간다.
```

## 저장·기록 규칙

```
저장: browser_take_screenshot의 filename에 절대 경로를 주면 그 위치에 바로 저장된다.
  scale 파라미터는 기본값이 있어도 명시하는 것이 안전하다.

컷별 URL: shots.md 표에 캡처한 페이지의 URL을 컷마다 기록한다 —
  재캡처 시 같은 페이지를 다시 찾을 수 있어야 한다.

최종 URL: 참조 URL과 실제 렌더링 URL이 다른 경우가 흔하다 (리다이렉트·도메인 이전).
  최종 URL을 기록하고, 다르면 정정 메모를 남긴다.

부산물 정리: navigate/screenshot마다 repo 루트 .playwright-mcp/에 snapshot .yml과
  console .log가 쌓인다. 작업 종료 시 반드시 rm -rf .playwright-mcp/ —
  staged 전에 제거해야 repo가 오염되지 않는다.

세션 정리: 작업 완료 후 browser_close 호출.
```

## shots.md 템플릿

```markdown
# {사이트명} — 화면 기록

캡처일: {날짜} · 최종 URL: {실제 렌더링 URL}
우리 분위기와 닿는 점: {한 줄}

| 파일 | 화면 | URL | 비고 |
|------|------|-----|------|
| landing.png | 첫 화면 | ... | |
| article.png | 콘텐츠 상세 | ... | |
```
