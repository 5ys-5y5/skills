# Skills

[Agent Skills 공식 규격](https://agentskills.io/specification)을 따르는 개인 스킬 저장소다. 자체 스킬과 외부 스킬의 본문·자료를 전용 포맷 변환 없이 제공한다. 개인 설정 전체 복원·MCP 자동 설치·전용 배포는 별도 요구사항이다.

## 표준 스킬 사용

호환 클라이언트에는 필요한 스킬 폴더 전체를 등록한다. `SKILL.md`와 함께 해당 폴더의 스크립트·참고 문서·자산을 보존한다. 제품별 플러그인 설정이나 `agents/openai.yaml`은 필요하지 않다. 내부 파일 참조는 스킬 폴더 기준 상대 경로를 사용한다.

```sh
# 현재 저장소의 스킬 발견 확인
npx skills@latest add . --list

# GitHub에 게시된 개별 스킬 설치
npx skills@latest add https://github.com/5ys-5y5/skills --skill crm-ui-mapping
```

자체 런타임은 [공식 클라이언트 가이드](https://agentskills.io/client-implementation/adding-skills-support)에 따라 일반적인 스킬 디렉터리를 발견하고 YAML을 파싱한다. 처음에는 이름·설명을 모델에 제공하며, 모델 판단 또는 사용자 명시적 선택으로 활성화한 본문과 필요한 자료만 단계적으로 읽는다. 스킬 루트를 기준으로 자료 경로를 해석하고, 파일 읽기와 스크립트 실행은 구분한다. 외부 규격 준수 스킬에 전용 메타데이터나 특정 호출 명령을 요구하지 않는다. 이름 충돌·잘못된 파일을 진단하고, 도구·인증·실행 환경이 없으면 제약을 명확히 알린다. 활성화된 스킬의 지침은 대화 압축 후에도 보존하거나 다시 로딩한다.

## 선택적 제품 설치와 표시 설정

제품별 부가 기능으로 `5ys` marketplace의 `5ys-skills` 플러그인이 실제 스킬 폴더를 묶는다. `.claude-plugin/plugin.json`은 이 선택적 패키지의 기준이며 표준 스킬 로딩의 필수 조건이 아니다. `skills/README.md`는 문서 탐색용이다.

현재 로컬 변경을 시험할 때는 저장소 루트에서 실행한다.

```sh
# Codex
codex plugin marketplace add .
codex plugin add 5ys-skills@5ys

# Claude Code: Codex 대신 이 환경을 사용할 경우
claude plugin marketplace add .
claude plugin install 5ys-skills@5ys
```

GitHub에 변경을 푸시한 뒤에는 첫 번째 명령의 `.` 대신 `5ys-5y5/skills`를 사용할 수 있다. 설치 후 새 세션에서 스킬 목록에 등록된 항목이 나타나는지 확인하고, 필요한 스킬 이름과 업무 요청을 전달한다. 이 문서는 설치 방법을 제공하며 사용자 환경에 플러그인을 자동 설치하지 않는다.

기존에 같은 스킬을 복사하거나 링크해 설치했다면 설치 방식을 하나로 정리한다. 플러그인과 수동 설치를 함께 사용하면 중복될 수 있다. 다른 에이전트에서는 각 항목 폴더 전체를 해당 환경의 지원 설치 방식으로 등록한다. 저장소를 clone하거나 경로 안내 문서를 읽는 것만으로 모든 스킬이 자동 등록되지는 않는다.

개별 `agents/openai.yaml`은 Codex 표시 이름과 요약만 제공한다. 자동 선택은 기본값을 유지하며, 실제 조치의 권한과 도구 연결은 업무 실행 시 확인한다. Chrome DevTools MCP 서버를 설치·실행하는 설정이나 CRM 자격 증명은 패키지에 포함하지 않는다.

패키지 형식은 [공식 플러그인 패키징 문서](https://developers.openai.com/plugins/build/plugins)의 Claude 호환 형식을, 표시 메타데이터는 [공식 스킬 문서](https://learn.chatgpt.com/docs/build-skills)를 참고했다. 분류별 경로를 유지하기 위해 호환 manifest에 스킬 폴더를 명시한다.

## 문서 구조

모든 항목은 `skills/<분류>/<이름>/SKILL.md`에 있다. 도구 사용 문서도 같은 경로 규칙을 사용하며, 별도 mcp 트리를 탐색하지 않는다.

```text
AGENTS.md
.agents/
.claude-plugin/
  plugin.json
  marketplace.json
.github/workflows/validate.yml
scripts/
  list-skills.sh
  validate-skills.py
  test-validation.py
skills/
  README.md
  engineering/
    README.md
    chrome-devtools/
      SKILL.md
      agents/openai.yaml
      references/
        source.json
        tool-reference.md
        troubleshooting.md
        LICENSE.txt
        validation.md
  hospital/
    README.md
    crm-ui-mapping/
      SKILL.md
      assets/profile.template.json
      references/context.schema.json
      references/prerequisites.md
      references/workflows/
      scripts/validate-context.py
      scripts/requirements.txt
```

병원 영역은 `crm-ui-mapping` 하나의 표준 스킬로 제공한다. 하위 업무는 그 안의 references/workflows 아래에 본문·contract.json·result.schema.json으로 묶는다. profile의 필수 XPath와 관계 검증 후 선택한 업무만 읽고, 실제 조작마다 현재 관찰값·필수 입력값을 검증한다. 병원별 매핑과 실제 업무 데이터는 호출 에이전트가 보관하며 이 저장소에는 틀만 둔다. 제품 표시 설정은 선택 사항이다.

시작 문서는 [skills/README.md](skills/README.md)다. 안내용 README는 스킬이 아니며, 각 실제 스킬의 SKILL.md와 필요한 자료를 읽는다. `skills/<분류>/<이름>`은 이 저장소의 구성 규칙이고 외부 스킬이나 소비 런타임에 강제하는 경로 규격이 아니다.

폴더별 항목은 [engineering](skills/engineering/README.md), [hospital](skills/hospital/README.md)에 있다. 분류 폴더 안에 스킬을 두고 README에서 각 SKILL.md를 안내하는 구성은 [참고 저장소](https://github.com/mattpocock/skills/tree/main/skills)를 따른다. `scripts/list-skills.sh`도 참고 저장소처럼 실제 SKILL.md 경로를 탐색하며 별도의 목록 데이터 파일을 유지하지 않는다.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r scripts/requirements.txt
bash scripts/list-skills.sh
.venv/bin/python scripts/validate-skills.py
.venv/bin/python scripts/test-validation.py
.venv/bin/python scripts/test-hospital-gate.py
# 제품별 패키지 유지보수 시에만 추가 검사
.venv/bin/python scripts/validate-skills.py --packaging
```

유지보수 검사는 Python 3.11 이상과 YAML 파서를 사용한다. 이 의존성은 스킬 소비 런타임의 필수 의존성이 아니다. 기본 검사는 표준 메타데이터·이름/폴더 일치·내부 상대 링크·원본 해시와 저장소 분류 규칙을 확인한다. `--packaging`만 선택적 제품 설정을 추가 검사한다. 테스트는 제품 설정을 제거해도 기본 검사가 통과하는지, 다중 행·인용 YAML을 수용하는지, 잘못된 필드·경로·원본 변조를 거부하는지 확인한다. CI에서도 실행한다.

양방향 호환성은 별도로 검증한다. 외부 스킬을 자체 런타임에 원본 그대로 제공해 발견·초기 메타데이터 공개·모델/사용자 선택·본문/자료 로딩을 확인하고, 자체 스킬도 제품 부가 설정 없이 다른 호환 런타임에서 같은 동작을 확인한다. 공식 `skills-ref`의 형식 검사·속성 읽기·프롬프트 생성은 보조 근거이며 전체 런타임 실행 검증을 대신하지 않는다. 런타임 버전·외부 원본 커밋·자료 해시·관찰 결과와 실행일을 기록한다. 접근할 수 없는 런타임·도구 환경은 미검증으로 남긴다.

이번 점검의 실제 결과와 미검증 항목은 [호환성 검증 기록](.agents/compatibility.md)에 구분해 두었다.

병원 유지보수 시나리오는 `.agents/scenarios/hospital/`에 보관하며 배포되는 스킬 폴더에 포함하지 않는다. 실제 CRM/MCP 시험은 허가된 테스트 환경에서 수행하고, 문서 검사·에이전트 판단 검사·서비스 실행 결과를 구분한다. 실제 환자 데이터와 인증 정보는 시험 자료나 Git 기록에 넣지 않는다.

## 업데이트

자체 스킬 변경은 Git으로 관리한다. 배포 시 `.claude-plugin/plugin.json`의 `version`을 올리고 위 검사를 실행한 뒤 커밋·푸시·태그를 수행한다. 루트에 별도 버전 목록이나 lock 파일을 만들지 않는다. 설치된 패키지의 갱신은 해당 에이전트의 플러그인 업데이트 기능을 사용한다. 로컬 설치는 원본 변경 후 갱신하고 새 세션에서 재확인한다.

외부 출처·버전·해시·갱신 절차는 해당 항목의 references/source.json 한 곳에 둔다. 자체 스킬 변경 이력은 Git으로 관리한다. 루트에 별도의 lock이나 업데이트 문서를 두지 않는다.

Chrome DevTools 항목은 연결된 MCP 서버를 사용하는 공식 문서다. 서버 제공·자동 설치를 뜻하지 않는다. 병원 업무 스킬은 특정 서비스 설정 규격이나 특정 MCP를 요구하지 않고 실행 환경에서 제공하는 권한·접속 정보·도구를 사용한다.

.agents/는 저장소 유지보수 규칙이다. 서비스의 설정·인증·캐시·문서 공급 구현은 이 저장소에 포함하지 않는다. 실제 업무 검증 완료를 뜻하지 않으며 자체 문서에 별도 공개 재배포 라이선스를 부여하지 않았다.

병원 진입점·하위 자료 구조는 표준의 단계적 로딩을 사용한다. 표준에는 스킬 간 자동 선행 실행이나 README 우선 실행 규정이 없다. 따라서 하위 업무를 별도 SKILL.md로 광고하지 않는다. 필수 실행 차단을 보장하려면 소비 런타임이 실제 조작 전에 검증 결과를 연결해야 한다. 검증 스크립트만으로 다른 런타임의 도구 호출을 가로챌 수는 없다.

병원 매핑 준비는 문서를 읽으면 CRM 접근·필요한 로그인·XPath 지정부터 시작한다. 완성된 매핑이나 검증기 설치를 준비 단계의 선행조건으로 두지 않는다. 제공 검증기는 Python 표준 라이브러리만 사용하며 실행할 수 없는 환경에서는 에이전트가 문서의 동일 조건을 직접 확인한다. 업무 실행의 필수 검증은 유지한다.
