from benchopt import safe_import_context
from benchmark_utils.optuna_solver import OSolver

# Protect the import with `safe_import_context()`. This allows:
# - skipping import to speed up autocompletion in CLI.
# - getting requirements info when all dependencies are not installed.
with safe_import_context() as import_ctx:
    import optuna  # noqa: F401
    from sklearn.linear_model import LogisticRegression


# The benchmark solvers must be named `Solver` and
# inherit from `BaseSolver` for `benchopt` to work properly.
class Solver(OSolver):

    # Name to select the solver in the CLI and to display the results.
    name = 'logreg_l2'
    requirements = ["pip:optuna"]

    parameters = {
        'penalty': ['l1', 'l2', 'elasticnet'],
    }

    def get_model(self):
        solver = 'lbfgs'
        if self.penalty == 'l1':
            solver = 'liblinear'
        elif self.penalty == 'elasticnet':
            solver = 'saga'
        return LogisticRegression(
            penalty=self.penalty, solver=solver
        )

    def sample_parameters(self, trial):
        params = {}
        params['C'] = trial.suggest_float(
            "C", 1e-3, 1e3, log=True
        )
        if self.penalty == 'elasticnet':
            params['l1_ratio'] = trial.suggest_float(
                "l1_ratio", 0, 1, step=0.1
            )

        return params
