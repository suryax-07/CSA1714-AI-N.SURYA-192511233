
def alpha_beta(depth, node, is_max, scores, alpha, beta):
    if depth == 2:
        return scores[node]

    if is_max:
        best = float("-inf")

        for child in [node * 2, node * 2 + 1]:
            value = alpha_beta(
                depth + 1, child, False, scores, alpha, beta
            )
            best = max(best, value)
            alpha = max(alpha, best)

            if alpha >= beta:
                break

        return best

    else:
        best = float("inf")

        for child in [node * 2, node * 2 + 1]:
            value = alpha_beta(
                depth + 1, child, True, scores, alpha, beta
            )
            best = min(best, value)
            beta = min(beta, best)

            if alpha >= beta:
                break

        return best


scores = [3, 5, 2, 9]

result = alpha_beta(
    0, 0, True, scores, float("-inf"), float("inf")
)

print("Best score:", result)
