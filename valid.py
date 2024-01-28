from utils import *
from tqdm import tqdm

def perform_insertion_and_validation(tree, filename):
    data = read_csv(filename)
    for key, value in tqdm(data, desc="Inserting data"):
        tree.insert_node(int(key), int(value))

    save_tree_to_csv(tree, 'inserted_data.csv')
    validate_inserted_data('inserted_data.csv', filename)

def perform_deletion_and_validation(tree, delete_filename, compare_filename):
    delete_data = read_csv(delete_filename)
    deleted_keys = set()

    for key in tqdm(delete_data, desc="Deleting data"):
        key_int = int(key[0])
        tree.delete_node(key_int)
        deleted_keys.add(key_int)

    save_tree_deletion(tree, deleted_keys, 'remaining_after_deletion.csv')
    validate_deletion('remaining_after_deletion.csv', compare_filename)

'''
    Validation Function 정의
'''

def validate_inserted_data(generated_file, original_file):
    generated_data = read_csv(generated_file, isComma=True)
    original_data = read_csv(original_file)

    generated_dict = {int(row[0]): int(row[1]) for row in generated_data}

    search_score, compare_score = 0, 0
    for key, value in tqdm(original_data, desc="Validating data"):
        key = int(key)
        value = int(value)

        if key in generated_dict:
            search_score += 1
            if generated_dict[key] == value:
                compare_score += 1

    total = len(original_data)
    print(f"[Insertion & Search]\nsearch_score: {search_score} / {total}\ncompare_score: {compare_score} / {total}")

def validate_deletion(generated_file, compare_file):
    generated_data = read_csv(generated_file, isComma=True)
    compare_data = read_csv(compare_file)

    generated_dict = {int(row[0]): row[1] for row in generated_data}
    compare_dict = {int(row[0]): row[1] for row in compare_data}

    search_score, compare_score = 0, 0
    for key, expected_value in tqdm(compare_dict.items(), desc="Validating deletion"):
        actual_value = generated_dict.get(key, "N/A")
        if actual_value == expected_value:
            compare_score += 1
        if actual_value != "N/A" or expected_value == "N/A":
            search_score += 1

    total = len(compare_dict)
    print(f"[Deletion]\nsearch_score: {search_score} / {total}\ncompare_score: {compare_score} / {total}")
