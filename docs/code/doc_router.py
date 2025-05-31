from fastapi import APIRouter, Depends, HTTPException
from shared.dto.response.api_responseDto import SuccessResponseDto
from auth.functions.get_user_or_error import get_user_or_error
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import httpx
import csv
import io

router = APIRouter()


api_translations = {
    # Postman APIs
    "GET /postman": "دریافت اطلاعات پست‌من",
    # Switch APIs
    "POST /switches/execCommand": "اجرای دستور روی سویچ",
    "GET /switches/checkConnectionStatus": "بررسی وضعیت اتصال سویچ",
    "GET /switches/info/{id}": "اطلاعات سویچ با شناسه",
    "GET /switches/byIP/{ip}": "اطلاعات سویچ بر اساس آی‌پی",
    "POST /switches/create": "ایجاد سویچ جدید",
    "PATCH /switches/update/": "به‌روزرسانی اطلاعات سویچ",
    "DELETE /switches/delete/{id}": "حذف سویچ با شناسه",
    "GET /switches/list": "لیست تمام سویچ‌ها",
    "GET /switches/checkHardening/{id}": "بررسی سخت‌سازی سویچ با شناسه",
    "POST /switches/createAsset/{id}": "ایجاد دارایی برای سویچ با شناسه",
    "GET /switches/ciscoAsset/{id}": "اطلاعات دارایی سیسکو برای سویچ با شناسه",
    "GET /switches/inventory/{id}": "موجودی سویچ با شناسه",
    "GET /switches/getSnmpData/{id}": "دریافت داده‌های SNMP سویچ با شناسه",
    "GET /switches/hardeningCheckNew/{id}": "بررسی سخت‌سازی جدید سویچ با شناسه",
    "GET /switches/hardeningCheckASA2/{id}": "بررسی سخت‌سازی ASA2 سویچ با شناسه",
    "GET /switches/hardeningSummaryDetail/{id}": "جزئیات خلاصه سخت‌سازی سویچ با شناسه",
    "POST /switches/neighbor/create/": "ایجاد همسایه سویچ",
    "DELETE /switches/neighbor/delete/": "حذف همسایه سویچ",
    "POST /switches/interfaces/create": "ایجاد اینترفیس سویچ",
    "PATCH /switches/interfaces/update": "به‌روزرسانی اینترفیس سویچ",
    "GET /switches/interfaces/list/{switchId}": "لیست اینترفیس‌های سویچ با شناسه",
    "DELETE /switches/interfaces/delete/{id}": "حذف اینترفیس سویچ با شناسه",
    # Sync APIs
    "GET /syncPostman/sync": "خلاصه وضعیت سخت‌سازی (هاردنینگ) با شناسه",
    # Auth APIs
    "POST /auth/login": "ورود به سیستم (لاگین) با نام کاربری و کلمه عبور",
    "POST /auth/register": "ثبت‌نام کاربر جدید با نام، نام کاربری و کلمه عبور",
    # OperatingSystem APIs
    "POST /os/create": "ایجاد سیستم‌عامل با مشخصات کامل",
    "PATCH /os/update": "به‌روزرسانی سیستم‌عامل با شناسه",
    "DELETE /os/delete/{id}": "حذف سیستم‌عامل با شناسه",
    "GET /os/list": "دریافت لیست سیستم‌عامل‌ها",
    "GET /os/updateListFromWazuh": "به‌روزرسانی لیست از Wazuh",
    "GET /os/updateListFromWazuhMock": "به‌روزرسانی نمونه لیست از Wazuh",
    # Hardening APIs
    "POST /hardening/create": "ایجاد مورد سخت‌سازی با جزئیات کامل",
    "PATCH /hardening/update": "به‌روزرسانی مورد سخت‌سازی با شناسه",
    "DELETE /hardening/delete/{id}": "حذف مورد سخت‌سازی با شناسه",
    "GET /hardening/info/{id}": "دریافت اطلاعات مورد سخت‌سازی با شناسه",
    "GET /hardening/list": "دریافت لیست موارد سخت‌سازی",
    # HardeningResult APIs
    "GET /hardeningResults/switches/{id}": "دریافت نتایج سخت‌سازی سویچ با شناسه",
    "GET /hardeningResults/switches/versions/{id}": "دریافت نسخه‌های نتایج سخت‌سازی سویچ با شناسه",
    # CIS APIs
    "POST /cis/create": "ایجاد CIS با نام و نسخه",
    "GET /cis/info/{id}": "دریافت اطلاعات CIS با شناسه",
    "GET /cis/list": "دریافت لیست CIS‌ها",
    "PATCH /cis/update/": "به‌روزرسانی CIS با شناسه",
    "DELETE /cis/delete/{id}": "حذف CIS با شناسه",
    # Category APIs
    "POST /category/create": "ایجاد دسته‌بندی با نام، شناسه CIS و شناسه والد",
    "GET /category/info/{id}": "دریافت اطلاعات دسته‌بندی با شناسه",
    "GET /category/list": "دریافت لیست دسته‌بندی‌ها",
    "GET /category/categorizedlist": "دریافت لیست دسته‌بندی‌شده",
    "PATCH /category/update/": "به‌روزرسانی دسته‌بندی با شناسه",
    "DELETE /category/delete/{id}": "حذف دسته‌بندی با شناسه",
    # Role APIs
    "GET /role/list": "دریافت لیست نقش‌ها",
    "PATCH /role/update": "به‌روزرسانی نقش",
    # UserRole APIs
    "POST /userRole/add": "افزودن نقش به کاربر",
    "DELETE /userRole/remove": "حذف نقش از کاربر",
    # Permission APIs
    "GET /permission/listByCategory/{category_id}": "دریافت دسترسی‌های یک دسته",
    "GET /permission/listByCategory": "دریافت دسترسی‌های یک دسته",
    # PermissionCategory APIs
    "GET /permissionCategory/list": "دریافت لیست دسته‌های دسترسی",
    # RolePermission APIs
    "POST /rolePermission/add": "افزودن دسترسی‌ها به نقش‌ها",
    "DELETE /rolePermission/remove": "حذف دسترسی‌ها از نقش‌ها",
    "GET /rolePermission/rolesOfPermission/{permission_id}": "دریافت نقش‌های یک دسترسی",
    "GET /rolePermission/permissionsOfRole/{role_id}": "دریافت دسترسی‌های یک نقش",
    # Docs APIs
    "GET /docs/api_csv": "خروجی گرفتن فایل CSV از API‌ها",
}


def extract_body_fields(details: dict, openapi: dict):  #
    body = ""
    if "requestBody" in details:
        content = details["requestBody"].get("content", {})
        schema = content.get("application/json", {}).get("schema", {})

        # Handle $ref
        if "$ref" in schema:
            schema = resolve_ref(schema["$ref"], openapi)

        props = schema.get("properties", {})
        if props:
            fields = []
            for name, field_schema in props.items():
                field_type = field_schema.get("type", "object")
                fields.append(f"{name}: {field_type}")
            body = ", ".join(fields)
    return body


def resolve_ref(ref: str, openapi: dict):
    """Given a $ref like '#/components/schemas/LoginRequest', return the actual schema."""
    parts = ref.strip("#/").split("/")
    result = openapi
    for part in parts:
        result = result.get(part, {})
    return result


@router.get("/api_csv")
async def export_apis():
    # Step 1 & 2: Fetch OpenAPI spec
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/openapi.json")
        openapi = response.json()

    output = io.StringIO()
    writer = csv.writer(output)

    # Step 4: CSV headers
    writer.writerow(
        [
            "دسته بندی",
            "آدرس",
            "متد",
            "توضیحات",
            "پارامتر درخواست",
            "کوئری های درخواست",
            "بدنه درخواست",
        ]
    )

    for path, methods in openapi.get("paths", {}).items():
        for method, details in methods.items():
            summary = details.get("summary", "")
            description = api_translations.get(f"{method.upper()} {path}", summary)

            # Extract params
            params = [
                p["name"] for p in details.get("parameters", []) if p["in"] == "path"
            ]
            query = [
                p["name"] for p in details.get("parameters", []) if p["in"] == "query"
            ]

            print(details)
            # Extract body fields
            body = extract_body_fields(details, openapi)
            # if "requestBody" in details:
            #     content = details["requestBody"]["content"]
            #     if "application/json" in content:
            #         schema = content["application/json"]["schema"]
            #         body = str(schema.get("properties", {}).keys())

            writer.writerow(
                [
                    path.split("/")[1],
                    path,
                    method.upper(),
                    description,
                    ", ".join(params),
                    ", ".join(query),
                    body,
                ]
            )

    # Step 5: Return CSV file
    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=api_export.csv"},
    )
