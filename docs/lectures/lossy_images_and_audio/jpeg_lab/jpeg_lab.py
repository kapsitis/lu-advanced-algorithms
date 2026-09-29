#!/usr/bin/env python3
"""
jpeg_lab.py -- a JPEG-like lossy image codec for experiments.

The program reads RGB pixels from a PNG file, runs them through the stages of
baseline JPEG, decodes the result back to pixels and writes another PNG file.
PNG is only a convenient container for pixels; everything in between is done
here, step by step, so that every stage can be changed or switched off from
the command line.

Encoder stages (numbered as in the lecture):
  1. Color space conversion   RGB -> YCbCr (or YIQ, or keep RGB)
  2. Chroma subsampling       4:4:4, 4:2:2, 4:2:0, 4:1:1
  3. Block splitting          N x N blocks, level shift (-128)
  4. Transform                DCT-II (or DST-VII, Hartley, Walsh-Hadamard,
                              Haar, KLT, identity), coefficient selection
  5. Quantization             divide by a quantization table and round
  6. Zig-zag and run-length   (RUN, SIZE) symbols as in baseline JPEG
  7. Entropy coding           not done; the size is estimated from the
                              empirical entropy of the symbols
Decoder: dequantize, inverse transform, merge blocks, optional deblocking
filter, chroma upsampling, conversion back to RGB.

Examples:
  python jpeg_lab.py bumblebee.png out.png
  python jpeg_lab.py bumblebee.png out.png --color-space rgb --chroma-quant-multiplier 2
  python jpeg_lab.py bumblebee.png out.png --block-size 32 --quality 10 --deblocking-filter
  python jpeg_lab.py bumblebee.png out.png --keep-coefficients 3 --energy-compensation scale
  python jpeg_lab.py bumblebee.png out.png --transform walsh-hadamard

Requires numpy and Pillow.  Run with --help for the list of all options.
"""

import argparse
import math
from collections import Counter

import numpy as np
from PIL import Image


# =============================================================================
# Constants
# =============================================================================

# JPEG standard (ISO/IEC 10918-1, Annex K), luminance table K.1 (quality 50).
JPEG_LUMA_TABLE = np.array([
    [16, 11, 10, 16,  24,  40,  51,  61],
    [12, 12, 14, 19,  26,  58,  60,  55],
    [14, 13, 16, 24,  40,  57,  69,  56],
    [14, 17, 22, 29,  51,  87,  80,  62],
    [18, 22, 37, 56,  68, 109, 103,  77],
    [24, 35, 55, 64,  81, 104, 113,  92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103,  99],
], dtype=np.float64)

# JPEG standard, chrominance table K.2 (quality 50).
JPEG_CHROMA_TABLE = np.array([
    [17, 18, 24, 47, 99, 99, 99, 99],
    [18, 21, 26, 66, 99, 99, 99, 99],
    [24, 26, 56, 99, 99, 99, 99, 99],
    [47, 66, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
], dtype=np.float64)

# Color spaces: planes = MATRIX @ (R, G, B) + OFFSET, where R, G, B are in 0..255.
# The first plane is treated as "luma" (brightness), the other two as "chroma".
COLOR_SPACES = {
    # JFIF (the file format of .jpg files), full range 0..255.
    "ycbcr": (np.array([[ 0.299,     0.587,     0.114   ],
                        [-0.168736, -0.331264,  0.5     ],
                        [ 0.5,      -0.418688, -0.081312]]),
              np.array([0.0, 128.0, 128.0])),
    # NTSC YIQ (see the lecture); I and Q are shifted by 128 like Cb and Cr.
    "yiq":   (np.array([[0.299,   0.587,   0.114 ],
                        [0.5959, -0.2746, -0.3213],
                        [0.2115, -0.5227,  0.3112]]),
              np.array([0.0, 128.0, 128.0])),
    # No conversion: R plays the role of Y, G of Cb (I), B of Cr (Q).
    "rgb":   (np.eye(3), np.zeros(3)),
}

# Chroma subsampling: (vertical factor, horizontal factor) for the two chroma planes.
SUBSAMPLING_FACTORS = {
    "4:4:4": (1, 1),
    "4:2:2": (1, 2),
    "4:2:0": (2, 2),
    "4:1:1": (1, 4),
}

TRANSFORM_NAMES = ["dct", "dst7", "hartley", "walsh-hadamard", "haar", "klt", "identity"]

PLANE_NAMES = {
    "ycbcr": ["Y", "Cb", "Cr"],
    "yiq": ["Y", "I", "Q"],
    "rgb": ["R", "G", "B"],
}


# =============================================================================
# Reading and writing pixels (PNG is only a container)
# =============================================================================

def load_rgb_pixels(path):
    """Return an array of shape (height, width, 3) with values 0..255 (float).
    Transparent images are placed on a white background."""
    image = Image.open(path).convert("RGBA")
    background = Image.new("RGBA", image.size, (255, 255, 255, 255))
    image = Image.alpha_composite(background, image).convert("RGB")
    return np.asarray(image, dtype=np.float64)


def save_rgb_pixels(path, rgb):
    pixels = np.clip(np.round(rgb), 0, 255).astype(np.uint8)
    Image.fromarray(pixels).save(path)


def save_gray_pixels(path, gray):
    pixels = np.clip(np.round(gray), 0, 255).astype(np.uint8)
    Image.fromarray(pixels).save(path)


# =============================================================================
# Stage 1: color space conversion
# =============================================================================

def rgb_to_planes(rgb, color_space):
    """RGB image (h, w, 3) -> list of three planes (h, w)."""
    matrix, offset = COLOR_SPACES[color_space]
    converted = rgb @ matrix.T + offset
    return [converted[:, :, c] for c in range(3)]


def planes_to_rgb(planes, color_space):
    """Inverse of rgb_to_planes (the planes must have the same size)."""
    matrix, offset = COLOR_SPACES[color_space]
    stacked = np.stack(planes, axis=-1)
    return (stacked - offset) @ np.linalg.inv(matrix).T


# =============================================================================
# Stage 2: chroma subsampling
# =============================================================================

def subsample(plane, vertical_factor, horizontal_factor):
    """Replace every (vertical_factor x horizontal_factor) rectangle by its average."""
    height, width = plane.shape
    new_height = math.ceil(height / vertical_factor)
    new_width = math.ceil(width / horizontal_factor)
    padded = np.pad(plane, ((0, new_height * vertical_factor - height),
                            (0, new_width * horizontal_factor - width)), mode="edge")
    rectangles = padded.reshape(new_height, vertical_factor, new_width, horizontal_factor)
    return rectangles.mean(axis=(1, 3))


def upsample(plane, vertical_factor, horizontal_factor, height, width):
    """Repeat every sample (nearest neighbor) and crop to height x width."""
    repeated = np.repeat(np.repeat(plane, vertical_factor, axis=0), horizontal_factor, axis=1)
    return repeated[:height, :width]


# =============================================================================
# Stage 3: splitting into blocks
# =============================================================================

def pad_to_multiple(plane, block_size):
    """Pad by repeating the last row and column (as JPEG encoders usually do)."""
    height, width = plane.shape
    pad_rows = (-height) % block_size
    pad_cols = (-width) % block_size
    return np.pad(plane, ((0, pad_rows), (0, pad_cols)), mode="edge")


def split_into_blocks(plane, block_size):
    """(H, W) -> (H/n, W/n, n, n); blocks[i, j] is the block in block-row i, block-column j."""
    height, width = plane.shape
    n = block_size
    return plane.reshape(height // n, n, width // n, n).swapaxes(1, 2)


def merge_blocks(blocks):
    """Inverse of split_into_blocks."""
    block_rows, block_cols, n, _ = blocks.shape
    return blocks.swapaxes(1, 2).reshape(block_rows * n, block_cols * n)


# =============================================================================
# Stage 4: transforms
#
# Every transform is an orthonormal n x n matrix T (T @ T.T = identity).
# A block A is transformed to B = T A T^T and restored by A = T^T B T.
# Row k of T is the k-th basis function; rows are ordered from "smooth" to
# "detailed", so the top-left corner of B holds the low frequencies.
# =============================================================================

def dct_matrix(n):
    """DCT-II (JPEG, MPEG, H.26x): cosines, implicit mirror extension at the edges."""
    k = np.arange(n).reshape(-1, 1)
    i = np.arange(n).reshape(1, -1)
    matrix = np.sqrt(2.0 / n) * np.cos((2 * i + 1) * k * np.pi / (2 * n))
    matrix[0, :] = np.sqrt(1.0 / n)
    return matrix


def dst7_matrix(n):
    """DST-VII (HEVC 4x4 intra luma, AV1 "ADST"): sines that start near 0 at the
    top/left edge and are largest at the bottom/right edge. Designed for
    prediction residuals, which are small next to the already decoded pixels."""
    k = np.arange(n).reshape(-1, 1)
    i = np.arange(n).reshape(1, -1)
    return np.sqrt(4.0 / (2 * n + 1)) * np.sin(np.pi * (2 * k + 1) * (i + 1) / (2 * n + 1))


def hartley_matrix(n):
    """Discrete Hartley transform: cas(x) = cos(x) + sin(x); a real-valued relative
    of the DFT. Like the DFT it treats the block as one period of a periodic signal.
    Rows are reordered by frequency (0, 1, -1, 2, -2, ...)."""
    k = np.arange(n).reshape(-1, 1)
    i = np.arange(n).reshape(1, -1)
    angle = 2 * np.pi * k * i / n
    matrix = (np.cos(angle) + np.sin(angle)) / np.sqrt(n)
    frequency = np.minimum(np.arange(n), n - np.arange(n))
    order = np.argsort(frequency, kind="stable")
    return matrix[order]


def walsh_hadamard_matrix(n):
    """Walsh-Hadamard transform: basis functions take only the values +1 and -1
    (no multiplications needed). Rows are sorted by sequency (number of sign changes).
    H.264 uses a Hadamard transform for the DC coefficients of 4x4 blocks."""
    if n & (n - 1):
        raise ValueError("walsh-hadamard needs a block size that is a power of 2")
    matrix = np.array([[1.0]])
    while matrix.shape[0] < n:
        matrix = np.block([[matrix, matrix], [matrix, -matrix]])
    sign_changes = (np.diff(np.sign(matrix), axis=1) != 0).sum(axis=1)
    return matrix[np.argsort(sign_changes)] / np.sqrt(n)


def haar_matrix(n):
    """Haar wavelet transform (the simplest wavelet; JPEG 2000 uses smoother
    wavelets on the whole image). Basis functions are short steps at several scales."""
    if n & (n - 1):
        raise ValueError("haar needs a block size that is a power of 2")
    matrix = np.array([[1.0]])
    while matrix.shape[0] < n:
        m = matrix.shape[0]
        averages = np.kron(matrix, [1.0, 1.0])
        differences = np.kron(np.eye(m), [1.0, -1.0])
        matrix = np.vstack([averages, differences]) / np.sqrt(2.0)
    return matrix


def klt_matrix(n, sample_plane):
    """Karhunen-Loeve transform (PCA): eigenvectors of the correlation matrix of
    the rows and columns of all blocks of sample_plane. It is the best orthonormal
    transform for this particular image, but the decoder would need the matrix
    (n*n extra numbers) and computing it is expensive."""
    blocks = split_into_blocks(pad_to_multiple(sample_plane, n), n)
    rows = blocks.reshape(-1, n)
    columns = blocks.swapaxes(2, 3).reshape(-1, n)
    vectors = np.vstack([rows, columns])
    correlation = vectors.T @ vectors / len(vectors)
    eigenvalues, eigenvectors = np.linalg.eigh(correlation)
    order = np.argsort(eigenvalues)[::-1]          # largest "energy" first
    matrix = eigenvectors[:, order].T
    signs = np.where(matrix.sum(axis=1) < 0, -1.0, 1.0)  # cosmetic: make rows start "positive"
    return matrix * signs.reshape(-1, 1)


def transform_matrix(name, n, sample_plane):
    if name == "dct":
        return dct_matrix(n)
    if name == "dst7":
        return dst7_matrix(n)
    if name == "hartley":
        return hartley_matrix(n)
    if name == "walsh-hadamard":
        return walsh_hadamard_matrix(n)
    if name == "haar":
        return haar_matrix(n)
    if name == "klt":
        return klt_matrix(n, sample_plane)
    if name == "identity":
        return np.eye(n)
    raise ValueError(f"unknown transform {name}")


def forward_transform(blocks, matrix):
    return matrix @ blocks @ matrix.T


def inverse_transform(coefficients, matrix):
    return matrix.T @ coefficients @ matrix


# =============================================================================
# Stage 4b (not in JPEG): keep only low frequencies, compensate the lost energy
# =============================================================================

def low_frequency_mask(block_size, keep):
    """True for the top-left keep x keep corner of a block."""
    mask = np.zeros((block_size, block_size), dtype=bool)
    mask[:keep, :keep] = True
    return mask


def drop_high_frequencies(coefficients, keep):
    """Set every coefficient outside the top-left keep x keep corner to 0.
    Returns the new coefficients and the dropped energy (sum of squares) of each block."""
    kept = low_frequency_mask(coefficients.shape[-1], keep)
    dropped_energy = (coefficients ** 2 * ~kept).sum(axis=(-2, -1), keepdims=True)
    return np.where(kept, coefficients, 0.0), dropped_energy


def scale_up_kept_coefficients(coefficients, dropped_energy, keep):
    """Energy compensation "scale" (encoder): multiply the kept AC coefficients of each
    block so that the block's AC energy is the same as before dropping. Low frequencies
    get "louder" instead of adding the missing high frequencies."""
    ac = low_frequency_mask(coefficients.shape[-1], keep)
    ac[0, 0] = False
    kept_ac_energy = (coefficients ** 2 * ac).sum(axis=(-2, -1), keepdims=True)
    has_ac = kept_ac_energy > 0
    factor = np.sqrt((kept_ac_energy + dropped_energy) / np.where(has_ac, kept_ac_energy, 1.0))
    return np.where(ac & has_ac, coefficients * factor, coefficients)


def fill_dropped_with_noise(coefficients, dropped_energy, keep, rng):
    """Energy compensation "noise" (decoder): put random values of the right total energy
    into the dropped positions ("noise filling", as in audio codecs). The encoder sends
    only one number per block (dropped_energy); the noise itself is made by the decoder."""
    dropped = ~low_frequency_mask(coefficients.shape[-1], keep)
    noise = rng.standard_normal(coefficients.shape) * dropped
    noise_energy = (noise ** 2).sum(axis=(-2, -1), keepdims=True)
    noise *= np.sqrt(dropped_energy / np.where(noise_energy > 0, noise_energy, 1.0))
    return np.where(dropped, noise, coefficients)


# =============================================================================
# Stage 5: quantization
# =============================================================================

def scale_table_by_quality(table, quality):
    """libjpeg quality scaling: quality 50 = the table itself, 100 = all ones."""
    if quality < 50:
        scale = 5000.0 / quality
    else:
        scale = 200.0 - 2.0 * quality
    return np.maximum(1.0, np.floor((scale * table + 50.0) / 100.0))


def resize_table(table, block_size):
    """Stretch (or shrink) an 8x8 table to block_size x block_size, so that the same
    fraction of the frequency range gets the same quantization step.
    (For orthonormal transforms a step Q means the same pixel error for every n.)"""
    index = (np.arange(block_size) * 8) // block_size
    return table[np.ix_(index, index)]


def make_quantization_tables(settings):
    """Return three tables (one per plane) of size block_size x block_size."""
    n = settings.block_size
    if settings.quant_table == "standard":
        luma_base, chroma_base = JPEG_LUMA_TABLE, JPEG_CHROMA_TABLE
    elif settings.quant_table == "luma-for-all":
        luma_base, chroma_base = JPEG_LUMA_TABLE, JPEG_LUMA_TABLE
    else:  # "flat"
        luma_base = np.full((8, 8), settings.flat_step)
        chroma_base = luma_base
    luma = scale_table_by_quality(resize_table(luma_base, n), settings.quality)
    chroma = scale_table_by_quality(resize_table(chroma_base, n), settings.quality)
    luma = np.maximum(1.0, np.round(luma * settings.luma_quant_multiplier))
    chroma = np.maximum(1.0, np.round(chroma * settings.chroma_quant_multiplier))
    return [luma, chroma, chroma]


def quantize(coefficients, table, rounding):
    ratio = coefficients / table
    if rounding == "nearest":
        return np.round(ratio)
    if rounding == "floor":
        return np.floor(ratio)
    if rounding == "toward-zero":
        return np.trunc(ratio)
    raise ValueError(f"unknown rounding {rounding}")


def dequantize(quantized, table):
    return quantized * table


# =============================================================================
# Stages 6-7: zig-zag order, run-length symbols, size estimate
# =============================================================================

def zigzag_order(n):
    """List of (row, column) positions in zig-zag order for an n x n block."""
    positions = [(r, c) for r in range(n) for c in range(n)]
    return sorted(positions, key=lambda p: (p[0] + p[1], p[0] if (p[0] + p[1]) % 2 else -p[0]))


def size_category(value):
    """JPEG "SIZE": number of bits needed for |value| (0 for value 0)."""
    return int(abs(value)).bit_length()


def entropy_bits(symbols):
    """Total bits if every symbol is coded with -log2(p) bits (an ideal entropy coder;
    a Huffman code needs at most 1 bit per symbol more)."""
    counts = Counter(symbols)
    total = len(symbols)
    return -sum(c * math.log2(c / total) for c in counts.values())


def estimate_plane_bits(quantized_blocks):
    """Estimate the compressed size of one plane in bits, following baseline JPEG:
    DC coefficients are coded as differences to the previous block (symbol SIZE plus
    SIZE extra bits); AC coefficients as (RUN, SIZE) symbols plus extra bits, with
    ZRL = (15, 0) for 16 zeros and EOB = (0, 0) for "only zeros remain"."""
    n = quantized_blocks.shape[-1]
    order = zigzag_order(n)
    rows = np.array([p[0] for p in order])
    cols = np.array([p[1] for p in order])
    zigzag = quantized_blocks[..., rows, cols].reshape(-1, n * n).astype(np.int64)

    dc_symbols, ac_symbols = [], []
    extra_bits = 0
    previous_dc = 0
    for block in zigzag:
        difference = block[0] - previous_dc
        previous_dc = block[0]
        dc_symbols.append(size_category(difference))
        extra_bits += size_category(difference)

        run = 0
        last_nonzero = np.flatnonzero(block[1:])
        end = last_nonzero[-1] + 1 if len(last_nonzero) else 0
        for value in block[1:end + 1]:
            if value == 0:
                run += 1
                continue
            while run > 15:
                ac_symbols.append((15, 0))
                run -= 16
            ac_symbols.append((run, size_category(value)))
            extra_bits += size_category(value)
            run = 0
        if end < n * n - 1:
            ac_symbols.append((0, 0))  # EOB
    return entropy_bits(dc_symbols) + entropy_bits(ac_symbols) + extra_bits


# =============================================================================
# Decoder extra: a simple deblocking filter
# =============================================================================

def deblock_vertical_edges(plane, block_size, threshold):
    """Smooth the step across every vertical block edge, if the step is small
    (probably a blocking artifact) and both sides are smooth. A large step is
    kept, because it is probably a real edge in the picture.
    Pixels p2 p1 p0 | q0 q1 q2 : the step d = q0 - p0 is replaced by a ramp."""
    result = plane.copy()
    width = plane.shape[1]
    for x in range(block_size, width - 2, block_size):
        if x < 3:
            continue
        p2, p1, p0 = plane[:, x - 3], plane[:, x - 2], plane[:, x - 1]
        q0, q1, q2 = plane[:, x], plane[:, x + 1], plane[:, x + 2]
        step = q0 - p0
        is_artifact = ((np.abs(step) < threshold)
                       & (np.abs(p2 - p0) < threshold / 2)
                       & (np.abs(q2 - q0) < threshold / 2))
        d = np.where(is_artifact, step, 0.0)
        result[:, x - 1] += 3 * d / 7
        result[:, x - 2] += 2 * d / 7
        result[:, x - 3] += 1 * d / 7
        result[:, x] -= 3 * d / 7
        result[:, x + 1] -= 2 * d / 7
        result[:, x + 2] -= 1 * d / 7
    return result


def deblock(plane, block_size, threshold):
    plane = deblock_vertical_edges(plane, block_size, threshold)
    return deblock_vertical_edges(plane.T, block_size, threshold).T


# =============================================================================
# Encoder and decoder of one plane
# =============================================================================

def encode_plane(plane, transform, table, settings):
    """Stages 3-5 for one plane. Returns the quantized coefficient blocks and the
    dropped energy of each block (side information for --energy-compensation noise)."""
    padded = pad_to_multiple(plane, settings.block_size)
    blocks = split_into_blocks(padded, settings.block_size)
    if settings.level_shift:
        blocks = blocks - 128.0
    coefficients = forward_transform(blocks, transform)
    dropped_energy = None
    if settings.keep_coefficients < settings.block_size:
        coefficients, dropped_energy = drop_high_frequencies(coefficients, settings.keep_coefficients)
        if settings.energy_compensation == "scale":
            coefficients = scale_up_kept_coefficients(coefficients, dropped_energy, settings.keep_coefficients)
    return quantize(coefficients, table, settings.rounding), dropped_energy


def decode_plane(quantized, dropped_energy, transform, table, height, width, settings, rng):
    """Inverse of encode_plane (plus the optional deblocking filter)."""
    coefficients = dequantize(quantized, table)
    if settings.energy_compensation == "noise" and dropped_energy is not None:
        coefficients = fill_dropped_with_noise(coefficients, dropped_energy, settings.keep_coefficients, rng)
    blocks = inverse_transform(coefficients, transform)
    if settings.level_shift:
        blocks = blocks + 128.0
    plane = merge_blocks(blocks)
    if settings.deblocking_filter:
        plane = deblock(plane, settings.block_size, settings.deblocking_threshold)
    return plane[:height, :width]


# =============================================================================
# Whole pipeline
# =============================================================================

def run_codec(rgb, settings):
    height, width, _ = rgb.shape
    rng = np.random.default_rng(settings.random_seed)
    vertical_factor, horizontal_factor = SUBSAMPLING_FACTORS[settings.chroma_subsampling]

    # Stage 1: color space conversion
    planes = rgb_to_planes(rgb, settings.color_space)

    # Stage 2: chroma subsampling (planes 1 and 2 only)
    stored_planes = [planes[0]] + [subsample(p, vertical_factor, horizontal_factor) for p in planes[1:]]

    # Stages 3-5 (encoder), 6-7 (size estimate) and decoder, plane by plane
    luma_for_klt = planes[0] - (128.0 if settings.level_shift else 0.0)
    transform = transform_matrix(settings.transform, settings.block_size, luma_for_klt)
    tables = make_quantization_tables(settings)

    decoded_planes = []
    total_bits = 0.0
    nonzero_count = 0
    for index, plane in enumerate(stored_planes):
        quantized, dropped_energy = encode_plane(plane, transform, tables[index], settings)
        total_bits += estimate_plane_bits(quantized)
        if dropped_energy is not None and settings.energy_compensation != "none":
            total_bits += 8 * dropped_energy.size   # one 8-bit energy value per block
        nonzero_count += int(np.count_nonzero(quantized))
        decoded = decode_plane(quantized, dropped_energy, transform, tables[index],
                               plane.shape[0], plane.shape[1], settings, rng)
        decoded_planes.append(decoded)

    # Decoder: chroma upsampling and conversion back to RGB
    full_size_planes = [decoded_planes[0]] + [
        upsample(p, vertical_factor, horizontal_factor, height, width) for p in decoded_planes[1:]]
    decoded_rgb = planes_to_rgb(full_size_planes, settings.color_space)

    report = {
        "transform": transform,
        "tables": tables,
        "bits": total_bits,
        "nonzero": nonzero_count,
        "planes_before": planes,
        "planes_after": full_size_planes,
    }
    return np.clip(np.round(decoded_rgb), 0, 255), report


# =============================================================================
# Reporting
# =============================================================================

def psnr(mse):
    return float("inf") if mse == 0 else 10 * math.log10(255.0 ** 2 / mse)


def print_report(original, decoded, report, settings):
    height, width, _ = original.shape
    pixels = height * width
    names = PLANE_NAMES[settings.color_space]
    print(f"Image: {width} x {height} pixels")
    print(f"Settings: color space {settings.color_space} ({'/'.join(names)}), "
          f"subsampling {settings.chroma_subsampling}, block {settings.block_size}x{settings.block_size}, "
          f"transform {settings.transform}, quality {settings.quality}")
    if settings.print_tables:
        np.set_printoptions(linewidth=200, precision=3, suppress=True)
        print("Transform matrix (rows = basis functions):")
        print(report["transform"])
        print(f"Quantization table for {names[0]}:")
        print(report["tables"][0].astype(int))
        print(f"Quantization table for {names[1]} and {names[2]}:")
        print(report["tables"][1].astype(int))
    errors = (original - decoded) ** 2
    for channel, name in enumerate("RGB"):
        mse = errors[:, :, channel].mean()
        print(f"  {name}: MSE {mse:8.2f}   PSNR {psnr(mse):6.2f} dB")
    mse = errors.mean()
    print(f"  all: MSE {mse:8.2f}   PSNR {psnr(mse):6.2f} dB")
    bits = report["bits"]
    print(f"Nonzero quantized coefficients: {report['nonzero']} "
          f"({report['nonzero'] / pixels:.3f} per pixel)")
    print(f"Estimated size: {bits / 8 / 1024:.1f} KiB = {bits / pixels:.3f} bits per pixel "
          f"(compression ratio {24 * pixels / bits:.1f} : 1 compared to 24 bits per pixel)")


def save_difference_image(path, original, decoded, amplification):
    """Gray 128 = no error; lighter/darker = decoded value too large/too small."""
    difference = (decoded - original).mean(axis=2)
    save_gray_pixels(path, 128 + amplification * difference)


def save_planes_image(path, report):
    """Top row: the three planes after stage 1; bottom row: the same planes after decoding."""
    top = np.hstack(report["planes_before"])
    bottom = np.hstack(report["planes_after"])
    save_gray_pixels(path, np.vstack([top, bottom]))


# =============================================================================
# Command line
# =============================================================================

def parse_settings():
    parser = argparse.ArgumentParser(
        description="JPEG-like lossy codec with adjustable stages (see the module docstring).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("input_png", help="input image (PNG or any format Pillow can read)")
    parser.add_argument("output_png", help="decoded image to write")

    stage1 = parser.add_argument_group("stage 1: color space")
    stage1.add_argument("--color-space", choices=sorted(COLOR_SPACES), default="ycbcr",
                        help="rgb = no conversion (R, G, B are coded as if they were Y, Cb, Cr)")

    stage2 = parser.add_argument_group("stage 2: chroma subsampling")
    stage2.add_argument("--chroma-subsampling", choices=list(SUBSAMPLING_FACTORS), default="4:2:0")

    stage3 = parser.add_argument_group("stage 3: blocks")
    stage3.add_argument("--block-size", type=int, default=8)
    stage3.add_argument("--no-level-shift", dest="level_shift", action="store_false",
                        help="do not subtract 128 before the transform")

    stage4 = parser.add_argument_group("stage 4: transform and coefficient selection")
    stage4.add_argument("--transform", choices=TRANSFORM_NAMES, default="dct")
    stage4.add_argument("--keep-coefficients", type=int, default=None, metavar="K",
                        help="keep only the top-left K x K coefficients of each block (default: all)")
    stage4.add_argument("--energy-compensation", choices=["none", "scale", "noise"], default="none",
                        help="what to do with the energy of the dropped coefficients")
    stage4.add_argument("--random-seed", type=int, default=1, help="for --energy-compensation noise")

    stage5 = parser.add_argument_group("stage 5: quantization")
    stage5.add_argument("--quality", type=int, default=50, help="1..100, libjpeg scaling of the tables")
    stage5.add_argument("--quant-table", choices=["standard", "luma-for-all", "flat"], default="standard",
                        help="standard = JPEG Annex K tables; flat = every entry equals --flat-step")
    stage5.add_argument("--flat-step", type=float, default=16.0, help="entry of the flat table at quality 50")
    stage5.add_argument("--luma-quant-multiplier", type=float, default=1.0,
                        help="multiply the table of plane 1 (Y, or R for --color-space rgb)")
    stage5.add_argument("--chroma-quant-multiplier", type=float, default=1.0,
                        help="multiply the table of planes 2 and 3 (Cb/Cr, I/Q, or G/B)")
    stage5.add_argument("--rounding", choices=["nearest", "floor", "toward-zero"], default="nearest")

    decoder = parser.add_argument_group("decoder")
    decoder.add_argument("--deblocking-filter", action="store_true", help="smooth small steps at block edges")
    decoder.add_argument("--deblocking-threshold", type=float, default=24.0,
                         help="steps larger than this are treated as real edges and kept")

    output = parser.add_argument_group("extra output")
    output.add_argument("--difference-png", metavar="PATH", help="write the (amplified) error image")
    output.add_argument("--difference-amplification", type=float, default=4.0)
    output.add_argument("--planes-png", metavar="PATH",
                        help="write the three planes before (top) and after (bottom) coding, as gray images")
    output.add_argument("--print-tables", action="store_true",
                        help="print the transform matrix and the quantization tables")

    settings = parser.parse_args()
    if settings.keep_coefficients is None:
        settings.keep_coefficients = settings.block_size
    if not 1 <= settings.keep_coefficients <= settings.block_size:
        parser.error("--keep-coefficients must be between 1 and --block-size")
    if not 1 <= settings.quality <= 100:
        parser.error("--quality must be between 1 and 100")
    if settings.block_size < 1:
        parser.error("--block-size must be positive")
    if settings.transform in ("walsh-hadamard", "haar") and settings.block_size & (settings.block_size - 1):
        parser.error(f"--transform {settings.transform} needs a --block-size that is a power of 2")
    return settings


def main():
    settings = parse_settings()
    original = load_rgb_pixels(settings.input_png)
    decoded, report = run_codec(original, settings)
    save_rgb_pixels(settings.output_png, decoded)
    print_report(original, decoded, report, settings)
    if settings.difference_png:
        save_difference_image(settings.difference_png, original, decoded, settings.difference_amplification)
    if settings.planes_png:
        save_planes_image(settings.planes_png, report)


if __name__ == "__main__":
    main()
