from dataclasses import dataclass


@dataclass
class GetCategoryDetailsQuery:
    """
    .NET'dagi `ProductCategoryDetailsQuery : IRequest<ProductCategoryDetailsVm>` ekvivalenti.
    """
    id: int

