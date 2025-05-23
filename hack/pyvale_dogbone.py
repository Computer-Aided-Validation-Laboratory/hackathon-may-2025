from pathlib import Path
import numpy as np
import pyvale as pyv
import mooseherder as mh

def main() -> None:
    data_path = Path.cwd()/"hack"/"dogbone_mech_3d_plas_ad_out.e"
    sim_data = mh.ExodusReader(data_path).read_all_sim_data()


    field_name = "disp"
    field_comps = ("disp_x","disp_y","disp_z")
    sim_data = pyv.scale_length_units(scale=1000.0,
                                      sim_data=sim_data,
                                      disp_comps=field_comps)

    pyv.print_dimensions(sim_data)

    # pv_plot = pyv.plot_sim_data(sim_data,"disp_y",elem_dims=3)
    # pv_plot.show()

    #---------------------------------------------------------------------------
    # Displacement Sensors
    sens_pos = np.array([(0.0,-2.0,0.6),
                         (0.0,0.0,0.6),
                         (0.0,2.0,0.6)])
    sens_data = pyv.SensorData(positions=sens_pos)

    disp_field = pyv.FieldVector(sim_data,field_name,field_comps,elem_dims=3)

    descriptor = pyv.SensorDescriptorFactory.displacement_descriptor()

    disp_sens_array = pyv.SensorArrayPoint(sens_data,
                                           disp_field,
                                           descriptor)

    measurements = disp_sens_array.calc_measurements()

    print(f"Extensometer Length: {np.linalg.norm(sens_pos[-1,:] - sens_pos[0,:])}")
    extensometer_disp = measurements[-1,:,:] - measurements[0,:,:]
    extensometer_strain = (extensometer_disp
                           /np.linalg.norm(sens_pos[-1,:] - sens_pos[0,:]))

    pv_plot = pyv.plot_point_sensors_on_sim(disp_sens_array,"disp_y")
    pv_plot.show(cpos="xy")









if __name__ == "__main__":
    main()