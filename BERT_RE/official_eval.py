import os
from sklearn.metrics import f1_score

EVAL_DIR = "eval"


# def official_f1():
#     # Run the perl script
#     try:
#         cmd = "perl {0}/semeval2010_task8_scorer-v1.2.pl {0}/proposed_answers.txt {0}/answer_keys.txt > {0}/result.txt".format(
#             EVAL_DIR
#         )
#         os.system(cmd)
#     except:
#         raise Exception("perl is not installed or proposed_answers.txt is missing")
#
#     with open(os.path.join(EVAL_DIR, "result.txt"), "r", encoding="utf-8") as f:
#         macro_result = list(f)[-1]
#         macro_result = macro_result.split(":")[1].replace(">>>", "").strip()
#         macro_result = macro_result.split("=")[1].strip().replace("%", "")
#         macro_result = float(macro_result) / 100
#
#     return macro_result

def compute_f1_from_files():
    """Reads the answer files and computes F1-score manually"""
    proposed_answers_path = os.path.join(EVAL_DIR, "proposed_answers.txt")
    answer_keys_path = os.path.join(EVAL_DIR, "answer_keys.txt")

    if not os.path.exists(proposed_answers_path) or not os.path.exists(answer_keys_path):
        raise Exception("Error: proposed_answers.txt or answer_keys.txt is missing")

    with open(proposed_answers_path, "r", encoding="utf-8") as f:
        proposed_answers = [line.strip() for line in f.readlines()]

    with open(answer_keys_path, "r", encoding="utf-8") as f:
        answer_keys = [line.strip() for line in f.readlines()]

    if len(proposed_answers) != len(answer_keys):
        raise ValueError("Mismatch: Number of proposed answers and answer keys are not the same.")

    # Convert string labels to integers (if necessary)
    unique_labels = list(set(answer_keys + proposed_answers))
    label_map = {label: idx for idx, label in enumerate(unique_labels)}

    y_true = [label_map[label] for label in answer_keys]
    y_pred = [label_map[label] for label in proposed_answers]

    return f1_score(y_true, y_pred, average="macro")  # Compute macro-averaged F1-score

def official_f1():
    """Replaces the original Perl script with a Python implementation"""
    macro_result = compute_f1_from_files()
    return macro_result

if __name__ == "__main__":
    print("macro-averaged F1 = {}%".format(official_f1() * 100))
