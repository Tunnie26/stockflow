from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions import AppError
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:
    def __init__(self, db: Session):
        self.db = db

    def create_customer(self, data: CustomerCreate) -> Customer:
        existing_customer = self.db.scalar(
            select(Customer).where(Customer.code == data.code)
        )

        if existing_customer is not None:
            raise AppError(
                "Customer code already exists",
                code="CUSTOMER_CODE_ALREADY_EXISTS",
            )

        customer = Customer(
            code=data.code,
            name=data.name,
            note=data.note,
        )

        self.db.add(customer)
        self.db.flush()

        return customer

    def list_customers(self) -> list[Customer]:
        statement = select(Customer).order_by(Customer.id)
        return list(self.db.scalars(statement).all())

    def get_customer(self, customer_id: int) -> Customer:
        customer = self.db.scalar(select(Customer).where(Customer.id == customer_id))

        if customer is None:
            raise AppError(
                "Customer not found",
                code="CUSTOMER_NOT_FOUND",
                status_code=404,
            )

        return customer

    def update_customer(
        self,
        customer_id: int,
        data: CustomerUpdate,
    ) -> Customer:
        customer = self.get_customer(customer_id)

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(customer, field, value)

        self.db.flush()

        return customer
