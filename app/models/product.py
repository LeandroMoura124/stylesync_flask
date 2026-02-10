from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from bson import ObjectId

class Product(BaseModel):
    id: Optional[ObjectId] = Field(None, alias='_id')
    name: str
    price: float
    description: Optional[str] = None
    stock: int

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class ProductDBModel(Product):
    def model_dump(self, *, mode = 'python', include = None, exclude = None, context = None, by_alias: bool | None = None, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, exclude_computed_fields: bool = False, round_trip: bool = False, warnings: bool = True, fallback = None, serialize_as_any: bool = False) -> dict[str, None]:
        data = super().model_dump(mode=mode, include=include, exclude=exclude, context=context, by_alias=by_alias, exclude_unset=exclude_unset, exclude_defaults=exclude_defaults, exclude_none=exclude_none, exclude_computed_fields=exclude_computed_fields, round_trip=round_trip, warnings=warnings, fallback=fallback, serialize_as_any=serialize_as_any)
        if self.id:
            key = '_id' if by_alias else 'id'
            if key in data:
                data[key] = str(data[key])
        return data
