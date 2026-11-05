from dataclasses import dataclass


@dataclass
class DeleteCategoryCommand:
    """
    .NET'dagi `DeleteProductCategoryCommand : IRequest` ekvivalenti.
    """
    id: int

