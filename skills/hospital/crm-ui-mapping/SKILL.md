---
name: crm-ui-mapping
description: CRM의 환자 조회·예약·접수·청구 조회·상담 또는 XPath 지정에 사용한다. 매핑이 없으면 실제 CRM 접근·필요한 로그인·화면 관찰로 XPath를 수집한 뒤 검증하고 업무를 수행한다.
compatibility: Requires authorized browser access to the CRM. Bundled checks use only the Python standard library; equivalent validation can be performed by the agent.
---

# 병원 CRM 업무 진입점과 필수 매핑 검증

병원 업무는 이 문서로 진입한다. 특정 CRM 페이지·병원·소비 서비스의 설정에 종속되지 않는다. 매핑과 환자·예약·청구·상담 실제 값은 호출 에이전트가 자신의 환경에서 보관한다. 이 저장소에는 스키마·빈 틀·검증 절차만 둔다.

## 문서를 읽으면 먼저 매핑 준비를 시작한다

매핑이 없거나 불완전하면 검증 스크립트부터 실행해 중단하지 말고 현재 CRM에서 XPath를 지정하는 흐름을 시작한다. 아래 준비 과정은 mapping_valid 이전에 허용된다. 매핑을 만들기 위해 완성된 매핑을 먼저 요구하지 않는다.

1. 사용자가 지정한 CRM 또는 현재 환경의 접속 정보를 확인하고 실제 브라우저로 페이지를 연다. 주소가 없을 때만 주소를 확인한다. 기존 로그인 세션을 우선 사용한다.
2. 로그인이 필요하면 사용 가능한 인증 수단으로 진행한다. 화면에서 로그인 입력란·버튼을 확인하고 그 XPath·역할을 먼저 기록한 뒤 필요한 인증을 수행한다. 비밀번호나 토큰은 매핑 자료에 넣지 않는다. 업무 전체 profile이 없다는 이유로 로그인까지 차단하지 않는다.
3. 요청 업무 contract를 읽고 필요한 메뉴·상세 영역·테이블·컬럼·입력란을 관찰해 실제 XPath를 채운다. 탐색·검색 필터·내용 펼치기가 필요하면 해당 요소의 역할과 XPath를 확인·기록하고 진행한다. 예약·수납·접수·상담 업무 기록을 생성하거나 변경하는 동작은 이 준비 과정에 포함하지 않는다.
4. 필요한 XPath·필수 여부·역할·관계를 수집한 뒤 매핑을 검증한다. 빠진 항목은 계속 관찰해 보완한다. 프로그램 실행 환경이 없으면 스키마와 검증 절차를 읽고 동일 항목을 직접 확인할 수 있다. 어떤 방식으로 무엇을 확인했는지 구분해 남기며 실행하지 않은 스크립트를 실행했다고 답하지 않는다.
5. ERR_BLOCKED_BY_CLIENT 등으로 화면이 열리지 않으면 기존에 허용된 다른 브라우저 접근 수단이 있는지 확인한다. 실제 화면을 볼 수 없다면 해당 페이지의 XPath는 미확정으로 남기고 접근에 필요한 조치를 알린다. 이 경우의 원인은 페이지 접근 실패이며 매핑 검증 실패나 Python 의존성 부재와 혼동하지 않는다.

## 처음 읽을 자료

1. [매핑·호출·관찰 스키마와 검증 절차](references/prerequisites.md)를 읽는다. 요청 업무 하나를 정하고 아래 표의 contract.json만 읽어 필요한 필드와 작업 종류를 확인한다. 다른 업무 본문이나 실제 환자 정보는 미리 읽지 않는다.
2. 병원별 profile이 없거나 필수 XPath·의미·범위·역할 또는 관련 선행 항목이 없으면 위 매핑 준비와 아래 대응 정의부터 수행한다. 수집한 profile과 이번 request로 mapping 검증한다. mapping_valid는 업무 절차를 시작하는 조건이며 준비를 위한 페이지 열기·인증·화면 관찰의 조건이 아니다.
3. mapping_valid 이후 선택한 업무의 procedure.md와 필요한 결과 스키마만 읽는다. 업무를 수행하는 실제 조작 전 현재 화면의 관찰 근거와 입력값을 action 검증한다. ready가 아닌 결과로 해당 업무 조작을 실행하지 않는다. 실제 결과는 요청한 result_fields와 함께 result 검증을 통과시킨 뒤 전달한다.

| 요청 업무 | 매핑·필수 항목 | 통과 후 읽을 업무 지침 | 얻을 정보의 스키마 |
|---|---|---|---|
| 환자 조회 | [contract](references/workflows/patient-lookup/contract.json) | [procedure](references/workflows/patient-lookup/procedure.md) | [result](references/workflows/patient-lookup/result.schema.json) |
| 예약 조회·신규·변경·취소 | [contract](references/workflows/appointment-manage/contract.json) | [procedure](references/workflows/appointment-manage/procedure.md) | [result](references/workflows/appointment-manage/result.schema.json) |
| 도착·접수 | [contract](references/workflows/visit-check-in/contract.json) | [procedure](references/workflows/visit-check-in/procedure.md) | [result](references/workflows/visit-check-in/result.schema.json) |
| 청구·수납 조회 | [contract](references/workflows/billing-lookup/contract.json) | [procedure](references/workflows/billing-lookup/procedure.md) | [result](references/workflows/billing-lookup/result.schema.json) |
| 상담 기록·콜백 | [contract](references/workflows/contact-record/contract.json) | [procedure](references/workflows/contact-record/procedure.md) | [result](references/workflows/contact-record/result.schema.json) |

각 업무는 독립 SKILL.md가 아닌 이 스킬의 참고 지침이다. 필요한 단계를 상대 경로로 읽으며 다른 스킬 호출 도구를 요구하지 않는다. 스키마에 항목과 의존 관계를 추가할 수 있지만 공통 필수 항목을 제거하거나 required를 false로 낮춰 통과시키지 않는다.

## 대응 정의

1. 요청 업무와 대상 범위를 정한다. 환자 검색, 예약 편집, 청구 조회, 상담 입력 등 실제 조작할 영역을 구분한다. 업무 수행에 필요한 항목만 매핑한다.
2. 기존 매핑이 제공되면 현재 페이지·화면 상태에서 확인한다. 없거나 맞지 않으면 현재 DOM·접근성 정보·표의 열 제목·연결된 레이블과 상세 영역을 관찰한다. 화면에 없는 필드나 XPath를 만들어내지 않는다.
3. 각 업무 항목에 실제 XPath, required, 업무 의미, 소속 대상과 적용 범위, 읽기/입력/실행 역할을 지정한다. 실제 XPath와 스코프가 없는 항목을 추론한 화면 위치로 대체하지 않는다. 추가 버튼을 눌러야 값이 나타나면 그 버튼도 확장 필드로 등록하고 depends_on으로 관계를 연결한다. 저장 위치·서비스 API·인증 방식은 정하지 않는다.
4. 대상 영역 안에서 로케이터가 의도한 요소 하나를 가리키는지 확인한다. 첫 번째 일치나 화면 순서만으로 대상을 고르지 않는다. 같은 레이블이 반복되면 환자·예약·청구 상세나 행·대화상자로 범위를 좁힌다.
5. 유일한 요소인지와 업무 의미가 맞는지를 별도로 확인한다. 잔액 표시와 수납액 입력, 예약 검색 날짜와 예약 일시 입력, 상담 검색어와 상담 본문 입력을 구분한다. 입력란의 소속 기록과 저장 실행 요소가 같은 편집 영역에 연결되는지도 확인한다.
6. 화면 이동·다시 그리기·대상 기록 변경 후에는 사용할 대응을 재확인한다. 이전 스냅샷의 임시 요소 번호를 다른 화면에서 재사용하지 않는다. 모호한 항목은 미확정으로 남기고 구분에 필요한 정보만 확인한다.

## 완료 기준과 차단

매핑 정의 완료는 mapping_valid, 개별 조작의 준비 완료는 ready로 구분한다. 결과는 실제 관찰한 정보를 선택한 업무의 result.schema.json에 대응시켜 호출 에이전트에게 전달한다. 확장 항목은 보존한다. 필수 정보를 얻을 수 없으면 임의 값·0·빈 문자열로 성공 결과를 채우지 않고 미확인 항목과 부족한 조건을 설명한다. 결과 스키마도 에이전트가 같은 환경에서 검증한다.

검증 스크립트는 외부 패키지 없이 Python 표준 라이브러리로 실행한다. Python 실행이 불가능하면 에이전트가 스키마·필수 항목·관계·관찰·입력값을 동등하게 검사한다. 어느 방식으로도 필요한 검증을 할 수 없으면 해당 업무 조작을 진행하지 않지만 매핑 관찰과 정의는 계속할 수 있다. 스크립트는 브라우저를 직접 관찰하거나 도구 실행을 가로채지 않는다. 실제 호출 차단은 런타임이 업무 조작에 검증 결과를 연결해야 보장된다.

이 스킬의 매핑 요청만으로 수납·예약·접수·상담 기록을 생성하거나 변경하지 않는다. 매핑 시험용 업무 기록 입력·저장은 하지 않는다. 준비에 필요한 로그인 입력과 검색 조건 입력은 허용된 실제 요청과 인증 범위에서 수행할 수 있다. 실제 쓰기 요청이 함께 있으면 확정된 대응을 사용하고 해당 업무의 대상·입력값·저장 결과를 확인한다. 매핑 정의를 보관할 때는 실제 환자 기록과 인증 정보를 포함하지 않는다.
