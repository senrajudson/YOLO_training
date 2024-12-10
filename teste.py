def generate_data_structure(yoloClasses):
    if isinstance(yoloClasses, list):
        classes = "\n".join(yoloClasses)
    else:
        classes = yoloClasses

    data = f"""
{classes}
"""
    return data


if __name__ == "__main__":
    yoloClasses1 = ["Hardhat", "Person"]
    yoloClasses2 = "Hardhat"

    data1 = generate_data_structure(yoloClasses1)
    data2 = generate_data_structure(yoloClasses2)

    print(data1)
    print(data2)
