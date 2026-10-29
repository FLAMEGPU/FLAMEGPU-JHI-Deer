import numpy as np
from scipy.ndimage import gaussian_filter


def generate_map(
    dimension,
    max_classes,
    patch_size=15,
    class_weights=None,
    seed=None,
):
    """
    Generate a random 2D land-use raster with spatially clustered patches.

    Parameters
    ----------
    dimension : int
        Raster dimensions width and height
    max_classes : int
        Maximum value of the land class values, e.g. 1 through max_classes.
    patch_size : float
        Approximate spatial scale of patches in pixels.
        Larger values produce larger, smoother patches.
    class_weights : array-like or None
        Relative probabilities for each class. Higher weights favor
        the corresponding class, but proportions are not exact.
    seed : int or None
        Random seed for reproducibility.

    Returns
    -------
    raster : numpy.ndarray
        2D integer raster containing the land-use class labels.
    """
    shape=(dimension, dimension)
    classes=range(1, max_classes)
    rng = np.random.default_rng(seed)
    classes = np.asarray(list(classes))

    if len(classes) == 0:
        raise ValueError("classes must not be empty.")
    if patch_size <= 0:
        raise ValueError("patch_size must be positive.")

    n_classes = len(classes)

    if class_weights is None:
        weights = np.ones(n_classes)
    else:
        weights = np.asarray(class_weights, dtype=float)
        if (
            weights.shape != (n_classes,)
            or not np.all(np.isfinite(weights))
            or np.any(weights < 0)
            or not np.any(weights > 0)
        ):
            raise ValueError(
                "class_weights must be nonnegative, finite, "
                "and have one positive weight per class."
            )

    # Generate one spatially correlated random field per class.
    fields = np.empty(( *shape, n_classes ), dtype=np.float32)

    for i in range(n_classes):
        noise = rng.standard_normal(shape)
        field = gaussian_filter(noise, sigma=patch_size)

        # Standardize each field to make class scores comparable.
        field_std = field.std()
        fields[..., i] = (field - field.mean()) / max(field_std, 1e-10)

    # Bias the class scores according to the relative weights.
    # A zero weight excludes that class entirely.
    scores = fields + np.log(
        np.maximum(weights / weights.max(), 1e-12)
    )[None, None, :]

    scores[..., weights == 0] = -np.inf

    # Assign each pixel to the class with the strongest field.
    raster = classes[np.argmax(scores, axis=-1)]

    return raster