# Minimization Example 1 from lecture last meeting

def minimize_dfa_ex1():
    states = ["A", "B", "C", "D", "E"]
    alphabet = ["0", "1"]
    start_state = "A"
    accept_states = {"E"}
    transitions = {
        "A": {"0": "B", "1": "C"},
        "B": {"0": "B", "1": "D"},
        "C": {"0": "B", "1": "C"},
        "D": {"0": "B", "1": "E"},
        "E": {"0": "B", "1": "C"},
    }

    # 0-Equivalence: Non-accepting vs Accepting
    partitions = [frozenset(set(states) - accept_states), frozenset(accept_states)]
    print(
        "0-Equivalence:",
        [sorted(list(p)) for p in sorted(partitions, key=lambda x: sorted(list(x))[0])],
    )

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

        # Sort for display consistency
        sorted_display = [
            sorted(list(p))
            for p in sorted(new_partitions, key=lambda x: sorted(list(x))[0])
        ]
        print(f"{k}-Equivalence:", sorted_display)

        if set(new_partitions) == set(partitions):
            break
        partitions = new_partitions
        k += 1

    # Map original states to combined state names (e.g., A & C -> AC)
    state_to_name = {
        s: "".join(sorted(grp)) for grp in partitions for s in grp
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

    # Display Minimized Transition Table
    print("\n--- Minimized DFA Transition Table ---")
    print("State | Input '0' | Input '1'")
    print("-" * 30)
    for s in sorted(min_transitions.keys()):
        prefix = "->" if s == min_start else "  "
        suffix = "*" if s in min_accept else " "
        print(
            f"{prefix}{s:4}{suffix} | {min_transitions[s]['0']:9} | {min_transitions[s]['1']}"
        )

    # Simulation on test strings (including strings written on board: 0110, 011011)
    def simulate(input_str):
        curr = min_start
        for char in input_str:
            curr = min_transitions[curr][char]
        return curr in min_accept

    test_inputs = ["0110", "011011", "011", "1011"]
    print("\n--- Input Simulation ---")
    for inp in test_inputs:
        result = "Accepted" if simulate(inp) else "Rejected"
        print(f"String '{inp}': {result}")


minimize_dfa_ex1()