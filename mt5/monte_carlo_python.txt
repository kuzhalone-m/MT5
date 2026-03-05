import numpy as np

def monte_carlo_sim(
    iterations=1000,
    days=100,
    trades_per_day=2,
    win_rate=0.48,
    win_r=1.5,
    loss_r=1.0,
    risk=0.005,
    daily_dd_limit=0.04,
    max_dd_limit=0.08
):
    
    survive_count = 0
    daily_breach_count = 0
    max_dd_breach_count = 0

    for _ in range(iterations):

        equity = 100000
        hwm = equity
        alive = True

        for day in range(days):

            day_start_equity = equity

            for trade in range(trades_per_day):

                if np.random.rand() < win_rate:
                    r_multiple = win_r
                else:
                    r_multiple = -loss_r

                equity *= (1 + r_multiple * risk)

                # Daily DD check
                daily_dd = (day_start_equity - equity) / day_start_equity
                if daily_dd >= daily_dd_limit:
                    daily_breach_count += 1
                    alive = False
                    break

                # Max DD check
                hwm = max(hwm, equity)
                max_dd = (hwm - equity) / hwm
                if max_dd >= max_dd_limit:
                    max_dd_breach_count += 1
                    alive = False
                    break

            if not alive:
                break

        if alive:
            survive_count += 1

    return {
        "survival_rate": survive_count / iterations,
        "daily_dd_breach_rate": daily_breach_count / iterations,
        "max_dd_breach_rate": max_dd_breach_count / iterations
    }

results = monte_carlo_sim()
print(results)