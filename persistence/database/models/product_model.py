from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from persistence.database.appdbcontext import Base


class ProductModel(Base):
    """
    PostgreSQL 'products' jadvali uchun SQLAlchemy ORM modeli.
    .NET: public class Product jadval konfiguratsiyasi
    """
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    price: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # 1. Foreign Key: categories jadvalining 'id' ustuniga bog'lanish
    # .NET: public int CategoryId { get; set; }
    category_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("categories.id", ondelete="RESTRICT"), 
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=text("true"), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("false"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # 2. Navigation Property (Bog'liqlik)
    # .NET: public virtual Category Category { get; set; }
    category = relationship("CategoryModel", backref="products")