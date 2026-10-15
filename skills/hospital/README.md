# Hospital

## Model-invoked

- [patient-lookup](patient-lookup/SKILL.md): 환자 검색과 요청한 정보 조회.
- [appointment-manage](appointment-manage/SKILL.md): 가용 시간과 예약 조회, 신규·변경·취소.
- [visit-check-in](visit-check-in/SKILL.md): 당일 도착과 접수.
- [billing-lookup](billing-lookup/SKILL.md): 진료비·미수금·이미 발급된 영수증 조회.
- [contact-record](contact-record/SKILL.md): 상담 기록과 직원 콜백 요청 등록.

업무 샘플이며 실제 CRM 검증 완료를 뜻하지 않는다. 호출 에이전트가 자신의 환경에서 접속 정보·권한·사용 가능한 도구를 확인한다.

## 업무 검증

각 항목의 테스트 환경 시나리오: [환자 조회](patient-lookup/references/validation.md), [예약 관리](appointment-manage/references/validation.md), [내원·접수](visit-check-in/references/validation.md), [수납 조회](billing-lookup/references/validation.md), [상담 기록](contact-record/references/validation.md).

시나리오는 합격 기준이며 실행 결과가 아니다. 테스트용 합성 데이터와 권한이 있는 환경에서만 실행한다. 판단 검사는 선택한 SKILL.md와 시나리오의 요청·관찰값을 평가 에이전트에게 주고, 판정자는 실제 조치와 합격 기준을 대조한다. 실제 서비스 검사는 같은 시나리오를 테스트 CRM에서 실행한다. 결과에는 문서 커밋, 에이전트·도구 버전, 실행일, 시나리오, 수행 조치, 합격/실패/차단과 근거를 기록한다. 접근 가능한 테스트 환경이 없으면 서비스 검증은 미실행으로 남긴다. 식별정보와 원본 응답은 저장소에 보관하지 않는다.
