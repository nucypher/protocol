### Using the median staking duration to modify the reward coefficient ###

#### Problem #### 

Currently, stakers/workers choose to lock their NU tokens for a variety of durations, in units of month. The staker's inflation-based rewards are modified by the reward coefficient 'kappa', which can be any of 12 discrete figures between 0.54 (= 1 month lock) and 1.0 (>= 12 months lock) – 0.54, 0.58, 0.63, etc. The longer you commit your stake, the higher the coefficient.

However, this reward coefficient is determined entirely by the individual staker’s choice of duration, and is completely static with regard to the wider reality of the network, and more specifically, what other stakers have chosen for their durations. It is the aggregate of stakers’ choices that truly impacts the utility of the network, and yet this has no bearing whatsoever on the kappa coefficient. If too many stakers choose short durations, this can seriously impede network users.

For the sake of argument, let's say that stakers choose short durations for any of the following three preferences:
1. to protect their assets against risk (e.g. the NU token significantly depreciating while their holding is locked)
2. to minimise opportunity costs (e.g. not being able to afford to migrate capital over to another more promising network)
3. to afford real-world short-term spending requirements (e.g. paying a monthly bill to an ISP).

Obviously, the actual list of preferences (i.e. explanations) for short term staking is longer, more complicated, and probably impossible to exhaustively produce. However, even if our three-point list did cover all possible preferences, it would still be very, very difficult to predict the strength of preference for each amongst a group of stakers at any given moment in the future. Plus, both population of stakers and each individual staker’s preferences will unpredictably change over time. Although a higher reward coefficient (i.e. extra compensation) for longer staking is specifically designed to counteract the preference for shorter staking, the problem is that we as designers have no real idea how strongly those preferences are held, what they're worth in money terms, or even what all of those preferences are. The inability to predict or quantify these preferences means it is far from guaranteed we will parameterize the corresponding reward coefficient correctly in advance of network launch, or even through updates later (although later updates allow observation-based changes to the coefficient, it may already be too late to save the network).

Launching the network with parameters that mismatch our stakers' preferences is problematic, or indeed if this incongruence occurs at any point while the network is live. For example, if the coefficient for longer staking is not enough to persuade a sufficient number of stakers to commit for long periods, this may lead to network users being unable to issue long term sharing policies, particularly if they require larger numbers of independent stakers to faciliate their sharing flow. This may also undermine user confidence in the long-term reliability of the network. An excessive amount of short stake durations can also cause greater token price volatility. 

#### Solution #### 

A solution to this problem is to implement a flexible, self-correcting reward coefficient, driven by the staking duration decisions of all network participants. Ideally, we want to legislate against group swings to either extreme (majority choosing short durations or majority choosing long durations) – but we have a general preference for longer-term staking, since the implications for network utility are far less severe. 

Our desired algorithm will do the following: if a majority of stakers have chosen short durations, the reward coefficient increases for stakers who now choose longer durations, and decreases for stakers who now choose shorter durations. And vice versa. 

This provides an extra incentive to go against the crowd, thereby providing a balancing mechanism. We cannot predict the future external factors that will collectively influence the stakers’ commitment length to the network, so instead we can attempt to capture these factors via the collective preferences of stakers, and use these to modify the reward coefficient appropriately. 

Note: to avoid stakers gaming the system, the reward coefficient can be calculated at the moment the staker formally chooses and submits their duration for a given set of tokens, and then can stay fixed at that rate until those tokens unlock. It would also help stakers a lot if the current average duration of stakes, and therefore the going reward rates, were accessible via the CLI or notherother staker-facing interface, so they can make an informed decision.

Note: this approach will impact the rate of tokens released. 

#### Historical Examples #### 

Livepeer's floating inflation rate, determined by the percentage of token-holders 'participating' (bonding tokens to transcoders), is a well-known and innovative attempt to avoid the trap of predefining an economic parameter that mismatches staker behaviour. Here is their algorithm (solidity): 

```sh
function setInflation() internal {
        uint256 currentBondingRate = 0;
        uint256 totalSupply = livepeerToken().totalSupply();
        if (totalSupply > 0) {
            uint256 totalBonded = bondingManager().getTotalBonded();
            currentBondingRate = MathUtils.percPoints(totalBonded, totalSupply);
        }
        if (currentBondingRate < targetBondingRate) {
            // Bonding rate is below the target - increase inflation
            inflation = inflation.add(inflationChange);
        } else if (currentBondingRate > targetBondingRate) {
            // Bonding rate is above the target - decrease inflation
            if (inflationChange > inflation) {
                inflation = 0;
            } else {
                inflation = inflation.sub(inflationChange);
            }
        }
```

One criticism of their approach is this function's reliance on predefining a target bonding rate, which arguably kicks the inflexibility issue from one parameter to another. On the other hand, it is no doubt easier to choose an ideal participation rate (LivePeer sets this to 50%), and add an inflation-correcting mechanism to achieve this, than the exact opposite.


#### Input variable: T_med #### 

What is the input variable with which to modify our reward coefficient? There are actually a number of possibilities here – because stakers can theoretically divide their stake into as many durations as the number of tokens they own. However, a simple approach is to line up all the tokens already staked by their individual duration attribute (from 1 to <12). For now, we can ignore who owns the token or how long their other tokens are staked for. From this two-column table it is straightforward to derive the mean, weighted mean or median duration of all staked tokens. We will use this variable, T_med, as our input, which will always be in discrete units of month (e.g. T_med = 4 months). 

#### Modifying the reward coefficient: c_kappa #### 

*Proposal 1*

The following python function computes a reward coefficient for a stake with a chosen a duration of T_s, where the current median duration of stakes is T_med. The output coefficient is normalised between 0 and 1.

```sh
small_stake_multiplier = 0.5
T_max = 12

def calc_c_kappa(T_med, T_s):
	if T_s > T_med:
		c_kappa = (min(T_s, T_max) - T_med) / float(T_max * 2) + small_stake_multiplier
	else:
		c_kappa =  (1 + ((min(T_s, T_max) - T_med) / float(T_max))) / 2
	return c_kappa

example_output = calc_c_kappa(T_med = 4, T_s = 11)
print(example_output)
# 0.791666666667
```
This function can be combined with any other function (e.g. the existing kappa calculation) to bias it towards longer or shorter durations, if desired. 

To get a sense of the outputs, here are all the combinatins of T_s and T_med. For example, if the median stake duration is 4 months, and you choose a duration of 11 months, your reward coefficient will be 0.79. If T_s is set 1 month, and T_med is 8 months, you will get the same coefficient (0.79).

|         | T_med: 1 | T_med: 2 | T_med: 3 | T_med: 4 | T_med: 5 | T_med: 6 | T_med: 7 | T_med: 8 | T_med: 9 | T_med: 10 | T_med: 11 | T_med: 12 |
|---------|----------|----------|----------|----------|----------|----------|----------|----------|----------|-----------|-----------|-----------|
| T_s: 1  | 0.50     | 0.46     | 0.42     | 0.38     | 0.33     | 0.29     | 0.25     | 0.21     | 0.17     | 0.13      | 0.08      | 0.04      |
| T_s: 2  | 0.54     | 0.50     | 0.46     | 0.42     | 0.38     | 0.33     | 0.29     | 0.25     | 0.21     | 0.17      | 0.13      | 0.08      |
| T_s: 3  | 0.58     | 0.54     | 0.50     | 0.46     | 0.42     | 0.38     | 0.33     | 0.29     | 0.25     | 0.21      | 0.17      | 0.13      |
| T_s: 4  | 0.63     | 0.58     | 0.54     | 0.50     | 0.46     | 0.42     | 0.38     | 0.33     | 0.29     | 0.25      | 0.21      | 0.17      |
| T_s: 5  | 0.67     | 0.63     | 0.58     | 0.54     | 0.50     | 0.46     | 0.42     | 0.38     | 0.33     | 0.29      | 0.25      | 0.21      |
| T_s: 6  | 0.71     | 0.67     | 0.63     | 0.58     | 0.54     | 0.50     | 0.46     | 0.42     | 0.38     | 0.33      | 0.29      | 0.25      |
| T_s: 7  | 0.75     | 0.71     | 0.67     | 0.63     | 0.58     | 0.54     | 0.50     | 0.46     | 0.42     | 0.38      | 0.33      | 0.29      |
| T_s: 8  | 0.79     | 0.75     | 0.71     | 0.67     | 0.63     | 0.58     | 0.54     | 0.50     | 0.46     | 0.42      | 0.38      | 0.33      |
| T_s: 9  | 0.83     | 0.79     | 0.75     | 0.71     | 0.67     | 0.63     | 0.58     | 0.54     | 0.50     | 0.46      | 0.42      | 0.38      |
| T_s: 10 | 0.88     | 0.83     | 0.79     | 0.75     | 0.71     | 0.67     | 0.63     | 0.58     | 0.54     | 0.50      | 0.46      | 0.42      |
| T_s: 11 | 0.92     | 0.88     | 0.83     | 0.79     | 0.75     | 0.71     | 0.67     | 0.63     | 0.58     | 0.54      | 0.50      | 0.46      |
| T_s: 12 | 0.96     | 0.92     | 0.88     | 0.83     | 0.79     | 0.75     | 0.71     | 0.67     | 0.63     | 0.58      | 0.54      | 0.50      |


![Proposal 1: visualised outputs in a scatter graph](collective_kappa_outputs.png)

*Proposal 2*

Based on @michwill’s suggestion to swap T_med = 1 and T_med = 12. 

![Proposal 2: visualised outputs in a scatter graph](collective_kappa_outputs2.png)

*Proposal 3*

This algorithm uses a varying output gradient (see graph below) in order to to: 
1) fulfil the original purpose of collective kappa – namely, to provide extra rewards for going against the crowd (particularly when the average staking duration is dangerously short). 
But simultaneously goes some way to:
2) avoid the issue of **overly** rewarding short duration stakers, in the scenario where the average staking duration is very short, **relative** to two other possible configurations:
 a) choosing a longer choice of staking duration in the same scenario 
 b) choosing the same (short) staking duration in other scenarios (e.g. when the average staking duration is very long)

```sh
min_kappa = 0.25
T_max = 12

def calc_c_kappa(T_med, T_s):
    if T_s < T_med + 1:
        c_kappa = 0.25
    else:
        c_kappa =  min_kappa + (T_s-T_med)/float(16-T_med)

    return c_kappa

example_output1  = calc_c_kappa(T_med = 2, T_s = 3)
print(example_output1)
#0.32
example_output2  = calc_c_kappa(T_med = 10, T_s = 11)
print(example_output2)
#0.42
example_output3  = calc_c_kappa(T_med = 4, T_s = 11)
print(example_output3)
#0.83

```
Full coefficient output table:

|         | T_med: 1 | T_med: 2 | T_med: 3 | T_med: 4 | T_med: 5 | T_med: 6 | T_med: 7 | T_med: 8 | T_med: 9 | T_med: 10 | T_med: 11 | T_med: 12 |
|---------|----------|----------|----------|----------|----------|----------|----------|----------|----------|-----------|-----------|-----------|
| T_s: 1  | 0.25     | 0.25     | 0.25     | 0.25     | 0.25     | 0.25     | 0.25     | 0.25     | 0.25     | 0.25      | 0.25      | 0.25      |
| T_s: 2  | 0.32     | 0.25     | 0.25     | 0.25     | 0.25     | 0.25     | 0.25     | 0.25     | 0.25     | 0.25      | 0.25      | 0.25      |
| T_s: 3  | 0.38     | 0.32     | 0.25     | 0.25     | 0.25     | 0.25     | 0.25     | 0.25     | 0.25     | 0.25      | 0.25      | 0.25      |
| T_s: 4  | 0.45     | 0.39     | 0.33     | 0.25     | 0.25     | 0.25     | 0.25     | 0.25     | 0.25     | 0.25      | 0.25      | 0.25      |
| T_s: 5  | 0.52     | 0.46     | 0.40     | 0.33     | 0.25     | 0.25     | 0.25     | 0.25     | 0.25     | 0.25      | 0.25      | 0.25      |
| T_s: 6  | 0.58     | 0.54     | 0.48     | 0.42     | 0.34     | 0.25     | 0.25     | 0.25     | 0.25     | 0.25      | 0.25      | 0.25      |
| T_s: 7  | 0.65     | 0.61     | 0.56     | 0.50     | 0.43     | 0.35     | 0.25     | 0.25     | 0.25     | 0.25      | 0.25      | 0.25      |
| T_s: 8  | 0.72     | 0.68     | 0.63     | 0.58     | 0.52     | 0.45     | 0.36     | 0.25     | 0.25     | 0.25      | 0.25      | 0.25      |
| T_s: 9  | 0.78     | 0.75     | 0.71     | 0.67     | 0.61     | 0.55     | 0.47     | 0.38     | 0.25     | 0.25      | 0.25      | 0.25      |
| T_s: 10 | 0.85     | 0.82     | 0.79     | 0.75     | 0.70     | 0.65     | 0.58     | 0.50     | 0.39     | 0.25      | 0.25      | 0.25      |
| T_s: 11 | 0.92     | 0.89     | 0.87     | 0.83     | 0.80     | 0.75     | 0.69     | 0.63     | 0.54     | 0.42      | 0.25      | 0.25      |
| T_s: 12 | 0.98     | 0.96     | 0.94     | 0.92     | 0.89     | 0.85     | 0.81     | 0.75     | 0.68     | 0.58      | 0.45      | 0.25      |

![Proposal 3: visualised outputs in a scatter graph](collective_kappa_outputs3.png)


#### Expected Outcomes ####

To be investigated/modelled following team feedback. 

Intuitively, and if staker preferences are evenly distributed from short to long durations (between 1 and 12 months) prior to being presented with this new incentive coefficient, then this approach will push median durations (T_med) to the centre, i.e. around 6 months. From a network point of view, it may be better for T_med to be a longer period than this. It is possible to configure the algorithm such that the 'centre' is pushes behaviour to a target median duration of 12 or 18 months. 

This also demonstrates an advantage that NuCypher has over LivePeer. Their target participation rate of 50% is a little arbitrary – the result of a compromise between two vaguely defined goals (on one had, maximising bonding, and on the other, quote: "the ability to transfer the token, the ability to use it for the main utility of the network, and the ability to use it within ecosystem applications are all reasons not to stake"). In our case, we can choose a target median duration rate as a direct requirement of our adopter/users, reflected in the lengths of their sharing policies. 

