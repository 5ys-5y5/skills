---
name: crm-ui-mapping
description: CRM의 환자 조회·예약·접수·청구 조회·상담 업무를 수행하거나 화면 XPath 대응을 지정할 때 사용한다. 업무별 스키마와 호출 에이전트의 매핑을 먼저 검증하고 필요한 업무 지침만 읽는다.
compatibility: Requires an authorized CRM browser session and execution of the bundled JSON Schema checks or equivalent validation.
---

# 병원 CRM 업무 진입점과 필수 매핑 검증

병원 업무는 이 문서로 진입한다. 특정 CRM 페이지·병원·소비 서비스의 설정에 종속되지 않는다. 매핑과 환자·예약·청구·상담 실제 값은 호출 에이전트가 자신의 환경에서 보관한다. 이 저장소에는 스키마·빈 틀·검증 절차만 둔다.

## 처음 읽을 자료

1. [매핑·호출·관찰 스키마와 검증 절차](references/prerequisites.md)를 읽는다. 요청 업무 하나를 정하고 아래 표의 contract.json만 읽어 필요한 필드와 작업 종류를 확인한다. 다른 업무 본문이나 실제 환자 정보는 미리 읽지 않는다.
2. 호출 에이전트가 보관한 병원별 profile과 이번 request로 mapping 검증을 수행한다. 필수 XPath·의미·범위·역할 또는 관련 선행 항목이 없으면 아래 대응 정의를 먼저 수행한다. mapping_valid가 되기 전 업무 절차를 실행하지 않는다.
3. mapping_valid 이후 선택한 업무의 procedure.md와 필요한 결과 스키마만 읽는다. 매 실제 조작 전 현재 화면의 관찰 근거와 입력값을 action 검증한다. ready가 아닌 결과로 도구를 호출하지 않는다. 실제 결과는 요청한 result_fields와 함께 result 검증을 통과시킨 뒤 전달한다.

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

검증 스크립트나 동등한 스키마·관계 검증을 실행할 수 없으면 업무를 진행하지 않는다. 스크립트는 에이전트가 전달한 자료를 검사하며 브라우저를 직접 관찰하거나 도구 실행을 가로채지 않는다. 실제 호출 차단은 런타임이 매 조작에 이 검증 결과를 연결해야 보장된다. 화면에 접근해 매핑을 정의하는 단계와 업무 조작 단계는 구분한다.

이 스킬의 매핑 요청만으로 수납·예약·접수·상담 기록을 생성하거나 변경하지 않는다. 매핑 확인을 위한 임의 입력·저장은 하지 않는다. 실제 쓰기 요청이 함께 있으면 확정된 대응을 사용하고 해당 업무의 대상·입력값·저장 결과를 확인한다. 매핑 정의를 보관할 때는 실제 환자 기록과 인증 정보를 포함하지 않는다.
