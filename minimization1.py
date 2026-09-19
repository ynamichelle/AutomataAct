def dfa_minimization_michy():
    # States using unique letters of MICHY in their original definition order
    states = ["M", "I", "C", "H", "Y"]
    alphabet = ["0", "1"]
    start_state = "M"
    accept_states = {"Y"}

    # Transition table
    transitions = {
        "M": {"0": "I", "1": "C"},
        "I": {"0": "I", "1": "H"},
        "C": {"0": "I", "1": "C"},
        "H": {"0": "I", "1": "Y"},
        "Y": {"0": "I", "1": "C"},
    }

    print("==================================================")
    print("      DFA MINIMIZATION (STATES: M - I - C - H - Y)")
    print("==================================================")

    # 1. Original Table
    print("\n--- ORIGINAL TRANSITION TABLE ---")
    print("       |  0  |  1  |")
    print("--------------------")
    for s in states:
        arrow = "-> " if s == start_state else "   "
        circle = f"({s})" if s in accept_states else f" {s} "
        print(f"{arrow}{circle} |  {transitions[s]['0']}  |  {transitions[s]['1']}  |")

    # 2. Step-by-Step Equivalence Partitions
    non_f = frozenset(set(states) - accept_states)
    f_set = frozenset(accept_states)
    partitions = [non_f, f_set]

    # Preserves the original states declaration order (e.g., M before C -> {M,I,C,H})
    def format_parts(parts):
        res = []
        sorted_groups = sorted(parts, key=lambda grp: min(states.index(s) for s in grp))
        for p in sorted_groups:
            ordered_items = sorted(list(p), key=lambda s: states.index(s))
            res.append("{" + ",".join(ordered_items) + "}")
        return " ".join(res)

    print("\n--- STEP-BY-STEP EQUIVALENCE ---")
    print(f"0 EQUIVALENCE:  {format_parts(partitions)}")

    k = 1
    while True:
        group_map = {s: i for i, grp in enumerate(partitions) for s in grp}
        new_partitions = []

        for grp in partitions:
            split_map = {}
            for s in grp:
                sig = tuple(group_map[transitions[s][sym]] for sym in alphabet)
                split_map.setdefault(sig, set()).add(s)
            for sub_grp in split_map.values():
                new_partitions.append(frozenset(sub_grp))

        print(f"{k} EQUIVALENCE:  {format_parts(new_partitions)}")

        if set(new_partitions) == set(partitions):
            break
        partitions = new_partitions
        k += 1

    # Preserve order so M and C merge into 'MC' instead of 'CM'
    state_to_name = {
        s: "".join(sorted(grp, key=lambda x: states.index(x)))
        for grp in partitions for s in grp
    }
    min_start = state_to_name[start_state]
    min_accept = {state_to_name[s] for s in accept_states}

    min_transitions = {}
    for grp in partitions:
        rep = next(iter(grp))
        name = state_to_name[rep]
        min_transitions[name] = {
            sym: state_to_name[transitions[rep][sym]] for sym in alphabet
        }

    # 3. Minimized Table
    print("\n--- MINIMIZED TRANSITION TABLE ---")
    print("       |  0   |  1   |")
    print("----------------------")
    ordered_states = sorted(
        min_transitions.keys(),
        key=lambda name: min(states.index(ch) for ch in name)
    )
    for s in ordered_states:
        arrow = "-> " if s == min_start else "   "
        circle = f"({s:2})" if s in min_accept else f" {s:2} "
        print(f"{arrow}{circle} |  {min_transitions[s]['0']:3} |  {min_transitions[s]['1']:3} |")

    # 4. Input String Testing
    def test_string(bitstring, label):
        curr = min_start
        path = [curr]
        for b in bitstring:
            curr = min_transitions[curr][b]
            path.append(curr)
        is_accepted = curr in min_accept
        mark = "✓" if is_accepted else "x"
        status = "ACCEPTED" if is_accepted else "REJECTED"
        print(f"{label:<12} | Input: '{bitstring:<7}' -> Path: {' -> '.join(path):<28} | {mark} {status}")

    print("\n--- STRING VERIFICATION ---")
    test_string("011",     "Accepted 1")
    test_string("1011",    "Accepted 2")
    test_string("010",     "Rejected 1")
    test_string("0110",    "Rejected 2")


dfa_minimization_michy()