"""Validate machine learning runtime dependencies."""

import numpy as np
import torch


def validate_runtime():
    print("NumPy version:", np.__version__)
    print("PyTorch version:", torch.__version__)

    tensor = torch.tensor([1.0, 2.0, 3.0])
    array = tensor.numpy()

    np.testing.assert_allclose(array, [1.0, 2.0, 3.0])

    restored_tensor = torch.from_numpy(array)
    assert torch.equal(tensor, restored_tensor)

    model = torch.nn.Linear(3, 1)
    output = model(tensor)

    assert output.shape == (1,)
    assert torch.isfinite(output).all()

    print("PASS: Tensor creation")
    print("PASS: NumPy conversion")
    print("PASS: PyTorch conversion")
    print("PASS: Neural network inference")
    print("All ML runtime checks passed.")


if __name__ == "__main__":
    validate_runtime()
