from summit import Runner
from summit.strategies import SOBO
from pathlib import Path
from summit.benchmarks import Allylation1

# Instantiate the reaction class
exp = Allylation1()

# Set up the strategy (in this case it is SOBO), passing in the optimisation domain
strategy = SOBO(exp.domain)

# Use the runner to run closed loop experiments
r = Runner(strategy=strategy, experiment=exp, max_iterations=50)

cwd = Path.cwd()
cwd.mkdir(exist_ok=True)

exp_no = "Exp6"
exp_dir = cwd / exp_no

# Start the closed loop run
r.run(save_dir=exp_dir, save_freq=1)

# Save final results
r.save(exp_dir / "Exp_data.json")
