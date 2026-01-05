from app.infrastructure.mapping.AutoMapper import Mapper
from app.domain.entities.Product import Product
from app.application.dtos.ProductDto import ProductDto


class ProductProfile:
    def __init__(self, mapper: Mapper):
        mapper.CreateMap(Product, ProductDto)
        mapper.CreateMap(ProductDto, Product)
