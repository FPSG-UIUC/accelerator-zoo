from copy import deepcopy

from fibertree_bootstrap import *

from teaal.parse import *
from teaal.trans.hifiber import HiFiber

def compile(yaml, generate_video = True):
    str_yaml = yaml
    if(generate_video == False):
       index = str_yaml.find("spacetime")
       str_yaml = str_yaml[:index]

    einsum = Einsum.from_str(str_yaml)
    mapping = Mapping.from_str(str_yaml)
    arch = Architecture.from_str(str_yaml)
    bindings = Bindings.from_str(str_yaml)
    format_ = Format.from_str(str_yaml)

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

def check_conv(I, F, O, stride=1):
    # Note: I, F, and O should be un-partitioned

    I_NCHW = I.swizzleRanks(rank_ids=["N", "C", "H", "W"])
    F_MCRS = F.swizzleRanks(rank_ids=["M", "C", "R", "S"])
    O_NMEF = O.swizzleRanks(rank_ids=["N", "M", "E", "F"])
    N, C, H, W = I_NCHW.getShape()
    M, C, R, S = F_MCRS.getShape()
    N, M, E, F = O_NMEF.getShape()

    O_NMEF_corr = Tensor(rank_ids=["N", "M", "E", "F"], name="O", shape=[N, M, E, F])
    o_n = O_NMEF_corr.getRoot()
    i_n = I_NCHW.getRoot()
    f_m = F_MCRS.getRoot()
    for n, (o_m, i_c) in o_n << i_n:
        for m, (o_e, f_c) in o_m << f_m:
            for e, o_f in o_e.iterRangeShapeRef(0, E, 1):
                for f, o_ref in o_f.iterRangeShapeRef(0, F, 1):
                    for c, (i_h, f_r) in i_c & f_c:
                        for r, (i_w, f_s) in i_h.project(trans_fn=lambda h: h + -stride * e, interval=(0, R)) & f_r:
                            for s, (i_val, f_val) in i_w.project(trans_fn=lambda w: w + -stride * f, interval=(0, S)) & f_s:
                                o_ref += i_val * f_val

    print("Result correct?", O_NMEF == O_NMEF_corr)

def check_MTTKRP(A_IJK, B_JF, C_KF, Y):
    T_IJF = Tensor(rank_ids=["I", "J", "F"], name="T")
    t_i = T_IJF.getRoot()
    a_i = A_IJK.getRoot()
    c_k = C_KF.getRoot()
    for i_pos, (i, (t_j, a_j)) in enumerate(t_i << a_i):
        for j_pos, (j, (t_f, a_k)) in enumerate(t_j << a_j):
            for k_pos, (k, (a_val, c_f)) in enumerate(a_k & c_k):
                for f_pos, (f, (t_ref, c_val)) in enumerate(t_f << c_f):
                    t_ref += a_val * c_val

    Y_IF = Tensor(rank_ids=["I", "F"], name="Y")
    y_i = Y_IF.getRoot()
    t_i = T_IJF.getRoot()
    b_j = B_JF.getRoot()
    for i_pos, (i, (y_f, t_j)) in enumerate(y_i << t_i):
        for j_pos, (j, (t_f, b_f)) in enumerate(t_j & b_j):
            for f_pos, (f, (y_ref, (t_val, b_val))) in enumerate(y_f << (t_f & b_f)):
                y_ref += t_val * b_val
    print("Result correct?", Y == Y_IF)

def check_TTMc(A_IJK, B_JV, C_KU, Y):
    T_IJU = Tensor(rank_ids=["I", "J", "U"], name="T")
    t_i = T_IJU.getRoot()
    a_i = A_IJK.getRoot()
    c_k = C_KU.getRoot()
    for i_pos, (i, (t_j, a_j)) in enumerate(t_i << a_i):
        for j_pos, (j, (t_u, a_k)) in enumerate(t_j << a_j):
            for k_pos, (k, (a_val, c_u)) in enumerate(a_k & c_k):
                for u_pos, (u, (t_ref, c_val)) in enumerate(t_u << c_u):
                    t_ref += a_val * c_val
    Y_IVU = Tensor(rank_ids=["I", "V", "U"], name="Y")
    y_i = Y_IVU.getRoot()
    t_i = T_IJU.getRoot()
    b_j = B_JV.getRoot()
    for i_pos, (i, (y_v, t_j)) in enumerate(y_i << t_i):
        for j_pos, (j, (t_u, b_v)) in enumerate(t_j & b_j):
            for v_pos, (v, (y_u, b_val)) in enumerate(y_v << b_v):
                for u_pos, (u, (y_ref, t_val)) in enumerate(y_u << t_u):
                    y_ref += t_val * b_val
    print("Result correct?", Y == Y_IVU)

def check_matrix_matrix_mul(A_IJ, B_JK, Y):
    Y_IK = Tensor(rank_ids=["I", "K"], name="Y")
    y_i = Y_IK.getRoot()
    a_i = A_IJ.getRoot()
    b_j = B_JK.getRoot()
    for i_pos, (i, (y_k, a_j)) in enumerate(y_i << a_i):
        for j_pos, (j, (a_val, b_k)) in enumerate(a_j & b_j):
            for k_pos, (k, (y_ref, b_val)) in enumerate(y_k << b_k):
                y_ref += a_val * b_val
    print("Result correct?", Y == Y_IK)

def check_matrix_vector_mul(A_IJ, B_J, Y):
    Y_I = Tensor(rank_ids=["I"], name="Y")
    y_i = Y_I.getRoot()
    a_i = A_IJ.getRoot()
    b_j = B_J.getRoot()
    for i_pos, (i, (y_ref, a_j)) in enumerate(y_i << a_i):
        for j_pos, (j, (a_val, b_val)) in enumerate(a_j & b_j):
            y_ref += a_val * b_val
    print("Result correct?", Y == Y_I)

def check_bfs_sssp(G_SD, start_vertex, P1_V):
    P1_V_checking = P1_V

    V = G_SD.getShape()[0]

    A0_S = Tensor.fromFiber(rank_ids=["S"], fiber=Fiber([start_vertex], [0]), default=float("inf"), name="A0")
    P0_V = Tensor.fromFiber(rank_ids=["V"], fiber=Fiber([start_vertex], [0], default=float("inf")), default=float("inf"), name="P0")

    while len(A0_S.getRoot()) > 0:
        SO_SD = Tensor(rank_ids=["S", "D"], name="SO")
        so_s = SO_SD.getRoot()
        g_s = G_SD.getRoot()
        a0_s = A0_S.getRoot()
        for s, (so_d, (g_d, a0_val)) in so_s << (g_s & a0_s):
            for d, (so_ref, g_val) in so_d << g_d:
                so_ref <<= g_val
        # Custom default
        R_V = Tensor(rank_ids=["V"], name="R", default=float("inf"))
        r_v = R_V.getRoot()
        so_s = SO_SD.getRoot()
        a0_s = A0_S.getRoot()
        for s, (so_d, a0_val) in so_s & a0_s:
            for v, (r_ref, so_val) in r_v << so_d.project(trans_fn=lambda d: d, interval=(0, V)):
                # + => min, * => +
                r_ref <<= min(r_ref, so_val + a0_val)
        # P0 and P1 are actually the same tensor
        P1_V = deepcopy(P0_V)
        p1_v = P1_V.getRoot()
        r_v = R_V.getRoot()
        p0_v = P0_V.getRoot()
        for v, (p1_ref, (_, r_val, p0_val)) in p1_v << (r_v | p0_v):
            # + => min
            p1_ref <<= min(r_val, p0_val)
        # Custom default
        M_V = Tensor(rank_ids=["V"], name="M", default=False)
        m_v = M_V.getRoot()
        p1_v = P1_V.getRoot()
        p0_v = P0_V.getRoot()
        for v, (m_ref, (_, p1_val, p0_val)) in m_v << (p1_v | p0_v):
            # - => !=
            m_ref <<= p1_val != p0_val
        # Custom default
        A1_V = Tensor(rank_ids=["V"], name="A1", default=float("inf"))
        a1_v = A1_V.getRoot()
        m_v = M_V.getRoot()
        p1_v = P1_V.getRoot()
        for v, (a1_ref, (m_val, p1_val)) in a1_v << (m_v & p1_v):
            a1_ref <<= p1_val

        # Prepare for the next iteration
        P0_V = P1_V
        A0_S = A1_V

    print("Result correct?", P1_V == P1_V_checking)

def check_attn(Q_PE, K_ME, V_MF, AV_PF):
    QK_PM = Tensor(rank_ids=["P", "M"])
    GM_P = Tensor(rank_ids=["P"], default=-float("inf"))
    SN_PM = Tensor(rank_ids=["P", "M"])
    SD_P = Tensor(rank_ids=["P"])
    A_PM = Tensor(rank_ids=["P", "M"])
    AV_PF_corr = Tensor(rank_ids=["P", "F"])
    q_p = Q_PE.getRoot()
    k_m = K_ME.getRoot()
    v_m = V_MF.getRoot()
    qk_p = QK_PM.getRoot()
    gm_p = GM_P.getRoot()
    sn_p = SN_PM.getRoot()
    sd_p = SD_P.getRoot()
    a_p = A_PM.getRoot()
    av_p = AV_PF_corr.getRoot()

    for p, (av_f, (a_m, (sd_ref, (sn_m, (gm_ref, (qk_m, q_e)))))) in av_p << (a_p << (sd_p << (sn_p << (gm_p << (qk_p << q_p))))):
        for m, (qk_ref, k_e) in qk_m << k_m:
            for e, (q_val, k_val) in q_e & k_e:
                qk_ref += q_val * k_val
            gm_ref <<= max(gm_ref, qk_ref)
        for m, (sn_ref, qk_val) in sn_m << qk_m:
            sn_ref <<= math.exp(Payload.get(qk_val - gm_ref))
            sd_ref += sn_ref
        for m, (a_ref, (v_f, sn_val)) in a_m << (v_m & sn_m):
            a_ref <<= sn_val / sd_ref
            for f, (av_ref, v_val) in av_f << v_f:
                av_ref += a_ref * v_val

    P, F = AV_PF.getShape()
    close = True
    for p in range(P):
        for f in range(F):
            close = close and (abs(Payload.get(AV_PF.getPayload(p, f) - AV_PF_corr.getPayload(p, f))) < 1e-5)

    print("Result correct?", close)

def check_sddmm(A, B, C, Z):
    # Note: A, B, C, and Z should be un-partitioned
    A_MK = A.swizzleRanks(rank_ids=["M", "K"])
    B_NK = B.swizzleRanks(rank_ids=["N", "K"])
    C_MN = C.swizzleRanks(rank_ids=["M", "N"])
    Z_MN = Z.swizzleRanks(rank_ids=["M", "N"])

    Z_MN_corr = Tensor(rank_ids=["M", "N"], name="Z")
    z_m = Z_MN_corr.getRoot()
    a_m = A_MK.getRoot()
    b_n = B_NK.getRoot()
    c_m = C_MN.getRoot()
    for m, (z_n, (c_n, a_k)) in z_m << (c_m & a_m):
        for n, (z_ref, (c_val, b_k)) in z_n << (c_n & b_n):
            for k, (a_val, b_val) in a_k & b_k:
                z_ref += a_val * b_val * c_val

    print("Result correct?", Z_MN == Z_MN_corr)

