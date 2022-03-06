A = 5
B = 10**9 + 7
C = 101
D = 50
E = 2**0.5


def generate_rs(n_max):
    for n in range(n_max):
        yield ((A**n % B) % C) + D


def generate_trolls(n_trolls):
    g = generate_rs(3 * n_trolls)
    for _ in range(n_trolls):
        yield next(g), next(g), next(g)


def get_troll_problem_data(n_trolls):
    # assert n_trolls == 8
    trolls = list(generate_trolls(n_trolls))
    # trolls = [(150, 50, 50)] * 1 + [(100, 150, 149)] + [(50, 50, 150)] * 6
    total_height = sum(t[0] for t in trolls)
    hole_depth = total_height / E
    print(hole_depth)
    total_iq = sum(t[2] for t in trolls)
    return trolls, total_height, hole_depth, total_iq

print(get_troll_problem_data(5))

def pe732_1(n_trolls):
    trolls, total_height, hole_depth, _ = get_troll_problem_data(n_trolls)
    trolls.sort(key=lambda t: t[0] + t[1])
    max_troll_reach = 2 * (C + D - 1)
    mh = int(total_height + max_troll_reach - hole_depth)   # max combined height of escaping trolls
    print(mh, total_height, hole_depth)
    dp = [[0] * (mh + 1) for _ in range(n_trolls + 1)]
    for i in range(1, n_trolls + 1):
        t_h, t_l, t_iq = trolls[i - 1]
        troll_mh = mh - (max_troll_reach - t_h - t_l)
        for j in range(troll_mh + 1):
            no_escape_total_iq = dp[i - 1][j]
            if j >= t_h:
                escape_total_iq = dp[i - 1][j - t_h] + t_iq
            else:
                escape_total_iq = 0
            dp[i][j] = max(no_escape_total_iq, escape_total_iq)
    escaped_iq_max = max(dp[-1])
    # print(f'pe732_1, maximum escaped iq for {n_trolls} trolls: {escaped_iq_max}')
    return escaped_iq_max

pe732_1(5)