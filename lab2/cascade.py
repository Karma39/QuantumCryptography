import numpy as np
import libraries.error_correction_lib as ec

bsc_channel = ec.add_errors
fixed_error_channel = ec.add_errors_prec

def parity(bits):
    """
    Compute parity (XOR) of a bit array
    """
    return np.sum(bits) % 2

def generate_block_sizes(constant, qber, rounds):
    block_sizes = []
    block_sizes.append(int(constant / qber))
    for i in range(1, rounds):
        block_sizes.append(2 * block_sizes[i-1])
    return block_sizes

def binary_search_error(alice_block, bob_block):
    """
    Locate a single error via binary search.

    Returns:
        error_index (int)
        disclosed_bits (int)
    """
    disclosed = 0
    left, right = 0, len(alice_block)

    while right - left > 1:
        mid = (left + right) // 2

        disclosed += 1
        if parity(alice_block[left:mid]) != parity(bob_block[left:mid]):
            right = mid
        else:
            left = mid

    return left, disclosed

def compute_metrics(cascade_results):
    f1_rslts = []
    f2_rslts = []
    lambdas_ec = []
    nzs = []
    success_cont = 0
    for cascade_result in cascade_results:
        qber = cascade_result["qber"]
        bits_disclosed = cascade_result["bits_disclosed"]
        key_length = len(cascade_result["alice_key"])
        hq = ec.h_b(qber)

        lambda_ec = bits_disclosed
        nz = key_length

        f1 = lambda_ec / (nz * hq) if hq > 0 else np.inf
        f2 = lambda_ec - nz * hq
        f1_rslts.append(f1)
        f2_rslts.append(f2)
        lambdas_ec.append(lambda_ec)
        nzs.append(nz)
        if cascade_result["success"]:
            success_cont += 1

    return {
        "qber": qber,
        "lambda_ec_mean": np.mean(lambdas_ec),
        "nz_mean": np.mean(nzs),
        "f1_mean": np.mean(f1_rslts),
        "f2_mean": np.mean(f2_rslts),
        "success_rate": success_cont / len(cascade_results),
    }

def cascade_round(alice, bob, block_size, permutation):
    """
    Execute one Cascade round
    """
    alice_p = alice[permutation]
    bob_p = bob[permutation].copy()

    n = len(alice)
    bits_disclosed = 0
    corrections = 0

    for i in range(0, n, block_size):
        a_block = alice_p[i:i + block_size]
        b_block = bob_p[i:i + block_size]

        bits_disclosed += 1
        if parity(a_block) != parity(b_block):
            idx, disclosed = binary_search_error(a_block, b_block)
            bits_disclosed += disclosed
            b_block[idx] = 1 - b_block[idx]
            corrections += 1

    # Undo permutation
    inverse_perm = np.argsort(permutation)
    bob[:] = bob_p[inverse_perm]

    return {
        "bits_disclosed": bits_disclosed,
        "corrections": corrections,
    }

def cascade_protocol(
    key_length,
    channel_fn,
    qber,
    rounds,
    block_sizes,
):
    """
    Run Cascade protocol with coherent key generation
    """
    alice_key = ec.generate_key(key_length)
    bob_key = channel_fn(alice_key.copy(),qber)
    total_disclosed = 0
    total_corrections = 0
    for r in range(rounds):
        permutation = np.random.permutation(key_length)

        round_result = cascade_round(
            alice_key,
            bob_key,
            block_sizes[r],
            permutation
        )

        total_disclosed += round_result["bits_disclosed"]
        total_corrections += round_result["corrections"]

    success = np.array_equal(alice_key, bob_key)

    return {
        "success": success,
        "qber": qber,
        "alice_key": alice_key,
        "bob_key": bob_key,
        "rounds": rounds,
        "bits_disclosed": total_disclosed,
        "corrections": total_corrections,
    }
