from typing import Callable
import numpy as np
import matplotlib.pyplot as plt


def uniaxial_linear_plas(strain: float,
                         elas_mod: float,
                         yield_stress: float,
                         hard_mod: float) -> tuple[float,float,float]:

    strain_yield = yield_stress/elas_mod

    if strain < strain_yield:
        stress = elas_mod*strain
        return (stress,strain,0.0)

    stress = yield_stress + hard_mod*(strain - yield_stress/elas_mod)
    elas_strain = stress/elas_mod
    plas_strain = strain - elas_strain
    return (stress,elas_strain,plas_strain)


def plasticity_1d(strain_total: np.ndarray,
                  mat_params: np.ndarray,
                  hard_func: Callable) -> tuple[np.ndarray,np.ndarray]:

    num_incs = strain_total.shape[0]
    strain_inc = np.zeros((num_incs,))
    strain_inc[1:] = np.diff(strain_total)

    stress_out = np.zeros((num_incs+1,))
    strain_out = np.zeros((num_incs+1,))

    stress_curr: float = 0.0
    strain_curr: float = 0.0
    eps_plas: float = 0.0
    peq: float = 0.0

    for ii in range(num_incs):
        strain_curr = strain_curr + strain_inc[ii]
        (stress_curr, peq, eps_plas) = radial_return_1d(strain_curr,
                                                        mat_params,
                                                        hard_func,
                                                        peq,
                                                        eps_plas)

        stress_out[ii+1] = stress_curr
        strain_out[ii+1] = strain_curr

    return (stress_out,strain_out)

def radial_return_1d(eps_total: float,
                     mat_params: np.ndarray,
                     hard_func: Callable,
                     peq: float,
                     eps_plas: float,
                     fun_tol: float = 1e-12,
                     step_tol: float = 1e-12,
                     max_iters: int = 100) -> tuple[float,float]:

    elas_mod: float = mat_params[0]
    stress_trial: float = elas_mod*(eps_total - eps_plas)
    (yield_curr,dyield_dpeq) = hard_func(mat_params,peq)

    yield_func_trial = abs(stress_trial) - yield_curr
    #---------------------------------------------------------------------------
    # Elastic case
    if yield_func_trial <= 0.0:
        # Keep the current accumulated plastic strain and return it
        return (stress_trial,peq,eps_plas)

    #---------------------------------------------------------------------------
    # Plastic case

    # Want yield function f = 0 for plasticy
    yield_func: float = yield_func_trial
    delta_lambda: float = 0.0
    yield_next: float = 0.0
    peq_next: float = 0.0

    for ii in range(max_iters):
        # jacobian
        dyieldfun_dlambda = -elas_mod-dyield_dpeq

        # delta_lambda_inc = -residual/jacobian
        # Change in the guess
        delta_lambda_inc = yield_func/dyieldfun_dlambda

        # Update lambda
        delta_lambda = delta_lambda - yield_func/dyieldfun_dlambda

        # Update the effective plastic strain state variable
        # peq remembers the accumulated plastic strain
        peq_next = peq + delta_lambda

        # Calculate the updated yield stress based on the accumulated plastic strain
        (yield_next,dyield_dpeq) = hard_func(mat_params,peq_next)

        # Calculate the yield function using the trial stress and the updated yield stress
        #yield_func = yield_func_trial - delta_lambda*elas_mod + (yield_curr - yield_next)
        yield_func = abs(stress_trial) - delta_lambda*elas_mod - yield_next

        # Can use yield_func (residual) or delta_gamma_inc (step) here as convergence
        if abs(delta_lambda_inc) < step_tol or abs(yield_func) < fun_tol:
            print(80*"-")
            print(f"Converged in {ii} iterations")
            print(f"{dyieldfun_dlambda=}")
            print(f"{dyield_dpeq=}")
            print(f"{delta_lambda=}")
            print(f"{delta_lambda_inc=}")
            print(f"{peq_next=}")
            print(f"{yield_func=}")
            break

    stress_out = (1-delta_lambda*elas_mod/abs(stress_trial))*stress_trial
    peq = peq_next
    eps_plas = eps_plas + delta_lambda*stress_trial/abs(stress_trial)

    print(80*"=")
    print(f"{stress_out=}")
    print(f"{peq=}")
    print(f"{eps_plas=}")
    print(80*"=")

    return (stress_out,peq,eps_plas)

def hard_linear(mat_params: np.ndarray, peq: float) -> tuple[float,float]:
    yield_init = mat_params[1]
    yield_curr = yield_init + mat_params[2]*peq
    dyield_dpeq = mat_params[2]
    return (yield_curr,dyield_dpeq)

def hard_voce(mat_params: np.ndarray, peq: float) -> tuple[float,float]:
    s0 = mat_params[1]
    r0 = mat_params[2]
    rinf = mat_params[3]
    b = mat_params[4]
    yield_curr = s0 + peq*r0 + rinf*(1-np.exp(-b*peq))
    dyield_dpeq = r0 + rinf*b*np.exp(-b*peq)
    return (yield_curr,dyield_dpeq)




def main() -> None:
    strain_inc = 1e-6 # 1 microstrain
    strain_max = 0.1  # 5%
    strain_divs = 1000
    strain_total = np.linspace(0.0,strain_max,strain_divs)
    #strain_total = np.arange(0,strain_max,strain_inc)
    print(f"{strain_total.shape=}")

    elas_mod = 200e3
    p_ratio = 0.3
    shear_mod = elas_mod/(2*(1+p_ratio))

    steel_linear = np.array([elas_mod,425.0,5000.0])
    steel_voce = np.array([elas_mod,300.0,5000.0,125.0,1000])

    check_stress = np.zeros_like(strain_total)
    check_elas_strain = np.zeros_like(strain_total)
    check_plas_strain = np.zeros_like(strain_total)
    for ss in range(strain_total.shape[0]):
        (check_stress[ss],
        check_elas_strain[ss],
        check_plas_strain[ss]) = uniaxial_linear_plas(
            strain_total[ss],elas_mod,steel_linear[1],steel_linear[2]
        )


    # n_divs = 1000
    # strain_path_max = 0.05
    # s_path_1 = np.linspace(0.0,strain_path_max,n_divs)
    # s_path_2 = np.linspace(strain_path_max,0.0,n_divs)
    # s_path_3 = np.linspace(0.0,strain_path_max,n_divs)
    # s_path_4 = np.linspace(strain_path_max,0.0,n_divs)
    # s_path_5 = np.linspace(0.0,strain_path_max,n_divs)
    # s_path_6 = np.linspace(strain_path_max,0.0,n_divs)
    # strain_path = np.hstack((s_path_1,
    #                          s_path_2[1:],
    #                          s_path_3[1:],
    #                          s_path_4[1:],
    #                          s_path_5[1:],
    #                          s_path_6[1:]))

    (stress_lin,strain_lin) = plasticity_1d(strain_total,steel_linear,hard_linear)
    (stress_voce,strain_voce) = plasticity_1d(strain_total,steel_voce,hard_voce)

    # fig, ax = plt.subplots()
    # ax.plot(strain_total,check_stress)
    # ax.plot(strain_lin,stress_lin)
    # ax.plot(strain_voce,stress_voce)
    # plt.show()

    n_divs = 1000
    strain_path_max = 0.05
    s_path_1 = np.linspace(0.0,strain_path_max,n_divs)
    s_path_2 = np.linspace(strain_path_max,-0.1*strain_path_max,n_divs)

    strain_path = np.hstack((s_path_1,
                             s_path_2[1:],))

    (stress_lin,strain_lin) = plasticity_1d(strain_path,steel_linear,hard_linear)


    fig, ax = plt.subplots()
    ax.plot(strain_lin,stress_lin)
    plt.show()













if __name__ == "__main__":
    main()