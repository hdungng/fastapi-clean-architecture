from typing import List
from fastapi import APIRouter, Depends

from app.application.dtos.ProductDto import ProductDto
from app.application.services.IProductService import IProductService
from app.application.services.ProductService import ProductService
from app.domain.repositories.IUnitOfWork import IUnitOfWork
from app.infrastructure.db.DbContext import DbContext
from app.infrastructure.repositories.UnitOfWork import UnitOfWork
from app.infrastructure.auth.Authorization import RequireRoles, RequirePermissions, UserPrincipal
from app.shared.api_responses import Ok, NotFound, Created, BadRequest


router = APIRouter(prefix="/api/products", tags=["Products"])


def GetDbContext():
    """Factory DbContext cho mỗi request (giống AddDbContext)."""
    db = DbContext()
    try:
        yield db
    finally:
        db.Dispose()


def GetUnitOfWork(db: DbContext = Depends(GetDbContext)) -> IUnitOfWork:
    """Resolve IUnitOfWork dùng DbContext."""
    return UnitOfWork(db)


def GetService(uow: IUnitOfWork = Depends(GetUnitOfWork)) -> IProductService:
    """Resolve IProductService từ UnitOfWork."""
    return ProductService(uow)


@router.get("")
async def GetProducts(
    service: IProductService = Depends(GetService),
    principal: UserPrincipal = Depends(RequireRoles("Admin")),
):
    """
    GET /api/products

    Summary:
    - Lấy tất cả sản phẩm.

    Authorization:
    - Role bắt buộc: Admin (RequireRoles("Admin"))
    - Permission có thể được check mềm trong business nếu cần.
    """
    items = await service.GetAll()
    return Ok(items)


@router.get("/{id}")
async def GetProductById(
    id: int,
    service: IProductService = Depends(GetService),
    principal: UserPrincipal = Depends(RequirePermissions("Products.Read", enforce=True)),
):
    """
    GET /api/products/{id}

    Summary:
    - Lấy thông tin sản phẩm theo Id.

    Authorization:
    - Permission bắt buộc: Products.Read (RequirePermissions(..., enforce=True))
    """
    result = await service.GetById(id)
    if not result:
        return NotFound("Product not found")
    return Ok(result)


@router.post("")
async def CreateProduct(
    dto: ProductDto,
    service: IProductService = Depends(GetService),
    principal: UserPrincipal = Depends(RequirePermissions("Products.Write", enforce=True)),
):
    """
    POST /api/products

    Summary:
    - Tạo mới sản phẩm.

    Authorization:
    - Permission bắt buộc: Products.Write

    Returns:
    - 201: ApiResponse[ProductDto]
    """
    if dto.Id is not None:
        return BadRequest("Id must be null when creating a new product")
    created = await service.Create(dto)
    location = f"/api/products/{created.Id}"
    return Created(location, created)


@router.put("/{id}")
async def UpdateProduct(
    id: int,
    dto: ProductDto,
    service: IProductService = Depends(GetService),
    principal: UserPrincipal = Depends(RequirePermissions("Products.Write", enforce=True)),
):
    """
    PUT /api/products/{id}

    Summary:
    - Cập nhật sản phẩm theo Id.

    Authorization:
    - Permission bắt buộc: Products.Write
    """
    updated = await service.Update(id, dto)
    return Ok(updated)


@router.delete("/{id}")
async def DeleteProduct(
    id: int,
    service: IProductService = Depends(GetService),
    principal: UserPrincipal = Depends(RequirePermissions("Products.Write", enforce=True)),
):
    """
    DELETE /api/products/{id}

    Summary:
    - Xoá sản phẩm theo Id.

    Authorization:
    - Permission bắt buộc: Products.Write
    """
    await service.Delete(id)
    return Ok({"message": "Product deleted"})
