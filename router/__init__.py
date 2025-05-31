from fastapi import APIRouter
from auth.routes.auth_router import router as auth_router
from public.routers.public_router import router as public_router
from roles.routes.roles_router import router as role_router
from syncPostman.routes import postman_router
from userRole.routes.user_roles_router import router as userRole_router
from permissionsCategory.routers.permission_category_router import (
    router as permission_category_router,
)
from rolePermissions.routes.roles_permission_router import (
    router as rolePermission_router,
)
from syncPostman.routes.postman_router import router as postman_router
from permissions.routes.permissions_router import router as permissions_router
from docs.code.doc_router import router as doc_router
from users.routes.myself.user_router import router as user_myself_router
from users.routes.admin.user_router import router as user_admin_router

routes = APIRouter()

#
#
#
# Public routes
#
routes.include_router(public_router, prefix="", tags=["PUBLIC"])


#
#
#
# Auth routes
routes.include_router(auth_router, prefix="/auth", tags=["auth"])


#
#
#
#
# Roles routes
#
routes.include_router(role_router, prefix="/role", tags=["ROLE"])

#
#
#
# User Role routes
routes.include_router(
    userRole_router,
    prefix="/userRole",
    tags=["USER ROLE"],
)


#
#
#
# Permission routes
routes.include_router(
    permissions_router,
    prefix="/permission",
    tags=["PERMISSION"],
)

#
#
#
# Permission Category routes
routes.include_router(
    permission_category_router,
    prefix="/permissionCategory",
    tags=["PERMISSION CATEGORY"],
)


#
#
#
# Role Permission routes
routes.include_router(
    rolePermission_router,
    prefix="/rolePermission",
    tags=["ROLE PERMISSION"],
)


#
#
#
# Docs routes
routes.include_router(
    doc_router,
    prefix="/docs",
    tags=["DOCS"],
)


#
#
#
# User routes
routes.include_router(user_myself_router, prefix="/user/myself", tags=["USER MYSELF"])
routes.include_router(user_admin_router, prefix="/user/admin", tags=["USER ADMIN"])
