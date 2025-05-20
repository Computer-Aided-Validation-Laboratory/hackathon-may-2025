#-------------------------------------------------------------------------
# 3Dstc,1mat,thermal,steady
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
#_* MOOSEHERDER VARIABLES - START

# NOTE: only used for transient solves
# endTime = 1
# timeStep = 1

# Thermal Loads/BCs
toK = 273.15
ambTemp = ${fparse 20.0 + toK}
coolantTemp = ${fparse 160.0 + toK}      # degK


# Mesh file string
mesh_file = 'stc_astested.msh'
elem_order = 'FIRST'

#** MOOSEHERDER VARIABLES - END
#-------------------------------------------------------------------------

[GlobalParams]
    displacements = 'disp_x disp_y disp_z'
[]

[Mesh]
    type = FileMesh
    file = ${mesh_file}
[]

[Variables]
    [temperature]
        family = LAGRANGE
        order = ${elem_order}
        initial_condition = ${coolantTemp}
    []
[]

[Kernels]
    [heat_conduction]
        type = ADHeatConduction
        variable = temperature
    []
[]

[Functions]
    [ss_density_fun]
        type = PiecewiseLinear
        data_file = ./data/ss316L_density_K.csv
        format = columns
    []
    [ss_therm_cond_fun]
        type = PiecewiseLinear
        data_file = ./data/ss316L_therm_cond_K.csv
        format = columns
    []
    [ss_therm_spec_heat_fun]
        type = PiecewiseLinear
        data_file = ./data/ss316L_therm_spec_heat_K.csv
        format = columns
    []

    [ss_therm_exp_fun]
        type = PiecewiseLinear
        data_file = ./data/ss316L_therm_exp_K.csv
        format = columns
    []
    [ss_mech_elas_mod_fun]
        type = PiecewiseLinear
        data_file = ./data/ss316L_mech_elas_mod_K.csv
        format = columns
    []

    [surf_hf_spat_fun]
        type = PiecewiseBilinear
        data_file = ./data/surf_hf.csv
        xaxis = 0 # x in csv is x geometry for the top surface
        yaxis = 2 # y in csv is z geometry for the top surface
    []
    [surf_hf_scale_fun]
        type = ParsedFunction
        expression = '1.0'
    []
    [surf_hf_fun]
        type = CompositeFunction
        functions = 'surf_hf_scale_fun surf_hf_spat_fun'
    []

[]

# https://mooseframework.inl.gov/syntax/Physics/SolidMechanics/QuasiStatic/index.html
[Physics/SolidMechanics/QuasiStatic]
    [all]
        strain = SMALL
        incremental = true
        add_variables = true

        use_automatic_differentiation = true
        automatic_eigenstrain_names = true

        material_output_family = MONOMIAL   # MONOMIAL, LAGRANGE
        material_output_order = FIRST      # CONSTANT, FIRST, SECOND,

        # 'effective_plastic_strain'
        generate_output = 'vonmises_stress stress_xx stress_yy stress_zz stress_xy stress_yz stress_xz strain_xx strain_yy strain_zz strain_xy strain_yz strain_xz'
    []
[]

[Materials]
    [ss_density]
        type = ADCoupledValueFunctionMaterial
        v = temperature
        prop_name = density
        function = ss_density_fun
        block = 'stc-vol'
    []
    [ss_thermal_conductivity]
        type = ADCoupledValueFunctionMaterial
        v = temperature
        prop_name = thermal_conductivity
        function = ss_therm_cond_fun
        block = 'stc-vol'
    []
    [ss_specific_heat]
        type = ADCoupledValueFunctionMaterial
        v = temperature
        prop_name = specific_heat
        function = ss_therm_spec_heat_fun
        block = 'stc-vol'
    []

    [ss_expansion]
        type = ADComputeInstantaneousThermalExpansionFunctionEigenstrain
        temperature = temperature
        stress_free_temperature = ${ambTemp}
        thermal_expansion_function = ss_therm_exp_fun
        eigenstrain_name = thermal_expansion_eigenstrain
        block = 'stc-vol'
    []

    [ss_elastic_modulus]
        type = ADCoupledValueFunctionMaterial
        v = temperature
        prop_name = elastic_modulus
        function = ss_mech_elas_mod_fun
        block = 'stc-vol'
    []
    [ss_elasticity]
        type = ADComputeVariableIsotropicElasticityTensor
        youngs_modulus = elastic_modulus
        poissons_ratio = 0.3
        block = 'stc-vol'
    []
    [stress]
        type = ADComputeFiniteStrainElasticStress
    []


    # HTC from sieder-tate with HIVE test conditions
    [coolant_heat_transfer_coefficient]
        type = ADPiecewiseLinearInterpolationMaterial
        xy_data = '
            274 23.6e3
            323 31.9e3
            373 38.8e3
            423 44.4e3
            473 48.9e3
            523 52.4e3
            573 67.6e3
        '
        variable = temperature
        property = heat_transfer_coefficient
        boundary = 'bc-pipe-htc'
    []
[]

[BCs]
    [heat_flux_out]
        type = ADConvectiveHeatFluxBC
        variable = temperature
        boundary = 'bc-pipe-htc'
        T_infinity = ${coolantTemp}
        heat_transfer_coefficient = heat_transfer_coefficient
    []
    [heat_flux_in]
        type = ADFunctionNeumannBC
        variable = temperature
        boundary = 'bc-top-heatflux'
        function = surf_hf_fun
    []
    [radiation_flux]
        type = ADFunctionRadiativeBC
        variable = temperature
        boundary = 'bc-top-heatflux bc-base-surf bc-left-surf bc-right-surf bc-front-surf bc-back-surf'
        emissivity_function = '1'
        Tinfinity = ${ambTemp}
        stefan_boltzmann_constant = 5.67e-8
        use_displaced_mesh = false
    []

    # Lock disp_y for whole base
    [mech_bc_c_dispy]
        type = ADDirichletBC
        variable = disp_y
        boundary = 'bc-base-surf'
        value = 0.0
    []
    [mech_bc_c_dispx]
        type = ADDirichletBC
        variable = disp_x
        boundary = 'bc-base-surf'
        value = 0.0
    []
    [mech_bc_c_dispz]
        type = ADDirichletBC
        variable = disp_z
        boundary = 'bc-base-surf'
        value = 0.0
    []
[]

[Executioner]
    type = Steady


    # Best solver options for low element count large deformation plasticity
    # solve_type = 'NEWTON'
    # petsc_options = '-snes_converged_reason'
    # petsc_options_iname = '-pc_type -ksp_type -ksp_gmres_restart'
    # petsc_options_value = ' lu       gmres     200'


    # Best options for thermal solve
    solve_type = 'NEWTON' # 'NEWTON' or 'PJFNK'
    petsc_options = '-snes_converged_reason'
    petsc_options_iname = '-pc_type -pc_hypre_type -ksp_type -ksp_gmres_restart'
    petsc_options_value = ' hypre    boomeramg      gmres     200'

    l_max_its = 200
    l_tol = 1e-6

    nl_max_its = 50
    nl_rel_tol = 1e-4
    nl_abs_tol = 1e-4

    # end_time= ${endTime}
    # dt = ${timeStep}

    # [Predictor]
    #     type = SimplePredictor
    #     scale = 1
    # []
[]

[Postprocessors]
    [temp_max]
        type = NodalExtremeValue
        variable = temperature
    []
    [temp_avg]
        type = AverageNodalVariableValue
        variable = temperature
    []
    [disp_x_max]
        type = NodalExtremeValue
        variable = disp_x
    []
    [disp_y_max]
        type = NodalExtremeValue
        variable = disp_y
    []
    [disp_z_max]
        type = NodalExtremeValue
        variable = disp_z
    []
[]

[Outputs]
    exodus = true
[]