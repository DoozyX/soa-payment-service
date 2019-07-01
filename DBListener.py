import pybreaker
import logging


class DBListener(pybreaker.CircuitBreakerListener):
    "Listener used by circuit breakers that execute database operations."

    def before_call(self, cb, func, *args, **kwargs):
        logging.info("Called before the circuit breaker `cb` calls `func`.")
        pass

    def state_change(self, cb, old_state, new_state):
        logging.info("Called when the circuit breaker `cb` state changes.")
        pass

    def failure(self, cb, exc):
        logging.info("Called when a function invocation raises a system error.")
        pass

    def success(self, cb):
        logging.info("Called when a function invocation succeeds.")
        pass

