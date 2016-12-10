import numpy as np 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from const import Const

def load_data(filename):
    next_state_vopt = np.load(filename)

if __name__ == '__main__':
  
  ## parameters from dynamic_programming
  max_t = 50
  vopt_plot_filename = "V_OPT_2D_PLOT.pdf"
  # piopt_plot_filename = "PI_OPT_2D_PLOT.jpg"

  v_opt_by_time = np.zeros((max_t,Const.BINS_Y))
  # pi_opt_by_time = np.zeros((max_t,Const.BINS_Y))

  for t in range(1, max_t + 1):

    filename_vopt = "Dynamic_programming_vopt_t=" + str(t) + ".txt"
    # filename_piopt = "Dynamic_programming_piopt_t=" +str(t) + ".txt"
    
    v_opt = np.loadtxt(filename_vopt)
    v_opt = v_opt.reshape([Const.BINS_Y, Const.BINS_VY, Const.BINS_VW])
    # pi_opt = np.loadtxt(filename_piopt)
    # pi_opt = pi_opt.reshape([Const.BINS_Y, Const.BINS_VY, Const.BINS_VW])

    v_opt_avgs = np.sum(v_opt,axis = (1,2))/(Const.BINS_VY * Const.BINS_VW + 0.0)
    # pi_opt_avgs = np.sum(pi_opt,axis = (1,2))/(Const.BINS_VY * Const.BINS_VW + 0.0)

    # print avgs
    # print "t =", t, "min", min(v_opt_avgs), "max", max(v_opt_avgs)

    v_opt_by_time[t-1] = v_opt_avgs
    # pi_opt_by_time[t-1] = pi_opt_avgs

  
  ##Plot the results for v_opt

  # Make X,Y arrays holding axis values for pcolormesh
  X = np.zeros((max_t + 1, Const.BINS_Y + 1))
  Y = np.zeros((max_t + 1, Const.BINS_Y + 1))
  for i in range(max_t + 1):
    for j in range(Const.BINS_Y + 1):
      X[i, j] = i
      Y[i, j] = (j * Const.BIN_SIZE_Y) + Const.Y_MIN

  plt.ioff()
  plt.figure()
  plt.pcolormesh(X, Y, v_opt_by_time)
  plt.colorbar()
  
  # Ensure plot is centered on y-axis
  plt.xlim((max_t,0))
  plt.xlabel("Time (seconds)")
  plt.ylim((Const.Y_MIN,Const.Y_MAX))
  plt.ylabel("Lateral distance from center of runway (km)")
  plt.title("Optimal Utility Map Averaged over v_y, v_w")
  # plt.axis('equal')
  plt.savefig(vopt_plot_filename)



