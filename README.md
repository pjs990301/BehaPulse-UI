# BehaPulse-UI
 
## 설명
이 프로젝트는 사용자 관리, 장치 관리 및 대시보드 기능을 포함하는 Python 기반 애플리케이션입니다. 이 프로젝트는 구성에 JSON을 사용하고 API 문서화에 Swagger를 사용합니다.

## 목차
- [설명](#설명)
- [기능](#기능)
- [프로젝트 구조](#프로젝트-구조)
- [디렉토리 구조](#디렉토리-구조)
- [설정](#설정)
    - [Flask 부분](#flask-부분)
    - [Dash 부분](#dash-부분)
- [사용법](#사용법)
    - [Flask 부분](#flask-부분-1)
    - [Dash 부분](#dash-부분-1)
- [API 문서](#api-문서)
- [데이터베이스 SQL](#데이터베이스-sql)
- [라이선스](#라이선스)

## 기능
- 사용자 관리: 사용자 세부 정보, 로그인 및 보안 질문에 대한 모델 포함
- 장치 관리: 장치 세부 정보 및 사용자-장치 연관 모델 포함
- 대시보드 관리: 사용자 대시보드 및 장치 연관 모델 포함
- JSON 파일을 사용한 구성 관리

## 프로젝트 구조
- `swagger.json`: API 문서화 및 모델 정의 포함
- `database/db_connector.py`: 데이터베이스 구성 로딩 처리
- `config/db_config.json`: 데이터베이스 구성 세부 정보 포함
- `README.md`: 프로젝트 문서
- `templates/`: Dash 템플릿 파일 포함
- `app.py`: Flask 애플리케이션 실행 파일
- `img/`: UI 및 API 관련 파일 포함


## 디렉토리 구조
<details>
<summary>접기/펼치기</summary>
  
```
BehaPulse-UI/
|   .gitignore
|   app.py
|   LICENSE
|   swagger.json
|   
+---API
|   |   dashboard.py
|   |   device.py
|   |   user.py
|   |   user_dashboard.py
|   |   user_dashboard_device.py
|   |   user_device.py
|   |   __init__.py
|
+---config
|       db_config.json
|
+---database
|   |   db_connector.py
|   |   __init__.py
|
+---img
|       [이미지 파일들]
|
+---model
|   |   dashboard.py
|   |   device.py
|   |   user.py
|   |   user_dashboard.py
|   |   user_dashboard_device.py
|   |   user_device.py
|   |   __init__.py
|
+---static
+---templates
|   \---page
|       |   app.py
|       |
|       +---assets
|       |   [CSS 및 이미지 파일들]
|       |
|       +---component
|       |       __init__.py
|       |
|       +---controller
|       |   |   dashboard.py
|       |   |   device.py
|       |   |   home.py
|       |   |   login.py
|       |   |   password.py
|       |   |   sidebar.py
|       |   |   signup.py
|       |   |   __init__.py
|       |
|       +---layout
|       |   |   login.py
|       |   |   main_page.py
|       |   |   password.py
|       |   |   sidebar.py
|       |   |   signup.py
|       |   |   topbar.py
|       |   |   __init__.py
|       |
|       +---content
|       |   |   dashboard.py
|       |   |   dashboard_add.py
|       |   |   dashboard_detail.py
|       |   |   dashboard_person_edit.py
|       |   |   dashboard_person_info.py
|       |   |   device.py
|       |   |   device_add.py
|       |   |   device_detail.py
|       |   |   device_edit.py
|       |   |   home.py
|       |   |   __init__.py
|
+---test
  
```    
</details>


## 설정

### Flask 부분
1. 저장소를 클론합니다:
    ```sh
    git clone https://github.com/pjs990301/BehaPulse-UI
    ```
2. 프로젝트 디렉토리로 이동합니다:
    ```sh
    cd BehaPulse-UI
    ```
3. 필요한 종속성을 설치합니다:
    ```sh
    pip install -r requirements.txt
    ```

### Dash 부분
1. Dash를 설치합니다:
    ```sh
    pip install dash
    ```

## 사용법

### Flask 부분
1. `config/db_config.json`에서 데이터베이스 구성이 올바르게 설정되었는지 확인합니다. 다음의 구조에 맞춰서 작성해야 합니다:
    ```json
    {
      "Database" : {
        "host": "",
        "user": "",
        "password": "",
        "database": "",
        "auth_plugin" : ""
      }
    }
    ```
2. 애플리케이션을 실행합니다:
    ```sh
    python app.py
    ```

### Dash 부분
1. Flask 애플리케이션이 실행되면 Dash 애플리케이션이 자동으로 실행됩니다.

## API 문서
API 문서는 `swagger.json` 파일에 있습니다. 다음 모델에 대한 정의를 포함합니다:
- `UserModel`
- `LoginModel`
- `SecurityQuestionModel`
- `DeviceModel`
- `UserDeviceModel`
- `DashboardModel`
- `UserDashboardModel`
- `UserDashboardDeviceModel`

## 데이터베이스 SQL
<details>
<summary>접기/펼치기</summary>

```sql
create table dashboard
(
    personId int auto_increment
        primary key,
    name     varchar(255) not null,
    gender   varchar(255) not null,
    birth    date         not null,
    location varchar(255) null,
    status   varchar(255) null
)
    charset = utf8mb3;

create table device
(
    deviceId         int auto_increment
        primary key,
    macAddress       varchar(255) not null,
    type             varchar(255) not null,
    install_location varchar(255) null,
    room             varchar(255) null,
    check_date       date         null,
    on_off           tinyint(1)   not null,
    note             varchar(255) null
)
    charset = utf8mb3;

create table user
(
    userEmail        varchar(255)                        not null
        primary key,
    userPassword     varchar(255)                        not null,
    userName         varchar(255)                        not null,
    createdAt        timestamp default CURRENT_TIMESTAMP null,
    securityQuestion varchar(255)                        not null,
    securityAnswer   varchar(255)                        not null
)
    charset = utf8mb3;

create table user_dashboard
(
    userDashboardId int auto_increment
        primary key,
    personId        int          not null,
    userEmail       varchar(255) not null,
    constraint user_dashboard_dashboard_personId_fk
        foreign key (personId) references dashboard (personId)
            on update cascade on delete cascade,
    constraint user_dashboard_user_userEmail_fk
        foreign key (userEmail) references user (userEmail)
            on update cascade on delete cascade
)
    charset = utf8mb3;

create index idx_user_dashboard_userEmail_personId
    on user_dashboard (userEmail, personId);

create table user_device
(
    userDeviceId int auto_increment
        primary key,
    userEmail    varchar(255) not null,
    deviceId     int          not null,
    constraint user_device_ibfk_1
        foreign key (userEmail) references user (userEmail)
            on update cascade on delete cascade,
    constraint user_device_ibfk_2
        foreign key (deviceId) references device (deviceId)
            on update cascade on delete cascade
)
    charset = utf8mb3;

create table user_dashboard_device
(
    userDashboardDeviceId int auto_increment
        primary key,
    userEmail             varchar(255) null,
    personId              int          null,
    deviceId              int          null,
    constraint user_dashboard_device_user_dashboard_fk
        foreign key (userEmail, personId) references user_dashboard (userEmail, personId)
            on update cascade on delete cascade,
    constraint user_dashboard_device_user_device_fk
        foreign key (userEmail, deviceId) references user_device (userEmail, deviceId)
            on update cascade on delete cascade
)
    charset = utf8mb3;

create index idx_user_device_userEmail_deviceId
    on user_device (userEmail, deviceId);
```

</details>

## 라이선스
이 프로젝트는 MIT 라이선스에 따라 라이선스가 부여됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하십시오.
