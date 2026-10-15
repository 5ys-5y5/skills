# Skills

특정 서비스의 설정 규격에 의존하지 않는 업무 스킬과 외부 MCP 사용 문서 모음이다. 업무 스킬은 무엇을 확인하고 처리할지 설명한다. 접속 정보·권한·인증·도구 연결은 호출한 에이전트가 자신의 환경에서 해결한다.

```text
AGENTS.md
.agents/
  writing-skills.md
  invocation.md
skill.md
skills/
  hospital/
    patient-lookup/SKILL.md
    appointment-manage/SKILL.md
    visit-check-in/SKILL.md
    billing-lookup/SKILL.md
    contact-record/SKILL.md
mcp/
  chrome-devtools/
    README.md
    SKILL.md
    references/
external-skills.lock.json
UPDATES.md
```

## 업무 스킬

[skill.md](skill.md)에서 필요한 경로를 찾고 해당 폴더의 SKILL.md를 읽는다. 이름·description으로 선택할 수 있으며 특정 Skill 호출 도구나 설정 API가 존재한다고 가정하지 않는다. 추가 참고 파일은 선택한 문서가 해당 작업에 필요하다고 안내할 때만 읽는다.

병원 업무는 예시 도메인이다. 스킬은 환자 조회, 예약, 접수, 수납 조회, 상담 기록의 업무 지식을 담으며 병원별 JSON schema나 설정 파일 위치를 정의하지 않는다. 실행 환경마다 접속 정보와 권한을 해석하는 책임이 있다. 스킬 문서가 자격증명이나 권한을 만들어 주지는 않는다.

## MCP는 연결된 서버가 필요하다

[Chrome DevTools MCP 안내](mcp/chrome-devtools/README.md)는 외부 MCP 서버를 사용하기 위한 공식 문서다. 서버 구현이나 일반 업무 스킬과 구분해 `mcp/`에 둔다. 읽거나 설치하는 것만으로 MCP 서버가 실행되거나 브라우저가 연결되지 않는다.

호출한 에이전트가 해당 서버를 사용할 의사와 권한이 있고 실제 도구 연결을 사용할 수 있을 때만 적용한다. 도구가 없으면 문서의 도구를 호출 가능한 것으로 취급하거나 서버를 임의로 만들지 않는다. 설치·시작·재설정이 필요하면 별도 작업으로 다룬다.

## 유지보수와 출처

AGENTS.md와 .agents/는 이 저장소를 편집하는 에이전트의 유지보수 지침이다. 실행 서비스의 설정 계약이나 모든 에이전트가 자동으로 인식하는 표준은 아니다. 특정 에이전트 제품 전용 메타데이터가 필요하면 그 제품이 지원하는 형식에 별도로 연결한다.

공식 MCP 문서는 원문과 라이선스를 보존한다. [출처·버전·해시 기록](external-skills.lock.json)과 [갱신 절차](UPDATES.md)를 참고한다. 자체 스킬에는 별도 공개 재배포 라이선스를 부여하지 않았다.

이 저장소에는 서비스 설정 예시·소비 서비스 API 계약·자격증명·실행 서버·npm 실행 라이브러리를 두지 않는다. 문서 폴더만으로 문서 배포·캐시·인증 또는 실제 CRM 실행이 구현되는 것은 아니다. 업무 샘플은 실제 CRM 검증 완료를 뜻하지 않는다.
