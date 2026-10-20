def minimax(depth, node, is_max, scores):
    if depth == 2:
        return scores[node]

    if is_max:
        return max(
            minimax(depth + 1, node * 2, False, scores),
            minimax(depth + 1, node * 2 + 1, False, scores)
        )
    else:
        return min(
            minimax(depth + 1, node * 2, True, scores),
            minimax(depth + 1, node * 2 + 1, True, scores)
        )

scores = [3, 5, 2, 9]
result = minimax(0, 0, True, scores)

print("Best score:", result)
