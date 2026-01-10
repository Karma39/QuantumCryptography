# Chosen code size for both cascade and ldpc
code_size = "1944"
#------------

f_start = 1.0  # initial efficiency of decoding
qber_start = 0.2
qber_end = 0.3
qber_step = 0.01  # range of QBERs
n_tries = 5  # number of keys proccessed for each QBER value

pn_range = [50, 100, 150, 200]
sn_range = [50, 100, 150, 200]

codes_dict = {
    1944: {
        "file": 'libraries/codes_1944.txt',
        "n": 1944
    },
    4000: {
        "file": 'libraries/codes_4000.txt',
        "n": 4000
    }
}

saving_folder = "results/"
