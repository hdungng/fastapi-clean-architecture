# FastAPI Clean Architecture Skeleton

Skeleton dự án FastAPI theo phong cách **ASP.NET Core + Clean Architecture**:

- Layers: API (Controllers) → Application (Services, DTOs) → Domain (Entities, Repositories) → Infrastructure (DB, Auth, Mapping)
- Convention giống ASP.NET Core:
  - Controller: `UserController`, `WeatherForecastController`, `AuthController`
  - Service: `UserService`, `WeatherForecastService`, `AuthService`
  - Interface: `IUserService`, `IWeatherForecastService`, `IUnitOfWork`, ...
  - DTO: `UserDto`, `WeatherForecastDto`, ...
- UnitOfWork + Repository pattern
- AutoMapper style: `Mapper`, `Profile` (WeatherForecastProfile, UserProfile)
- Auth: JWT (login), bcrypt password hashing
- API response chuẩn: `ApiResponse<T>`
- Global exception handler + ModelState-like validation errors
- Alembic migrations
- Seed script tạo admin
- Cấu hình qua `.env`
- Logging cấu hình trung tâm

---

## 1. Cài đặt

```bash
pip install -r requirements.txt
```

Tạo file `.env` (đã có sẵn bản mẫu):

```env
ENV=development
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=super-secret-dev-key-change-me
ACCESS_TOKEN_EXPIRE_MINUTES=60
LOG_LEVEL=INFO
```

---

## 2. Chạy migration (Alembic)

```bash
alembic upgrade head
```

Cấu hình Alembic nằm ở:

- `alembic.ini`
- `alembic/env.py` (import `Base`, `DATABASE_URL` từ `app.infrastructure.db.base`)

---

## 3. Seed admin user

```bash
python seed_admin.py
```

Script sẽ tạo user:

- UserName: `admin`
- Email: `admin@example.com`
- Password: `123456`

Password được hash bằng `bcrypt` trước khi lưu DB.

---

## 4. Chạy API

```bash
uvicorn app.main:app --reload --app-dir=src
```

Swagger UI:

- http://localhost:8000/docs

---

## 5. Cấu trúc thư mục chính

```text
src/app
├─ api/
│  ├─ controllers/
│  │  ├─ AuthController.py
│  │  ├─ UserController.py
│  │  └─ WeatherForecastController.py
│  └─ router.py              # RegisterRoutes(app)
├─ application/
│  ├─ dtos/
│  └─ services/
├─ config/
│  └─ settings.py            # đọc .env bằng pydantic BaseSettings
├─ domain/
│  ├─ entities/
│  └─ repositories/
├─ infrastructure/
│  ├─ auth/                  # JWT, password hashing, auth dependencies
│  ├─ db/
│  │  ├─ base.py             # Base, engine, SessionLocal, InitDb()
│  │  ├─ DbContext.py        # DbContext (wrap Session)
│  │  └─ models/
│  │     ├─ user_model.py
│  │     └─ weather_forecast_model.py
│  ├─ mapping/               # AutoMapper + Profiles
│  └─ repositories/          # UnitOfWork + repos
├─ shared/
│  ├─ api_response.py
│  ├─ api_responses.py       # Ok, Created, BadRequest, NotFound
│  ├─ datetime_helper.py
│  ├─ string_helper.py
│  ├─ pagination.py
│  ├─ exception_handlers.py  # global exception handlers
│  └─ logging_config.py      # configure_logging(), get_logger()
└─ main.py
```

---

## 6. ApiResponse<T> & lỗi ModelState

Mọi API đều trả về dạng:

```json
{
  "success": true,
  "data": ...,
  "meta": { ... } | null,
  "message": null,
  "errors": null
}
```

Khi validate lỗi (body / query / path):

```json
{
  "success": false,
  "data": null,
  "meta": null,
  "message": "One or more validation errors occurred.",
  "errors": {
    "body.Email": ["value is not a valid email address"],
    "body.UserName": ["field required"]
  }
}
```

Các lỗi HTTP (401, 403, 404, …) cũng được wrap:

```json
{
  "success": false,
  "data": null,
  "meta": null,
  "message": "User not found",
  "errors": null
}
```

---

## 7. Convention comment

- **Controller endpoint**: mỗi action đều có docstring mô tả:
  - method + route
  - Summary
  - Params (query/body)
  - Kiểu trả về (ApiResponse[T])

Ví dụ:

```python
@router.get("")
async def GetUsers(...):
    """
    GET /api/users

    Summary:
    - Lấy danh sách người dùng có phân trang, sort, search, filter.
    """
```

- **Service**: class/method có docstring mô tả use-case:
  - Không dùng FastAPI ở đây, chỉ DTO & entities
  - Controller wrap kết quả vào ApiResponse

---

## 8. Thêm module mới (ví dụ Product)

1. Domain:
   - `domain/entities/Product.py`
   - `domain/repositories/IProductRepository.py`
2. DB model:
   - `infrastructure/db/models/product_model.py`
3. Repository:
   - `infrastructure/repositories/ProductRepository.py`
4. DTO + Service:
   - `application/dtos/ProductDto.py`
   - `application/services/IProductService.py`
   - `application/services/ProductService.py`
5. Controller:
   - `api/controllers/ProductController.py`
6. AutoMapper profile:
   - `infrastructure/mapping/ProductProfile.py` + đăng ký trong `ConfigureMappings()`
7. Router:
   - include `ProductController.router` trong `api/router.py`

---

## 9. Logging

- Config: `shared/logging_config.configure_logging()`
- Đọc mức log từ `.env` (`LOG_LEVEL=INFO` / `DEBUG` / `WARNING` ...)
- Lấy logger:
  ```python
  from app.shared.logging_config import get_logger
  logger = get_logger(__name__)
  logger.info("Hello")
  ```

---

## 10. Gợi ý mở rộng

- Refresh token, revoke token
- Role/permission
- Soft-delete, audit fields (CreatedBy, CreatedAt, ...)
- Multi-tenant
- Event bus / domain events
- Unit test cho service + repository


---

## 11. Module Product (demo full flow)

- Entity: `domain/entities/Product.py`
- DB model: `infrastructure/db/models/product_model.py`
- Repository: `infrastructure/repositories/ProductRepository.py`
- Service: `application/services/ProductService.py`
- DTO: `application/dtos/ProductDto.py`
- Controller: `api/controllers/ProductController.py`
- Mapping: `infrastructure/mapping/ProductProfile.py`
- Đăng ký router: `api/router.py`

Authorization demo trên Product:

- `GET /api/products` yêu cầu **role**: `Admin` (RequireRoles("Admin"))
- `GET /api/products/{id}` yêu cầu **permission**: `Products.Read`
- `POST/PUT/DELETE /api/products` yêu cầu **permission**: `Products.Write`

Admin seed mặc định:

- Roles: `["Admin"]`
- Permissions: `["Users.Read", "Users.Write", "Products.Read", "Products.Write"]`

---

## 12. Policy-based auth (Role + Permission)

- Role: bắt buộc, dùng `RequireRoles("Admin", "Manager")`
- Permission: mềm dẻo, dùng `RequirePermissions("Products.Write", enforce=True/False)`

Ví dụ:

```python
# Bắt buộc phải có role Admin
principal: UserPrincipal = Depends(RequireRoles("Admin"))

# Bắt buộc phải có permission Products.Write
principal: UserPrincipal = Depends(RequirePermissions("Products.Write", enforce=True))

# Permission optional: chỉ inject principal, service sẽ tự quyết định có chặn hay không
principal: UserPrincipal = Depends(RequirePermissions("Feature.X", enforce=False))
```


---

## 13. Roles & Permissions

### Bảng & quan hệ

- `Roles` (RoleModel)
- `Permissions` (PermissionModel)
- `UserRoles` (UserRoleModel) – quan hệ N-N User ↔ Role
- `RolePermissions` (RolePermissionModel) – quan hệ N-N Role ↔ Permission

User vẫn có cột `Roles` và `Permissions` dạng string (cache) để auth nhanh,
được sync lại qua `seed_admin.py` hoặc sau các thao tác gán role/permission.

### API

- `GET /api/roles` – list roles
- `POST /api/roles` – tạo role
- `PUT /api/roles/{id}` – sửa role
- `DELETE /api/roles/{id}` – xóa role
- `POST /api/roles/{roleId}/users/{userId}` – gán role cho user
- `DELETE /api/roles/{roleId}/users/{userId}` – bỏ role khỏi user

- `GET /api/permissions` – list permissions
- `POST /api/permissions` – tạo permission
- `PUT /api/permissions/{id}` – sửa
- `DELETE /api/permissions/{id}` – xóa
- `POST /api/permissions/assign?roleId=&permissionId=` – gán permission cho role
- `DELETE /api/permissions/unassign?roleId=&permissionId=` – bỏ permission khỏi role

Tất cả các API này yêu cầu role `Admin` (RequireRoles("Admin")).

### Seed SuperAdmin + default roles/permissions

`seed_admin.py` sẽ:

- Tạo các role: `SuperAdmin`, `Admin`, `User`
- Tạo các permission:
  - `Users.Read`, `Users.Write`
  - `Products.Read`, `Products.Write`
  - `Roles.Read`, `Roles.Write`
  - `Permissions.Read`, `Permissions.Write`
- Gán mọi permission cho `SuperAdmin`
- Gán các permission liên quan cho `Admin` và `User`
- Tạo/tái sử dụng user `admin` và gán role `SuperAdmin`
- Sync cache `Users.Roles` và `Users.Permissions` cho admin

---

## 14. Refresh token (bật/tắt mềm dẻo)

Cấu hình trong `.env`:

```env
ENABLE_REFRESH_TOKEN=true
REFRESH_TOKEN_EXPIRE_DAYS=7
```

Nếu `ENABLE_REFRESH_TOKEN=false`:

- `/api/auth/login` vẫn trả về AccessToken
- `/api/auth/refresh` sẽ trả về lỗi 400 "Refresh token is disabled by configuration"

### Bảng RefreshTokens

- `RefreshTokens` (RefreshTokenModel):
  - Id, UserId, Token, ExpiresAt, RevokedAt, ReplacedByToken, IsRevoked
  - Kế thừa `AuditMixin` (CreatedAt, CreatedBy, UpdatedAt, UpdatedBy)

### Luồng API

- `POST /api/auth/login`
  - Đăng nhập → trả về `AccessToken` + (nếu bật) `RefreshToken`
- `POST /api/auth/refresh?refreshToken=...`
  - Kiểm tra refresh token còn hạn, chưa revoke
  - Tạo access token mới + refresh token mới (rotate)
  - Đánh dấu token cũ `IsRevoked = true`
- `POST /api/auth/revoke?refreshToken=...`
  - Revoke một refresh token cụ thể

---

## 15. Audit fields

Tất cả model chính đều kế thừa `AuditMixin`:

```python
class AuditMixin:
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    CreatedBy = Column(String(100), nullable=True)
    UpdatedAt = Column(DateTime(timezone=True), onupdate=func.now())
    UpdatedBy = Column(String(100), nullable=True)
```

Models hiện tại:

- `UserModel`, `ProductModel`, `WeatherForecastModel`
- `RoleModel`, `PermissionModel`, `UserRoleModel`, `RolePermissionModel`
- `RefreshTokenModel`

=> Mặc định sẽ có CreatedAt/UpdatedAt tự động.

---

## 16. Tổng hợp Module

- **User**: CRUD + paging + auth protection  
- **Product**: CRUD + role/permission-based auth  
- **Role**: CRUD + assign User ↔ Role  
- **Permission**: CRUD + assign Role ↔ Permission  
- **Auth**: JWT + (optional) RefreshToken + revoke


---

## 17. User self endpoints (xem/đổi roles/permissions của chính mình)

### Xem thông tin

- `GET /api/users/me`
  - Trả về `UserDto` của user hiện tại (bao gồm Roles, Permissions cache)
- `GET /api/users/me/roles`
  - Trả về `string[]` danh sách tên role
- `GET /api/users/me/permissions`
  - Trả về `string[]` danh sách tên permission hiệu lực (union từ các role)

### Đổi roles của chính mình

- `PUT /api/users/me/roles`

Body:

```json
{
  "Roles": ["Admin", "User"]
}
```

Auth:

- Bắt buộc permission: `Users.Self.ManageRoles`
- Permission này đã được seed mặc định và gán cho role `SuperAdmin`.
  - Bạn có thể gán nó cho role khác (ví dụ: "CustomerAdmin") thông qua các API `/api/roles` và `/api/permissions`.

Cơ chế:

- Clear toàn bộ `UserRoles` hiện tại của user
- Gán lại roles theo danh sách tên gửi lên
- Tự động build lại:
  - `Users.Roles` (cache string)
  - `Users.Permissions` (cache union mọi permission từ roles)

Như vậy, auth layer sử dụng `UserDto.Roles` & `UserDto.Permissions` vẫn luôn đồng bộ với quan hệ User ⇄ Role ⇄ Permission ở DB.


---

## 18. User tự đổi mật khẩu

Endpoint:

- `PUT /api/users/me/password`

Body:

```json
{
  "CurrentPassword": "old-pass",
  "NewPassword": "new-pass"
}
```

Đặc điểm:

- Chỉ yêu cầu user đăng nhập (JWT) – không cần permission đặc biệt
- Service sẽ:
  - Lấy user theo Id hiện tại
  - Verify `CurrentPassword` với `PasswordHash`
  - Nếu sai → trả về ApiResponse `success = false`, message = `"Current password is incorrect"`
  - Nếu đúng → hash `NewPassword` và cập nhật

Đây là luồng tương tự `ChangePasswordAsync` trong ASP.NET Identity, nhưng được implement ở `UserService.ChangePassword`.
