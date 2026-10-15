# Skills

모든 항목은 `skills/<분류>/<이름>/SKILL.md`에 있다. 도구 사용 문서도 같은 경로 규칙을 사용하며, 별도 mcp 트리를 탐색하지 않는다.

```text
AGENTS.md
.agents/
scripts/
  list-skills.sh
  validate-skills.py
skills/
  SKILL.md
  engineering/
    README.md
    chrome-devtools/
      SKILL.md
      references/
        source.json
        tool-reference.md
        troubleshooting.md
        LICENSE.txt
  hospital/
    README.md
    patient-lookup/SKILL.md
    appointment-manage/SKILL.md
    visit-check-in/SKILL.md
    billing-lookup/SKILL.md
    contact-record/SKILL.md
```

시작 문서는 [skills/SKILL.md](skills/SKILL.md)다. 그 문서와 분류 폴더가 같은 디렉터리에 있으며, 선택한 항목의 SKILL.md를 읽고 그 안에서 안내한 참고 파일만 추가로 읽는다.

폴더별 항목은 [engineering](skills/engineering/README.md), [hospital](skills/hospital/README.md)에 있다. 분류 폴더 안에 스킬을 두고 README에서 각 SKILL.md를 안내하는 구성은 [참고 저장소](https://github.com/mattpocock/skills/tree/main/skills)를 따른다. `scripts/list-skills.sh`도 참고 저장소처럼 실제 SKILL.md 경로를 탐색하며 별도의 목록 데이터 파일을 유지하지 않는다.

```sh
bash scripts/list-skills.sh
python3 scripts/validate-skills.py
```

외부 출처·버전·해시·갱신 절차는 해당 항목의 references/source.json 한 곳에 둔다. 자체 스킬 변경 이력은 Git으로 관리한다. 루트에 별도의 lock이나 업데이트 문서를 두지 않는다.

Chrome DevTools 항목은 연결된 MCP 서버를 사용하는 공식 문서다. 서버 제공·자동 설치를 뜻하지 않는다. 병원 업무 스킬은 특정 서비스 설정 규격이나 특정 MCP를 요구하지 않고 실행 환경에서 제공하는 권한·접속 정보·도구를 사용한다.

.agents/는 저장소 유지보수 규칙이다. 서비스의 설정·인증·캐시·문서 공급 구현은 이 저장소에 포함하지 않는다. 실제 업무 검증 완료를 뜻하지 않으며 자체 문서에 별도 공개 재배포 라이선스를 부여하지 않았다.
