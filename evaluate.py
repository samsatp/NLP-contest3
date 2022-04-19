"""Evaluation script

Note that this evaluation only cares about the phrase level extraction.
Also, it does not care where the phrases come from.

Usage:
    python3 evaluate.py gold_entities.json predicted_entities.json
"""
import json
import sys

def compute_prf(gold_list_list, pred_list_list):
    total_gold, total_pred, total_correct = 0, 0, 0
    for g_ent_list, p_ent_list in zip(gold_list_list, pred_list_list):
        g_ent_set = set(g_ent_list)
        p_ent_set = set(p_ent_list)
        total_gold += len(g_ent_set)
        total_pred += len(p_ent_set)
        total_correct += len(g_ent_set.intersection(p_ent_set))
    precision = total_correct / total_pred if total_pred != 0 else 0
    recall = total_correct / total_gold if total_gold != 0 else 0
    if precision + recall == 0:
        f1 = 0
    else:
        f1 = (2 * precision * recall) / (precision + recall)
    return (precision, recall, f1)


def evaluate_answer(gold_file, prediction_file):
    gold = json.load(open(gold_file))
    pred = json.load(open(prediction_file))

    assert (len(gold) == len(pred))
    ent_types =['ORG', 'PER', 'MEA', 'LOC', 'TTL', 'DTM', 'NUM', 'DES', 'MISC', 'TRM', 'BRN']

    results = {}
    gold = [[(e,x) for e,x in alist] for alist in gold]
    pred = [[(e,x) for e,x in alist] for alist in pred]
    p, r, f = compute_prf(gold, pred)
    results['0 Overall F1'] = f
    results['0 Overall P'] = p
    results['0 Overall R'] = r

    for i, ent_type in enumerate(ent_types):
        filtered_gold = [[(e,x) for e,x in alist if e == ent_type] for alist in gold]
        filtered_pred = [[(e,x) for e,x in alist if e == ent_type] for alist in pred]
        _, _, f = compute_prf(filtered_gold, filtered_pred)
        results['{} {} F1'.format(i+1, ent_type)] = f
    return results

if __name__ == '__main__':
    gold_file = sys.argv[1]
    prediction_file = sys.argv[2]
    print (json.dumps(evaluate_answer(gold_file, prediction_file), indent=2))
