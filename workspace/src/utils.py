from fibertree_bootstrap import *

from teaal.parse import *
from teaal.trans.hifiber import HiFiber

def compile(yaml):
    einsum = Einsum.from_str(yaml)
    mapping = Mapping.from_str(yaml)
    arch = Architecture.from_str(yaml)
    bindings = Bindings.from_str(yaml)
    format_ = Format.from_str(yaml)

    hifiber = HiFiber(einsum, mapping, arch, bindings, format_)

    get_ipython().set_next_input("# Autogenerated HiFiber\n\n" + str(hifiber))

def check_matmul(A, B, Z):
    # Note: A, B, and Z should be un-partitioned
    A_MK = A.swizzleRanks(rank_ids=["M", "K"])
    B_NK = B.swizzleRanks(rank_ids=["N", "K"])
    Z_MN = Z.swizzleRanks(rank_ids=["M", "N"])

    Z_MN_corr = Tensor(rank_ids=["M", "N"], name="Z")
    z_m = Z_MN_corr.getRoot()
    a_m = A_MK.getRoot()
    b_n = B_NK.getRoot()
    for m, (z_n, a_k) in z_m << a_m:
        for n, (z_ref, b_k) in z_n << b_n:
            for k, (a_val, b_val) in a_k & b_k:
                z_ref += a_val * b_val

    print("Result correct?", Z_MN == Z_MN_corr)

def check_conv(I, F, O, step=1):
    # Note: I, F, and O should be un-partitioned
    print(I.getRankIds())
    I_BCHW = I.swizzleRanks(rank_ids=["N", "C", "H", "W"])
    F_MCRS = F.swizzleRanks(rank_ids=["M", "C", "R", "S"])
    O_BMPQ = O.swizzleRanks(rank_ids=["N", "M", "E", "F"])

    B, C, H, W = I_BCHW.getShape()
    M, C, R, S = F_MCRS.getShape()
    B, M, P, Q = O_BMPQ.getShape()

    O_BMPQ_corr = Tensor(rank_ids=["N", "M", "E", "F"], name="O")
    o_b = O_BMPQ_corr.getRoot()
    i_b = I_BCHW.getRoot()
    f_m = F_MCRS.getRoot()
    for b, (o_m, i_c) in o_b << i_b:
        for m, (o_p, f_c) in o_m << f_m:
            for c, (i_h, f_r) in i_c & f_c:
                for r, f_s in f_r:
                    for s, f_val in f_s:
                        for p, (o_q, i_w) in o_p << i_h.project(trans_fn=lambda h: -1 / step * r + 1 / step * h, interval=(0, P)).prune(trans_fn=lambda i, c, p: c % 1 == 0):
                            for q, (o_ref, i_val) in o_q << i_w.project(trans_fn=lambda w: -1 / step * s + 1 / step * w, interval=(0, Q)).prune(trans_fn=lambda i, c, p: c % 1 == 0):
                                o_ref += i_val * f_val

    print("Result correct?", O_BMPQ == O_BMPQ_corr)
