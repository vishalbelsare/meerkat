from typing import List, Union

import numpy as np
import torch

from meerkat.block.abstract import BlockView
from meerkat.block.numpy_block import NumPyBlock
from meerkat.block.torch_block import TorchBlock

from ..abstract import Column

TensorColumnTypes = Union[np.ndarray, torch.TensorType]


class TensorColumn(Column):
    def __new__(cls, data: TensorColumnTypes = None, backend: str = None):
        from .numpy import NumPyTensorColumn
        from .torch import TorchTensorColumn

        backends = {"torch": TorchTensorColumn, "numpy": NumPyTensorColumn}

        if backend is not None:
            if backend not in backends:
                raise ValueError(
                    f"Backend {backend} not supported. "
                    f"Expected one of {list(backends.keys())}"
                )
            else:
                return super().__new__(backends[backend])

        if isinstance(data, BlockView):
            if isinstance(data.block, TorchBlock):
                backend = TorchTensorColumn
            elif isinstance(data.block, NumPyBlock):
                backend = NumPyTensorColumn

        if (cls is not TensorColumn) or (data is None):
            return super().__new__(cls)

        if isinstance(data, BlockView):
            if isinstance(data.block, TorchBlock):
                from .torch import TorchTensorColumn

                return super().__new__(TorchTensorColumn)
            elif isinstance(data.block, NumPyBlock):
                from .numpy import NumPyTensorColumn

                return super().__new__(NumPyTensorColumn)

        if isinstance(data, np.ndarray):
            from .numpy import NumPyTensorColumn

            return super().__new__(NumPyTensorColumn)
        elif torch.is_tensor(data):
            from .torch import TorchTensorColumn

            return super().__new__(TorchTensorColumn)
        elif isinstance(data, List):
            if len(data) == 0:
                raise ValueError(
                    "Cannot create `TensorColumn` from empty list of tensors."
                )
            elif torch.is_tensor(data[0]):
                from .torch import TorchTensorColumn

                return super().__new__(TorchTensorColumn)
            else:
                from .numpy import NumPyTensorColumn

                return super().__new__(NumPyTensorColumn)

        else:
            raise ValueError(
                f"Cannot create `TensorColumn` from object of type {type(data)}."
            )
