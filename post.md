# From Power Flow to Safety: How Far Does GENCO’s Capability Carry?

**Can learning power flow help a model assess grid safety?** GENCO learns relationships among network structure, power injections, voltages, and reactive power. These relationships also matter for safety, making capability reuse a reasonable expectation. But predicting a physical state and deciding whether it violates an operating limit are different tasks. We investigate how far that reuse carries, and where it breaks down.

**How do we test this capability?** We built an N−1 contingency dataset for four small grids unseen during GENCO’s training, generating AC power-flow solutions and safety labels to evaluate the frozen model. We also evaluated published N−2 predictions on the Texas 2000-bus grid used in GENCO’s training. A scenario is unsafe if it has a thermal overload or a PQ-bus voltage violation. Separately, we test whether lightweight probes can predict generator reactive-limit switching from frozen hidden features or decoded-output features.

**Can GENCO help prioritize safety checks?** Yes. On Texas, ranking contingencies by GENCO’s predicted violations identifies more unsafe scenarios than a DC power-flow baseline at the same review budget. Its predictions can therefore help prioritize cases for exact AC evaluation, extending their value beyond numerical state estimation.

**Where does accurate prediction still fall short?** Near an operating limit, a small prediction error can flip a safety judgment. At the tested review budget, all 122 missed unsafe Texas scenarios lie close to operating limits. Safety assessment requires resolving which side of a limit a scenario occupies, not merely predicting a nearby state.

**Are final predictions the best starting point for a new task?** For generator reactive-limit switching, probes using frozen hidden features distinguish cases that hit reactive-power limits from those that do not more effectively than probes using the tested local output features. Hidden features score higher in seven of eight grid–probe comparisons; the remaining comparison ties.

## Conclusion

On Texas, GENCO’s outputs improve safety-review prioritization, while the remaining misses cluster near operating limits. For reactive-limit prediction on unseen small grids, frozen hidden features can be more useful than the tested local output features.
