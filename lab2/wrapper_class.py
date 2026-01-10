import libraries.error_correction_lib as ec
import numpy as np

bsc_channel = ec.add_errors
fixed_error_channel = ec.add_errors_prec

# I was thinking of adding more rate option but for fixed p_n and s_n it makes no sense

def test_ec_fixed(qber, R_range, codes, n, n_tries, s_n = -1, p_n = -1, channel = ec.add_errors, f_start=1, show=1, discl_k=1):
    #same as test_ec but for fixed R, s_n and p_n whitou
    if s_n == -1 or p_n == -1:
        print("auto chose sn and pn")
        R, s_n, p_n = ec.choose_sp(qber, f_start, R_range, n)
    else:
        print("fixed sn and pn:", s_n, p_n)
        R = R_range[0]  # just take the first one
    k_n = n-s_n-p_n
    m = (1-R)*n
    code_params = codes[(R, n)]
    s_y_joins = code_params['s_y_joins']
    y_s_joins = code_params['y_s_joins']
    punct_list = code_params['punct_list']
    syndrome_len = code_params['syndrome_len']
    p_n_max = len(punct_list)
    discl_n = int(round(n*(0.0280-0.02*R)*discl_k))
    qber_est = qber
    f1_rslt = []
    f2_rslt = []
    com_iters_rslt = []
    n_incor = 0

    print("QBER = ", qber, "R =", R, "s_n =", s_n, "p_n =",
          p_n, '(', p_n_max, ')', 'discl_n', discl_n)

    for i in range(n_tries):
        print(i, end=' ')
        x = ec.generate_key(n-s_n-p_n)
        y = channel(x, qber)
        add_info, com_iters, x_dec, ver_check = ec.perform_ec(
            x, y, s_y_joins, y_s_joins, qber_est, s_n, p_n, punct_list=punct_list, discl_n=discl_n, show=show)
        f_cur = float(m-p_n+add_info)/(n-p_n-s_n)/ec.h_b(qber)
        f1_rslt.append(f_cur)
        f_cur = float(m-p_n+add_info)/(n-p_n-s_n) - ec.h_b(qber)
        f2_rslt.append(f_cur)
        com_iters_rslt.append(com_iters)
        if not ver_check:
            n_incor += 1
    print('Mean efficiency:', np.mean(f1_rslt),
          '\nMean additional communication rounds', np.mean(com_iters_rslt),"Effective R: ", (R-(s_n/n))/(1-s_n/n-p_n/n))
    #code_n, n_tries, qber, f_mean, com_iters_mean, R, s_n, p_n, p_n_max, k_n, discl_n, FER
    return {
        "com_iters_mean": np.mean(com_iters_rslt),
        "qber": qber,
        "f1_mean": np.mean(f1_rslt),
        "f2_mean": np.mean(f2_rslt),
        "R": R,
        "s_n": s_n,
        "p_n": p_n,
        "p_n_max": p_n_max,
        "k_n": k_n,
        "discl_n": discl_n,
        "FER": float(n_incor)/n_tries
    }

print("wrapper_class loaded correctly")