#ifndef TICK_INFERENCE_SRC_HAWKES_SDCA_LOGLIK_KERN_H_
#define TICK_INFERENCE_SRC_HAWKES_SDCA_LOGLIK_KERN_H_

// License: BSD 3 clause

#include "base.h"
#include "sdca.h"
#include "base/hawkes_list.h"

/**
 * \class HawkesSDCALoglikKern
 * \brief TODO fill
 */
class HawkesSDCALoglikKern : public ModelHawkesList {
  //! @brief Decay shared by all Hawkes exponential kernels
  double decay;

  //! @brief kernel intensity of node j on node i at time t_i_k
  ArrayDouble2dList1D g;

  //! @brief compensator of kernel intensity of node j on node i between 0 and end_time
  ArrayDoubleList1D G;

  std::vector<SDCA> sdca_list;

  bool weights_allocated;

  // SDCA attributes
  double l_l2sq;
  double tol;
  RandType rand_type;
  int seed;

 public:
  HawkesSDCALoglikKern(double decay, double l_l2sq,
                       int max_n_threads = 1, double tol = 0.,
                       RandType rand_type = RandType::unif, int seed = -1);

  //! @brief allocate buffer arrays once data has been given
  void compute_weights();

  //! @brief Perform one iteration of the algorithm
  void solve();

  double get_decay() const;
  void set_decay(double decay);

  SArrayDoublePtr get_iterate();

 private:
  void allocate_weights();
  void compute_weights_dim_i(ulong i_r, std::shared_ptr<ArrayDouble2dList1D> G_buffer);

  void synchronize_sdca();
};

#endif  // TICK_INFERENCE_SRC_HAWKES_SDCA_LOGLIK_KERN_H_