import os
def read(filename=1):
    """
    This will read in a movement pattern file
    :param filename: <int> : no of pattern to run
    :return: <list>
    """
    deltas = []
    folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(folder, "patterns", f"pattern{filename}.txt")) as f:
        content = f.readlines()
        for line in content:
            try:
                text = line.split("\n")
                values = text[0].split(" ")
                deltas.append((int(values[0]), int(values[1])))
            except ValueError:
                pass
    return deltas