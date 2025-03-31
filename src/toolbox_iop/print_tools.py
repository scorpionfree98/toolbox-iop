def dict_printer(process_count_dict: dict, total=None, print_method=print):
    if total is None:
        total = sum(process_count_dict.values())
    for key, value in process_count_dict.items():
        print()
        if isinstance(value, int):
            print_method(f"{key} {value} {value / total:.2%}")
        elif isinstance(value, dict):
            reject_total = sum(value.values())
            if reject_total == 0:
                reject_total = 1
            for k, v in value.items():
                # print(key, k, v, f"{v/reject_total:.2%}")

                print_method(f"{key} {k} {v} {v / reject_total:.2%}")
        else:
            raise NotImplementedError(f"value type {type(value)} not implemented")
