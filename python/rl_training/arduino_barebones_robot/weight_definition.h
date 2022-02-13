constexpr int input_size = 3;
constexpr int first_layer_size = 6;
constexpr int second_layer_size = 6;
constexpr int output_layer_size = 2;
constexpr int first_layer_weight_size = first_layer_size*input_size;
constexpr int second_layer_weight_size = first_layer_size*second_layer_size;
constexpr int output_layer_weight_size = second_layer_size*output_layer_size;


float input_holder[input_size]{};
float mu_0_weight[first_layer_weight_size]{};
float mu_0_bias[first_layer_size]{};
float mu_2_weight[second_layer_weight_size]{};
float mu_2_bias[second_layer_size]{};
float mu_4_weight[output_layer_weight_size]{};
float mu_4_bias[output_layer_size]{};
#define NUM(a) (sizeof(a) / sizeof(*a))
Params mu_0_weight_params = { 0, NUM(mu_0_weight),  mu_0_weight };
Params mu_0_bias_params = { 1, NUM(mu_0_bias),  mu_0_bias };
Params mu_2_weight_params = { 2, NUM(mu_2_weight),  mu_2_weight };
Params mu_2_bias_params = { 3, NUM(mu_2_bias),  mu_2_bias };
Params mu_4_weight_params = { 4, NUM(mu_4_weight),  mu_4_weight };
Params mu_4_bias_params = { 5, NUM(mu_4_bias),  mu_4_bias };
