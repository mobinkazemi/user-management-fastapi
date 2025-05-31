from router import routes as api_router

from permissionsCategory.repository import PermissionCategoryRepository
from permissions.repository import PermissionRepository
from seeder.constants.permission_dictionary import permissions_dict

prRepo = PermissionRepository()
prCategoryRepo = PermissionCategoryRepository()

category_translator = {
    "postman": "داکیومنت API ها",
    "switches": "مدیریت سوییچ ها",
    "auth": "مدیریت احراز هویت",
    "os": "مدیریت سیستم عامل",
    "hardening": "مدیریت هاردنینگ",
    "hardeningResults": "مدیریت گزارش های هاردنینگ",
    "cis": "مدیریت داکیومنت سی-آی-اس",
    "category": "مدیریت دسته بندی ها",
    "role": "مدیریت نقش ها",
    "userRole": "مدیریت نقش های کاربران",
}
undefined_category = "نامشخص"


def permission_and_permissionCategory_seeder():

    permission_category_seeder()

    permission_seeder()


def permission_category_seeder():
    for item in category_translator:
        if prCategoryRepo.findOne(name=category_translator.get(item, None)):
            continue
        prCategoryRepo.createOne({"name": category_translator.get(item), "ref": item})

    if prCategoryRepo.findOne(name=undefined_category):
        return
    prCategoryRepo.createOne({"name": undefined_category})


def permission_seeder():
    permissionDictlist = []
    for route in api_router.routes:
        path: str = route.path
        method = next(iter(route.methods))
        category = path.split("/")[1]
        db_category = prCategoryRepo.findOne(
            name=category_translator.get(category, None), ref=category
        )
        if not db_category:
            db_category = prCategoryRepo.findOne(name=undefined_category)

        if not prRepo.findOne(
            method=method,
            url=path,
        ):
            prRepo.createOne(
                dict(
                    {
                        "method": method,
                        "url": path,
                        "category_id": db_category.get("id"),
                        "text": permissions_dict.get(path, ""),
                    }
                )
            )
