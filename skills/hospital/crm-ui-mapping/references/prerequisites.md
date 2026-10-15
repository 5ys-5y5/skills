# 호출 에이전트 소유 자료와 선행 검증

이 문서의 자료 형식은 이 병원 업무 스킬이 사용하는 공개 JSON 데이터 틀이다. Agent Skills 자체의 메타데이터 확장이나 소비 서비스의 API·DB·인증 규약이 아니다. 에이전트는 원래 저장 방식을 유지하면서 필요한 값을 이 틀로 내보내 검사할 수 있다. 실제 자료는 이 저장소에 저장하지 않는다.

## 자료 구성

[context.schema.json](context.schema.json)이 profile·request·evidence 구조를 정의한다. 빈 profile 틀은 스킬 루트의 assets/profile.template.json이다. 아직 XPath가 없는 빈 틀은 실행 가능한 매핑이 아니며 검증에 실패하는 것이 정상이다.

| 부분 | 내용과 의미 |
|---|---|
| profile.context | hospital·crm·revision으로 에이전트가 관리하는 적용 대상을 구분한다. 매핑 변경 시 revision도 바꾼다. 인증 정보는 넣지 않는다. |
| profile.fields | 업무 항목 ID별 xpath·required·role·description·scope를 정의한다. 표준 항목은 요청 업무 contract의 이름을 사용하고 추가 항목 이름은 에이전트가 정한다. |
| xpath | 현재 CRM에서 검증한 실제 경로다. DOM에 따라 에이전트가 지정하며 이 저장소의 예시 경로로 대체하지 않는다. |
| required | 해당 매핑에서 반드시 갖춰야 하는 추가 항목인지 표시한다. contract가 필수로 정한 항목은 true여야 한다. |
| role | read·input·action·container로 표시값·입력란·실행 요소·범위를 구분한다. |
| description·scope | 업무 의미와 현재 환자/예약/청구 등 소속 범위를 설명한다. xpath 일치만으로 의미를 추정하지 않는다. |
| scope_field | 상대 XPath를 평가할 실제 컨테이너 필드 ID다. 지정하면 그 컨테이너도 현재 화면에서 검증한다. 없는 경우 XPath는 현재 문서 기준이며 scope의 의미를 관찰해 확인한다. |
| depends_on | 이 필드를 사용하기 전에 충족할 필드 ID들의 목록이다. 해당 항목의 description에 버튼 실행이나 로그인 상태 등 충족 조건과 드러나는 정보의 관계를 설명한다. 순환 관계는 허용하지 않는다. |
| effect | 클릭·입력이 navigation·filter·record 중 어떤 효과인지 지정한다. 조회 업무는 record 효과의 조작을 허용하지 않는다. 생략하면 record로 취급한다. |
| value_required | 이번 호출에서 값이 반드시 필요한 추가 항목인지 표시한다. fill·select의 입력값은 이 설정과 관계없이 필수다. |
| result_key | 확장 화면 항목이 결과의 어떤 필드에 대응하는지 지정한다. 기본 항목의 대응은 업무 contract의 result_bindings를 사용한다. 기존 결과의 대응을 다른 항목으로 덮어쓰지 않는다. |
| request | 매 호출의 새 id, workflow, operation, context, 이번 조작의 targets·action과 필요한 values를 에이전트가 제공한다. 실제 값은 이 호출 자료에만 포함한다. |
| request.result_fields·result | 이번 요청에서 얻어야 할 결과 항목 이름과 실제 관찰 결과다. result 검증에서 필수값과 타입을 확인한다. 미요청 금액·상태를 채우기 위해 불필요한 조회를 하지 않는다. |
| evidence | 같은 request_id·context와 시간대가 있는 observed_at, 현재 대상별 matches·visible·semantic_confirmed·owner_confirmed, 충족된 선행 항목 satisfied를 에이전트가 실제 도구 관찰에서 구성한다. |

컨테이너 안의 컬럼은 scope_field로 테이블/행에 연결하고 XPath를 그 컨테이너 기준으로 지정한다. 반복 환자 행은 대상 환자로 범위를 좁힌 뒤 한 항목을 지정한다. 로그인 버튼·환자 테이블·예약 날짜 컬럼 등 추가 항목을 fields에 넣을 수 있다. 없는 정보를 추정해 필드를 확정하지 않는다.

contract의 read 항목은 실제 표시 요소 또는 값을 읽을 수 있는 input에 대응할 수 있다. input이라는 이유로 쓰기가 허용되는 것은 아니다. 요청 action과 조회/쓰기 업무 범위도 통과해야 한다. 필수 항목은 현재 선택한 operation 기준으로 정하며 다른 업무에만 필요한 필드를 모두 채우도록 강제하지 않는다.

profile은 이번 업무에 해당하는 항목을 내보낸 자료다. required가 true인 확장 항목도 검증 대상이므로 다른 업무에서만 필요한 항목은 이 호출 자료에 필수로 내보내지 않는다. contract.optional_fields는 요청할 때 targets로 지정하거나 해당 필드를 required로 올려 검사한다. result_fields로 요청한 정보도 result_bindings를 통해 필수 매핑으로 올린다. 확장 결과 항목은 result_key로 연결한다. 예약 공개 가능 시간 조회는 availability operation을 사용하며 개인 환자 식별을 요구하지 않는다.

예약 여부 버튼을 눌러야 날짜가 보이는 CRM이라면 버튼 항목을 action으로 등록하고, 날짜 항목의 depends_on에 그 버튼 항목 ID를 연결한다. 먼저 버튼 자체의 action 검증을 통과해 조작한 뒤 실제 날짜 표시를 관찰한다. 해당 호출에서 충족한 근거가 있을 때만 버튼 ID를 satisfied에 넣고 날짜를 검증한다. 이미 날짜가 표시되는 경우는 설명된 충족 조건을 실제 관찰해 판단하며 같은 버튼을 불필요하게 다시 누르지 않는다.

로그인된 세션에서는 존재하지 않는 로그인 버튼을 필수 대상에 넣지 않는다. 로그인이 필요하면 버튼·입력란과 선행 관계를 추가하고 인증 정보는 런타임의 기존 수단으로 취급한다. 매핑 정의 중 허용된 관찰·탐색과 실제 업무 쓰기를 구분한다.

## 호출 순서

1. 선택 업무의 contract.json으로 operation의 필수 항목과 역할을 읽는다. 필요한 확장 항목·관계를 추가한다. profile과 request를 표준 JSON 자료로 준비한다.
2. mapping 검증을 실행한다. mapping_required이면 누락 XPath·역할·범위·관계를 정의하는 작업으로 돌아간다. mapping_valid이면 선택한 업무 지침을 읽는다. 다른 병원이나 다른 revision의 자료를 재사용하지 않는다.
3. 실제 화면의 다음 조작 대상으로 targets를 정한다. targets와 scope_field 컨테이너는 현재 화면에서 각각 한 요소이며 의미·소속이 확인되어야 한다. 모든 업무 화면이 동시에 표시될 필요는 없다. DOM XPath 문법과 실제 평가 결과는 에이전트의 브라우저 도구로 확인한다.
4. 이번 요청의 실제 관찰값과 충족된 선행 관계를 evidence로 제공하고 action 검증을 실행한다. 관찰은 5분 이내여야 하며, 그 안이라도 화면·기록·DOM이 바뀌면 다시 관찰한다. 다른 호출의 관찰은 사용할 수 없다. satisfied·semantic_confirmed·owner_confirmed는 추측이나 검증기 통과 목적의 값으로 채우지 않는다.
5. ready인 해당 조작만 실행한다. 다음 조작에서는 evidence와 필요한 입력값을 새로 확인한다. blocked이면 해당 조건을 해결하기 전 조작하지 않는다. 저장 결과는 같은 대상 상세에서 확인한다.
6. 요청 결과 필드 이름을 request.result_fields에, 실제 정보를 result에 넣고 result 검증을 수행한다. result_valid 이전에는 결과 형식 검증을 통과했다고 답하지 않는다. 입력값은 작업 contract의 input_schemas도 적용한다. 원래 숫자인 0은 값으로 인정하며 미확인 값을 0으로 만들어 넣지는 않는다.

## 제공 스크립트

스킬 루트 기준 Python 3.11 이상과 scripts/requirements.txt의 jsonschema가 필요하다. 에이전트의 실행 환경에 이미 있는 동등한 JSON Schema 검증기를 사용할 수도 있지만 타입 검사뿐 아니라 contract 필수 항목·관계 순환·현재 조작 근거·입력값 검사도 동일하게 수행해야 한다. 필요한 실행 환경이 없으면 제약을 설명하고 중단한다.

```sh
python scripts/validate-context.py --phase mapping < agent-owned-context.json
python scripts/validate-context.py --phase action < agent-owned-context.json
python scripts/validate-context.py --phase result < agent-owned-context.json
```

위 파일명은 입력 전달 예시이며 저장 경로를 강제하지 않는다. stdin으로 직접 전달해도 된다. 스크립트는 CRM 접속·파일 저장·로그인을 수행하지 않으며 출력에는 status와 실패한 항목만 포함한다. mapping_valid·ready·result_valid는 종료 코드 0, 누락·차단은 0이 아닌 종료 코드다. 런타임은 문서 읽기만으로 준비 완료를 인정하지 말고 각 실제 조작을 검증 결과에 연결한다. 이 스크립트만으로 모든 Agent Skills 호환 런타임의 도구 호출을 강제 차단할 수는 없다.

## 정보 결과

각 업무의 result.schema.json은 얻은 정보를 전달할 기본 틀이다. 에이전트는 관찰한 값을 이 형식으로 보유하고 추가 properties도 보존할 수 있다. 결과 스키마의 필수 정보가 확인되지 않으면 완성된 결과로 검증하지 않는다. JSON Schema 검사는 자료의 형식을 확인하며 실제 업무 성공 여부는 화면과 기록 상태로 별도로 확인한다.
