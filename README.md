## Protocol: Open Research 

Following mainnet launch, the protocol governing the economics of the NuCypher network will continue to evolve. Although certain initial parameters and design choices are irreversible post-launch, there are a number of significant mechanisms that can be upgraded or augmented in order to improve security, service quality and the general health of the network. The following list introduces some open, protocol-related research topics: 

1. **Pricing structure, free market dynamics and commercial engagement**

The definition of a service unit (the _pricing structure_) and its cost (the _price point_) will initially be fixed and universal to all engagements between service-provider and user. However, both the pricing structure and price point may diversify over time through individual provider strategies and response to demand trends. This research area refers to the means by which the protocol facilitates or restricts NuCypher's free market, for example via mechanisms enabling users to efficiently discover prices, or by providing a choice of pricing structures to providers. Relevant discussions: https://github.com/nucypher/protocol/issues/14, https://github.com/nucypher/nucypher/issues/1567, https://github.com/nucypher/protocol/issues/7

2. **Payment tooling** 

This refers to upgrading the process through which users settle their bills, for example via probabilistic and/or conditional micro-payments. Relevant discussion: https://forum.nucypher.com/t/a-skeleton-logic-proposal-for-another-economic-model-of-grant/157

3. **Slashing conditions and penalty calculation**

Incorrect re-encryptions can be provably detected and punished. However, the exact basis on which a service-provider is penalized (e.g. per incorrect request vs. per policy), the severity of punishment, and the inputs to the penalty calculation itself (for example, computing based on a percentage of locked stake, an absolute/universal figure, or both), are all open research questions. Relevant discussion: https://github.com/nucypher/protocol/issues/12

4. **Subsidies and service quality** 

The action required to earn subsidies (inflationary rewards) does not align perfectly with actual work performed on behalf of users, which risks some service-providers configuring their machines to execute the bare minimum required to collect the subsidy, and neglecting real service requests from users (e.g. by being offline). Relevant discussions: https://github.com/nucypher/nucypher/issues/1272, https://github.com/nucypher/protocol/issues/13

5. **Service-provider selection conditions**

The probability with which a service-provider is selected for a job can be leveraged as a low-risk nudge towards good behavior. 
Relevant discussions: https://github.com/nucypher/protocol/issues/9


If you are interested in contributing ideas, analysis or in-depth feedback to one or more of these topics, as part of the Contributor Phase of the incentivized testnet (Come and Stake it) or otherwise, please drop us a email at submissions@nucypher.com. Summarize what you'd like to work on and we'll get back to you. Include the email, name, and ETH staking address you used to register for Come and Stake It. We reserve the sole right to determine how valuable a specific contribution is. 

Note that in NuCypher repositories _service-providers_ are also referred to as 'Ursulas', 'stakers', 'workers', 'proxies' and just 'providers'. In addition to perusing the links above, we recommend searching for discussions in our public Discord channels – in particular, to check if a question you have has already been answered.

----

### Protocol: Mint Paper (in progress)

A paper documenting the protocol/economic mechanisms and parameters associated with the NuCypher network that have been implemented, deployed or established with some stability. This does not exclude mechanisms that may change later, but this would necessitate an update to the paper. Sources are in Latex.


