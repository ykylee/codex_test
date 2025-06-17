# 소프트웨어 요구 사항 명세서

이 문서는 Django 프레임워크를 이용하여 구축된 사용자 관리 시스템에 대한 요구 사항을 정리한 것입니다. 외부 데이터베이스와 Atlassian Crowd를 연동하여 사용자 정보를 관리합니다.

## 개요

- **목적**: 외부 DB의 직원 정보와 Atlassian Crowd에 등록된 사용자를 비교 및 동기화하여 사용자 계정을 관리합니다.
- **대상**: 관리자나 운영자가 웹 인터페이스를 통해 두 사용자 목록을 확인하고, 필요 시 Crowd 사용자 상태를 업데이트합니다.

## 기능 요구 사항

1. **외부 직원 정보 관리**
   - `ExternalEmployee` 모델을 통해 외부 DB에서 가져온 직원 정보를 저장합니다.
   - `username`, `full_name`, `is_employed` 필드를 포함합니다.

2. **Crowd API 연동**
   - `CrowdClient` 클래스를 통해 Atlassian Crowd REST API에 접근합니다.
   - 활성 사용자 목록 조회(`list_active_users`)와 사용자 비활성화(`deactivate_user`) 기능을 제공합니다.

3. **사용자 비교 페이지**
   - `/compare/` URL에서 외부 직원 목록과 Crowd 활성 사용자를 비교하여 보여줍니다.
   - 각 직원이 Crowd에 존재하는지 여부를 테이블 형태로 표시합니다.

4. **관리 명령어**
   - `sync_crowd_users` 명령어로 외부 DB에 존재하지 않는 Crowd 사용자를 비활성화할 수 있습니다.

## 설치 및 실행 방법

```bash
pip install django requests
python manage.py migrate
python manage.py runserver
```

웹 브라우저에서 `/compare/` 경로로 접속하여 비교 페이지를 확인할 수 있습니다.

## 비고

- Crowd API 정보를 환경 변수(`CROWD_URL`, `CROWD_APP_USERNAME`, `CROWD_APP_PASSWORD`)로 설정해야 합니다.
- 테스트 환경에서는 Crowd API가 설정되지 않아도 동작하도록 오프라인 모드를 지원합니다.
